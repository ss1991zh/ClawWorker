# cross

### 返回两个(数组)向量的叉积
$ a $和$ b $的叉积是同时与$ a $和$ b $垂直的一个向量（相应分量相加之和为零） 输入： `a`：数组密文，第一个向量（数组） `b`：数组密文，第二个向量（数组） `axis1`：整型，可选 定义向量(数组)的$ a $的轴。默认情况下，最后一个轴。 `axis2`：整型，可选 定义向量(数组)的$ b $的轴。默认情况下，最后一个轴。 `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定$ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若$ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

向量密文 `cross`：$ a $和$ b $的矢量叉积 1. 若$ a=(x_1,\ y_1),\ b=(x_2,\ y_2) $ 则$ cross(a,\ b)=x_1y_2-x_2y_1 $ 2. 若$ a=(x_1,\ y_1,\ z_1), \ b=(x_2,\ y_2,\ z_2) $ 则$ cross(a,\ b)=(y_1z_2-y_2z_1,\ x_2z_1-x_1z_2,\ x_1y_2-x_2y_1) $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 三维向量
aa1 = np.array([0.5, 0.3, 4.3])
a1 = ct.encrypt(aa1)
bb1 = np.array([2.1, 4.0, 5.2])
b1 = ct.encrypt(bb1)
res = hp.cross(a1, b1)
print(ct.decrypt(res))
# 输出 [-15.64   6.43   1.37]

# 二维向量
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
bb2 = np.array([2.1, 4.0])
b2 = ct.encrypt(bb2)
res = hp.cross(a2, b2)
print(ct.decrypt(res))
# 输出 1.3699999999999992

# 3*3 数组和 3*3 数组
aa33 = np.array([[ 1.,  0.5,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
a33 = ct.encrypt(aa33)
bb33 = np.array([[ -1.,  2.,  3.],[ 3., -3.,  1.],[ 3.,  5.,  -6.]])
b33 = ct.encrypt(bb33)
res = hp.cross(a33, b33)
print(ct.decrypt(res))
# 输出 [[ -4.5  -6.    2.5]
#       [  9.   10.    3. ]
#       [-26.   30.   12. ]]

# 2*3 数组和 3*2 数组, axis1 = 1, axis2 = 0
cc23 = np.array([[ 1.,  0.5,  3.],[ 2., -3.,  4.]])
c23 = ct.encrypt(cc23)
dd32 = np.array([[ -1.,  2.],[ 3., -3.],[ 3.,  5.]])
d32 = ct.encrypt(dd32)
res = hp.cross(c23, d32, axis1 = 1, axis2 = 0)
print(ct.decrypt(res))
# 输出 [[-7.5 -6.   3.5]
#       [-3.  -2.   0. ]]

# 2*2 数组和 2*2 数组
ee22 = np.array([[ 1.,  2.],[ 2., -3.]])
e22 = ct.encrypt(ee22)
ff22 = np.array([[ 0.5,  4.],[ 4., 5.],])
f22 = ct.encrypt(ff22)
res = hp.cross(e22, f22)
print(ct.decrypt(res))
# 输出  [[ 3. 22.]]

# 2*3 数组和 2*2 数组, axis1 = 1, axis2 = 1
res = hp.cross(c23, e22, axis1 = 1, axis2 = 1)
print(ct.decrypt(res))
# 输出  [[-6.   3.   1.5]
#       [12.   8.   0. ]]
```
