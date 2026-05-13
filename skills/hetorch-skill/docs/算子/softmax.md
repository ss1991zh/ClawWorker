# softmax

Softmax，对应 `torch.softmax`。

## 签名

`hetorch2.softmax(input, dim)`

## 参数

- `input`: CipherTensor
- `dim`: int — 在指定维上做 softmax

## 返回值

CipherTensor — 概率分布。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0, 3.0], [1.0, 1.0, 1.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.softmax(xc, dim=-1)
print(ct.decrypt_tensor(out))
```
