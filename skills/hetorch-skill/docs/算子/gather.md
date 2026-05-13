# gather

收集元素，对应 `torch.gather`。

## 签名

`hetorch2.gather(input, dim, index)`

## 参数

- `input`: CipherTensor
- `dim`: 聚集维度
- `index`: 明文 long 张量 — 与 `torch.gather` 一致

## 返回值

CipherTensor — 按 `index` 从 `input` 取值。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[10.0, 20.0], [30.0, 40.0]], dtype=torch.float64)
idx = torch.tensor([[0, 0], [1, 0]], dtype=torch.long)
xc = ct.encrypt_tensor(x)
out = hetorch2.gather(xc, 1, idx)
print(ct.decrypt_tensor(out))
```
