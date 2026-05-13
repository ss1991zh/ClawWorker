# interp

### 一维线性插值
单调增加样本点的一维线性插值。

将一维分段线性插值返回给具有给定离散数据点$ (xp,\ fp) $的函数，计算值为$ x $。 输入： `x`：标量密文或数组密文，用于计算插值的$ x $坐标 `xp`：一维数组密文，数据点的$ x $坐标 `fp`：一维数组密文，数据点的$ y $坐标，长度与$ xp $相同 `left`：标量密文，与$ fp $对应，可选 当$ x<xp[0] $时的返回值，默认是$ fp[0] $ `right`：标量密文，与$ fp $对应，可选 当$ x<xp[-1] $时的返回值，默认是$ fp[-1] $ `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定$ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若$ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文，形状与$ x $相同 `interp`： $ x $的插值

$ xp=[x_0,\ x_1,…,\ x_n] $ $ fp=[y_0,\ y_1,…,\ y_n] $ 若$ x<x_0 $，返回$ interp(x)=left $ 若 $ x_i\leq x\leq x_{i+1}    $，返回$ interp(x)=((x-x_i)/(x_{i+1}-x_i)*(y_{i+1}-y_i)+y_i $ 若$ x>x_n $，返回$ interp(x)=right $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量，默认情况
x = ct.encrypt(3.0)
xxp = np.array([-0.1, 0.7, 2.2, 3.8])
xp = ct.encrypt(xxp)
ffp = np.array([-7.1, 2.7, 13.2, 9.8])
fp = ct.encrypt(ffp)
res = hp.interp(x, xp, fp)
print(ct.decrypt(res))
# 输出 11.500000000000007

# 标量，指定 left, right
right = ct.encrypt(5.0)
left = ct.encrypt(0.3)
res = hp.interp(x, xp, fp, left, right)
print(ct.decrypt(res))
# 输出 11.500000000000007

# 向量，默认情况
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.interp(a, xp, fp)
print(ct.decrypt(res))
# 输出 [ 0.25 -2.2   9.8  -4.65]

# 向量，指定 left, right
res = hp.interp(a, xp, fp, left, right)
print(ct.decrypt(res))
# 输出 [ 0.25 -2.2   5.   -4.65]

# 数组，默认情况
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.interp(A, xp, fp)
print(ct.decrypt(res))
# 输出 [[ 4.8 11.8 11.5]
#       [11.8 -7.1  9.8]
#       [11.5  4.8  9.8]]

# 数组，指定 left, right
res = hp.interp(A, xp, fp, left, right)
print(ct.decrypt(res))
# 输出 [[ 4.8 11.8 11.5]
#		[11.8  0.3  5. ]
#		[11.5  4.8  5. ]]
```
