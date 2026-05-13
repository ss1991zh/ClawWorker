# pow

幂运算，对应 `torch.pow`。

## 签名

`hetorch2.pow(input, exponent)`

## 参数

- `input`: CipherTensor — 底数
- `exponent`: 标量或与 `input` 可广播的张量 — 指数

## 返回值

CipherTensor — 逐元素幂。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[2.0, 3.0], [4.0, 5.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.pow(xc, 2.0)
print(ct.decrypt_tensor(out))
```
