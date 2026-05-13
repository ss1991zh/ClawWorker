# Tanh

密文 Tanh 激活层，对应 PyTorch `nn.Tanh`。

## 签名

```python
hetorch2.nn.Tanh()
```

## 参数

无构造函数参数。

## 示例

```python
import hetorch2
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

tanh = nn.Tanh()
x = torch.randn(2, 64, dtype=torch.float64)
cx = ct.encrypt_tensor(x)
out = tanh(cx)
y = ct.decrypt_tensor(out)
print(y.shape)  # torch.Size([2, 64])
```
