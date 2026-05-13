# scatter_add

散布加法，对应 `torch.scatter_add`。

## 签名

`hetorch2.scatter_add(input, dim, index, src)`

## 参数

- `input`: CipherTensor
- `dim`: 维度
- `index`: 明文 long，与 `torch.scatter_add` 一致
- `src`: CipherTensor

## 返回值

CipherTensor — 将 `src` 按 `index` 累加到 `input`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

base = torch.zeros(2, 4, dtype=torch.float64)
idx = torch.tensor([[0, 1, 2, 3], [3, 2, 1, 0]], dtype=torch.long)
src = torch.ones(2, 4, dtype=torch.float64)
xc = ct.encrypt_tensor(base)
sc = ct.encrypt_tensor(src)
out = hetorch2.scatter_add(xc, 1, idx, sc)
print(ct.decrypt_tensor(out))
```
