"""
Persistence stores for config, token usage, skills, and FHE keys.

All state lives under ./data/ as plain JSON / files so it is easy to
inspect, back up, and reset.
"""

from __future__ import annotations

import json
import pathlib
import threading
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

CONFIG_FILE = DATA / "config.json"
USAGE_FILE = DATA / "usage.jsonl"
SKILLS_DIR = DATA / "skills"
FHE_DIR = DATA / "fhe-keys"
SKILLS_DIR.mkdir(exist_ok=True)
FHE_DIR.mkdir(exist_ok=True)

_lock = threading.Lock()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Config: LLM providers, active model, alert thresholds
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "providers": [],
    "activeProvider": "",
    "activeModel": "",
    "alert": {"enabled": False, "dailyTokenLimit": 200000},
}


def load_config() -> dict:
    with _lock:
        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2))
            return json.loads(json.dumps(DEFAULT_CONFIG))
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            return json.loads(json.dumps(DEFAULT_CONFIG))


def save_config(cfg: dict) -> dict:
    with _lock:
        CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
    return cfg


def active_provider(cfg: dict | None = None) -> dict | None:
    cfg = cfg or load_config()
    return next((p for p in cfg.get("providers", []) if p["id"] == cfg.get("activeProvider")), None)


# ---------------------------------------------------------------------------
# Token usage: append-only log + aggregates + alert check
# ---------------------------------------------------------------------------

def record_usage(session_id: str, model: str, in_tok: int, out_tok: int) -> None:
    rec = {
        "ts": now_iso(),
        "session": session_id,
        "model": model,
        "in": int(in_tok or 0),
        "out": int(out_tok or 0),
        "total": int((in_tok or 0) + (out_tok or 0)),
    }
    with _lock:
        with USAGE_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _read_usage() -> list[dict]:
    if not USAGE_FILE.exists():
        return []
    out = []
    for line in USAGE_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def usage_summary() -> dict:
    recs = _read_usage()
    today = datetime.now(timezone.utc).date().isoformat()
    total = sum(r["total"] for r in recs)
    today_total = sum(r["total"] for r in recs if r["ts"][:10] == today)
    # Per-day series (last 14 days)
    by_day: dict[str, int] = {}
    for r in recs:
        day = r["ts"][:10]
        by_day[day] = by_day.get(day, 0) + r["total"]
    series = sorted(by_day.items())[-14:]
    # Per-model breakdown
    by_model: dict[str, int] = {}
    for r in recs:
        by_model[r["model"]] = by_model.get(r["model"], 0) + r["total"]

    cfg = load_config()
    alert = cfg.get("alert", {})
    limit = int(alert.get("dailyTokenLimit", 0) or 0)
    alerting = bool(alert.get("enabled")) and limit > 0 and today_total >= limit

    return {
        "totalTokens": total,
        "todayTokens": today_total,
        "callCount": len(recs),
        "series": [{"day": d, "tokens": t} for d, t in series],
        "byModel": [{"model": m, "tokens": t} for m, t in sorted(by_model.items(), key=lambda x: -x[1])],
        "recent": list(reversed(recs[-30:])),
        "alert": {"enabled": bool(alert.get("enabled")), "dailyTokenLimit": limit, "triggered": alerting},
    }


# ---------------------------------------------------------------------------
# Skills: SKILL.md-style markdown files under data/skills/
# ---------------------------------------------------------------------------

def list_skills() -> list[dict]:
    out = []
    for d in sorted(SKILLS_DIR.iterdir()):
        md = d / "SKILL.md" if d.is_dir() else d
        if d.is_dir() and md.exists():
            text = md.read_text(encoding="utf-8", errors="replace")
            name, desc = _parse_skill_frontmatter(text, d.name)
            out.append({"name": name, "id": d.name, "description": desc, "size": md.stat().st_size})
        elif d.is_file() and d.suffix == ".md":
            text = d.read_text(encoding="utf-8", errors="replace")
            name, desc = _parse_skill_frontmatter(text, d.stem)
            out.append({"name": name, "id": d.stem, "description": desc, "size": d.stat().st_size})
    return out


def _parse_skill_frontmatter(text: str, fallback: str) -> tuple[str, str]:
    name, desc = fallback, ""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            for line in text[3:end].splitlines():
                if line.strip().startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                elif line.strip().startswith("description:"):
                    desc = line.split(":", 1)[1].strip()
    return name, desc


def add_skill(skill_id: str, content: str) -> None:
    safe = "".join(c for c in skill_id if c.isalnum() or c in "-_")
    d = SKILLS_DIR / safe
    d.mkdir(exist_ok=True)
    (d / "SKILL.md").write_text(content, encoding="utf-8")


def delete_skill(skill_id: str) -> bool:
    import shutil

    safe = "".join(c for c in skill_id if c.isalnum() or c in "-_")
    target = SKILLS_DIR / safe
    if target.is_dir():
        shutil.rmtree(target)
        return True
    f = SKILLS_DIR / f"{safe}.md"
    if f.exists():
        f.unlink()
        return True
    return False


# ---------------------------------------------------------------------------
# FHE keys: skf / dictf / user_authorization stored under data/fhe-keys/
# ---------------------------------------------------------------------------

FHE_KEY_NAMES = ("skf", "dictf", "user_authorization")


def fhe_status() -> list[dict]:
    out = []
    for name in FHE_KEY_NAMES:
        p = FHE_DIR / name
        if p.exists():
            st = p.stat()
            out.append(
                {
                    "name": name,
                    "present": True,
                    "size": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(
                        timespec="seconds"
                    ),
                }
            )
        else:
            out.append({"name": name, "present": False, "size": 0, "mtime": None})
    return out


def fhe_save(name: str, data: bytes) -> dict:
    if name not in FHE_KEY_NAMES:
        raise ValueError(f"invalid key name: {name}")
    p = FHE_DIR / name
    p.write_bytes(data)
    try:
        p.chmod(0o400)
    except Exception:
        pass
    return {"name": name, "size": p.stat().st_size}


def fhe_delete(name: str) -> bool:
    if name not in FHE_KEY_NAMES:
        raise ValueError(f"invalid key name: {name}")
    p = FHE_DIR / name
    if p.exists():
        p.unlink()
        return True
    return False
