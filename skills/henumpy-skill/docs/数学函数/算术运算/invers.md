# invers

### 对两个输入元素作除，返回$ x_2/x_1 $ 输入：标量密文或数组密文 `x_1`：除数 `x_2`：被除数 如果$ x_1.shape \neq x_2.shape $，则将它们广播到通用形状（成为输出的形状）。 输出：标量密文或数组密文 `div`：$ x_2/x_1 $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量和标量
x1 = ct.encrypt(5)
x2 = ct.encrypt(3)
res = hp.invers(x1, x2)	
print(ct.decrypt(res))
# 输出  0.5999999999999999

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.invers(a, b)		
print(ct.decrypt(res))
# 输出 [  4.2         13.33333333   1.20930233 405.        ]

# 标量和向量
res = hp.invers(x1, a)		
print(ct.decrypt(res))
# 输出 [0.1  0.06 0.86 0.02]

# 向量和标量
res = hp.invers(b, x2)
print(ct.decrypt(res))
# 输出 [1.42857143 0.75       0.57692308 0.07407407]

# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.invers(A, B)     
print(ct.decrypt(res))
# 输出 [[ 0.5         2.          0.66666667]
#       [ 2.         -1.66666667 -1.5       ]
#       [-0.03333333  0.7         0.55      ]]

# 标量和数组		
res = hp.invers(x1, B)		
print(ct.decrypt(res))
# 输出  [[ 0.1   0.8   0.4 ]
#       [ 0.8   1.   -1.2 ]
#       [-0.02  0.14  0.44]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 1.,  2.],[ 2., -3.]])
C = ct.encrypt(CC)
res = hp.invers(a2, C)		
print(ct.decrypt(res))
# 输出 [[  2.           6.66666667]
#       [  4.         -10.        ]]
```
