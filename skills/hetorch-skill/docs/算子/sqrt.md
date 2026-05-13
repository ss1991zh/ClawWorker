# sqrt

平方根，对应 `torch.sqrt`。

## 签名

`hetorch2.sqrt(input)`

## 参数

- `input`: CipherTensor — 非负输入

## 返回值

CipherTensor — 逐元素平方根。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[0.0, 4.0], [9.0, 16.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.sqrt(xc)
print(ct.decrypt_tensor(out))
```
