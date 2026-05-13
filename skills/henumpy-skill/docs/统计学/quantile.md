# quantile

### 沿着指定的轴计算数据的第$ q $个分位数
给定长度为$ n $的向量$ a $，$ a $的第$ q $个分位数是$ a $的排序副本中从最小值到最大值的第$ q $个。如果归一化排序与$ q $的位置不完全匹配，则通过两个最近邻居的值和距离确定分位数。如果$ q=0.5 $，此函数与中位数相同，如果$ q=0.0 $，此函数等于最小值，如果$ q=1.0 $，则此函数等于最大值。 输入： `a`：数组密文，输入数组 `q`：浮点型标量明文，要计算的分位数的概率。值必须介于 0 和 1 之间（含 0 和 1） `axis`：$ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `quantile(a,q)`：$ a $的第$ q $个分位数

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
q = 0.35
res = hp.quantile(a, q)	
print(ct.decrypt(res))
# 输出 0.3099999999999998

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.quantile(A, q)		
print(ct.decrypt(res))
# 输出 1.7999999999999998

# 数组, axis=0
res = hp.quantile(A, q, axis=0)
print(ct.decrypt(res))
# 输出 [ 1.7 -0.2  3.7]
```
