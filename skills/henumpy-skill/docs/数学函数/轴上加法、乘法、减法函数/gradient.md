# gradient

### 返回 N 维数组的梯度

## 参数

- `x`：数组密文，输入数组
- `axis`： $ None $或整数或整数元组，可选 默认值 $ axis=None $将计算输入数组中所有轴的梯度。如果轴为负数，则从最后一个轴计数到第一个轴。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `gradient`：$ x $的梯度 $ x=[x_0,x_1,\dots,x_n] $ $ gradient(x)=[x_1-x_0,\frac{x_2-x_0}{2},\cdots,\frac{x_n-x_{n-2}}{2},x_n-x_{n-1}] $

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
res = hp.gradient(a)	
print(ct.decrypt(res))
# 输出 [-0.2  1.9 -0.1 -4.2]

# 数组, axis=1
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.gradient(A, axis=1)		
print(ct.decrypt(res))
# 输出 [[ 1.   1.   1. ]
#       [-5.   1.   7. ]
#       [-2.   0.5  3. ]]
```
