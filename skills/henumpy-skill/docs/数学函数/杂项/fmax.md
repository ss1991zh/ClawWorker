# fmax

### 取两个数组中的最大元素

## 参数

标量密文或数组密文

- `a`：待比较的第一个元素
- `b`：待比较的第二个元素 如果 $ a.shape\neq b.shape $，则将它们广播到通用形状（成为输出的形状）。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量明文或数组明文 `fmax`：返回两个输入数组的最大元素，如果被比较的元素之一是 NaN，则忽略NaN，返回非 NaN 元素。

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
res = hp.fmax(x1, x2)
print(ct.decrypt(res))
# 输出 5.000000000000001

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.fmax(a, b)
print(ct.decrypt(res))
# 输出 [ 2.1  4.   5.2 40.5]

# 标量和向量
res = hp.fmax(x2, a)
print(ct.decrypt(res))
# 输出 [3.  3.  4.3 3. ]

# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.fmax(A, B)		
print(ct.decrypt(res))
# 输出 [[1. 4. 3.]
#       [4. 5. 4.]
#       [3. 1. 4.]]

# 标量和数组		
res = hp.fmax(x2, B)	
print(ct.decrypt(res))
# 输出 [[3. 4. 3.]
#       [4. 5. 3.]
#       [3. 3. 3.]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 1.,  2.],[ 2., -3.]])
C = ct.encrypt(CC)
res = hp.fmax(a2, C)		
print(ct.decrypt(res))
# 输出 [[1.  2. ]
#       [2.  0.3]]
```
