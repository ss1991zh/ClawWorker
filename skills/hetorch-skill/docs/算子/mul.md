# mul

密文逐元素乘法（`multiply` 是别名）。注意：这是逐元素乘法，不是矩阵乘法，对应 `torch.mul`。

## 签名

`hetorch2.mul(input, other)`

## 参数

- `input`: 密文张量或与 `other` 可广播的明文张量/标量
- `other`: 密文张量或与 `input` 可广播的明文张量/标量
- `multiply` — `mul` 的别名，语义相同

## 返回值

CipherTensor — 逐元素积。矩阵乘法请使用 `hetorch2.matmul`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float64)
y = torch.tensor([[2.0, 0.5], [1.0, 3.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
yc = ct.encrypt_tensor(y)
out = hetorch2.mul(xc, yc)
print(ct.decrypt_tensor(out))
```
