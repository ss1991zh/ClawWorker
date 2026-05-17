"""
LangGraph agent — model built dynamically from config, with Skill support
(progressive disclosure) and a sandboxed Python runner that uses the FHE
virtualenv so 密态计算 skills can actually execute.

CLI:
    python agent.py "加密 [1,2,3] 和 [4,5,6] 求点积"
"""

import pathlib
import subprocess
import sys
import tempfile
from datetime import datetime

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

try:
    from langchain.agents import create_agent as create_react_agent
except ImportError:  # pragma: no cover
    from langgraph.prebuilt import create_react_agent

import stores
from stores import active_provider, load_config

ROOT = pathlib.Path(__file__).parent
SKILLS_DIR = ROOT / "data" / "skills"
FHE_VENV_PY = ROOT / ".venv-fhe" / "bin" / "python"


# --- generic tools ---
@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '23 * 19 + 4'.
    Only +, -, *, /, parentheses and numbers are allowed.
    """
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "error: expression contains disallowed characters"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception as exc:  # pragma: no cover
        return f"error: {exc}"


@tool
def current_time() -> str:
    """Return the current local date and time as an ISO-8601 string."""
    return datetime.now().isoformat(timespec="seconds")


# --- skill tools (progressive disclosure, OpenClaw-style) ---
@tool
def read_skill(skill_id: str) -> str:
    """Load a skill's full SKILL.md instructions plus the list of its
    related files. Call this when the user's task matches a skill listed
    in the system prompt's <available_skills>. `skill_id` is the skill id
    shown there.
    """
    skill_dir = SKILLS_DIR / skill_id
    md = skill_dir / "SKILL.md"
    if not md.exists():
        # try recursive (nested category dirs)
        hits = list(SKILLS_DIR.rglob("SKILL.md"))
        match = next((h for h in hits if h.parent.name == skill_id), None)
        if match is None:
            return f"error: skill '{skill_id}' not found"
        skill_dir, md = match.parent, match
    body = md.read_text(encoding="utf-8", errors="replace")
    files = sorted(
        str(p.relative_to(skill_dir))
        for p in skill_dir.rglob("*")
        if p.is_file() and p.name != "SKILL.md"
    )
    extra = (
        "\n\n--- 关联文件（用 read_skill_file 按需读取）---\n" + "\n".join(files)
        if files
        else ""
    )
    return f"# SKILL: {skill_id}\n\n{body}{extra}"


@tool
def read_skill_file(skill_id: str, relpath: str) -> str:
    """Read a related file inside a skill directory (e.g. a reference,
    template, or script the SKILL.md points to)."""
    base = (SKILLS_DIR / skill_id).resolve()
    if not base.exists():
        hits = [h.parent for h in SKILLS_DIR.rglob("SKILL.md") if h.parent.name == skill_id]
        if not hits:
            return f"error: skill '{skill_id}' not found"
        base = hits[0].resolve()
    target = (base / relpath).resolve()
    if not str(target).startswith(str(base)):
        return "error: path traversal blocked"
    if not target.is_file():
        return f"error: file '{relpath}' not found in skill '{skill_id}'"
    data = target.read_bytes()
    if len(data) > 200_000:
        return f"(file too large: {len(data)} bytes; first 200KB)\n" + data[:200_000].decode(
            "utf-8", errors="replace"
        )
    return data.decode("utf-8", errors="replace")


# --- Python runner (FHE venv) ---
@tool
def run_python(code: str) -> str:
    """Execute Python code and return its stdout/stderr.

    Runs inside the project's FHE virtualenv where `crypto_toolkit`,
    `henumpy`, `pandaseal`, `helearn` are installed and the encryption
    keys are linked. Use this to actually run code generated from an
    FHE/密态计算 skill.

    For encrypted-computation tasks ALWAYS print, in order:
      1. the ciphertext object(s) right after ct.encrypt(...)
      2. the computed ciphertext object after the hp/ps/hl operation
      3. the decrypted plaintext after ct.decrypt(...)
    so the user can see 密文→计算→明文 the whole way.
    """
    py = str(FHE_VENV_PY) if FHE_VENV_PY.exists() else sys.executable
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        proc = subprocess.run(
            [py, path],
            capture_output=True,
            text=True,
            timeout=240,
            cwd=str(ROOT),
        )
    except subprocess.TimeoutExpired:
        return "error: execution timed out (240s)"
    finally:
        try:
            pathlib.Path(path).unlink()
        except OSError:
            pass
    out = proc.stdout.strip()
    err = proc.stderr.strip()
    # FHE libs spew a harmless atexit FreeDoublePtr traceback on shutdown.
    # Drop everything from the first such traceback onward.
    if err:
        lines = err.splitlines()
        cut = len(lines)
        for i, ln in enumerate(lines):
            if "free_double_ptr" in ln or "FreeDoublePtr" in ln or "Exception ignored" in ln:
                # walk back to the start of this traceback block
                j = i
                while j > 0 and not lines[j].startswith("Traceback"):
                    j -= 1
                cut = min(cut, j)
                break
        err = "\n".join(lines[:cut]).strip()
    parts = []
    if out:
        parts.append(out)
    if err:
        parts.append(f"[stderr]\n{err}")
    if proc.returncode != 0 and not parts:
        parts.append(f"(exit code {proc.returncode}, no output)")
    return "\n".join(parts) or "(no output)"


GENERIC_TOOLS = [calculator, current_time, read_skill, read_skill_file, run_python]


def _skill_catalog() -> str:
    skills = stores.list_skills()
    if not skills:
        return ""
    lines = [
        "\n\n以下技能提供针对特定任务的专门指引。当用户任务匹配某技能描述时，"
        "先用 read_skill(skill_id) 读取它的完整指引，再按指引用 run_python 执行：\n",
        "<available_skills>",
    ]
    for s in skills:
        lines.append(
            f"  <skill id=\"{s['id']}\" name=\"{s['name']}\">{s['description']}</skill>"
        )
    lines.append("</available_skills>")
    lines.append(
        "\n密态计算（FHE）任务要点：read_skill 读 zfhe-skill 路由，按需再读子技能"
        "（henumpy/pandaseal/helearn）；生成的代码顶部需 hp.initDict()+ct.initSK()；"
        "在 run_python 里务必依次打印【加密后的密文对象】【计算后的密文对象】"
        "【解密后的明文】，让用户看到 密文→计算→明文 全过程。"
    )
    return "\n".join(lines)


SYSTEM_BASE = (
    "你是 ClawWorker 智能助手，一个可调用工具与技能的 AI Agent。"
    "回答用中文。需要计算/查询/密态运算时主动使用工具。"
)


def build_model() -> ChatOpenAI:
    cfg = load_config()
    prov = active_provider(cfg)
    if not prov:
        raise RuntimeError("没有可用的模型供应商，请在配置中添加。")
    return ChatOpenAI(
        model=cfg.get("activeModel") or (prov.get("models") or ["openai/gpt-5.1-chat"])[0],
        api_key=prov["apiKey"],
        base_url=prov["baseUrl"],
        temperature=0,
        timeout=240,
    )


def build_agent(checkpointer=None):
    """Build a ReAct agent: current model + generic tools + skill catalog."""
    model = build_model()
    system_prompt = SYSTEM_BASE + _skill_catalog()
    kwargs = {"system_prompt": system_prompt}
    if checkpointer is not None:
        kwargs["checkpointer"] = checkpointer
    return create_react_agent(model, GENERIC_TOOLS, **kwargs)


if __name__ == "__main__":
    a = build_agent()
    q = " ".join(sys.argv[1:]).strip() or "加密 [1,2,3,4,5] 和 [10,20,30,40,50]，求点积"
    print(f">>> {q}\n")
    res = a.invoke({"messages": [{"role": "user", "content": q}]})
    for m in res["messages"]:
        if getattr(m, "type", "") == "ai" and m.content:
            print(m.content)
