# trace

### 计算矩阵的迹

## 参数

矩阵密文

`A`：输入元素，$ n\times n $维方阵

## 返回值

标量密文 `trace`：$ A $的迹 $ trace(A)=\sum_{i=0}^{n-1}a_{ii}=a_{00}+a_{11}+\dots+a_{n-1,n-1} $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.trace(A)
print(ct.decrypt(res))
# 输出 2.0000000000000013
```
