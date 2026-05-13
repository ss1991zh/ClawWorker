# compare

### 比较两个输入元素的大小

## 参数

标量密文或数组密文

- `a`：待比较的第一个元素
- `b`：待比较的第二个元素 如果 $ a.shape\neq b.shape $，则将它们广播到通用形状（成为输出的形状）。

## 返回值

标量明文或数组明文 $ compare[i]=\begin{cases}1 & a[i]>b[i]\\0 & a[i]=b[i]\\-1 & a[i]<b[i]\end{cases}  $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()
    
# 标量 vs 标量
x1 = ct.encrypt(5.0)
x2 = ct.encrypt(3.0)
res = hp.compare(x1, x2)
print(res)
# 输出 1

# 向量 vs 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.compare(a, b)
print(res)
# 输出 [-1 -1 -1 -1]

# 数组 vs 数组
XX = np.array([[ 1.,  0.5,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
X = ct.encrypt(XX)
YY = np.array([[ -1.,  2.,  3.],[ 3., -3.,  1.],[ 3.,  5.,  -6.]])
Y = ct.encrypt(YY)
res = hp.compare(X, Y)
print(res)
# 输出 [[ 1 -1  0]
#		[-1  0  1]
#		[ 0 -1  1]]

# 标量 vs 向量
res = hp.compare(x2, a)
print(res)
# 输出 [1 1 -1 1]

# 标量 vs 数组
res = hp.compare(x2, X)
print(res)
# 输出 [[ 1  1  0]
#		[ 1  1 -1]
#		[ 0  1 -1]]

# 向量 vs 数组
xx = np.array([0.5, 0.3, 4.3])
x = ct.encrypt(xx)
res = hp.compare(x, X)
print(res)
# 输出 [[-1 -1  1]
#		[-1  1  1]
#		[-1 -1  1]]
```
