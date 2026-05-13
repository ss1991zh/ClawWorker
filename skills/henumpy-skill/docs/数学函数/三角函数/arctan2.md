# arctan2

### $ x_1/x_2 $的反正切，并正确选择象限 输入：标量密文或数组密文 `x_1`：$ y $坐标 `x_2`：$ x $坐标

如果 $ x_1.shape \neq x_2.shape $，则将它们广播到通用形状（成为输出的形状）。 `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定$ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若$ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `arctan2`：点$ (x,y) $和坐标原点所连线段与$ x $轴正方向所夹角度，默认弧度制，值域是$ [-\pi,\pi] $

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
res = hp.arctan2(x1, x2)
print(ct.decrypt(res))
# 输出  1.0303768265242415

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.arctan2(a, b)
print(ct.decrypt(res))
# 输出 [0.23374318 0.07485985 0.69094323 0.00246913]

# 标量和向量
res = hp.arctan2(a, x2)
print(ct.decrypt(res))
# 输出 [0.16514868 0.09966865 0.96163286 0.033321  ]

# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.arctan2(A, B)
print(ct.decrypt(res))
# 输出 [[ 1.10714872  0.46364761  0.98279372]
#       [ 0.46364761 -0.5404195   2.55359005]
#       [ 1.60411732  0.96007036  1.06795312]]

# 标量和数组		
res = hp.arctan2(x1, B)	
print(ct.decrypt(res))
# 输出 [[1.47112767 0.89605538 1.19028995]
#       [0.89605538 0.78539816 2.44685438]
#       [1.59079366 1.43170039 1.15628945]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 1.,  2.],[ 2., -3.]])
C = ct.encrypt(CC)
res = hp.arctan2(a2, C)		
print(ct.decrypt(res))
# 输出 [[0.46364761 0.14888995]
#       [0.24497866 3.041924  ]]
```
