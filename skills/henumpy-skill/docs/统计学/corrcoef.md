# hp.corrcoef

计算皮尔逊乘积矩相关系数矩阵。

## 签名

```python
hp.corrcoef(A, B=None, output_encrypt_type=None)
```

## 参数

- `A`: 数组密文 — 二维数组，每行代表一个变量，每列代表一个观测
- `B` (可选): 数组密文 — 额外变量集，须与 A 形状相同
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

数组密文 — 相关系数矩阵。`ρ(A,B) = cov(A,B) / (σ_A * σ_B)`

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

A = ct.encrypt(np.array([[1., 2.], [2., -3.]]))
B = ct.encrypt(np.array([[0.5, 4.], [4., 5.]]))
res = hp.corrcoef(A, B)
print(ct.decrypt(res))
# 输出 [[ 1. -1.  1.  1.]
#       [-1.  1. -1. -1.]
#       [ 1. -1.  1.  1.]
#       [ 1. -1.  1.  1.]]
```
