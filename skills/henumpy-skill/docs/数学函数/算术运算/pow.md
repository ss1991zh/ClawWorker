# hp.pow

幂运算，支持分数次幂。计算 `x^(n/m)`。

## 签名

```python
hp.pow(x, n, m=1, output_encrypt_type=None)
```

## 参数

- `x`: 标量密文/数组密文 — 底数
- `n`: int (明文) — 指数的分子部分
- `m` (可选): int (明文) — 指数的分母部分，默认 `m=1`
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

标量密文或数组密文 — `x` 的 `n/m` 次幂，即 `x^(n/m)`。

> **备注**: `**` 运算符可作为 `hp.pow` 的简写（仅整数幂）。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量平方
x = ct.encrypt(5)
res = hp.pow(x, 2)     # 等价于 x ** 2
print(ct.decrypt(res))
# 输出 25.000000000000004

# 分数次幂: x^(2/3)
res = hp.pow(x, 2, 3)
print(ct.decrypt(res))
# 输出 2.9240177382128643

# 向量平方
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
res = hp.pow(a, 2)     # 等价于 a ** 2
print(ct.decrypt(res))
# 输出 [2.500e-01 9.000e-02 1.849e+01 1.000e-02]

# 矩阵 x^(2/3)
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
res = hp.pow(A, 2, 3)
print(ct.decrypt(res))
# 输出 [[1.         1.58740105 2.08008382]
#       [1.58740105        nan 2.5198421 ]
#       [2.08008382 1.         2.5198421 ]]
```
