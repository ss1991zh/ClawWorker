# trapz

### 使用复合梯形规则沿给定轴积分

## 参数

- `a`：数组密文，待积分数组
- `x`：数组密文，可选 对应于 $ a $值的采样点， $ x $和 $ a $的长度要一致。默认 $ x=None $， 假定采样点相距 $ dx $均匀分布。
- `dx`：标量，可选 $ x=None
 $时采样点之间的间距，默认值为 1 `axis`：$ None $或整数，可选 要沿其积分的轴。默认值$ axis=1 $沿行积分，若$ axis=0 $则沿列积分。

## 返回值

数组密文 `trapz`：$ a $的梯形积分 设$ a=[a_1,\ a_2,\dots,a_n] $，间距为$ x=[x_1,\ x_2,\dots,x_n] $ 则$ trapz(a)=\frac{1}{2}\sum_{i=1}^{n-1}(a_{i+1}+a_i)(x_{i+1}-x_i) $ 若$ x=None
 $，则$ trapz(a)=\frac{1}{2}\sum_{i=1}^{n-1}(a_{i+1}+a_i)*dx $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# a 为向量, 默认情况, dx=1
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.trapz(a)
print(ct.decrypt(res))
# 输出 4.900000000000001

# a 为向量, 指定采样点
xx = np.array([2.1, 4.0, 5.2, 40.5])
x = ct.encrypt(xx)
res = hp.trapz(a, x)
print(ct.decrypt(res))
# 输出 81.17999999999998

# A 为数组, 默认情况, dx=1
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.trapz(A)
print(ct.decrypt(res))
# 输出 [4.  0.  4.5]

# A 为数组, 指定采样点 X 也是数组, 默认轴
XX = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
X = ct.encrypt(XX)
res = hp.trapz(A, X)
print(ct.decrypt(res))
# 输出 [ 0.25 -6.    5.35]

# A 为数组, 指定采样点 X 也是数组, axis=0
res = hp.trapz(A, X, axis=0)
print(ct.decrypt(res))
# 输出 [-5.   3.8  4.8]

# A 为数组,  yy 是长度与 A 相等的向量
yy = np.array([0.5, 0.3, 4.3])
y = ct.encrypt(yy)
res = hp.trapz(A, y)
print(ct.decrypt(res))
# 输出 [9.7 2.1 9.6]
```
