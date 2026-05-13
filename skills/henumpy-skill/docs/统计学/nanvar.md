# nanvar

### 计算沿指定轴的方差，忽略任何 NaN
方差是与平均值的平方偏差的平均值

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `nanvar`：$ a $沿指定轴的方差，忽略 NaN 值 $ nanvar(a)=nanmean((a-nanmean(a))^2) $

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
res = hp.nanvar(a)	
print(ct.decrypt(res))
# 输出 3.019999999999999

# 数组
AA = np.array([[ 1.,  np.nan,  3.],[ 2., -3.,  4.],[ 3.,  1., np.nan]])
A = ct.encrypt(AA)
res = hp.nanvar(A)		
print(ct.decrypt(res))
# 输出 4.530612244897959

# 数组, axis=0
res = hp.nanvar(A, axis=0)
print(ct.decrypt(res))
# 输出 [0.66666667 4.         0.25      ]
```
