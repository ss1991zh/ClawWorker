# var

### 计算沿指定轴的方差
方差是与平均值的平方偏差的平均值

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `var`：$ a $沿指定轴的方差 $ var(a)=mean((a-mean(a))^2) $

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
res = hp.var(a)	
print(ct.decrypt(res))
# 输出 3.0199999999999974

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.var(A)		
print(ct.decrypt(res))
# 输出 4.098765432098767

# 数组, axis=0
res = hp.var(A, axis=0)
print(ct.decrypt(res))
# 输出 [0.66666667 4.66666667 0.22222222]
```
