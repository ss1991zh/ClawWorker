# div

密文除法，对应 `torch.div`。

## 签名

`hetorch2.div(input, other)`

## 参数

- `input`: 密文张量或与 `other` 可广播的明文张量/标量 — 被除数
- `other`: 密文张量或与 `input` 可广播的明文张量/标量 — 除数（不可为零）

## 返回值

CipherTensor — 逐元素商 `input / other`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[4.0, 6.0], [8.0, 9.0]], dtype=torch.float64)
y = torch.tensor([[2.0, 3.0], [4.0, 3.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
yc = ct.encrypt_tensor(y)
out = hetorch2.div(xc, yc)
print(ct.decrypt_tensor(out))
```
