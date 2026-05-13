# flatten

展平，对应 `torch.flatten`。

## 签名

`hetorch2.flatten(input, start_dim=0, end_dim=-1)`

## 参数

- `input`: CipherTensor
- `start_dim` / `end_dim` (可选): 展平区间

## 返回值

CipherTensor — 形状与 `torch.flatten` 一致。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.arange(12, dtype=torch.float64).reshape(2, 2, 3)
xc = ct.encrypt_tensor(x)
out = hetorch2.flatten(xc, start_dim=1)
print(ct.decrypt_tensor(out).shape)
```
