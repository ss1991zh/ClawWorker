# ClawWorker 说明文档

> **基于 OpenClaw fork 的密态计算 AI 数字员工**
> 仓库：[ss1991zh/ClawWorker](https://github.com/ss1991zh/ClawWorker)
> 上游：[openclaw/openclaw](https://github.com/openclaw/openclaw)
> 文档版本：v0.2（结合产品介绍 V0.1 与 fork 实施进度）

---

## 一、产品概述

**ClawWorker（爪子工人）** 是一款面向企业的**安全 AI 数字员工**，能够自动执行任务、调用技能并处理数据。区别于传统 AI Agent，ClawWorker 在设计之初就将**安全性**作为核心前提，把**全同态加密（FHE）计算能力**与**可信硬件机制**直接嵌入 AI 数字员工体系。

**一句话定位**：让 AI 在加密状态下完成业务计算的安全数字员工。

### 与传统 AI Agent 的关键差异

| 维度 | 传统 AI Agent | **ClawWorker** |
|------|---------------|----------------|
| 数据处理 | 明文计算 → 泄露风险 | **密文计算**（FHE） |
| 私钥位置 | 服务端 / 不透明 | **本地客户端 + 隔离保护** |
| 硬件保护 | 无 | **可信芯片** |
| 执行约束 | 自由度高、误操作风险 | **权限控制 + 审计** |
| 部署形态 | 云端 SaaS | **本地黑盒 + 服务站** |
| 协作模式 | 单 Agent | **主脑 + 多 Worker 协作** |

---

## 二、行业背景

### 2.1 AI 演进阶段

```
模型阶段 → 辅助阶段 → 执行阶段（Agent）
文本生成   协助人类     自主理解+执行
```

到了 Agent 阶段，AI 不再只是工具，而是**执行者**——能够参与到实际业务流程中，承担具体工作任务。

### 2.2 中小企业的核心诉求

| # | 诉求 | ClawWorker 应对 |
|---|------|----------------|
| 1 | 提升效率，降低人力成本 | Multi-Worker 调度 + 自动化技能体系 |
| 2 | 简化使用门槛 | 黑盒形态，开箱即用 |
| 3 | 支持持续自动化运行 | 数字员工持续运行 + 任务隔离 |
| 4 | 保障数据安全 | **FHE 密态计算 + 本地密钥** |

---

## 三、系统架构

### 3.1 多数字员工协作架构

```
┌──────────────────────────────────────────────────────┐
│                    主脑（决策与调度）                       │
│   任务理解 │ 任务拆解 │ 子任务分发 │ 结果汇总                │
└──────────────────┬───────────────────────────────────┘
                   │
   ┌───────────────┼───────────────┐
   │               │               │
┌──▼───┐       ┌──▼───┐       ┌──▼───┐
│Worker│       │Worker│       │Worker│   ← 多 Claw Worker
│  #1  │       │  #2  │       │  #3  │     并行 / 协作执行
└──┬───┘       └──┬───┘       └──┬───┘
   │              │              │
   └──────────────┼──────────────┘
                  │
       ┌──────────▼──────────┐
       │   Skill Engine      │  ← 统一能力支撑
       │  ┌───────────────┐  │
       │  │ 密态计算技能    │  │  HENumpy / HELearn / HETorch
       │  │ 通用自动化技能  │  │  PandaSeal / Key++
       │  │ 任务执行技能    │  │  Computer / Browser / File / API
       │  └───────────────┘  │
       └─────────────────────┘
```

### 3.2 协作模式

| 模式 | 触发场景 | 任务结构 | 优势 |
|------|----------|----------|------|
| **分解优先** | 流程明确的多阶段任务（数据采集→处理→报告） | 预先拆解、固定路径 | 可控性、稳定性强 |
| **调度优先** | 持续运行、变化快的任务（实时分析、长期自动化） | 动态分配、路径变化 | 资源利用率、响应能力强 |

### 3.3 五层安全机制

```
┌───────────────────────────────────────────────────────┐
│ ① 全同态加密（FHE）                                       │
│   数据加密状态下参与计算，明文不离开本地                       │
├───────────────────────────────────────────────────────┤
│ ② 密钥管理与本地隔离                                       │
│   私钥 永远 在用户本地 / 服务端只见密文                       │
│   "本地加解密 + 远程计算" 架构                              │
├───────────────────────────────────────────────────────┤
│ ③ 可信芯片                                              │
│   硬件级安全 / 受控执行环境 / 防止关键数据被访问或篡改           │
├───────────────────────────────────────────────────────┤
│ ④ 权限控制与执行约束                                       │
│   高风险操作约束 / 执行过程审计 / 减少误操作风险               │
├───────────────────────────────────────────────────────┤
│ ⑤ 数据与任务隔离                                          │
│   每个 Worker 独立环境 / 避免任务间数据交叉                   │
└───────────────────────────────────────────────────────┘
```

---

## 四、核心能力体系

### 4.1 密态计算能力（差异化核心）

| 组件 | 对标 | 功能 | 在 fork 中状态 |
|------|------|------|---------------|
| **HENumpy** | NumPy | 密文数值计算、向量/矩阵运算 | ✅ 已 vendor + 测试通过 |
| **PandaSeal** | Pandas | 密文 DataFrame 数据分析 | ✅ 已 vendor |
| **HELearn** | scikit-learn | 密文机器学习训练/推理 | ✅ 已 vendor |
| **HETorch** | PyTorch | 密文深度学习推理 | 📋 Skill 文档已就位（待 vendor 包） |
| **Key++** | — | 密钥与计算中间件 | ✅ crypto_toolkit 已 vendor |

### 4.2 通用 Skill 能力

| Skill | 功能 |
|-------|------|
| Computer Skill | 控制本地应用与系统操作 |
| Browser Skill | 自动浏览网页、抓取/提交数据 |
| File Skill | 文件读写与管理 |
| API Skill | 调用外部系统与服务接口 |
| Automation Skill | 定时任务与流程自动执行 |

> 注：上述通用 Skill 继承自 OpenClaw 上游的 50+ 内置技能体系。

### 4.3 自动任务执行能力

| 机制 | 职责 |
|------|------|
| **Task Planner** | 任务理解与拆解 |
| **Workflow Engine** | 多步骤任务流程执行 |
| **Multi-Worker 调度** | 多个 Worker 并行执行 |

---

## 五、产品形态

### 5.1 ClawWorker 黑盒（中小企业）

**轻量化本地设备**，让 AI 数字员工在用户环境中运行。

- 🔒 **本地部署**：数据不出本地
- 📦 **开箱即用**：无需复杂配置
- 🔋 **低功耗运行**：适合 7×24 长期自动化
- 🛡 **安全环境**：内置安全架构

**适用**：中小企业日常自动化（运营、报表、客户数据处理）

### 5.2 ClawWorker 服务站（企业级）

**面向更复杂场景的高性能形态**：

- 💪 **高性能计算能力**：复杂数据处理 + AI 推理
- 👥 **多 Worker 支持**：更多数字员工并行
- 📈 **扩展能力**：大规模任务与业务场景
- ⏰ **稳定运行**：长期连续运行

**适用**：企业级数据分析、多任务自动化、高负载业务

---

## 六、应用场景

### 6.1 企业运营自动化

| 替代的人工工作 | ClawWorker 处理方式 |
|--------------|-------------------|
| 数据整理 | Task Planner 拆解 → Multi-Worker 并行 |
| 信息录入 | Browser/API Skill 自动执行 |
| 报表生成 | PandaSeal 密文统计 → 报告输出 |

### 6.2 数据分析与业务支持

- **销售数据分析**：HENumpy/PandaSeal 在密文上做趋势/聚合
- **用户画像**：密态机器学习（HELearn）
- **业务预测**：HETorch 密文神经网络推理

### 6.3 客户与业务数据处理

- 客户信息处理：本地加解密 + 远程密文计算
- 订单数据处理：权限控制限制访问范围
- 业务数据处理：任务隔离避免交叉

---

## 七、技术实现现状（Fork 进度）

> 这部分记录 [ss1991zh/ClawWorker](https://github.com/ss1991zh/ClawWorker) 二次开发实际进度，对应产品介绍文档的工程化落地。

### 7.1 仓库结构

```
ClawWorker/
├── src/                          # OpenClaw 核心（TypeScript）
│   ├── fhe-keys/                 # ✅ 新增：FHE 密钥管理后端
│   │   ├── index.ts              # 程序化 API
│   │   ├── doctor-check.ts       # openclaw doctor 检查
│   │   └── index.test.ts         # 单元测试
│   ├── gateway/                  # 网关 / 路由 / RPC
│   ├── agents/                   # Agent 路由
│   ├── channels/                 # 22+ IM 渠道适配
│   └── memory/                   # 长期记忆（计划 FHE 加密）
│
├── skills/                       # 预装技能库
│   ├── zfhe-skill/               # ✅ 元编排（推荐入口）🔐
│   ├── henumpy-skill/            # ✅ 密文 NumPy 🔢
│   ├── pandaseal-skill/          # ✅ 密文 Pandas 🐼
│   ├── hetorch-skill/            # ✅ 密文 PyTorch 🔥
│   ├── helearn-skill/            # ✅ 密文 sklearn 📊
│   └── ...                       # OpenClaw 上游 50+ 技能
│
├── vendor/fhe-runtime/           # ✅ 新增：密态计算运行时
│   ├── crypto_toolkit-64_dev/    #   Key++ / 底层加密
│   ├── henumpy-dev/              #   HENumpy 实现
│   ├── pandaseal-dev/            #   PandaSeal 实现
│   ├── helearn-dev/              #   HELearn 实现
│   ├── install.sh                #   一键安装
│   ├── link-keys.sh              #   密钥软链
│   ├── README.md                 #   运维指南
│   └── tests/                    #   端到端 smoke + agent demo
│
├── scripts/
│   ├── fhe-keys.mjs              # ✅ 密钥管理 CLI
│   └── fhe-agent.mjs             # ✅ Agent → Skill → 代码 → 执行 demo
│
├── docs/
│   └── fhe-keys-ui.md            # ✅ UI 配置面板设计与代码
│
└── ~/.openclaw/fhe-keys/         # 用户密钥目录（不入 git）
    ├── skf                       #   SKF 私钥
    ├── dictf                     #   授权运算字典（~160 MB）
    └── user_authorization        #   软件使用许可
```

### 7.2 已完成阶段

| 阶段 | 内容 | 状态 |
|------|------|------|
| **A** | Vendor 4 个 FHE Python 包 | ✅ |
| **B** | 密钥管理目录约定 + 链接脚本 | ✅ |
| **C** | 5 个 FHE skill manifest 升级（emoji、requires、install hint） | ✅ |
| **D1** | TypeScript fhe-keys 后端模块 | ✅ |
| **D2** | Node.js 密钥管理 CLI | ✅ |
| **D3** | doctor 检查器 | ✅ |
| **D4** | UI 配置面板设计文档（含完整代码补丁） | ✅ |
| **E1** | 端到端 smoke 测试（4 项加密计算）| ✅ |
| **E2** | Agent → Skill → 代码生成 → 执行 demo（9 项统计）| ✅ |

### 7.3 已验证的端到端链路

```
用户自然语言（聊天/CLI）
   ↓
Agent 加载 zfhe-skill SKILL.md + 路由/init/error 文档
   ↓
LLM 生成 ```python``` 代码（henumpy / pandaseal / helearn 调用）
   ↓
.venv-fhe (Python 3.11) 子进程执行
   ↓
hp.initDict() + ct.initSK()  ← 加载 skf/dictf/user_authorization
   ↓
ct.encrypt(明文)  → 密文
   ↓
hp.mean / sum / max / min / std / var / dot / sub …  ← 全程密文运算
   ↓
ct.decrypt(密文结果)  → 用户可读
```

**实测**：9 项统计在密文上的计算结果与明文 NumPy 一致到浮点精度（误差约 1e-14）。

### 7.4 待办路线图

| 优先级 | 任务 | 预期工作量 |
|--------|------|-----------|
| 🔴 高 | UI Settings → FHE Keys 配置面板落地（按 docs/fhe-keys-ui.md） | 中 |
| 🔴 高 | 完整 OpenClaw gateway 本地跑通 + WebChat 验证 | 中 |
| 🟡 中 | HETorch 包 vendor + 密文 LLM/Transformer 推理 demo | 大 |
| 🟡 中 | Multi-Worker 调度引擎落地（产品介绍 §4.2） | 大 |
| 🟢 低 | 可信芯片集成（SGX / Apple Secure Enclave） | 大 |
| 🟢 低 | 加密 Memory（参考"加密语义检索"设计） | 大 |

---

## 八、安装与使用

### 8.1 环境要求

- **Python 3.11**（FHE 运行时必须）
- **Node.js 24**（推荐）或 22.16+
- **macOS**（已验证 Apple Silicon）或 Linux
- 用户密钥三件套：`skf`、`dictf`、`user_authorization`

### 8.2 三步安装

```bash
# 1. 克隆仓库
git clone https://github.com/ss1991zh/ClawWorker.git
cd ClawWorker

# 2. 放置密钥
mkdir -p ~/.openclaw/fhe-keys
cp /path/to/skf                ~/.openclaw/fhe-keys/
cp /path/to/dictf              ~/.openclaw/fhe-keys/
cp /path/to/user_authorization ~/.openclaw/fhe-keys/

# 3. 安装 FHE 运行时（venv 模式）
bash vendor/fhe-runtime/install.sh --venv .venv-fhe
```

### 8.3 验证安装

```bash
# 查看密钥状态
node scripts/fhe-keys.mjs status

# 跑端到端 smoke 测试
source .venv-fhe/bin/activate
python vendor/fhe-runtime/tests/smoke_test.py

# 跑 agent 自然语言 demo（需要 ANTHROPIC_API_KEY）
node scripts/fhe-agent.mjs "加密 [1,2,3,4,5] 和 [10,20,30,40,50]，求点积"
```

### 8.4 密钥日常管理

```bash
node scripts/fhe-keys.mjs status              # 查看状态表
node scripts/fhe-keys.mjs set skf ./new-skf   # 替换某个密钥
node scripts/fhe-keys.mjs link                # 重新软链
node scripts/fhe-keys.mjs remove dictf        # 移除密钥
node scripts/fhe-keys.mjs install             # 重跑完整安装
```

---

## 九、与 OpenClaw 上游的关系

| 维度 | OpenClaw 上游 | **ClawWorker（本 fork）** |
|------|---------------|--------------------------|
| 定位 | 个人 AI 助手 | 企业级安全数字员工 |
| 加密能力 | 无 | **FHE 密态计算** |
| 部署形态 | 本地软件 | **黑盒硬件 + 服务站** |
| 协作 | 单 Agent + 子 session | **主脑 + 多 Worker 协作** |
| 安全模型 | 沙箱 + 配对 | **+ FHE + 可信芯片 + 密钥隔离** |
| 目标用户 | 个人极客 | **中小企业 / 企业** |

**协同策略**：保留 `upstream` remote，未来上游的 IM 渠道、Agent 路由、Skill 体系改进可以拉回 ClawWorker；ClawWorker 专注密态计算和企业能力增强。

```bash
git fetch upstream
git merge upstream/main   # 同步上游
```

---

## 十、相关文档

| 文档 | 说明 |
|------|------|
| [docs/fhe-keys-ui.md](docs/fhe-keys-ui.md) | UI 密钥管理面板的完整集成补丁 |
| [vendor/fhe-runtime/README.md](vendor/fhe-runtime/README.md) | FHE 运行时安装与维护 |
| [vendor/fhe-runtime/tests/smoke_test.py](vendor/fhe-runtime/tests/smoke_test.py) | 端到端 4 项加密计算测试 |
| [vendor/fhe-runtime/tests/agent_demo_query.py](vendor/fhe-runtime/tests/agent_demo_query.py) | HR 薪资 9 项统计 Agent demo |
| [skills/zfhe-skill/SKILL.md](skills/zfhe-skill/SKILL.md) | 密态计算技能元编排 |
| openclaw_说明文档.md | 上游 OpenClaw 项目说明 |
| hermes_vs_openclaw_对比文档.md | 与 Hermes Agent 的对比分析 |

---

## 十一、一句话总结

> **OpenClaw 让普通人有了本地 AI 助手；ClawWorker 让企业有了"在加密数据上工作"的 AI 数字员工。**
>
> 安全不是补丁，而是底层架构。FHE + 本地密钥 + 可信硬件 + 执行约束，构成"敢让 AI 看数据"的四道防线。
