---
name: henumpy-skill
description: >
  同态加密数值计算代码生成。使用 henumpy (hp) 和 crypto_toolkit (ct) 在密文上
  执行 NumPy 风格的数值运算。
  触发条件：用户提及加密计算、密文运算、henumpy、HE-Numpy、同态加密、
  homomorphic encryption、ciphertext computation、crypto_toolkit，
  或需要在加密数据上做数值计算（hp.add、hp.mul、ct.encrypt 等）。
  不适用于：普通 numpy 明文运算。
user-invocable: true
metadata: {"openclaw":{"emoji":"🔐"}}
---

# henumpy — 同态加密数值计算

基于 `henumpy` 的同态加密数值计算代码生成 Skill。

两个核心库协同工作：
- **`henumpy`**（别名 `hp`）— 密文上的计算算子，API 对齐 NumPy
- **`crypto_toolkit`**（别名 `ct`）— 加解密操作

## 何时使用

当用户请求满足以下任一条件时激活此 skill：
- 提及 henumpy、HE-Numpy、crypto_toolkit
- 提及加密计算、密文运算、同态加密、homomorphic encryption
- 需要在加密数据上做数值计算
- 使用 `hp.*` 或 `ct.*` API

**不适用于**：普通 numpy 明文运算、非加密场景。

## 快速参考

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

x = ct.encrypt(np.array([1.0, 2.0, 3.0]))
y = ct.encrypt(np.array([4.0, 5.0, 6.0]))

z = hp.add(x, y)       # 或 x + y
w = hp.sub(x, y)       # 或 x - y
v = hp.mul(x, y)       # 或 x * y
u = hp.div(x, y)       # 或 x / y
s = hp.sum(x)
m = hp.mean(x)
p = hp.matmul(A, B)    # 或 A @ B
t = hp.transpose(A)    # 或 A.T

print(ct.decrypt(z))   # [5.0, 7.0, 9.0]
```

## 常见计算模式

| 目标 | 实现方式 |
|------|---------|
| Z-score 归一化 | `hp.div(hp.sub(x, hp.mean(x)), hp.std(x))` |
| 欧几里得距离 | `hp.sqrt(hp.sum(hp.square(hp.sub(a, b))))` |
| 线性层 y=Xw+b | `hp.add(hp.matmul(X, w), b)` 或 `X @ w + b` |
| ReLU 近似 | `hp.where(x > 0, x, 0)` |
| Min-Max 归一化 | `hp.div(hp.sub(x, hp.min(x)), hp.sub(hp.max(x), hp.min(x)))` |
| 加权求和 | `hp.sum(hp.mul(x, weights))` |
| 协方差矩阵 | `hp.cov(X)` |
| 多项式求值 | 嵌套 `hp.add(hp.mul(...), ...)` 或 `hp.polyfit` |

## 代码生成工作流

处理用户请求时按以下步骤执行：

1. **分解需求** — 将用户需求拆解为数学运算序列。
2. **映射算子** — 将每个运算映射到 `hp.*` 算子。
   - 在上方快速参考中？直接使用
   - 不在？查阅 `{baseDir}/INDEX.md` 获取函数签名和文档路径
   - INDEX.md 中无直接对应？查看常见计算模式，或用已有算子组合
3. **查阅文档** — 对非基础算子，读取 `{baseDir}/docs/` 下的具体文档确认参数和行为。仅读取所需文档（2-5 个），不要批量加载。涉及加密类型、离散数组、并行化时，额外读取 `{baseDir}/constraints.md`。
4. **生成代码** — 组合算子生成完整代码。必须包含初始化（`hp.initDict()` + `ct.initSK()`）。
5. **自检** — 对照下方硬性规则检查。

## 硬性规则

1. **禁止凭 numpy 记忆猜测** — 函数名和参数可能与 numpy 不同。不确定时必须查文档。关键差异：`hp.mul`（非 multiply）、`hp.sub`（非 subtract）、`hp.div`（非 divide）、`hp.invers`（非 inverse）。
2. **禁止编造算子** — `{baseDir}/INDEX.md` 中找不到的算子不存在。
3. **必须初始化** — 每个脚本以 `hp.initDict()` + `ct.initSK()` 开头。
4. **运算符已重载** — `+` `-` `*` `/` `@` `.T` `>` `<` `==` 等可直接使用。
5. **比较返回布尔值** — `hp.greater()` 等返回 Python `True`/`False`，不是密文。

## 错误处理

- 如果用户请求的运算在 INDEX.md 中不存在，明确告知并建议可用的替代组合。
- 如果参数类型不确定（标量/数组/密文/明文），查阅对应文档的参数说明。
- 如果涉及精度问题，提醒用户同态加密存在固有浮点误差。

## 参考文件

- 算子索引：`{baseDir}/INDEX.md`
- 约束与注意事项：`{baseDir}/constraints.md`
- API 文档目录：`{baseDir}/docs/`
- 完整示例：`{baseDir}/examples/`
