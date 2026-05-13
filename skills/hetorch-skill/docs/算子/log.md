# log

自然对数，对应 `torch.log`。

## 签名

`hetorch2.log(input)`

## 参数

- `input`: CipherTensor — 输入张量（取值应在合法正数域内）

## 返回值

CipherTensor — 逐元素自然对数。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0], [2.718281828, 10.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.log(xc)
print(ct.decrypt_tensor(out))
```
