# rsqrt

平方根倒数，对应 `torch.rsqrt`。

## 签名

`hetorch2.rsqrt(input)`

## 参数

- `input`: CipherTensor — 正数输入

## 返回值

CipherTensor — 逐元素 `1/sqrt(input)`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 4.0], [16.0, 25.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.rsqrt(xc)
print(ct.decrypt_tensor(out))
```
