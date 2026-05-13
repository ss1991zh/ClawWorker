# scatter

散布元素，对应 `torch.scatter`。

## 签名

`hetorch2.scatter(input, dim, index, src)`

## 参数

- `input`: CipherTensor — 被写入的目标
- `dim`: 散布维度
- `index`: 明文 long
- `src`: CipherTensor 或明文 — 源值

## 返回值

CipherTensor — 与 `torch.scatter` 一致。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

base = torch.zeros(2, 4, dtype=torch.float64)
idx = torch.tensor([[0, 1], [2, 3]], dtype=torch.long)
src = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(base)
sc = ct.encrypt_tensor(src)
out = hetorch2.scatter(xc, 1, idx, sc)
print(ct.decrypt_tensor(out))
```
