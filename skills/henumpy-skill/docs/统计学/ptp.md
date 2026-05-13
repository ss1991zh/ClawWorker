# ptp

### 沿轴的值的范围

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `ptp`：$ a $沿轴的值的范围 $ ptp(a)=max(a)-min(a) $

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
res = hp.ptp(a)	
print(ct.decrypt(res))
# 输出 4.199999999999999

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.ptp(A)		
print(ct.decrypt(res))
# 输出 7.0

# 数组, axis=0
res = hp.ptp(A, axis=0)
print(ct.decrypt(res))
# 输出 [2. 5. 1.]
```
