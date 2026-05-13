# hp.mean

沿指定轴计算算术平均值。

## 签名

```python
hp.mean(a, axis=None)
```

## 参数

- `a`: 数组密文 — 输入数组
- `axis` (可选): None 或 int — 计算轴。默认 None，对全部元素求均值

## 返回值

标量密文或数组密文 — 指定轴的算术平均值 `sum(a) / size(a)`。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量均值
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
print(ct.decrypt(hp.mean(a)))
# 输出 1.2999999999999996

# 矩阵全局均值
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
print(ct.decrypt(hp.mean(A)))
# 输出 1.8888888888888884

# 按列均值 (axis=0)
print(ct.decrypt(hp.mean(A, axis=0)))
# 输出 [ 2.00000000e+00 -7.30099038e-16  3.66666667e+00]
```
