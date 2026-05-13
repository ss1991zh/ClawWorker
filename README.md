<h1 align="center">🦞 ClawWorker</h1>

<p align="center">
  <strong>面向企业的安全 AI 数字员工 · Secure AI Digital Worker for Enterprises</strong>
</p>

<p align="center">
  <a href="docs/clawworker-overview.md"><img src="https://img.shields.io/badge/Docs-Overview-1f6feb?style=for-the-badge" alt="Docs"></a>
  <a href="https://github.com/ss1991zh/ClawWorker"><img src="https://img.shields.io/badge/Status-v0.2--alpha-orange?style=for-the-badge" alt="Status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"></a>
  <a href="https://github.com/openclaw/openclaw"><img src="https://img.shields.io/badge/Forked%20from-OpenClaw-5865F2?style=for-the-badge" alt="Forked from OpenClaw"></a>
</p>

---

**ClawWorker** 在 [OpenClaw](https://github.com/openclaw/openclaw) 基础上做企业向二次开发，把 **全同态加密（FHE）** 直接嵌入 AI Agent 的能力栈。让 AI 在密文上做数值/统计/机器学习推理——**数据不出本地、私钥不离用户、企业敢用**。

---

## ✨ 核心特性

| 维度 | ClawWorker |
|------|------------|
| 🔐 **密态计算** | HENumpy / PandaSeal / HELearn / HETorch + crypto_toolkit 五件套 vendored 入仓 |
| 🧠 **多 Worker 协作** | 主脑 + 多个 Worker + Skill Engine（分解优先 / 调度优先双模式） |
| 🛡 **五层安全** | FHE · 本地密钥隔离 · 可信芯片 · 权限约束 · 任务隔离 |
| 📦 **预装 FHE 技能** | 5 个开箱即用的 zion-skill（zfhe / henumpy / pandaseal / hetorch / helearn）|
| 🛠 **完整工具链** | `fhe-keys` CLI · `fhe-agent` 自然语言→密文计算 demo · doctor 自检 |
| 🏢 **产品形态** | 黑盒（中小企业）+ 服务站（企业级） |

---

## 🚀 快速开始

```bash
# 1. 克隆
git clone https://github.com/ss1991zh/ClawWorker.git
cd ClawWorker

# 2. 放置 FHE 密钥（vendor 提供：skf / dictf / user_authorization）
mkdir -p ~/.openclaw/fhe-keys
cp /path/to/skf                ~/.openclaw/fhe-keys/
cp /path/to/dictf              ~/.openclaw/fhe-keys/
cp /path/to/user_authorization ~/.openclaw/fhe-keys/

# 3. 安装 FHE 运行时（Python 3.11 + venv）
bash vendor/fhe-runtime/install.sh --venv .venv-fhe

# 4. 检查就绪状态
node scripts/fhe-keys.mjs status
```

### 端到端验证

```bash
# 加密 → 密文计算 → 解密（smoke test）
source .venv-fhe/bin/activate
python vendor/fhe-runtime/tests/smoke_test.py

# 自然语言 → Agent 生成代码 → 密文执行（需 ANTHROPIC_API_KEY）
node scripts/fhe-agent.mjs "加密 [1,2,3,4,5] 和 [10,20,30,40,50]，求点积"
```

---

## 🧭 架构一览

```
┌──────────────────────────────────────────────┐
│             主脑（任务调度核心）                  │
└──────────────┬───────────────────────────────┘
        ┌──────┼──────┬──────┐
        ▼      ▼      ▼      ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │Worker 1│ │Worker 2│ │Worker N│  ← 多数字员工并行/协作
   └───┬────┘ └───┬────┘ └───┬────┘
       └──────────┼──────────┘
                  ▼
       ┌──────────────────────┐
       │     Skill Engine     │
       │ ┌──────────────────┐ │
       │ │ 密态计算技能（FHE）│ │
       │ │ 通用自动化技能     │ │
       │ │ 任务执行技能       │ │
       │ └──────────────────┘ │
       └──────────────────────┘
```

详细架构、安全模型、能力分层与产品形态见 **[docs/clawworker-overview.md](docs/clawworker-overview.md)**。

---

## 📂 仓库结构

```
ClawWorker/
├── src/fhe-keys/                   FHE 密钥管理后端（TS 模块 + doctor 检查）
├── skills/                         53 个预装技能，含 5 个 FHE skills
│   ├── zfhe-skill/         🔐    密态计算元编排（推荐入口）
│   ├── henumpy-skill/      🔢    密文 NumPy
│   ├── pandaseal-skill/    🐼    密文 Pandas
│   ├── helearn-skill/      📊    密文 scikit-learn
│   └── hetorch-skill/      🔥    密文 PyTorch
├── vendor/fhe-runtime/             4 个 Python 包 + install/link 脚本 + 测试
├── scripts/
│   ├── fhe-keys.mjs                密钥管理 CLI
│   └── fhe-agent.mjs               自然语言 → 密文计算 演示
├── docs/
│   ├── clawworker-overview.md      ⭐ 完整项目说明（产品 + 架构 + 进度）
│   ├── fhe-keys-ui.md              UI 配置面板集成补丁
│   └── openclaw-upstream-readme.md 上游 OpenClaw 原 README
└── ~/.openclaw/fhe-keys/           用户密钥（不入 git）
```

---

## 🛣 路线图

| 优先级 | 任务 |
|--------|------|
| 🔴 | UI Settings → FHE Keys 配置面板落地 |
| 🔴 | 完整 OpenClaw gateway 本地跑通 + WebChat 验证 |
| 🟡 | HETorch 包 vendor + 密文 LLM/Transformer 推理 |
| 🟡 | Multi-Worker 调度引擎落地 |
| 🟢 | 可信芯片集成（SGX / Apple Secure Enclave） |
| 🟢 | 加密 Memory（FHE 向量检索） |

---

## 🤝 与 OpenClaw 上游的关系

| 维度 | OpenClaw 上游 | **ClawWorker** |
|------|---------------|----------------|
| 定位 | 个人 AI 助手 | 企业级安全数字员工 |
| 加密能力 | 无 | **FHE 密态计算** |
| 部署形态 | 本地软件 | **黑盒硬件 + 服务站** |
| 协作模型 | 单 Agent + 子 session | **主脑 + 多 Worker 协作** |
| 目标用户 | 个人极客 | **中小企业 / 企业** |

保留 `upstream` remote 持续吸收上游的渠道与 Agent 改进：

```bash
git fetch upstream
git merge upstream/main
```

---

## 📚 文档导航

| 文档 | 适用读者 |
|------|---------|
| [`docs/clawworker-overview.md`](docs/clawworker-overview.md) | **新成员 / 产品 / 商务** —— 完整项目说明 |
| [`vendor/fhe-runtime/README.md`](vendor/fhe-runtime/README.md) | 部署/运维 —— FHE 运行时维护 |
| [`docs/fhe-keys-ui.md`](docs/fhe-keys-ui.md) | UI 工程师 —— 密钥管理面板集成 |
| [`skills/zfhe-skill/SKILL.md`](skills/zfhe-skill/SKILL.md) | AI Agent 上下文 —— 密态计算编排 |
| [`docs/openclaw-upstream-readme.md`](docs/openclaw-upstream-readme.md) | 上游开发者 —— OpenClaw 原 README |

---

## 📝 License

MIT — 继承自上游 [OpenClaw](https://github.com/openclaw/openclaw)。

---

<p align="center">
  <strong>OpenClaw 让普通人有了本地 AI 助手；<br>
  ClawWorker 让企业有了在加密数据上工作的 AI 数字员工。</strong>
</p>
