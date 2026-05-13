# linear

密文线性变换 \(y = x W^T + b\)，对应 PyTorch `F.linear`。

## 签名

`hetorch2.nn.functional.linear(input, weight, bias=None)`

## 参数

- `input`: 密文 Tensor，形状 `(*, in_features)`。
- `weight`: 权重矩阵，形状 `(out_features, in_features)`。
- `bias`: 可选偏置，形状 `(out_features,)`；为 `None` 时不加偏置。

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

x = torch.randn(3, 8, dtype=torch.float64)
weight = torch.randn(16, 8, dtype=torch.float64)
bias = torch.randn(16, dtype=torch.float64)
x_enc = ct.encrypt_tensor(x)
w_enc = ct.encrypt_tensor(weight)
b_enc = ct.encrypt_tensor(bias)
out_enc = F.linear(x_enc, w_enc, b_enc)
out = ct.decrypt_tensor(out_enc)
```
