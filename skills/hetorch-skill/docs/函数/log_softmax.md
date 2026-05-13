# log_softmax

密文 Log-Softmax，对应 PyTorch `F.log_softmax`。

## 签名

`hetorch2.nn.functional.log_softmax(input, dim)`

## 参数

- `input`: 密文 Tensor。
- `dim`: 在指定维度上计算 \(\log \mathrm{softmax}\)。

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

x = torch.randn(2, 5, dtype=torch.float64)
x_enc = ct.encrypt_tensor(x)
out_enc = F.log_softmax(x_enc, dim=-1)
out = ct.decrypt_tensor(out_enc)
```
