# equal

密文判等，对应 `torch.equal`。

## 签名

`hetorch2.equal(input, other)`

## 参数

- `input`: 密文张量或与 `other` 可广播的明文张量/标量
- `other`: 密文张量或与 `input` 可广播的明文张量/标量

## 返回值

CipherTensor 或按实现约定的布尔/掩码表示 — 逐元素是否相等（与 `torch.equal` 逐元素语义一致）。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0], [2.0, 2.0]], dtype=torch.float64)
y = torch.tensor([[1.0, 0.0], [2.0, 2.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
yc = ct.encrypt_tensor(y)
out = hetorch2.equal(xc, yc)
print(ct.decrypt_tensor(out))
```
