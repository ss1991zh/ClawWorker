# nanmedian

### 沿指定轴计算中位数，忽略任何 NaN

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `nanmedian`：$ a $沿轴的中位数，忽略 NaN 值 给定长度为 n 的向量 a ，当 n 为奇数时，$ nanmedian(a) $是 a 的已排序副本的中间值，而当 n 为偶数时，$ nanmedian(a) $是两个中间值的平均值。

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1, np.nan])
a = ct.encrypt(aa)
res = hp.nanmedian(a)	
print(ct.decrypt(res))
# 输出 0.3999999999999999

# 数组
AA = np.array([[ 1.,  np.nan,  3.],[ 2., -3.,  4.],[ 3.,  1., np.nan]])
A = ct.encrypt(AA)
res = hp.nanmedian(A)		
print(ct.decrypt(res))
# 输出 2.000000000000001

# 数组, axis=0
res = hp.nanmedian(A, axis=0)
print(ct.decrypt(res))
# 输出 [ 2.  -1.   3.5]
```
