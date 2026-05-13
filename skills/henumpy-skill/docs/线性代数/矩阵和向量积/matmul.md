# hp.matmul

矩阵乘法。

## 签名

```python
hp.matmul(A, B, output_encrypt_type=None)
```

## 参数

- `A`: 数组密文 — 第一个输入，m×p 维
- `B`: 数组密文 — 第二个输入，p×n 维（A 的列数须等于 B 的行数）
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

标量密文或矩阵密文：
- 一维×一维 → 标量（内积）：`sum(a_i * b_i)`
- 二维×二维 → 矩阵乘积：`(AB)_ij = sum(a_ik * b_kj)`

> **备注**: `@` 运算符可作为 `hp.matmul` 的简写。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量内积
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
b = ct.encrypt(np.array([2.1, 4.0, 5.2, 40.5]))
res = hp.matmul(a, b)       # 等价于 a @ b
print(ct.decrypt(res))
# 输出 28.660000000000004

# 矩阵乘法
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
B = ct.encrypt(np.array([[0.5, 4., 2.], [4., 5., -6.], [-0.1, 0.7, 2.2]]))
res = hp.matmul(A, B)       # 等价于 A @ B
print(ct.decrypt(res))
# 输出 [[  8.2  16.1  -3.4]
#       [-11.4  -4.2  30.8]
#       [  5.1  19.8   8.8]]
```
