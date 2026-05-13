# nanprod

### 返回给定轴上的数组元素的乘积，将非数字 (NaN) 视为 1

## 参数

- `x`：数组密文，输入数组
- `axis`： $ None $或整数或整数元组，可选 默认值 $ axis=None $将计算输入数组中所有元素的乘积。如果轴为负数，则从最后一个轴计数到第一个轴。如果 $ axis $是整数元组，则在元组中指定的所有轴上执行乘积，而不是像以前那样在单个轴或所有轴上执行乘积。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `nanprod`：$ x $指定轴元素的乘积，将非数字 (NaN) 视为1。 $ x=[x_0,x_1,\dots,x_n] $ $ nanprod(x)=\prod_{i=0}^{n}x_i $

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
res = hp.nanprod(a)	
print(ct.decrypt(res))
# 输出 0.06450000000000002

# 数组
AA = np.array([[ 1.,  np.nan,  3.],[ 2., -3.,  4.],[ 3.,  1., np.nan]])
A = ct.encrypt(AA)
res = hp.nanprod(A)		
print(ct.decrypt(res))
# 输出 -215.99999999999991

# 数组, axis=0
res = hp.nanprod(A, axis=0)
print(ct.decrypt(res))
# 输出 [ 6. -3. 12.]
```
