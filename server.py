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
import queue as _queue
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone

import httpx

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
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
    stores.delete_traces(sid)
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
    traces = stores.get_traces(sid)
    out: list = []
    last_ai = None
    turn = 0

    def flush():
        nonlocal last_ai, turn
        if last_ai is not None:
            tr = traces[turn] if turn < len(traces) else []
            out.append({"role": "assistant", "text": last_ai, "trace": tr})
            turn += 1
            last_ai = None

    for m in msgs:
        r = getattr(m, "type", "")
        if r == "human":
            flush()  # close previous turn's assistant answer
            out.append({"role": "user", "text": m.content})
        elif r == "ai" and getattr(m, "content", ""):
            last_ai = m.content  # keep latest; final one is the answer
    flush()
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
            # 中间 AI 消息：先记思考文本（若有），再记工具调用
            if r == "ai" and m.content:
                trace.append({"kind": "thinking", "text": str(m.content)})
            for tc in tcs:
                trace.append({"kind": "tool-call", "text": f"{tc['name']}({tc['args']})"})
        elif r == "tool":
            trace.append({"kind": "tool-result", "text": str(m.content)})
        elif r == "ai" and m.content:
            # 最终回答；上一个被当作 answer 的中间内容降级为思考
            if answer:
                trace.append({"kind": "thinking", "text": answer})
            answer = m.content

    stores.record_usage(req.session_id, cfg.get("activeModel", "?"), in_tok, out_tok)
    stores.append_trace(req.session_id, trace)  # 持久化，刷新后可重看

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


######################################################################
# Background "jobs" so that a chat run is decoupled from the SSE client.
#
# Why: with the old design, refreshing the page mid-answer killed the
# SSE generator, which in turn cut off `ag.stream(...)` — so the agent's
# work was lost and nothing was persisted. Now we spawn the agent in a
# background thread and keep a per-session Job that buffers every SSE
# event. The HTTP /api/chat/stream endpoint merely subscribes to that
# buffer. If the browser disconnects, the thread keeps running; when the
# user reopens the page we can GET /api/chat/stream/{sid} to replay the
# buffered events and tail any new ones until completion.
######################################################################

_SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
_JOB_TTL = 600  # keep finished jobs for 10 minutes for late refresh / resume


class _Job:
    def __init__(self) -> None:
        self.events: list[dict] = []           # full ordered history
        self.done: bool = False
        self.finished_at: float | None = None
        self.subscribers: list[_queue.Queue] = []
        self.lock = threading.Lock()

    def emit(self, ev: dict) -> None:
        with self.lock:
            self.events.append(ev)
            subs = list(self.subscribers)
        for q in subs:
            try:
                q.put_nowait(ev)
            except Exception:
                pass

    def finish(self) -> None:
        with self.lock:
            self.done = True
            self.finished_at = time.time()
            subs = list(self.subscribers)
            self.subscribers.clear()
        for q in subs:
            try:
                q.put_nowait(None)  # sentinel
            except Exception:
                pass

    def subscribe(self) -> _queue.Queue:
        q: _queue.Queue = _queue.Queue()
        with self.lock:
            for ev in self.events:
                q.put_nowait(ev)
            if self.done:
                q.put_nowait(None)
            else:
                self.subscribers.append(q)
        return q

    def unsubscribe(self, q: _queue.Queue) -> None:
        with self.lock:
            try:
                self.subscribers.remove(q)
            except ValueError:
                pass


_jobs: dict[str, _Job] = {}
_jobs_lock = threading.Lock()


def _evict_expired_jobs() -> None:
    now = time.time()
    with _jobs_lock:
        for sid in [s for s, j in _jobs.items()
                    if j.done and j.finished_at and now - j.finished_at > _JOB_TTL]:
            _jobs.pop(sid, None)


def _start_chat_job(sid: str, text: str, override: bool) -> _Job:
    job = _Job()
    with _jobs_lock:
        _jobs[sid] = job

    def run() -> None:
        try:
            over, today_tok, limit = _over_limit()
            if over and not override:
                job.emit({
                    "t": "blocked",
                    "message": (
                        f"今日 Token 用量已达到上限（{today_tok:,} / {limit:,}）。\n"
                        "为控制成本，已暂停继续调用。你可以选择继续使用（忽略今日上限），"
                        "或等待明日 0 点自动重置。"
                    ),
                })
                return
            cfg = stores.load_config()
            ag = get_agent()
            if ag is None:
                job.emit({"t": "error",
                          "message": "尚未配置大模型，请在「配置中心 → 大模型配置」填写 API 并保存。"})
                return

            config = {"configurable": {"thread_id": sid}}
            trace: list = []
            answer = ""
            in_tok = out_tok = 0
            try:
                for chunk in ag.stream(
                    {"messages": [{"role": "user", "content": text}]},
                    config,
                    stream_mode="updates",
                ):
                    for _node, upd in (chunk or {}).items():
                        msgs = (upd or {}).get("messages", []) if isinstance(upd, dict) else []
                        for m in msgs:
                            r = getattr(m, "type", "")
                            um = getattr(m, "usage_metadata", None)
                            if um:
                                in_tok += um.get("input_tokens", 0) or 0
                                out_tok += um.get("output_tokens", 0) or 0
                            tcs = getattr(m, "tool_calls", None)
                            if tcs:
                                if r == "ai" and m.content:
                                    step = {"kind": "thinking", "text": str(m.content)}
                                    trace.append(step)
                                    job.emit({"t": "step", **step})
                                for tc in tcs:
                                    step = {"kind": "tool-call",
                                            "text": f"{tc['name']}({tc['args']})"}
                                    trace.append(step)
                                    job.emit({"t": "step", **step})
                            elif r == "tool":
                                step = {"kind": "tool-result", "text": str(m.content)}
                                trace.append(step)
                                job.emit({"t": "step", **step})
                            elif r == "ai" and m.content:
                                if answer:
                                    step = {"kind": "thinking", "text": answer}
                                    trace.append(step)
                                    job.emit({"t": "step", **step})
                                answer = m.content
            except Exception as exc:  # pragma: no cover
                job.emit({"t": "error", "message": f"模型调用失败：{exc}"})
                return

            stores.record_usage(sid, cfg.get("activeModel", "?"), in_tok, out_tok)
            stores.append_trace(sid, trace)
            with _lock:
                s = _load_sessions()
                meta = _find(s, sid)
                title = "新会话"
                if meta:
                    if meta["title"] == "新会话":
                        meta["title"] = text[:20] + ("…" if len(text) > 20 else "")
                    meta["updated_at"] = _now()
                    _save_sessions(s)
                    title = meta["title"]
            summary = stores.usage_summary()
            job.emit({
                "t": "done",
                "answer": answer or "（无回复）",
                "title": title,
                "usage": {"in": in_tok, "out": out_tok},
                "alert": summary["alert"],
            })
        finally:
            job.finish()

    threading.Thread(target=run, daemon=True).start()
    return job


def _subscribe_gen(job: _Job):
    q = job.subscribe()

    def gen():
        try:
            while True:
                try:
                    ev = q.get(timeout=15)
                except _queue.Empty:
                    yield ": keep-alive\n\n"
                    continue
                if ev is None:
                    return
                yield "data: " + json.dumps(ev, ensure_ascii=False) + "\n\n"
        finally:
            job.unsubscribe(q)

    return gen()


@app.post("/api/chat/stream")
def chat_stream(req: ChatRequest):
    """Start an agent run in the background and stream its events.

    The actual work is done in a thread (see `_start_chat_job`), so the
    agent keeps running even if the browser refreshes or disconnects.
    """
    text = (req.message or "").strip()
    if not text:
        raise HTTPException(400, "empty message")
    with _lock:
        if not _find(_load_sessions(), req.session_id):
            raise HTTPException(404, "session not found")
    _evict_expired_jobs()
    with _jobs_lock:
        existing = _jobs.get(req.session_id)
    if existing and not existing.done:
        raise HTTPException(409, "该会话正在生成回复，请先等待完成或取消后再发送。")
    job = _start_chat_job(req.session_id, text, req.override)
    return StreamingResponse(_subscribe_gen(job),
                             media_type="text/event-stream", headers=_SSE_HEADERS)


@app.get("/api/chat/inflight/{sid}")
def chat_inflight(sid: str):
    """Frontend uses this on page load to decide whether to auto-reattach."""
    _evict_expired_jobs()
    with _jobs_lock:
        job = _jobs.get(sid)
    return {"inflight": bool(job and not job.done)}


@app.get("/api/chat/stream/{sid}")
def chat_stream_resume(sid: str):
    """Subscribe to an existing job's events (replay from beginning,
    then tail until completion). Used after page refresh."""
    _evict_expired_jobs()
    with _jobs_lock:
        job = _jobs.get(sid)
    if not job:
        return StreamingResponse(
            iter([": no-inflight\n\n"]),
            media_type="text/event-stream", headers=_SSE_HEADERS,
        )
    return StreamingResponse(_subscribe_gen(job),
                             media_type="text/event-stream", headers=_SSE_HEADERS)


@app.post("/api/chat/cancel/{sid}")
def chat_cancel(sid: str):
    """Detach the in-memory job so the user can start a new turn.

    NOTE: The background thread itself continues to run to completion
    (we can't safely interrupt the LLM/tool calls mid-execution) but its
    events are no longer surfaced and it won't block a fresh /api/chat/stream
    POST. The trace + usage from the abandoned run are still persisted.
    """
    with _jobs_lock:
        job = _jobs.pop(sid, None)
    return {"ok": True, "had_job": bool(job)}


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
    content: str
    id: str | None = None  # 可选；缺省时按 frontmatter 的 name 推导


@app.get("/api/skills")
def get_skills():
    return stores.list_skills()


@app.post("/api/skills")
def post_skill(b: SkillBody):
    ok, err, name, desc = stores.validate_skill(b.content or "")
    if not ok:
        raise HTTPException(400, f"SKILL.md 格式校验失败：{err}")
    skill_id = (b.id or "").strip() or name
    stores.add_skill(skill_id, b.content)
    return {"ok": True, "id": skill_id, "name": name, "description": desc}


class SkillBundle(BaseModel):
    # [{path: "skillA/SKILL.md", b64: "..."}, ...]
    files: list[dict]


@app.post("/api/skills/upload")
def post_skill_bundle(b: SkillBundle):
    """Install one or more skills from a dropped folder (multi-file skills,
    OpenClaw spec: SKILL.md + references/scripts/templates/assets)."""
    if not b.files:
        raise HTTPException(400, "未收到任何文件")
    result = stores.install_skill_bundle(b.files)
    if not result.get("ok"):
        raise HTTPException(400, result.get("error") or "未找到有效的 SKILL.md")
    return result


@app.delete("/api/skills/{sid:path}")
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
