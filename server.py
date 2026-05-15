"""
Web UI server — multi-session chat + configuration center.

Config center covers:
  - LLM API provider management (add / edit / delete)
  - Model selection
  - Token usage history + per-day / per-model breakdown
  - Token usage alert (daily limit)
  - Skill management (SKILL.md files)
  - FHE (homomorphic) key management (skf / dictf / user_authorization)

Run:
    source .venv/bin/activate
    python server.py   # http://127.0.0.1:8800
"""

from __future__ import annotations

import base64
import json
import pathlib
import sqlite3
import threading
import uuid
from datetime import datetime, timezone

import httpx

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel

import agent as agent_mod
import stores

ROOT = pathlib.Path(__file__).parent
STATIC = ROOT / "static"
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
SESSIONS_FILE = DATA / "sessions.json"
CHECKPOINT_DB = DATA / "checkpoints.sqlite"

_lock = threading.Lock()
_conn = sqlite3.connect(str(CHECKPOINT_DB), check_same_thread=False)
checkpointer = SqliteSaver(_conn)

# Agent is rebuilt whenever model config changes. It may be None until a
# provider is configured via the settings UI.
_agent_lock = threading.Lock()


def _try_build():
    try:
        return agent_mod.build_agent(checkpointer=checkpointer)
    except Exception:
        return None


_agent = _try_build()


def rebuild_agent() -> None:
    global _agent
    with _agent_lock:
        _agent = _try_build()


def get_agent():
    with _agent_lock:
        return _agent


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_sessions() -> list[dict]:
    if not SESSIONS_FILE.exists():
        return []
    try:
        return json.loads(SESSIONS_FILE.read_text())
    except Exception:
        return []


def _save_sessions(s: list[dict]) -> None:
    SESSIONS_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2))


def _find(s: list[dict], sid: str) -> dict | None:
    return next((x for x in s if x["id"] == sid), None)


app = FastAPI(title="LangGraph Agent")


# ===== chat / sessions =====
class ChatRequest(BaseModel):
    session_id: str
    message: str
    # Per-request override: the user must explicitly click 继续使用 each page
    # session. It is NOT persisted server-side, so a page reload re-prompts.
    override: bool = False


def _over_limit():
    """Return (over: bool, today_tokens: int, limit: int) — pure usage check,
    independent of any override."""
    cfg = stores.load_config()
    alert = cfg.get("alert", {})
    if not alert.get("enabled"):
        return False, 0, 0
    limit = int(alert.get("dailyTokenLimit", 0) or 0)
    if limit <= 0:
        return False, 0, 0
    summary = stores.usage_summary()
    today_tokens = summary["todayTokens"]
    return today_tokens >= limit, today_tokens, limit


@app.get("/api/sessions")
def list_sessions():
    with _lock:
        return sorted(_load_sessions(), key=lambda s: s["updated_at"], reverse=True)


@app.post("/api/sessions")
def create_session():
    with _lock:
        s = _load_sessions()
        sid = uuid.uuid4().hex[:12]
        now = _now()
        m = {"id": sid, "title": "新会话", "created_at": now, "updated_at": now}
        s.append(m)
        _save_sessions(s)
        return m


@app.delete("/api/sessions/{sid}")
def delete_session(sid: str):
    with _lock:
        s = _load_sessions()
        if not _find(s, sid):
            raise HTTPException(404, "session not found")
        _save_sessions([x for x in s if x["id"] != sid])
    try:
        with _lock:
            _conn.execute("DELETE FROM checkpoints WHERE thread_id = ?", (sid,))
            _conn.execute("DELETE FROM writes WHERE thread_id = ?", (sid,))
            _conn.commit()
    except Exception:
        pass
    return {"ok": True}


@app.get("/api/sessions/{sid}/messages")
def get_messages(sid: str):
    with _lock:
        if not _find(_load_sessions(), sid):
            raise HTTPException(404, "session not found")
    ag = get_agent()
    if ag is None:
        return []
    state = ag.get_state({"configurable": {"thread_id": sid}})
    msgs = state.values.get("messages", []) if state and state.values else []
    out = []
    for m in msgs:
        r = getattr(m, "type", "")
        if r == "human":
            out.append({"role": "user", "text": m.content})
        elif r == "ai" and getattr(m, "content", ""):
            out.append({"role": "assistant", "text": m.content})
    return out


@app.post("/api/chat")
def chat(req: ChatRequest):
    text = (req.message or "").strip()
    if not text:
        raise HTTPException(400, "empty message")
    with _lock:
        if not _find(_load_sessions(), req.session_id):
            raise HTTPException(404, "session not found")

    # Limit pre-check. Only the explicit per-request override (the user
    # clicked 继续使用 in this page session) bypasses it.
    over, today_tok, limit = _over_limit()
    if over and not req.override:
        return {
            "blocked": True,
            "message": (
                f"今日 Token 用量已达到上限（{today_tok:,} / {limit:,}）。\n"
                "为控制成本，已暂停继续调用。你可以选择继续使用（忽略今日上限），"
                "或等待明日 0 点自动重置。"
            ),
            "today": today_tok,
            "limit": limit,
        }

    cfg = stores.load_config()
    ag = get_agent()
    if ag is None:
        raise HTTPException(400, "尚未配置大模型，请先在「配置中心 → 大模型配置」中填写 API 并保存。")
    config = {"configurable": {"thread_id": req.session_id}}
    try:
        result = ag.invoke({"messages": [{"role": "user", "content": text}]}, config)
    except Exception as exc:
        raise HTTPException(502, f"模型调用失败：{exc}")

    trace, answer, in_tok, out_tok = [], "", 0, 0
    for m in result["messages"]:
        r = getattr(m, "type", "?")
        um = getattr(m, "usage_metadata", None)
        if um:
            in_tok += um.get("input_tokens", 0) or 0
            out_tok += um.get("output_tokens", 0) or 0
        if r == "human":
            continue
        tcs = getattr(m, "tool_calls", None)
        if tcs:
            for tc in tcs:
                trace.append({"kind": "tool-call", "text": f"{tc['name']}({tc['args']})"})
        elif r == "tool":
            trace.append({"kind": "tool-result", "text": str(m.content)})
        elif r == "ai" and m.content:
            answer = m.content

    stores.record_usage(req.session_id, cfg.get("activeModel", "?"), in_tok, out_tok)

    with _lock:
        s = _load_sessions()
        meta = _find(s, req.session_id)
        title = "新会话"
        if meta:
            if meta["title"] == "新会话":
                meta["title"] = text[:20] + ("…" if len(text) > 20 else "")
            meta["updated_at"] = _now()
            _save_sessions(s)
            title = meta["title"]

    summary = stores.usage_summary()
    return {
        "answer": answer or "（无回复）",
        "trace": trace,
        "title": title,
        "usage": {"in": in_tok, "out": out_tok},
        "alert": summary["alert"],
    }


# ===== config: providers / model / alert =====
class ConfigBody(BaseModel):
    providers: list[dict] | None = None
    activeProvider: str | None = None
    activeModel: str | None = None
    alert: dict | None = None


@app.get("/api/config")
def get_config():
    cfg = stores.load_config()
    # Mask api keys for display.
    safe = json.loads(json.dumps(cfg))
    for p in safe.get("providers", []):
        k = p.get("apiKey", "")
        p["apiKeyMasked"] = (k[:10] + "…" + k[-4:]) if len(k) > 16 else "（已设置）" if k else ""
        p["apiKey"] = ""
    return safe


@app.put("/api/config")
def put_config(body: ConfigBody):
    cfg = stores.load_config()
    incoming = body.model_dump(exclude_none=True)
    if "providers" in incoming:
        # Preserve existing api keys when client sends empty (masked) key.
        old = {p["id"]: p for p in cfg.get("providers", [])}
        for p in incoming["providers"]:
            if not p.get("apiKey") and p["id"] in old:
                p["apiKey"] = old[p["id"]].get("apiKey", "")
        cfg["providers"] = incoming["providers"]
    if "activeProvider" in incoming:
        cfg["activeProvider"] = incoming["activeProvider"]
    if "activeModel" in incoming:
        cfg["activeModel"] = incoming["activeModel"]
    if "alert" in incoming:
        cfg["alert"] = incoming["alert"]
    stores.save_config(cfg)
    rebuild_agent()
    return {"ok": True}


@app.get("/api/models")
def list_models():
    prov = stores.active_provider()
    return {"models": (prov or {}).get("models", []), "active": stores.load_config().get("activeModel")}


class ProbeBody(BaseModel):
    baseUrl: str
    apiKey: str | None = None


@app.post("/api/probe-models")
def probe_models(b: ProbeBody):
    """Query an OpenAI-compatible provider's /models endpoint to auto-detect
    which models the supplied API key can use."""
    base = (b.baseUrl or "").rstrip("/")
    if not base:
        return {"ok": False, "error": "Base URL 为空", "models": []}
    key = (b.apiKey or "").strip()
    if not key:
        # Fall back to the saved key for the active provider.
        prov = stores.active_provider()
        key = (prov or {}).get("apiKey", "")
    if not key:
        return {"ok": False, "error": "缺少 API Key", "models": []}
    try:
        r = httpx.get(
            f"{base}/models",
            headers={"Authorization": f"Bearer {key}"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        items = data.get("data", data if isinstance(data, list) else [])
        models = sorted(
            {m.get("id") for m in items if isinstance(m, dict) and m.get("id")}
        )
        if not models:
            return {"ok": False, "error": "供应商未返回模型列表", "models": []}
        return {"ok": True, "models": models, "count": len(models)}
    except httpx.HTTPStatusError as e:
        return {"ok": False, "error": f"HTTP {e.response.status_code}", "models": []}
    except Exception as e:  # pragma: no cover
        return {"ok": False, "error": str(e), "models": []}


# ===== token usage =====
@app.get("/api/usage")
def get_usage():
    return stores.usage_summary()


@app.get("/api/limit-status")
def limit_status():
    """Pure usage-vs-limit status, shared across sessions. The 继续使用
    decision is held client-side per page session, not here."""
    cfg = stores.load_config()
    alert = cfg.get("alert", {})
    enabled = bool(alert.get("enabled"))
    limit = int(alert.get("dailyTokenLimit", 0) or 0)
    summary = stores.usage_summary()
    today_tok = summary["todayTokens"]
    over = enabled and limit > 0 and today_tok >= limit
    return {"enabled": enabled, "limit": limit, "today": today_tok, "over": over}


# ===== skills =====
class SkillBody(BaseModel):
    id: str
    content: str


@app.get("/api/skills")
def get_skills():
    return stores.list_skills()


@app.post("/api/skills")
def post_skill(b: SkillBody):
    if not b.id.strip():
        raise HTTPException(400, "skill id required")
    stores.add_skill(b.id.strip(), b.content)
    return {"ok": True}


@app.delete("/api/skills/{sid}")
def del_skill(sid: str):
    return {"ok": stores.delete_skill(sid)}


# ===== FHE keys =====
class FheUpload(BaseModel):
    name: str
    dataBase64: str


@app.get("/api/fhe-keys")
def fhe_list():
    return stores.fhe_status()


@app.post("/api/fhe-keys")
def fhe_upload(b: FheUpload):
    try:
        data = base64.b64decode(b.dataBase64)
    except Exception:
        raise HTTPException(400, "invalid base64")
    try:
        stores.fhe_save(b.name, data)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"ok": True, "status": stores.fhe_status()}


@app.delete("/api/fhe-keys/{name}")
def fhe_del(name: str):
    try:
        ok = stores.fhe_delete(name)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"ok": ok, "status": stores.fhe_status()}


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8800)
