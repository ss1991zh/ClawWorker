---
name: hetorch-skill
description: >
  同态加密深度学习推理代码生成。使用 hetorch2 和 crypto_toolkit (ct) 在密文上
  执行 PyTorch 风格的神经网络推理。
  触发条件：用户提及 hetorch2、HeTorch2、CipherTensor、密文深度学习、
  密文推理、encrypted inference、homomorphic deep learning，
  或需要在加密数据上做 PyTorch 风格的模型推理（nn.Linear、nn.ReLU、F.relu 等）。
  不适用于：普通 PyTorch 明文训练/推理。
user-invocable: true
metadata:
  openclaw:
    emoji: "🔥"
    requires:
      bins: ["python3.11"]
    install:
      - id: "fhe-runtime"
        kind: "reply"
        label: "Install FHE runtime: bash vendor/fhe-runtime/install.sh (requires Python 3.11 + skf/dictf/user_authorization in ~/.openclaw/fhe-keys/)"
---

# hetorch2 — 同态加密深度学习推理

基于 `hetorch2` 的同态加密深度学习推理代码生成 Skill。

两个核心库协同工作：
- **`hetorch2`** — 密文上的 PyTorch 风格深度学习算子（v2.0，API 与 PyTorch 对齐）
- **`crypto_toolkit`**（别名 `ct`）— 加解密操作

## 何时使用

当用户请求满足以下任一条件时激活此 skill：
- 提及 hetorch2、HeTorch2、CipherTensor
- 提及密文深度学习、密文推理、encrypted inference
- 需要在加密数据上做 PyTorch 风格的模型推理
- 使用 `hetorch2.*` 或 `ct.encrypt_tensor` / `ct.decrypt_tensor` API

**不适用于**：普通 PyTorch 明文训练/推理、非加密场景。

## 快速参考

```python
import hetorch2
import hetorch2.nn as nn
import hetorch2.nn.functional as F
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

# 加密 Tensor
x = torch.randn(1, 784, dtype=torch.float64)
cx = ct.encrypt_tensor(x)

# 密文推理
linear = nn.Linear(784, 10)
out = linear(cx)
out = F.relu(out)

# 解密结果
result = ct.decrypt_tensor(out)
print(result)
```

## 命名规则（与 PyTorch 对齐）

hetorch2 的命名 **直接对齐 PyTorch**，不再使用 `He` / `h` 前缀。

| PyTorch | hetorch2 | 说明 |
|---------|----------|------|
| `torch.nn.Linear` | `hetorch2.nn.Linear` | Layer 层直接用 PyTorch 原名 |
| `torch.nn.ReLU` | `hetorch2.nn.ReLU` | 同上 |
| `torch.nn.functional.relu` | `hetorch2.nn.functional.relu` | 函数式接口直接用原名 |
| `torch.add` | `hetorch2.add` | 顶层算子直接用原名 |
| `torch.matmul` | `hetorch2.matmul` | 同上 |
| `torch.Tensor` | `hetorch2.CipherTensor` | 密文张量 |

## 常见计算模式

| 目标 | 实现方式 |
|------|---------|
| 密文线性层 | `nn.Linear(in_features, out_features)` |
| 密文 ReLU | `nn.ReLU()` 或 `F.relu(x)` |
| 密文 Sigmoid | `nn.Sigmoid()` 或 `F.sigmoid(x)` |
| 密文 SiLU(Swish) | `nn.SiLU()` 或 `F.silu(x)` |
| 密文嵌入 | `nn.Embedding(num_embeddings, embedding_dim)` |
| 密文批归一化 | `nn.BatchNorm1d(n)` / `nn.BatchNorm2d(n)` |
| 密文层归一化 | `nn.LayerNorm(normalized_shape)` |
| 密文展平 | `hetorch2.flatten(x, start_dim)` |
| 密文矩阵乘 | `hetorch2.matmul(x, y)` |
| 密文逐元素乘 | `hetorch2.mul(x, y)` |
| 密文加法 | `hetorch2.add(x, y)` 或 `x + y` |
| 密文 Softmax | `hetorch2.softmax(x, dim)` 或 `F.softmax(x, dim)` |
| 条件选择 | `hetorch2.where(cond, x, y)` |
| 张量拼接 | `hetorch2.cat([a, b], dim)` |
| 形状变换 | `hetorch2.reshape(x, shape)` / `hetorch2.view(x, shape)` |
| 排序 | `hetorch2.sort(x, dim)` |
| Top-K | `hetorch2.topk(x, k)` |
| 裁剪 | `hetorch2.clamp(x, min, max)` |
| 残差连接 | `hetorch2.add(out, identity)` 或 `out + identity` |

## 代码生成工作流

处理用户请求时按以下步骤执行：

1. **分解需求** — 将用户需求拆解为神经网络层和操作序列。
2. **映射算子** — 将每个 PyTorch 操作映射到 `hetorch2.*` 算子。
   - 在上方快速参考中？直接使用
   - 不在？查阅 `{baseDir}/INDEX.md` 获取函数签名和文档路径
   - INDEX.md 中无直接对应？用已有算子组合
3. **查阅文档** — 对非基础算子，读取 `{baseDir}/docs/` 下的具体文档确认参数和行为。仅读取所需文档（2-5 个），不要批量加载。
4. **生成代码** — 组合算子生成完整代码。必须包含初始化（`hetorch2.initDict()` + `ct.initSK()`）。
5. **自检** — 对照下方硬性规则检查。

## 硬性规则

1. **必须初始化** — 每个脚本以 `hetorch2.initDict()` + `ct.initSK()` 开头。
2. **不需要 henumpy** — hetorch2 有独立的 `initDict()`，不需要 `import henumpy`。
3. **禁止编造算子** — `{baseDir}/INDEX.md` 中找不到的算子不存在。
4. **加解密方法** — Tensor 加密 `ct.encrypt_tensor(tensor)`，解密 `ct.decrypt_tensor(tensor)`。
5. **CipherTensor 包装** — 从普通 Tensor 转为密文张量：`hetorch2.CipherTensor(tensor)`。
6. **mul 是逐元素乘，matmul 是矩阵乘** — `hetorch2.mul(a, b)` 是逐元素乘法，`hetorch2.matmul(a, b)` 是矩阵乘法。与 PyTorch 语义一致。
7. **不再使用 He/h 前缀** — 旧版 hetorch 的 `HeLinear`、`hrelu` 等命名已废弃，直接使用 PyTorch 风格名称。
8. **import 路径** — Layer 层通过 `hetorch2.nn` 访问，函数式接口通过 `hetorch2.nn.functional` 访问，顶层算子通过 `hetorch2` 直接访问。

## 错误处理

- 如果用户请求的操作在 INDEX.md 中不存在，明确告知并建议可用的替代组合。
- 如果参数类型不确定，查阅对应文档的参数说明。
- 如果涉及精度问题，提醒用户同态加密存在固有浮点误差。
- hetorch2 目前不支持 Conv2d、MaxPool、LSTM、MultiheadAttention、Transformer、Dropout、GraphConv — 如用户需要这些，说明当前版本未提供，建议用已有算子手动组合替代。

## 参考文件

- API 索引：`{baseDir}/INDEX.md`
- API 文档目录：`{baseDir}/docs/`
- 完整示例：`{baseDir}/examples/`
