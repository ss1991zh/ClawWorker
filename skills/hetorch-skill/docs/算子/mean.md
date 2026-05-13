# mean

均值，对应 `torch.mean`。

## 签名

`hetorch2.mean(input, dim=None, keepdim=False)`

## 参数

- `input`: CipherTensor
- `dim` (可选): 归约维度
- `keepdim` (可选): 是否保留维度

## 返回值

CipherTensor — 均值。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.mean(xc, dim=0)
print(ct.decrypt_tensor(out))
```
