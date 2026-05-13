# sigmoid

密文 Sigmoid 激活，对应 PyTorch `F.sigmoid`。

## 签名

`hetorch2.nn.functional.sigmoid(input)`

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
out_enc = F.sigmoid(x_enc)
out = ct.decrypt_tensor(out_enc)
```
