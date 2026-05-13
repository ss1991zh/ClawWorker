# argmin

### 返回最小值对应的索引

## 参数

- `a`：数组密文，输入数组
- `axis`：整型，可选 默认情况下， 将数组平展成一维数组，否则沿指定的轴。

## 返回值

标量明文 `argmin`：$ a $在指定的第$ axis $维度（轴）上的最小值对应的位置索引，若$ a $中在指定轴上有多个最小值，则返回第一个最小值的索引，$ axis $的取值范围就是数据维数的取值范围。

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
res = hp.argmin(a)
print(res)
# 输出 3

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.argmin(A)
print(res)
# 输出 4

# 数组, axis=0
res = hp.argmin(A, axis=0)
print(res)
# 输出 [0 1 0]
```
