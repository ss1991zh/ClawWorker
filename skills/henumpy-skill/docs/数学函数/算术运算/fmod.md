# fmod

### 返回除法的余数

## 参数

标量密文、数组密文、标量明文(float)

- `x_1`：被除数
- `x_2`：除数 如果 $ x_1.shape \neq x_2.shape $，则将它们广播到通用形状（成为输出的形状）。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `fmod`：除法的余数 $ fmod(x_1,\ x_2)=x_1-x_2\times fix(div(x_1,\ x_2)) $

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
res = hp.fmod(x1, x2)	
print(ct.decrypt(res))
# 输出  2.0000000000000084

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.fmod(b, a)		
print(ct.decrypt(res))
# 输出 [1.0000000e-01 1.0000000e-01 9.0000000e-01 4.3584575e-14]

# 标量和向量
res = hp.fmod(x1, a)		
print(ct.decrypt(res))
# 输出 [4.90514374e-15 2.00000000e-01 7.00000000e-01 6.13142968e-15]

# 标量密文和标量明文
res = hp.fmod(x1, 2)		
print(ct.decrypt(res))
# 输出 1.0000000000000122

# 向量密文和标量明文
res = hp.fmod(b, 2)		
print(ct.decrypt(res))
# 输出 [1.00000000e-01 3.15409074e-15 1.20000000e+00 5.00000000e-01]
    
# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.fmod(A, B)     
print(ct.decrypt(res))
# 输出 [[ 1.43752154e-15  2.00000000e+00  1.00000000e+00]
#       [ 2.00000000e+00 -3.00000000e+00  4.00000000e+00]
#       [ 1.57268130e-14  3.00000000e-01  1.80000000e+00]]

# 标量和数组		
res = hp.fmod(x1, B)		
print(ct.decrypt(res))
# 输出  [[4.78905137e-15 1.00000000e+00 1.00000000e+00]
#       [1.00000000e+00 8.12973755e-15 5.00000000e+00]
#       [2.13208393e-14 1.00000000e-01 6.00000000e-01]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 1.,  2.],[ 2., -3.]])
C = ct.encrypt(CC)
res = hp.fmod(a2, C)		
print(ct.decrypt(res))
# 输出 [[0.5 0.3]
#       [0.5 0.3]]

# 数组和明文
res = hp.fmod(A, 4)		
print(ct.decrypt(res))
# 输出 [[ 1.00000000e+00  2.00000000e+00  3.00000000e+00]
#       [ 2.00000000e+00 -3.00000000e+00  0.00000000e+00]
#       [ 3.00000000e+00  1.00000000e+00 -2.29568544e-15]]
```
