# cumprod

### 返回给定轴上元素的累积乘积

## 参数

- `x`：数组密文，输入数组
- `axis`： $ None $或整数，可选 计算累积乘积的轴。默认情况下，是将输入平展，计算所有元素的累积乘积。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `cumprod`：$ x $指定轴元素的累积乘积 $ x=[x_0,x_1,\dots,x_n] $ $ cumprod(x)=[x_0,\ x_0\times x_1,\cdots,\prod_{i=0}^nx_i] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.cumprod(a)	
print(ct.decrypt(res))
# 输出 [0.5    0.15   0.645  0.0645]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.cumprod(A)		
print(ct.decrypt(res))
# 输出 [ 1.000e+00  2.000e+00  6.000e+00  1.200e+01 -3.600e+01 -1.440e+02 -4.320e+02 -4.320e+02 -1.728e+03]

# 数组, axis=0
res = hp.cumprod(A, axis=0)
print(ct.decrypt(res))
# 输出 [[ 1.  2.  3.]
#       [ 2. -6. 12.]
#       [ 6. -6. 48.]]
```
