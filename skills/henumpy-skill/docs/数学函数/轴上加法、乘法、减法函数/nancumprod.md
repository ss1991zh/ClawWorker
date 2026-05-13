# nancumprod

### 返回给定轴上的数组元素的累积乘积，将非数字 (NaN) 视为1。

## 参数

- `x`：数组密文，输入数组
- `axis`： $ None $或整数，可选 计算累积乘积的轴。默认情况下，是将输入平展，计算所有元素的累积乘积。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `nancumprod`：$ x $指定轴元素的累积乘积，将非数字 (NaN) 视为1。 $ x=[x_0,x_1,\dots,x_n] $ $ nancumprod(x)=[x_0,\ x_0\times x_1,\cdots,\prod_{i=0}^nx_i] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1, np.nan])
a = ct.encrypt(aa)
res = hp.nancumprod(a)	
print(ct.decrypt(res))
# 输出 [0.5    0.15   0.645  0.0645 0.0645]

# 数组
AA = np.array([[ 1.,  np.nan,  3.],[ 2., -3.,  4.],[ 3.,  1., np.nan]])
A = ct.encrypt(AA)
res = hp.nancumprod(A)		
print(ct.decrypt(res))
# 输出 [   1.    1.    3.    6.  -18.  -72. -216. -216. -216.]

# 数组, axis=0
res = hp.nancumprod(A, axis=0)
print(ct.decrypt(res))
# 输出 [[ 1.  1.  3.]
#       [ 2. -3. 12.]
#       [ 6. -3. 12.]]
```
