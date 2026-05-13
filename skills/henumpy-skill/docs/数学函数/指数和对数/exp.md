# hp.exp

逐元素指数函数，计算 `e^x`。

## 签名

```python
hp.exp(x, output_encrypt_type=None)
```

## 参数

- `x`: 标量密文/数组密文 — 输入
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

标量密文或数组密文 — `e^x`。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
print(ct.decrypt(hp.exp(x)))
# 输出 148.41315910258135

# 向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
print(ct.decrypt(hp.exp(a)))
# 输出 [ 1.64872127  1.34985881 73.6997937   1.10517092]

# 矩阵
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
print(ct.decrypt(hp.exp(A)))
# 输出 [[2.71828183e+00 7.38905610e+00 2.00855369e+01]
#       [7.38905610e+00 4.97870684e-02 5.45981500e+01]
#       [2.00855369e+01 2.71828183e+00 5.45981500e+01]]
```
