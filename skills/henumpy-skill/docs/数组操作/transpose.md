# hp.transpose

数组转置。

## 签名

```python
hp.transpose(A, output_encrypt_type=None)
```

## 参数

- `A`: 数组密文 — 输入数组（m×n 维）。一维向量(1×n)转置后为二维数组(n×1)
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

数组密文 — `A` 的转置。

> **备注**: `.T` 属性可作为 `hp.transpose` 的简写。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量转置 → 列向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
res = hp.transpose(a)
print(ct.decrypt(res))
# 输出 [[0.5]
#       [0.3]
#       [4.3]
#       [0.1]]

# 矩阵转置
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
res = hp.transpose(A)   # 等价于 A.T
print(ct.decrypt(res))
# 输出 [[ 1.  2.  3.]
#       [ 2. -3.  1.]
#       [ 3.  4.  4.]]
```
