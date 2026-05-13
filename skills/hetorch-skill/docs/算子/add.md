# add

密文加法，对应 `torch.add`。

## 签名

`hetorch2.add(input, other)`

## 参数

- `input`: 密文张量或与 `other` 可广播的明文张量/标量 — 左操作数
- `other`: 密文张量或与 `input` 可广播的明文张量/标量 — 右操作数

## 返回值

CipherTensor — 逐元素和。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float64)
y = torch.tensor([[0.5, 1.0], [1.5, 2.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
yc = ct.encrypt_tensor(y)
out = hetorch2.add(xc, yc)
print(ct.decrypt_tensor(out))
```
