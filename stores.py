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
TRACES_DIR = DATA / "traces"
SKILLS_DIR.mkdir(exist_ok=True)
FHE_DIR.mkdir(exist_ok=True)
TRACES_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Per-session trace log (思考与工具调用记录) — persisted so it survives
# page refresh and can be re-rendered on session reload.
# ---------------------------------------------------------------------------

def append_trace(session_id: str, trace: list) -> None:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")
    if not safe:
        return
    p = TRACES_DIR / f"{safe}.json"
    try:
        cur = json.loads(p.read_text()) if p.exists() else []
    except Exception:
        cur = []
    cur.append(trace or [])
    p.write_text(json.dumps(cur, ensure_ascii=False))


def get_traces(session_id: str) -> list:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")
    p = TRACES_DIR / f"{safe}.json"
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text())
    except Exception:
        return []


def delete_traces(session_id: str) -> None:
    safe = "".join(c for c in session_id if c.isalnum() or c in "-_")
    p = TRACES_DIR / f"{safe}.json"
    if p.exists():
        try:
            p.unlink()
        except OSError:
            pass

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
    # Per-day series — fixed window of the last 14 calendar days,
    # filling 0 for days with no usage so the bar chart is continuous.
    from datetime import timedelta

    by_day: dict[str, int] = {}
    for r in recs:
        day = r["ts"][:10]
        by_day[day] = by_day.get(day, 0) + r["total"]
    today_date = datetime.now(timezone.utc).date()
    series = [
        (
            (today_date - timedelta(days=offset)).isoformat(),
            by_day.get((today_date - timedelta(days=offset)).isoformat(), 0),
        )
        for offset in range(13, -1, -1)  # 13 天前 → 今天，共 14 天
    ]
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
    """Recursively find every SKILL.md under data/skills/. A skill is its
    containing directory (OpenClaw spec: SKILL.md + references/scripts/
    templates/assets). Supports nested category dirs and multi-file skills."""
    out = []
    if not SKILLS_DIR.exists():
        return out
    for md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        skill_dir = md.parent
        rel = skill_dir.relative_to(SKILLS_DIR)
        skill_id = str(rel) if str(rel) != "." else skill_dir.name
        text = md.read_text(encoding="utf-8", errors="replace")
        name, desc = _parse_skill_frontmatter(text, skill_dir.name)
        files = [
            str(p.relative_to(skill_dir))
            for p in sorted(skill_dir.rglob("*"))
            if p.is_file()
        ]
        total = sum((skill_dir / f).stat().st_size for f in files)
        out.append(
            {
                "name": name,
                "id": skill_id,
                "description": desc,
                "size": total,
                "fileCount": len(files),
                "files": files,
            }
        )
    # Legacy: bare *.md directly under skills/ (single-file skill)
    for f in sorted(SKILLS_DIR.glob("*.md")):
        if f.name == "SKILL.md":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        name, desc = _parse_skill_frontmatter(text, f.stem)
        out.append(
            {"name": name, "id": f.stem, "description": desc, "size": f.stat().st_size,
             "fileCount": 1, "files": [f.name]}
        )
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


def validate_skill(content: str) -> tuple[bool, str, str, str]:
    """Validate a SKILL.md. Returns (ok, error, name, description).

    Required: a YAML-ish frontmatter block delimited by `---` containing
    at least `name:` and `description:`, plus a non-empty body.
    """
    text = (content or "").strip()
    if not text.startswith("---"):
        return False, "缺少 frontmatter（文件须以 --- 开头）", "", ""
    end = text.find("---", 3)
    if end < 0:
        return False, "frontmatter 未闭合（缺少结束的 ---）", "", ""
    name, desc = "", ""
    for line in text[3:end].splitlines():
        s = line.strip()
        if s.startswith("name:"):
            name = s.split(":", 1)[1].strip()
        elif s.startswith("description:"):
            desc = s.split(":", 1)[1].strip()
    if not name:
        return False, "frontmatter 缺少 name 字段", "", ""
    if not desc:
        return False, "frontmatter 缺少 description 字段", "", ""
    body = text[end + 3 :].strip()
    if not body:
        return False, "技能正文为空（--- 之后需有说明内容）", "", ""
    return True, "", name, desc


def add_skill(skill_id: str, content: str) -> None:
    safe = "".join(c for c in skill_id if c.isalnum() or c in "-_") or "skill"
    d = SKILLS_DIR / safe
    d.mkdir(exist_ok=True)
    (d / "SKILL.md").write_text(content, encoding="utf-8")


def _safe_rel(rel: str) -> pathlib.PurePosixPath | None:
    """Sanitize an incoming relative path: no abs, no .. traversal."""
    rel = (rel or "").lstrip("/").replace("\\", "/")
    parts = [p for p in pathlib.PurePosixPath(rel).parts if p not in ("", ".")]
    if any(p == ".." for p in parts) or not parts:
        return None
    return pathlib.PurePosixPath(*parts)


def install_skill_bundle(files: list[dict]) -> dict:
    """Install one or more skills from a dropped folder.

    `files` = [{path: "skillA/SKILL.md", b64: "..."}, {path:
    "skillA/references/x.md", b64: "..."}, ...]

    Every SKILL.md defines a skill (its parent dir is the skill root). The
    whole skill subtree is copied under data/skills/<skill-id>/. Returns
    per-skill results.
    """
    import base64 as _b64

    # Index files by sanitized relative path.
    by_path: dict[str, bytes] = {}
    for f in files:
        rel = _safe_rel(f.get("path", ""))
        if rel is None:
            continue
        try:
            by_path[str(rel)] = _b64.b64decode(f.get("b64", ""))
        except Exception:
            continue

    # Find every SKILL.md → its dir is a skill root.
    skill_roots = sorted(
        {str(pathlib.PurePosixPath(p).parent) for p in by_path if p.endswith("SKILL.md")}
    )
    if not skill_roots:
        return {"ok": False, "error": "未找到任何 SKILL.md", "skills": []}

    results = []
    for root in skill_roots:
        root_pp = pathlib.PurePosixPath(root)
        md_key = str(root_pp / "SKILL.md")
        try:
            md_text = by_path[md_key].decode("utf-8", errors="replace")
        except Exception:
            md_text = ""
        ok, err, name, desc = validate_skill(md_text)
        skill_id = root_pp.name if root_pp.name not in ("", ".") else (name or "skill")
        safe_id = "".join(c for c in skill_id if c.isalnum() or c in "-_") or "skill"
        if not ok:
            results.append({"id": safe_id, "name": name or safe_id, "ok": False, "error": err})
            continue
        # Copy every file whose path is under this skill root.
        dest_root = SKILLS_DIR / safe_id
        prefix = root + "/" if root not in ("", ".") else ""
        count = 0
        for path, data in by_path.items():
            if root in ("", ".") or path == root or path.startswith(prefix):
                sub = path[len(prefix):] if prefix else pathlib.PurePosixPath(path).name
                if not sub:
                    continue
                target = dest_root / pathlib.Path(*pathlib.PurePosixPath(sub).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                count += 1
        results.append(
            {"id": safe_id, "name": name, "description": desc, "ok": True, "fileCount": count}
        )

    ok_n = sum(1 for r in results if r["ok"])
    return {"ok": ok_n > 0, "installed": ok_n, "total": len(results), "skills": results}


def delete_skill(skill_id: str) -> bool:
    import shutil

    # Allow nested ids like "category/skill"; sanitize each segment.
    parts = [
        "".join(c for c in seg if c.isalnum() or c in "-_")
        for seg in (skill_id or "").replace("\\", "/").split("/")
        if seg
    ]
    if not parts:
        return False
    target = SKILLS_DIR.joinpath(*parts)
    if target.is_dir():
        shutil.rmtree(target)
        return True
    f = SKILLS_DIR.joinpath(*parts[:-1]) / f"{parts[-1]}.md"
    if f.exists():
        f.unlink()
        return True
    return False


# ---------------------------------------------------------------------------
# FHE keys: skf / dictf / user_authorization stored under data/fhe-keys/
# ---------------------------------------------------------------------------

FHE_KEY_NAMES = ("skf", "dictf", "user_authorization")

# Where each key must end up inside the vendored FHE packages so the
# Python runtime can find it (paths from vendor/fhe-runtime/README.md).
_FHE_RUNTIME = ROOT / "vendor" / "fhe-runtime"
_FHE_LINK_TARGETS = {
    "skf": _FHE_RUNTIME / "crypto_toolkit-64_dev" / "crypto_toolkit" / "file" / "skf",
    "dictf": _FHE_RUNTIME / "henumpy-dev" / "henumpy" / "file" / "dictf",
    "user_authorization": _FHE_RUNTIME / "henumpy-dev" / "henumpy" / "file" / "user_authorization",
}


def _fhe_link(name: str) -> None:
    """Symlink data/fhe-keys/<name> into the vendored package's file/ dir."""
    src = FHE_DIR / name
    dst = _FHE_LINK_TARGETS.get(name)
    if dst is None or not src.exists():
        return
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() or dst.is_symlink():
            dst.unlink()
        dst.symlink_to(src.resolve())
    except Exception:
        pass


def _fhe_unlink(name: str) -> None:
    dst = _FHE_LINK_TARGETS.get(name)
    if dst is not None and (dst.exists() or dst.is_symlink()):
        try:
            dst.unlink()
        except Exception:
            pass


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
    _fhe_link(name)  # 自动放置到 vendor 包 file/ 目录
    return {"name": name, "size": p.stat().st_size}


def fhe_delete(name: str) -> bool:
    if name not in FHE_KEY_NAMES:
        raise ValueError(f"invalid key name: {name}")
    _fhe_unlink(name)
    p = FHE_DIR / name
    if p.exists():
        p.unlink()
        return True
    return False
