# cipherLen

### 返回输入数组的长度

## 参数

`a`：数组密文，需要计算长度的数组

## 返回值

标量明文 `cipherLen`：$ a $的长度

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
res = hp.cipherLen(a)
print(res)
# 输出 4

# 数组
data_array_plain = np.array([[ 1.,  2.,  3.],[ 4., 5.,  6.]])
data_array = ct.encrypt(data_array_plain)
res = hp.cipherLen(data_array)
print(res)
# 输出 2
```
