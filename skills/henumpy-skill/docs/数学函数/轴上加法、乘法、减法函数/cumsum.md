# cumsum

### 返回给定轴上元素的累积和

## 参数

- `x`：数组密文，输入数组
- `axis`： $ None $或整数，可选 计算累积加和的轴。默认情况下，是将输入平展，计算所有元素的累积和。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `cumsum`：$ x $指定轴元素的累计和 $ x=[x_0,x_1,\dots,x_n] $ $ cumprod(x)=[x_0,\ x_0+ x_1,\cdots,\sum_{i=0}^nx_i] $

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
res = hp.cumsum(a)	
print(ct.decrypt(res))
# 输出 [0.5 0.8 5.1 5.2]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.cumsum(A)		
print(ct.decrypt(res))
# 输出 [ 1.  3.  6.  8.  5.  9. 12. 13. 17.]

# 数组, axis=0
res = hp.cumsum(A, axis=0)
print(ct.decrypt(res))
# 输出 [[ 1.00000000e+00  2.00000000e+00  3.00000000e+00]
#      [ 3.00000000e+00 -1.00000000e+00  7.00000000e+00]
#      [ 6.00000000e+00  3.94824362e-16  1.10000000e+01]]
```
