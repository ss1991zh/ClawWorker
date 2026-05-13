# percentile

### 沿着指定的轴计算数据的第$ q $个百分位数
百分位数是统计中使用的度量，表示小于这个值的观察值的百分比。第$ q $个百分位数是指它使得至少有$ q\% $的数据项小于或等于这个值，且至少有$ (100-q)\% $的数据项大于或等于这个值。 输入： `a`：数组密文，输入数组 `q`：浮点型标量明文，要计算的百分位数的百分比。值必须介于 0 和 100 之间（含 0 和 100） `axis`：$ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `percentile(a,q)`：$ a $的第$ q $个百分位数

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
q = 35
res = hp.percentile(a, q)	
print(ct.decrypt(res))
# 输出 0.3100000000000001

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.percentile(A, q)		
print(ct.decrypt(res))
# 输出 1.7999999999999994

# 数组, axis=0
res = hp.percentile(A, q, axis=0)
print(ct.decrypt(res))
# 输出 [ 1.7 -0.2  3.7]
```
