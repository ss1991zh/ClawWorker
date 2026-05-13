# median

### 沿指定轴计算中位数

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `median`：$ a $沿轴的中位数 给定长度为 n 的向量 a ，当 n 为奇数时，$ median(a) $是 a 的已排序副本的中间值，而当 n 为偶数时，$ median(a) $是两个中间值的平均值。

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
res = hp.median(a)	
print(ct.decrypt(res))
# 输出 0.39999999999999997

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.median(A)		
print(ct.decrypt(res))
# 输出 2.000000000000001

# 数组, axis=0
res = hp.median(A, axis=0)
print(ct.decrypt(res))
# 输出 [2. 1. 4.]
```
