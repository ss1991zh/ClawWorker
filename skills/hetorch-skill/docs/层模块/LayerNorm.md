# LayerNorm

密文层归一化，对应 PyTorch `nn.LayerNorm`。

## 签名

```python
hetorch2.nn.LayerNorm(normalized_shape, eps=1e-5, elementwise_affine=True, device='cpu')
```

## 参数

- `normalized_shape`: 在最后若干维上做归一化的形状，可为 `int` 或 `tuple`（与 PyTorch 一致）。
- `eps`: 数值稳定项，加在方差上。
- `elementwise_affine`: 是否使用可学习的 `weight` 与 `bias`。
- `device`: 参数所在设备，默认 `'cpu'`。

## 示例

```python
import hetorch2
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

ln = nn.LayerNorm(128)
x = torch.randn(2, 10, 128, dtype=torch.float64)
cx = ct.encrypt_tensor(x)
out = ln(cx)
y = ct.decrypt_tensor(out)
print(y.shape)  # torch.Size([2, 10, 128])
```
