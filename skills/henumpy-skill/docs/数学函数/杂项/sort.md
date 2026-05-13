# sort

### 对给定的数组的元素进行排序

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认情况 $ None $按行排序， $ axis=1 $按列排序
- `decrement`：布尔型，可选 排序方式，默认情况为 $ decrement=False $，返回升序排序， $ decrement=True $，返回降序排列
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `sort`：$ a $排序后的数组

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
res = hp.sort(a)
print(ct.decrypt(res))
# 输出 [0.1 0.3 0.5 4.3]

# 向量, 降序
res = hp.sort(a, True)
print(ct.decrypt(res))
# 输出 [0.1 0.3 0.5 4.3]

# 数组, 默认升序
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.sort(A)
print(ct.decrypt(res))
# 输出 [[ 1.  2.  3.]
#       [-3.  2.  4.]
#       [ 1.  3.  4.]]

# 数组, axis = 0
res = hp.sort(A, axis = 0)
print(ct.decrypt(res))
# 输出 [[ 1. -3.  3.]
#       [ 2.  1.  4.]
#       [ 3.  2.  4.]]
```
