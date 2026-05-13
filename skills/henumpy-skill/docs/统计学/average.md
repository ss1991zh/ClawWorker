# average

### 计算沿指定轴的加权平均

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 计算加权平均的 $ a $的轴。默认值 $ axis=None $将平均输入数组的所有元素。
- `weights`：数组密文或明文，可选 与 $ a $中的值关联的权重数组。 $ a $中的每个值都根据其关联的权重贡献平均值。权重数组可以是一维（在这种情况下，其长度必须是沿给定轴的 $ a $的大小）或与 $ a $的形状相同。如果 $ weights=None $，则假定 $ a $中的所有数据的权重都等于 1。

## 返回值

标量密文 `average`：$ a $沿指定轴的加权平均 $ average(a,\ weights)=\frac{sum(a*weights)}{sum(weights)} $ 当$ sum(weights)=0 $时，$ average(a,\ weights)=nan $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量, 默认权重
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.average(a)
print(ct.decrypt(res))
# 输出 1.3000000000000003

# 向量, 给定权重
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)	
res = hp.average(a, b)		# 等价于 res = hp.average(a, bb) 
print(ct.decrypt(res))
# 输出 0.5532818532818533

# 数组, 默认权重
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.average(A)
print(ct.decrypt(res))
# 输出 1.8888888888888884

# A 为数组, axis=0, 给定权重 weights 为数组
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.average(A, B, axis=0)		# 等价于 res = hp.average(A, BB, axis=0) 
print(ct.decrypt(res))
# 输出 [ 1.86363636 -0.64948454  5.11111111]

# A 为数组, axis=1, 给定权重 weights 为向量
xx = np.array([0.5, 0.3, 4.3])
x = ct.encrypt(xx)
res = hp.average(A, weight=x, axis=1)
print(ct.decrypt(res))
# 输出 [2.74509804 3.39215686 3.7254902 ]
```
