# hp.sqrt

逐元素计算非负平方根。

## 签名

```python
hp.sqrt(x, output_encrypt_type=None)
```

## 参数

- `x`: 标量密文/数组密文 — 输入（负值将返回 NaN）
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

标量密文或数组密文 — `x` 的非负平方根。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
print(ct.decrypt(hp.sqrt(x)))
# 输出 2.2360679774997902

# 向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
print(ct.decrypt(hp.sqrt(a)))
# 输出 [0.70710678 0.54772256 2.07364414 0.31622777]

# 矩阵（含负值 → NaN）
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
print(ct.decrypt(hp.sqrt(A)))
# 输出 [[1.         1.41421356 1.73205081]
#       [1.41421356        nan 2.        ]
#       [1.73205081 1.         2.        ]]
```
