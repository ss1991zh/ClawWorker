# batch_norm

密文批归一化（推理态统计量），对应 PyTorch `F.batch_norm`。

## 签名

`hetorch2.nn.functional.batch_norm(input, running_mean, running_var, weight=None, bias=None, eps=1e-5)`

## 参数

- `input`: 密文 Tensor，通常为 `(N, C, ...)`。
- `running_mean`: 运行时均值，形状 `(C,)`，`dtype=torch.float64`。
- `running_var`: 运行时方差，形状 `(C,)`，`dtype=torch.float64`。
- `weight`: 可选缩放参数 \(\gamma\)，形状 `(C,)`。
- `bias`: 可选平移参数 \(\beta\)，形状 `(C,)`。
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

x = torch.randn(2, 8, 4, 4, dtype=torch.float64)
running_mean = torch.zeros(8, dtype=torch.float64)
running_var = torch.ones(8, dtype=torch.float64)
weight = torch.ones(8, dtype=torch.float64)
bias = torch.zeros(8, dtype=torch.float64)
x_enc = ct.encrypt_tensor(x)
rm_enc = ct.encrypt_tensor(running_mean)
rv_enc = ct.encrypt_tensor(running_var)
w_enc = ct.encrypt_tensor(weight)
b_enc = ct.encrypt_tensor(bias)
out_enc = F.batch_norm(x_enc, rm_enc, rv_enc, w_enc, b_enc, eps=1e-5)
out = ct.decrypt_tensor(out_enc)
```
