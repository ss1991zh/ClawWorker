# max

### 返回数组的最大值

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况下，使用平展输入。

## 返回值

标量密文 `max`：$ a $指定轴的最大值

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
res = hp.max(a)	
print(ct.decrypt(res))
# 输出 4.300000000000001

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.max(A)		
print(ct.decrypt(res))
# 输出 4.000000000000001

# 数组, axis=0
res = hp.max(A, axis=0)
print(ct.decrypt(res))
# 输出 [3. 2. 4.]
```
