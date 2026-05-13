# 示例：矩阵运算

矩阵乘法、转置、线性层的密文计算。

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 矩阵乘法
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
B = ct.encrypt(np.array([[0.5, 4., 2.], [4., 5., -6.], [-0.1, 0.7, 2.2]]))

C = hp.matmul(A, B)     # 等价于 A @ B
print(ct.decrypt(C))
# [[ 8.2 16.1 -3.4]
#  [-11.4 -4.2 30.8]
#  [ 5.1 19.8  8.8]]

# 向量点积
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
b = ct.encrypt(np.array([2.1, 4.0, 5.2, 40.5]))
dot_result = hp.matmul(a, b)  # 等价于 a @ b
print(ct.decrypt(dot_result))
# 28.66

# 转置
AT = hp.transpose(A)     # 等价于 A.T
print(ct.decrypt(AT))

# 线性层: output = X @ W + bias
X = ct.encrypt(np.random.randn(4, 3))
W = ct.encrypt(np.random.randn(3, 2))
bias = ct.encrypt(np.array([0.1, -0.2]))

output = X @ W + bias     # 运算符写法
print(ct.decrypt(output).shape)  # (4, 2)

# 查看密文元信息
print(A.cipherShape())            # (3, 3)
print(A.get_encryption_type())    # 0 (行加密)
```
