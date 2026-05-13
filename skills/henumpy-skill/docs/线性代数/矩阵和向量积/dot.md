# dot

### 计算两个数组的点积

## 参数

标量密文或数组密文

- `a`：第一个输入元素
- `b`：第二个输入元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 + 如果$ a $或$ b $有一个是标量，则等价于$ mul $，优先使用 $ hp.mul(a,b) $或$ a*b $ + 如果$ a $和$ b $都是一维数组，则返回的是$ a $和$ b $的内积 $ dot(a,b)=\sum_{i=0}^n a_ib_i $

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
res = hp.dot(x1, x2)
print(ct.decrypt(res))
# 输出  14.999999999999995

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.dot(a, b)
print(ct.decrypt(res))
# 输出 28.660000000000007

# 标量和向量
res = hp.dot(x2, b)
print(ct.decrypt(res))
# 输出 [  6.3  12.   15.6 121.5]

# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.dot(A, B)
print(ct.decrypt(res))
# 输出 [[  8.2  16.1  -3.4]
#       [-11.4  -4.2  30.8]
#       [  5.1  19.8   8.8]]

# 标量和数组		
res = hp.dot(x1, B)	
print(ct.decrypt(res))
# 输出 [[  2.5  20.   10. ]
#       [ 20.   25.  -30. ]
#       [ -0.5   3.5  11. ]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 1.,  2.],[ 2., -3.]])
C = ct.encrypt(CC)
res = hp.dot(a2, C)		
print(ct.decrypt(res))
# 输出 [1.1 0.1]
```
