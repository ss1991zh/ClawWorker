# argsort

### 将数组进行排序，提取其在排列前对应的索引输出

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况 $ axis=1 $按行排序， $ axis=0 $按列排序
- `decrement`：布尔型，可选 排序方式，默认情况为 $ decrement=False $，返回升序排序， $ decrement=True $，返回降序排列

## 返回值

数组明文 `argsort`：$ a $排序前对应的下标

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量, 默认升序
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.argsort(a)
print(res)
# 输出 [3 1 0 2]

# 数组, 按列降序
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.argsort(A, axis=0, decrement=True)
print(res)
# 输出 [[2 0 1]
#		[1 2 2]
#		[0 1 0]]
```
