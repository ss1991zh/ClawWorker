# topk

Top-K，返回 `(values: CipherTensor, indices: torch.Tensor)`，对应 `torch.topk`。

## 签名

`hetorch2.topk(input, k, dim=None, largest=True, sorted=True)`

## 参数

- `input`: CipherTensor
- `k`: 取前 k 个
- `dim` (可选): 维度；`None` 表示展平
- `largest` / `sorted` (可选): 与 `torch.topk` 一致

## 返回值

tuple — `(values: CipherTensor, indices: torch.Tensor)`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 5.0, 3.0, 2.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
vals, idx = hetorch2.topk(xc, 2, dim=-1)
print(ct.decrypt_tensor(vals), idx)
```
