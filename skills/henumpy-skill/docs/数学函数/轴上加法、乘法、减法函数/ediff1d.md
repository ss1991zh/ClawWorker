# ediff1d

### 数组的连续元素之间的差异
连续两个元素直接做差，矩阵则先将其展平，返回永远是一维数组

## 参数

`x`：数组密文，输入数组

## 返回值

标量密文或数组密文 `ediff1d`：$ x $连续元素之间的差异 $ x=[x_0,x_1,\dots,x_n] $ $ ediff1d(x)=[x_1-x_0,x_2-x_1,\cdots,x_n-x_{n-1}] $

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
res = hp.ediff1d(a)	
print(ct.decrypt(res))
# 输出 [-0.2  4.  -4.2]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.ediff1d(A)		
print(ct.decrypt(res))
# 输出 [ 1.  1. -1. -5.  7. -1. -2.  3.]
```
