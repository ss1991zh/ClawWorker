# hypot

### hypot 传入直角三角形的“直角边”，返回斜边

## 参数

标量密文或数组密文

- `x_1`：直角三角形的第一组直角边
- `x_2`：直角三角形的第二组直角边 如果 $ x_1.shape \neq x_2.shape $，则将它们广播到通用形状（成为输出的形状）。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `hypot`：以$ x_1 $和$ x_2 $为直角边的斜边

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
res = hp.hypot(x1, x2)
print(ct.decrypt(res))
# 输出  5.830951894845299

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.hypot(a, b)
print(ct.decrypt(res))
# 输出 [ 2.15870331  4.01123422  6.74759216 40.50012346]

# 标量和向量
res = hp.hypot(a, x2)
print(ct.decrypt(res))
# 输出 [3.04138127 3.01496269 5.24309069 3.0016662 ]

# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.hypot(A, B)
print(ct.decrypt(res))
# 输出 [[1.11803399 4.47213595 3.60555128]
#       [4.47213595 5.83095189 7.21110255]
#       [3.0016662  1.22065556 4.56508488]]

# 标量和数组		
res = hp.hypot(x1, B)	
print(ct.decrypt(res))
# 输出 [[5.02493781 6.40312424 5.38516481]
#       [6.40312424 7.07106781 7.81024968]
#       [5.0009999  5.04876222 5.46260011]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 1.,  2.],[ 2., -3.]])
C = ct.encrypt(CC)
res = hp.hypot(a2, C)		
print(ct.decrypt(res))
# 输出 [[1.11803399 2.02237484]
#       [2.06155281 3.01496269]]
```
