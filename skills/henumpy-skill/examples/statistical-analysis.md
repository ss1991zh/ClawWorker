# 示例：统计分析

在密文上计算均值、方差、标准差等统计量。

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))

# 求和
print(ct.decrypt(hp.sum(a)))          # 5.2
print(ct.decrypt(hp.sum(A)))          # 17.0
print(ct.decrypt(hp.sum(A, axis=0)))  # [6. 0. 11.]

# 均值
print(ct.decrypt(hp.mean(a)))         # 1.3
print(ct.decrypt(hp.mean(A, axis=0))) # [2. 0. 3.67]

# 方差和标准差
print(ct.decrypt(hp.var(a)))
print(ct.decrypt(hp.std(a)))

# 最值
print(ct.decrypt(hp.max(A)))
print(ct.decrypt(hp.min(A, axis=0)))

# 中位数和百分位数
print(ct.decrypt(hp.median(a)))
print(ct.decrypt(hp.percentile(a, 75)))

# 相关系数矩阵
x_data = ct.encrypt(np.random.randn(100))
y_data = ct.encrypt(np.random.randn(100))
stacked = hp.append(x_data.reshape(1, -1), y_data.reshape(1, -1), axis=0)
print(ct.decrypt(hp.corrcoef(stacked)))

# 忽略 NaN 的安全计算
data_with_nan = ct.encrypt(np.array([1.0, np.nan, 3.0, 4.0]))
print(ct.decrypt(hp.nanmean(data_with_nan)))
print(ct.decrypt(hp.nansum(data_with_nan)))
```
