# minimum

### 取数组中最小的元素

## 参数

标量密文或数组密文

- `a`：待比较的第一个元素
- `b`：待比较的第二个元素 如果 $ a.shape\neq b.shape $，则将它们广播到通用形状（成为输出的形状）。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量明文或数组明文 `minimum`：返回两个输入数组的最小元素，如果被比较的元素之一是 NaN，则返回NaN。

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
res = hp.minimum(x1, x2)
print(ct.decrypt(res))
# 输出 3.0

# 向量和向量
aa_nan = np.array([0.5, 0.3, 4.3, 0.1, np.nan])
a_nan = ct.encrypt(aa_nan)
bb_nan = np.array([2.1, np.nan, 4.0, 5.2, 40.5])
b_nan = ct.encrypt(bb_nan)
res = hp.minimum(a_nan, b_nan)
print(ct.decrypt(res))
# 输出 [0.5 nan 4.  0.1 nan]

# 标量和向量
res = hp.minimum(x2, b_nan)
print(ct.decrypt(res))
# 输出 [2.1 nan 3.  3.  3. ]

# 数组和数组
AA_nan = np.array([[ 1.,  np.nan,  3.],[ 2., -3.,  4.],[ 3.,  1., np.nan]])
A_nan = ct.encrypt(AA_nan)
BB_nan = np.array([[ 0.5,  4.,  np.nan],[ np.nan, 5.,  -6.],[ -0.1,  0.7,  2.2]])
B_nan = ct.encrypt(BB_nan)
res = hp.minimum(A_nan, B_nan)		
print(ct.decrypt(res))
# 输出 [[ 0.5  nan  nan]
#       [ nan -3.  -6. ]
#       [-0.1  0.7  nan]]

# 标量和数组		
res = hp.minimum(x2, B_nan)	
print(ct.decrypt(res))
# 输出 [[ 0.5  3.   nan]
#       [ nan  3.  -6. ]
#       [-0.1  0.7  2.2]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC_nan = np.array([[ 1.,  np.nan],[ 2., -3.]])
C_nan = ct.encrypt(CC_nan)
res = hp.minimum(a2, C_nan)		
print(ct.decrypt(res))
# 输出 [[ 0.5  nan]
#       [ 0.5 -3. ]]
```
