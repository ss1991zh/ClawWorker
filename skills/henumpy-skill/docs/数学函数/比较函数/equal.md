# equal

### 比较两个输入元素是否相等

## 参数

标量密文、数组密文、标量明文

- `a`：待比较的第一个元素
- `b`：待比较的第二个元素 如果 $ a.shape\neq b.shape $，则将它们广播到通用形状（成为输出的形状）。

## 返回值

布尔型标量或数组 若$ a=b $，则$ equal(a,\ b)=True $ 若$ a\neq b $，则$ equal(a,\ b)=False $

> **备注**: == 运算符可以用作 hp.equal 的简写

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
res = hp.equal(x1, x2)		# 等价于 res = x1 == x2
print(res)
# 输出 False

# 向量 vs 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.equal(a, b)		# 等价于 res = a == b
print(res)
# 输出 [False False False False]

# 数组 vs 数组
XX = np.array([[ 1.,  0.5,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
X = ct.encrypt(XX)
YY = np.array([[ -1.,  2.,  3.],[ 3., -3.,  1.],[ 3.,  5.,  -6.]])
Y = ct.encrypt(YY)
res = X == Y			# 等价于 res = hp.equal(X, Y)
print(res)
# 输出 [[False False  True]
#		[False  True False]
#		[ True False False]]
    
# 标量 vs 向量
res = x2 == a		# 等价于 res = hp.equal(x2, a)
print(res)
# 输出 [False False False False]

# 标量 vs 数组
res = X == x2			# 等价于 res = hp.equal(X, x2)
print(res)
# 输出 [[False False  True]
#		[False False False]
#		[ True False False]]

# 向量 vs 数组
xx = np.array([0.5, 0.3, 4.3])
x = ct.encrypt(xx)
res = x == X			# 等价于 res = hp.equal(x, X)
print(res)
# 输出 [[False False False]
#		[False False False]
#		[False False False]]

# 标量明文 vs 标量密文
res = x1 == 5
print(res)
# 输出 True

# 标量明文 vs 向量密文
res = a == 4.3
print(res)
# 输出 [False False  True False]

# 标量明文 vs 数组密文
res = X == 3
print(res)
# 输出 [[False False  True]
#		[False False False]
#		[ True False False]]
```
