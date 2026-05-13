---
name: zfhe-skill
description: >
  同态加密全流程数据分析编排。根据用户一句话需求，自动识别数据源类型与分析目标，
  调度 pandaseal（密文 Pandas）、henumpy（密文 NumPy）、helearn（密文 sklearn）、
  hetorch2（密文 PyTorch）四个子 skill，生成端到端的密文数据分析代码。
  触发条件：用户需要在加密数据上执行完整的数据分析流程，包括数据读取、探索、
  预处理、统计分析、机器学习训练/预测、深度学习推理等任意组合。
  适用于无法明确归类到单个子 skill 的综合性需求，或需要跨库协作的场景。
user-invocable: true
metadata: {"openclaw":{"emoji":"🔐"}}
---

# zfhe-skill — 同态加密全流程数据分析编排

元编排层（meta-orchestrator），不引入新 API，而是协调四个子 skill 生成完整的密文数据分析代码。

四个子 skill：
- **pandaseal**（别名 `ps`）— 密文 DataFrame 操作，对标 pandas
- **henumpy**（别名 `hp`）— 密文数值计算，对标 numpy
- **helearn**（别名 `hl`）— 密文机器学习，对标 sklearn
- **hetorch2** — 密文深度学习推理，对标 PyTorch

## 何时使用

当用户请求满足以下任一条件时激活此 skill：
- 需要对加密数据执行完整的分析流程（读取 → 处理 → 分析 → 输出）
- 需求跨越多个子 skill 的能力边界（如读取 Excel 后做机器学习）
- 提及"加密数据分析"、"密文数据处理"、"FHE 数据分析"等综合性表述
- 不确定该用哪个具体子 skill 时，由此 skill 统一入口路由

**如果需求明确只涉及单个子 skill**（如纯数值计算、纯 DataFrame 操作、纯模型推理），可直接使用对应子 skill。

## 意图分类决策树

收到用户需求后，按以下两步识别数据源和任务类型，然后确定子 skill 组合。

### Step 1: 数据源识别

| 用户线索 | 数据源类型 | 主要子 skill | 读取方式 |
|---------|-----------|------------|---------|
| Excel/xlsx/csv/json/表格/DataFrame | 结构化文件 | pandaseal | `ps.read_excel()` / `ps.read_csv()` / `ps.read_json()` |
| 数组/向量/矩阵/数值列表 | 数值数组 | henumpy | `ct.encrypt()` / `ct.encrypt_ndarray()` |
| 图像/张量/Tensor/模型权重 | 张量 | hetorch2 | `ct.encrypt_tensor()` |
| 数据集名称（breast_cancer/boston） | 内置数据集 | helearn | `hl.datasets.load_*()` |
| CSV 文件 + 机器学习场景 | CSV→ML | helearn | `ct.encrypt_csv()` |
| 明文 Excel/CSV 需先加密 | 文件级加密 | pandaseal | `ct.encrypt_df()` 或 `ct.encrypt_excel()` / `ct.encrypt_csv()` |

### Step 2: 任务类型识别

| 用户线索 | 任务类型 | 主要子 skill |
|---------|---------|------------|
| 探索/查看/统计描述/分组/聚合/EDA/筛选/排序 | 数据探索 | pandaseal |
| 均值/方差/相关/协方差/线代/多项式拟合/数值运算 | 数值计算 | henumpy |
| 分类/逻辑回归/GBDT/XGBoost/训练/二分类 | ML 分类 | helearn |
| 回归/线性回归/GBRT/房价预测/数值预测 | ML 回归 | helearn |
| CNN/RNN/LSTM/Transformer/推理/深度学习/图像识别 | DL 推理 | hetorch2 |

### Step 3: 组合模式（跨 skill 联合）

| 组合 | 典型场景 | 初始化 |
|------|---------|--------|
| pandaseal 单独 | 加密 Excel EDA | `hp.initDict()` + `ct.initSK()` |
| henumpy 单独 | 密文数值计算 | `hp.initDict()` + `ct.initSK()` |
| pandaseal + henumpy | 读表格 → 数值分析 | `hp.initDict()` + `ct.initSK()` |
| helearn（+ henumpy） | 密文 ML 训练/预测 | `hp.initDict()` + `ct.initSK()` |
| pandaseal + helearn | 读 CSV → ML 建模 | `hp.initDict()` + `ct.initSK()` |
| hetorch2 单独 | 密文深度学习推理 | `hetorch2.initDict()` + `ct.initSK()` |
| hetorch2 + pandaseal/henumpy | 混合流水线 | `hp.initDict()` + `hetorch2.initDict()` + `ct.initSK()` |

## 代码生成工作流

处理用户请求时按以下步骤执行：

1. **意图解析** — 根据上方决策树确定数据源类型 + 任务类型。
2. **路由决策** — 确定需要哪些子 skill（1~3 个）。不确定时读取 `{baseDir}/docs/routing.md`。
3. **子 skill 加载** — 读取对应子 skill 的 SKILL.md 和 INDEX.md：
   - pandaseal → `pandaseal-skill/SKILL.md` + `pandaseal-skill/INDEX.md`
   - henumpy → `henumpy-skill/SKILL.md` + `henumpy-skill/INDEX.md`
   - helearn → `helearn-skill/SKILL.md` + `helearn-skill/INDEX.md`
   - hetorch2 → `hetorch-skill/SKILL.md` + `hetorch-skill/INDEX.md`
4. **查阅初始化** — 参考 `{baseDir}/docs/initialization.md` 确定正确的初始化组合。
5. **分段生成** — 按流水线顺序生成代码：
   - 初始化（import + initDict + initSK）
   - 数据读取/加密
   - 预处理（清洗、转换、特征工程）
   - 分析/建模（统计、训练、推理）
   - 输出/解密（解密结果 + 打印/导出）
6. **自检** — 对照下方硬性规则和错误处理规则逐条检查。

## 硬性规则

1. **不引入新 API** — zfhe-skill 本身不定义任何 API，所有 API 来自四个子 skill。
2. **API 必须可查** — 每个生成脚本中的 API 必须能在对应子 skill 的 INDEX.md 中找到。
3. **初始化必须完整** — 初始化必须覆盖所有用到的子 skill，参见上方组合模式表。
4. **数据格式显式转换** — 跨 skill 传递数据时必须显式转换格式，参考 `{baseDir}/docs/data-flow.md`。
5. **initDict 不互通** — `hetorch2.initDict()` 与 `hp.initDict()` 不互通，混用时必须两个都调用。
6. **禁止猜测** — 不确定时优先查子 skill 的 INDEX.md，禁止凭明文库记忆猜测 API 名称。

## 错误处理规则

错误处理分为三个层面：代码生成阶段自检、生成代码中的防御性编程、路由阶段的兜底。
详细规则参见 `{baseDir}/docs/error-handling.md`，以下为核心摘要。

### A. 代码生成阶段 — LLM 自检

生成代码后、交付用户前，必须逐条检查：

1. **初始化完整性** — 扫描所有 import，确认每个库的 initDict 已调用且在计算操作之前。
2. **API 存在性** — 每个 API 调用必须在对应子 skill INDEX.md 中存在。警惕命名误用：
   - `hp.multiply` → 不存在，应为 `hp.mul`
   - `hp.subtract` → 不存在，应为 `hp.sub`
   - `hp.divide` → 不存在，应为 `hp.div`
   - `hl.XGBClassifier` → 拼写错误，应为 `hl.XGBClassfier`
3. **加解密方法匹配** — 数据类型与加解密函数必须对应：
   - DataFrame → `ct.encrypt_df()` / `ct.decrypt_df()`
   - ndarray → `ct.encrypt()` / `ct.decrypt()` 或 `ct.encrypt_ndarray()` / `ct.decrypt_ndarray()`
   - Tensor → `ct.encrypt_tensor()` / `ct.decrypt_tensor()`
   - 文件级 → `ct.encrypt_csv()` / `ct.encrypt_excel()` / `ct.encrypt_json()`
4. **数据格式兼容性** — 确认数据类型满足目标 API 的要求：
   - helearn `fit(X, y)` 需要 CipherArray，不接受 CipherDataFrame
   - GBDT/XGBoost 要求列加密（`encrypt_by_column=True`）
   - hetorch2 Layer 要求 CipherTensor
   - pandaseal `fillna` 参数必须是密文标量（如 `ct.encrypt(0)`）
   - pandaseal `groupby` 基于索引（`level=0`），不支持按列名
5. **形状一致性** — 矩阵乘法维度兼容、训练数据行数匹配、模型输入形状匹配。
6. **不可用操作降级** — INDEX.md 中不存在的操作：先尝试组合实现；无法组合则明确告知用户，禁止编造。

### B. 生成代码中的防御性编程

1. **文件 I/O 防御** — 读取加密文件前检查文件存在性和扩展名匹配。
2. **加密数据校验** — 加密后可选地打印密文形状和类型以确认。
3. **解密结果验证** — 解密后打印结果，并提醒 FHE 固有精度误差。
4. **helearn 训练防御** — 加载数据集后验证非空；预测结果注明返回格式（分类返回 `(pred, label)`）。
5. **hetorch2 推理防御** — 确保 dtype 为 `torch.float64`；加载权重前确认文件存在。
6. **跨 skill 转换防御** — 格式转换后注释说明不可再用原 skill 的方法。
7. **精度提示** — 脚本末尾包含精度误差提醒注释。

### C. 路由阶段兜底

1. **意图模糊** — 无法明确分类时：
   - 提及表格/文件 → 默认 pandaseal EDA
   - 提及训练/预测 → 默认 helearn，询问分类还是回归
   - 提及推理 → 默认 hetorch2 MLP 模板，询问模型结构
   - 仍不明确 → **必须向用户提问澄清**，不可猜测生成
2. **跨 skill 冲突** — 检测互斥操作（如"用 hetorch2 训练 sklearn 模型" → 引导到 helearn）。

## 参考文件

- 路由逻辑：`{baseDir}/docs/routing.md`
- 初始化模式：`{baseDir}/docs/initialization.md`
- 数据格式转换：`{baseDir}/docs/data-flow.md`
- 错误处理详解：`{baseDir}/docs/error-handling.md`
- 完整示例：`{baseDir}/examples/`
- 子 skill 入口：
  - `henumpy-skill/SKILL.md` + `henumpy-skill/INDEX.md`
  - `pandaseal-skill/SKILL.md` + `pandaseal-skill/INDEX.md`
  - `helearn-skill/SKILL.md` + `helearn-skill/INDEX.md`
  - `hetorch-skill/SKILL.md` + `hetorch-skill/INDEX.md`

