# PReLU

密文参数化 ReLU 层，对应 PyTorch `nn.PReLU`。

## 签名

```python
hetorch2.nn.PReLU(num_parameters=1, init=0.25)
```

## 参数

- `num_parameters`: 可学习的 `weight` 元素个数；`1` 表示所有通道共享一个负斜率，更大时表示按通道等维度区分（与输入广播方式同 PyTorch）。
- `init`: 负斜率参数的初始值，默认 `0.25`。

## 示例

```python
import hetorch2
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

prelu = nn.PReLU(num_parameters=1, init=0.25)
x = torch.randn(2, 64, dtype=torch.float64)
cx = ct.encrypt_tensor(x)
out = prelu(cx)
y = ct.decrypt_tensor(out)
print(y.shape)  # torch.Size([2, 64])
```
