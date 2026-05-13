# diff

### 计算沿给定轴的第 n 个离散差

## 参数

- `x`：数组密文，输入数组
- `n`： $ None $或整数，可选0 沿指定轴做离散差的次数，默认为 1，若 n=0，则按原样返回输入。
- `axis`： $ None $或整数，可选 取差值的轴，默认为最后一个轴。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `diff`：$ x $指定轴的离散差 $ x=[x_0,x_1,\dots,x_n] $ 默认 n=1，$ diff(x)=[x_1-x_0,x_2-x_1,\cdots,x_n-x_{n-1}] $ n=2，$ diff(x,\ 2)=[x_2-2x_1+x_0,\ x_3-2x_2+x_1,\dots,x_n-2x_{n-1}+x_{n-2}] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.diff(a)	
print(ct.decrypt(res))
# 输出 [-0.2  4.  -4.2]

# 向量, n=2
res = hp.diff(a, 2)
print(ct.decrypt(res))
# 输出 [ 4.2 -8.2]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.diff(A)		
print(ct.decrypt(res))
# 输出 [[ 1.  1.]
#       [-5.  7.]
#       [-2.  3.]]

# 数组, n=2, axis=0
res = hp.diff(A, n=2, axis=0)
print(ct.decrypt(res))
# 输出 [[ 1.02518914e-15  9.00000000e+00 -1.00000000e+00]]
```
