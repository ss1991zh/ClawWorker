# index_add

索引加法，对应 `torch.index_add`。

## 签名

`hetorch2.index_add(input, dim, index, source)`

## 参数

- `input`: CipherTensor — 累加目标（原地或新张量依实现）
- `dim`: 维度
- `index`: 明文 long 一维张量
- `source`: CipherTensor — 待加片段

## 返回值

CipherTensor — `input[index] += source` 语义。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

base = torch.zeros(4, 3, dtype=torch.float64)
src = torch.ones(2, 3, dtype=torch.float64)
index = torch.tensor([0, 2], dtype=torch.long)
xc = ct.encrypt_tensor(base)
sc = ct.encrypt_tensor(src)
out = hetorch2.index_add(xc, 0, index, sc)
print(ct.decrypt_tensor(out))
```
