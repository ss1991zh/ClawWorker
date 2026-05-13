# layer_norm

密文层归一化，对应 PyTorch `F.layer_norm`。

## 签名

`hetorch2.nn.functional.layer_norm(input, normalized_shape, weight=None, bias=None, eps=1e-5)`

## 参数

- `input`: 密文 Tensor。
- `normalized_shape`: 与 PyTorch 相同，为待归一化的尾部维度形状（如 `(C,)` 或 `(H, W)` 等）。
- `weight`: 可选缩放参数 \(\gamma\)，形状与 `normalized_shape` 一致。
- `bias`: 可选平移参数 \(\beta\)，形状与 `normalized_shape` 一致。
- `eps`: 数值稳定项，默认 `1e-5`。

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

x = torch.randn(2, 8, 16, dtype=torch.float64)
normalized_shape = (16,)
weight = torch.ones(16, dtype=torch.float64)
bias = torch.zeros(16, dtype=torch.float64)
x_enc = ct.encrypt_tensor(x)
w_enc = ct.encrypt_tensor(weight)
b_enc = ct.encrypt_tensor(bias)
out_enc = F.layer_norm(x_enc, normalized_shape, w_enc, b_enc, eps=1e-5)
out = ct.decrypt_tensor(out_enc)
```
