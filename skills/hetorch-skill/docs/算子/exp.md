# exp

指数函数，对应 `torch.exp`。

## 签名

`hetorch2.exp(input)`

## 参数

- `input`: CipherTensor — 输入张量

## 返回值

CipherTensor — 逐元素 `exp(input)`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[0.0, 1.0], [2.0, -0.5]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.exp(xc)
print(ct.decrypt_tensor(out))
```
