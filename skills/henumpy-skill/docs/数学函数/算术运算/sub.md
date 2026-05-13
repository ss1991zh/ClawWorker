# hp.sub

逐元素减法。

## 签名

```python
hp.sub(x1, x2, output_encrypt_type=None)
```

## 参数

- `x1`: 标量密文/数组密文/标量明文 — 被减数
- `x2`: 标量密文/数组密文/标量明文 — 减数
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

若 `x1.shape ≠ x2.shape`，自动广播到通用形状。

## 返回值

标量密文或数组密文 — `x1 - x2` 的逐元素差。

> **备注**: `-` 运算符可作为 `hp.sub` 的简写。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量 - 标量
x1 = ct.encrypt(5)
x2 = ct.encrypt(3)
res = hp.sub(x1, x2)   # 等价于 x1 - x2
print(ct.decrypt(res))
# 输出 2.000000000000002

# 向量 - 向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
b = ct.encrypt(np.array([2.1, 4.0, 5.2, 40.5]))
res = hp.sub(a, b)      # 等价于 a - b
print(ct.decrypt(res))
# 输出 [ -1.6  -3.7  -0.9 -40.4]

# 密文 - 明文
res = hp.sub(x1, 2)     # 等价于 x1 - 2
print(ct.decrypt(res))
# 输出 2.9999999999999996

# 矩阵 - 矩阵
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
B = ct.encrypt(np.array([[0.5, 4., 2.], [4., 5., -6.], [-0.1, 0.7, 2.2]]))
res = hp.sub(A, B)      # 等价于 A - B
print(ct.decrypt(res))
# 输出 [[ 0.5 -2.   1. ]
#       [-2.  -8.  10. ]
#       [ 3.1  0.3  1.8]]
```
