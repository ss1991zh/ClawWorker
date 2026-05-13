# Linear

密文全连接层，对应 PyTorch `nn.Linear`。

## 签名

```python
hetorch2.nn.Linear(in_features, out_features, bias=True, device='cpu')
```

## 参数

- `in_features`: 每个输入样本的特征维度。
- `out_features`: 每个输出样本的特征维度。
- `bias`: 是否使用可学习的偏置，默认 `True`。
- `device`: 权重与偏置所在设备，默认 `'cpu'`。

## 示例

```python
import hetorch2
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

linear = nn.Linear(784, 128)
x = torch.randn(4, 784, dtype=torch.float64)
cx = ct.encrypt_tensor(x)
out = linear(cx)
y = ct.decrypt_tensor(out)
print(y.shape)  # torch.Size([4, 128])
```
