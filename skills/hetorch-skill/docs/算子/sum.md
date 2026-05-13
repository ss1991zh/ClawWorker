# sum

求和，对应 `torch.sum`。

## 签名

`hetorch2.sum(input, dim=None, keepdim=False)`

## 参数

- `input`: CipherTensor
- `dim` (可选): 归约维度；`None` 表示全局求和
- `keepdim` (可选): 是否保留被归约的维度

## 返回值

CipherTensor 或标量密文 — 与 `torch.sum` 语义一致。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.sum(xc, dim=1, keepdim=True)
print(ct.decrypt_tensor(out))
```
