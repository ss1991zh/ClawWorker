"""
LangGraph agent — model built dynamically from config (provider/model
switchable at runtime via the settings UI).

CLI:
    python agent.py "计算 23 * 19 + 7"
"""

import sys
from datetime import datetime

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

try:
    from langchain.agents import create_agent as create_react_agent
except ImportError:  # pragma: no cover
    from langgraph.prebuilt import create_react_agent

from stores import active_provider, load_config


# --- tools ---
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


TOOLS = [calculator, current_time]


def build_model() -> ChatOpenAI:
    """Construct the chat model from the active provider/model in config."""
    cfg = load_config()
    prov = active_provider(cfg)
    if not prov:
        raise RuntimeError("没有可用的模型供应商，请在配置中添加。")
    return ChatOpenAI(
        model=cfg.get("activeModel") or (prov.get("models") or ["openai/gpt-5.1-chat"])[0],
        api_key=prov["apiKey"],
        base_url=prov["baseUrl"],
        temperature=0,
        timeout=120,
    )


def build_agent(checkpointer=None):
    """Build a ReAct agent using the current config's model."""
    model = build_model()
    if checkpointer is not None:
        return create_react_agent(model, TOOLS, checkpointer=checkpointer)
    return create_react_agent(model, TOOLS)


if __name__ == "__main__":
    a = build_agent()
    q = " ".join(sys.argv[1:]).strip() or "计算 23 * 19 + 7，再告诉我现在几点"
    print(f">>> {q}\n")
    res = a.invoke({"messages": [{"role": "user", "content": q}]})
    for m in res["messages"]:
        if getattr(m, "type", "") == "ai" and m.content:
            print(m.content)
