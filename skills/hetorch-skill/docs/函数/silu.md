# silu

密文 SiLU（Swish）激活，对应 PyTorch `F.silu`。同目录下还提供优化实现 `F.silu_opt(input)`，在支持的形状与精度下可减少开销，语义与 `silu` 一致。

## 签名

`hetorch2.nn.functional.silu(input)`

`hetorch2.nn.functional.silu_opt(input)`（优化变体）

## 参数

- `input`: 密文 Tensor，输入特征。

## 返回值

密文 Tensor（CipherTensor）。

## 示例

```python
import hetorch2
import hetorch2.nn.functional as F
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.randn(2, 4, dtype=torch.float64)
x_enc = ct.encrypt_tensor(x)
out_enc = F.silu(x_enc)
out = ct.decrypt_tensor(out_enc)

# 可选：使用优化路径
# out_enc = F.silu_opt(x_enc)
# out = ct.decrypt_tensor(out_enc)
```
