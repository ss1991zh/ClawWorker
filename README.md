# LangGraph Agent

基于 LangGraph 的轻量级 AI Agent，带中文 Web UI、多会话、配置中心。本地部署。

## 功能

- **多会话**：新建 / 删除 / 切换 / 历史持久化（LangGraph SqliteSaver）
- **配置中心**
  - 大模型配置（OpenAI 兼容 API；输入后可自动探测可用模型）
  - Token 用量及监控（统计 + 趋势 + 每日上限预警，超限拦截弹窗）
  - Skill 管理（SKILL.md 文件）
  - 同态密钥管理（skf / dictf / user_authorization）
- **打字机效果**回复、响应式蓝色简约 UI、全中文

## 目录

```
agent.py            ReAct agent（model 由配置动态构建）
server.py           FastAPI：会话 / 聊天 / 配置 / 用量 / skill / 密钥 API
stores.py           本地持久化（config / usage / skills / fhe-keys）
static/index.html   单文件 Web UI
requirements.txt
data/               运行时数据（gitignore，含密钥不入库）
```

## 运行

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
# 打开 http://127.0.0.1:8800 → 配置中心填 API → 开始使用
```

## 技术栈

LangGraph · LangChain · FastAPI · 原生 JS（无构建）。模型层走 OpenAI 兼容
endpoint（OpenRouter / OpenAI / 自建网关 / Ollama 等均可）。
