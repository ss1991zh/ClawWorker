# hp.mul

逐元素乘法。

## 签名

```python
hp.mul(x1, x2, discrete=False, output_encrypt_type=None)
```

## 参数

- `x1`: 标量密文/数组密文/标量明文/数组明文 — 第一个乘数
- `x2`: 标量密文/数组密文/标量明文/数组明文 — 第二个乘数
- `discrete` (可选): bool — 输出为数组时的密文格式。`False`(默认)=连续密文数组, `True`=离散密文数组
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

若 `x1.shape ≠ x2.shape`，自动广播到通用形状。

## 返回值

标量密文或数组密文 — `x1` 和 `x2` 的逐元素积。

> **备注**: `*` 运算符可作为 `hp.mul` 的简写。注意名称是 `mul`，不是 `multiply`。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量 * 标量
x1 = ct.encrypt(5)
x2 = ct.encrypt(3)
res = hp.mul(x1, x2)   # 等价于 x1 * x2
print(ct.decrypt(res))
# 输出 15.000000000000004

# 向量 * 向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
b = ct.encrypt(np.array([2.1, 4.0, 5.2, 40.5]))
res = hp.mul(a, b)      # 等价于 a * b
print(ct.decrypt(res))
# 输出 [ 1.05  1.2  22.36  4.05]

# 密文 * 明文标量
res = hp.mul(x1, 2)     # 等价于 x1 * 2
print(ct.decrypt(res))
# 输出 10.0

# 密文 * 明文向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
res = hp.mul(x1, aa)    # 等价于 x1 * aa
print(ct.decrypt(res))
# 输出 [ 2.5  1.5 21.5  0.5]

# 矩阵 * 矩阵（逐元素）
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
B = ct.encrypt(np.array([[0.5, 4., 2.], [4., 5., -6.], [-0.1, 0.7, 2.2]]))
res = hp.mul(A, B)      # 等价于 A * B
print(ct.decrypt(res))
# 输出 [[  0.5   8.    6. ]
#       [  8.  -15.  -24. ]
#       [ -0.3   0.7   8.8]]
```
