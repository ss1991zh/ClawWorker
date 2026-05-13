# mod

### 返回除法元素的余数

## 参数

标量密文、数组密文、标量明文(float)

- `x_1`：被除数
- `x_2`：除数 如果 $ x_1.shape \neq x_2.shape $，则将它们广播到通用形状（成为输出的形状）。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `mod`：除法的余数 $ mod(x_1,\ x_2)=x_1-x_2\times floor(div(x_1,\ x_2)) $

> **备注**: % 运算符可以用作 hp.mod 的简写

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
res = hp.mod(x1, x2)	# 等价于 res = x1 % x2
print(ct.decrypt(res))
# 输出  2.000000000000014

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.mod(b, a)		# 等价于 res = b % a
print(ct.decrypt(res))
# 输出 [1.00000000e-01 1.00000000e-01 9.00000000e-01 7.81017729e-14]

# 标量和向量
res = x1 % a	# 等价于 res = hp.mod(x1, a)	
print(ct.decrypt(res))
# 输出 [2.03717889e-15 2.00000000e-01 7.00000000e-01 2.03717889e-15]

# 标量密文和标量明文
res = hp.mod(x1, 2.0)  	# 等价于 res = x1 % 2	
print(ct.decrypt(res))
# 输出 1.0000000000000058

# 向量密文和标量明文
res = b % 2  	# 等价于 res = hp.mod(b, 2.0)	
print(ct.decrypt(res))
# 输出 [1.00000000e-01 6.84917626e-15 1.20000000e+00 5.00000000e-01]
    
# 数组和数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.mod(A, B)     # 等价于 res = A % B
print(ct.decrypt(res))
# 输出 [[ 4.81875144e-16  2.00000000e+00  1.00000000e+00]
#       [ 2.00000000e+00  2.00000000e+00 -2.00000000e+00]
#       [-1.00000000e-01  3.00000000e-01  1.80000000e+00]]

# 标量和数组		
res = hp.mod(x1, B)		# 等价于 res = x1 % B
print(ct.decrypt(res))
# 输出  [[-3.81587717e-15  1.00000000e+00  1.00000000e+00]
#       [ 1.00000000e+00  6.20673788e-15 -1.00000000e+00]
#       [-1.00000000e-01  1.00000000e-01  6.00000000e-01]]

# 向量和数组
aa2 = np.array([0.5, 0.3])
a2 = ct.encrypt(aa2)
CC = np.array([[ 1.,  2.],[ 2., -3.]])
C = ct.encrypt(CC)
res = hp.mod(a2, C)			# 等价于 res = a2 % C
print(ct.decrypt(res))
# 输出 [[0.5 0.3]
#       [0.5 -2.7]]

# 数组和明文
res = hp.mod(A, 4)		# 等价于 res = A % 4
print(ct.decrypt(res))
# 输出 [[1.00000000e+00 2.00000000e+00 3.00000000e+00]
#       [2.00000000e+00 1.00000000e+00 6.54509274e-15]
#       [3.00000000e+00 1.00000000e+00 2.10809240e-15]]
```
