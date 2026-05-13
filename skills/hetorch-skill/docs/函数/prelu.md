# prelu

密文参数化 ReLU（PReLU），对应 PyTorch `F.prelu`。

## 签名

`hetorch2.nn.functional.prelu(input, weight)`

## 参数

- `input`: 密文 Tensor，输入特征。
- `weight`: 可学习斜率参数（与 PyTorch 中 `PReLU` 的 `weight` 一致），形状需与广播规则兼容。

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
weight = torch.randn(4, dtype=torch.float64)
x_enc = ct.encrypt_tensor(x)
w_enc = ct.encrypt_tensor(weight)
out_enc = F.prelu(x_enc, w_enc)
out = ct.decrypt_tensor(out_enc)
```
