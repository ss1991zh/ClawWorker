# cipherShape

### 返回输入数组的形状

## 参数

`a`：数组密文，需要计算形状的数组

## 返回值

标量明文 `cipherShape`：$ a $的形状

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
res = a.cipherShape()
print(res)
# 输出 (4,)

# 数组
data_array_plain = np.array([[ 1.,  2.,  3.],[ 4., 5.,  6.]])
data_array = ct.encrypt(data_array_plain)
res = data_array.cipherShape()
print(res)
# 输出 (2, 3)
```
