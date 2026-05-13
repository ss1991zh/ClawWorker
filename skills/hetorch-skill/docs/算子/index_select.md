# index_select

索引选择，对应 `torch.index_select`。

## 签名

`hetorch2.index_select(input, dim, index)`

## 参数

- `input`: CipherTensor
- `dim`: 选择维度
- `index`: 明文 long 张量 — 下标

## 返回值

CipherTensor — `input.index_select(dim, index)`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.arange(12, dtype=torch.float64).reshape(4, 3)
idx = torch.tensor([0, 2], dtype=torch.long)
xc = ct.encrypt_tensor(x)
out = hetorch2.index_select(xc, 0, idx)
print(ct.decrypt_tensor(out).shape)
```
