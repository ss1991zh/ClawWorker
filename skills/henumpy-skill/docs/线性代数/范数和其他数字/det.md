# det

### 计算数组的行列式

## 参数

矩阵密文

`A`：输入元素，$ n\times n $维方阵

## 返回值

标量密文 `det`：$ A $的行列式 $ det(A)=\sum_{j_1j_2\dots j_n}(-1)^{\tau(j_1j_2\dots j_n)}a_{0j_1}a_{1j_2}\dots a_{n-1 j_n} $ 其中$ \tau(j_1j_2\dots j_n) $为$ j_1j_2\dots j_n $的逆序数。

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.det(A)
print(ct.decrypt(res))
# 输出 24.999999999999947
```
