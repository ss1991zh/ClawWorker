# get_encryption_type

### 获取加密类型

## 参数

标量密文或数组密文

`a`：需要获取加密类型的密文

## 返回值

标量明文 `get_encryption_type`：$ a $的密文加密类型 + $ a $为行加密，$ get\_encryption\_type(a)=0 $ + $ a $为列加密，$ get\_encryption\_type(a)=1 $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 行加密
data_array_plain = np.array([[ 1.,  2.,  3.],[ 4., 5.,  6.]])
data_array = ct.encrypt(data_array_plain)
res = data_array.get_encryption_type()
print(res)
# 输出 0
```
