# hp.add

逐元素加法。

## 签名

```python
hp.add(x1, x2, output_encrypt_type=None)
```

## 参数

- `x1`: 标量密文/数组密文/标量明文 — 第一个加数
- `x2`: 标量密文/数组密文/标量明文 — 第二个加数
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

若 `x1.shape ≠ x2.shape`，自动广播到通用形状。

## 返回值

标量密文或数组密文 — `x1` 和 `x2` 的逐元素和。

> **备注**: `+` 运算符可作为 `hp.add` 的简写。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量 + 标量
x1 = ct.encrypt(5)
x2 = ct.encrypt(3)
res = hp.add(x1, x2)   # 等价于 x1 + x2
print(ct.decrypt(res))
# 输出 7.999999999999999

# 向量 + 向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
b = ct.encrypt(np.array([2.1, 4.0, 5.2, 40.5]))
res = hp.add(a, b)      # 等价于 a + b
print(ct.decrypt(res))
# 输出 [ 2.6  4.3  9.5 40.6]

# 密文 + 明文标量
res = hp.add(x1, 2)     # 等价于 x1 + 2
print(ct.decrypt(res))
# 输出 7.000000000000003

# 向量 + 明文标量
res = hp.add(a, 2)      # 等价于 a + 2
print(ct.decrypt(res))
# 输出 [2.5 2.3 6.3 2.1]

# 矩阵 + 矩阵
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
B = ct.encrypt(np.array([[0.5, 4., 2.], [4., 5., -6.], [-0.1, 0.7, 2.2]]))
res = hp.add(A, B)      # 等价于 A + B
print(ct.decrypt(res))
# 输出 [[ 1.5  6.   5. ]
#       [ 6.   2.  -2. ]
#       [ 2.9  1.7  6.2]]

# 标量 + 矩阵（广播）
res = hp.add(x1, B)     # 等价于 x1 + B
print(ct.decrypt(res))
# 输出 [[ 5.5  9.   7. ]
#       [ 9.  10.  -1. ]
#       [ 4.9  5.7  7.2]]
```
