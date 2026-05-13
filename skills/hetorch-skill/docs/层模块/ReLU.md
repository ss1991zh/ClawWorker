# ReLU

密文 ReLU 激活层，对应 PyTorch `nn.ReLU`。

## 签名

```python
hetorch2.nn.ReLU(inplace=False)
```

## 参数

- `inplace`: 是否与 PyTorch 接口对齐；密文实现中通常仍返回新密文张量，不建议依赖原地语义。

## 示例

```python
import hetorch2
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

relu = nn.ReLU()
x = torch.randn(2, 64, dtype=torch.float64)
cx = ct.encrypt_tensor(x)
out = relu(cx)
y = ct.decrypt_tensor(out)
print(y.shape)  # torch.Size([2, 64])
```
