# sort

排序，返回 `(values: CipherTensor, indices: torch.Tensor)`，对应 `torch.sort`。

## 签名

`hetorch2.sort(input, dim=-1, descending=False)`

## 参数

- `input`: CipherTensor
- `dim` (可选): 排序维度
- `descending` (可选): 是否降序

## 返回值

tuple — `(values: CipherTensor, indices: torch.Tensor)`，`indices` 为明文 long。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[3.0, 1.0, 2.0], [9.0, 5.0, 7.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
vals, idx = hetorch2.sort(xc, dim=-1)
print(ct.decrypt_tensor(vals), idx)
```
