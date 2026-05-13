# where

条件选择（`condition` 为明文 bool 张量；`x` 与 `y` 可为 CipherTensor 或标量，不能同时为标量），对应 `torch.where`。

## 签名

`hetorch2.where(condition, x, y)`

## 参数

- `condition`: torch.BoolTensor（明文）
- `x`, `y`: CipherTensor 或标量；二者不可同时为标量

## 返回值

CipherTensor — `condition` 为真取 `x`，否则取 `y`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

cond = torch.tensor([[True, False], [False, True]])
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float64)
y = torch.tensor([[0.0, 0.0], [0.0, 0.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
yc = ct.encrypt_tensor(y)
out = hetorch2.where(cond, xc, yc)
print(ct.decrypt_tensor(out))
```
