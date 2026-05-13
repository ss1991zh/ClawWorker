# matmul

密文矩阵乘法。注意：这是矩阵乘法，与 mul（逐元素乘法）不同，对应 `torch.matmul`。

## 签名

`hetorch2.matmul(input, other)`

## 参数

- `input`: 密文或明文二维（及符合广播规则的批次）张量 — 左矩阵
- `other`: 密文或明文张量 — 右矩阵

## 返回值

CipherTensor — 矩阵乘积 `@` 语义与 `torch.matmul` 一致。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float64)
b = torch.tensor([[0.5, 1.0], [1.5, 2.0]], dtype=torch.float64)
ac = ct.encrypt_tensor(a)
bc = ct.encrypt_tensor(b)
out = hetorch2.matmul(ac, bc)
print(ct.decrypt_tensor(out))
```
