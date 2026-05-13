# isclose

### 判断数组元素是否在误差范围内相等

## 参数

- `a`：标量密文或数组密文，待比较的第一个元素
- `b`：标量密文或数组密文，待比较的第二个元素 如果 $ a.shape\neq b.shape $，则将它们广播到通用形状（成为输出的形状）。
- `rtol`：标量明文，可选 相对公差，默认值为 $ 1\times10^{-5} $ `atol`：标量明文，可选 绝对公差，默认值为$ 1\times10^{-8} $

## 返回值

布尔数组，形状与$ a $或$ b $相同 `isclose`：表示$ a $和$ b $是否在误差范围内相等 如果$ absolute(a-b)\leq(atol+rtol*absolute(b)) $，返回 True，否则返回 False

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量和标量
x1 = ct.encrypt(5.0)
x2 = ct.encrypt(3.0)
res = hp.isclose(x1, x2)
print(res)
# 输出 False

# 向量和向量, 指定 rtol
aa = np.array([0.5, 3.9, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 4.2, 40.5])
b = ct.encrypt(bb)
res = hp.isclose(a, b, rtol = 0.1)
print(res)
# 输出 [False  True  True False]

# 标量和向量, 指定 rtol 和 atol
res = hp.isclose(x2, a, rtol = 0.01, atol = 1e-3)
print(res)
# 输出 [False False False False]

# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  3.],[ 2, 5.,  -6.],[ -0.1,  1,  2.2]])
B = ct.encrypt(BB)
res = hp.isclose(A, B)		
print(res)
# 输出 [[False False  True]
#     	[ True False False]
#     	[False  True False]]

# 标量和数组, 指定 rtol		
res = hp.isclose(x1, B, rtol = 0.1)	
print(res)
# 输出 [[False False False]
#     	[False  True False]
#     	[False False False]]

# 向量和数组, 指定 rtol 和 atol
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 0.5,  2.],[ 2., 0.3]])
C = ct.encrypt(CC)
res = hp.isclose(a2, C, rtol = 0.01, atol = 1e-3)		
print(res)
# 输出 [[ True False]
#    	[False  True]]
```
