---
name: helearn-skill
description: >
  同态加密机器学习代码生成。使用 helearn、henumpy (hp) 和 crypto_toolkit (ct)
  在密文上执行 sklearn 风格的机器学习训练与推理。
  触发条件：用户提及 helearn、HE-Learn、密文机器学习、密文训练、密文推理、
  encrypted ML、homomorphic machine learning，
  或需要在加密数据上做逻辑回归、线性回归、GBDT、XGBoost 等模型。
  不适用于：普通 sklearn/明文机器学习。
user-invocable: true
---

# helearn — 同态加密机器学习

基于 `helearn` 的同态加密机器学习代码生成 Skill。

三个核心库协同工作：
- **`helearn`**（别名 `hl`）— 密文上的 sklearn 风格机器学习模型
- **`henumpy`**（别名 `hp`）— 同态加密数值计算、字典初始化
- **`crypto_toolkit`**（别名 `ct`）— 加解密操作

## 何时使用

当用户请求满足以下任一条件时激活此 skill：
- 提及 helearn、HE-Learn
- 提及密文机器学习、密文训练、密文预测
- 需要在加密数据上做分类（逻辑回归、GBDT、XGBoost）
- 需要在加密数据上做回归（线性回归、GBRT、XGBoost）
- 使用 `hl.*`、`ct.encrypt_ndarray`、`ct.encrypt_csv` API

**不适用于**：普通 sklearn 明文训练/推理、深度学习（使用 hetorch-skill）。

## 快速参考

```python
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 加载密文数据集
data = hl.datasets.load_breast_cancer(data_type="cipher")
X_train = data.train_data
y_train = data.train_target
X_test = data.test_data

# 初始化模型
model = hl.XGBClassfier(learning_rate=0.3, n_estimators=10, max_depth=6)

# 密文训练
model.fit(X=X_train, y=y_train)

# 密文预测
pred, label = model.predict(X=X_test)
```

## 可用模型

| 任务 | 模型 | 类名 |
|------|------|------|
| 分类 | 逻辑回归 | `hl.LogisticRegression()` |
| 分类 | GBDT 梯度提升树 | `hl.GradientBoostingClassifier(...)` |
| 分类 | XGBoost 极限梯度提升树 | `hl.XGBClassfier(...)` |
| 回归 | 线性回归 | `hl.LinearRegression()` |
| 回归 | GBRT 梯度提升树 | `hl.GradientBoostingRegressor(...)` |
| 回归 | XGBoost 极限梯度提升树 | `hl.XGBRegressor(...)` |

## 加解密方式

| 操作 | API | 说明 |
|------|-----|------|
| 数组加密 | `ct.encrypt_ndarray(arr)` | 支持单值/一维/二维数组 |
| 数组解密 | `ct.decrypt_ndarray(arr)` | 自动判断行/列加密 |
| CSV 加密 | `ct.encrypt_csv(in, out)` | 按列加密，忽略表头 |
| CSV 解密 | `ct.decrypt_csv(in, out)` | 按列解密，忽略表头 |

## 常见工作模式

| 模式 | 关键步骤 |
|------|---------|
| 密文分类 | 加载数据 → 初始化模型 → `fit(X, y)` → `predict(X)` → 获取 `(pred, label)` |
| 密文回归 | 加载数据 → 初始化模型 → `set_params(...)` 或构造器参数 → `fit(X, y)` → `predict(X)` |
| 数据加密 | `ct.encrypt_ndarray(numpy_array)` 或 `ct.encrypt_csv(input, output)` |
| 数据集加载 | `hl.datasets.load_breast_cancer(data_type="cipher")` 或 `hl.datasets.load_boston()` |

## 代码生成工作流

1. **分解需求** — 确定任务类型（分类/回归）和模型选择。
2. **映射 API** — 在上方快速参考中查找对应模型。
   - 不在？查阅 `{baseDir}/INDEX.md` 获取完整签名和文档路径
   - INDEX.md 中无对应？用已有模型组合
3. **查阅文档** — 对非基础用法，读取 `{baseDir}/docs/` 下的具体文档确认参数。
4. **生成代码** — 组合生成完整代码。必须包含初始化。
5. **自检** — 对照下方硬性规则检查。

## 硬性规则

1. **必须初始化** — 每个脚本以 `hp.initDict()` + `ct.initSK()` 开头（如使用加解密功能）。仅使用 helearn 模型时至少需要 `hp.initDict()`。
2. **三个 import** — `import helearn as hl`、`import henumpy as hp`、`import crypto_toolkit as ct`。
3. **禁止编造 API** — `{baseDir}/INDEX.md` 中找不到的 API 不存在。
4. **XGBClassfier 拼写** — 注意类名为 `XGBClassfier`（不是 Classifier），这是 helearn 的命名。
5. **数据格式** — 训练数据为密文数组类型；GBDT/XGBoost 使用列加密数据。
6. **LR 模型初始化** — `LogisticRegression` 和 `LinearRegression` 通过 `set_params()` 设置参数后再调用 `fit()`。

## 参考文件

- API 索引：`{baseDir}/INDEX.md`
- API 文档目录：`{baseDir}/docs/`
- 完整示例：`{baseDir}/examples/`
