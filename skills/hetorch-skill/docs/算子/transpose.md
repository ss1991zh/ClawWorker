# transpose

转置，对应 `torch.transpose`。

## 签名

`hetorch2.transpose(input, dim0, dim1)`

## 参数

- `input`: CipherTensor
- `dim0`, `dim1`: 要交换的两维

## 返回值

CipherTensor — 交换两维。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.arange(6, dtype=torch.float64).reshape(2, 3)
xc = ct.encrypt_tensor(x)
out = hetorch2.transpose(xc, 0, 1)
print(ct.decrypt_tensor(out).shape)
```
