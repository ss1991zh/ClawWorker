# flip

### 沿着指定轴翻转数组元素的顺序

## 参数

- `a`：数组密文，输入数组
- `axis`： $ None $或整数，可选 要操作的轴，默认为 None

## 返回值

数组密文 `flip`：$ a $沿指定轴翻转后的数组

+ 一维数组

[1, 2, 3] →  [3, 2, 1]

+ 二维数组
    1. 不指定轴

[[1 2 3]          [[9 8 7]

 [4 5 6]    →    [6 5 4]

 [7 8 9]]          [3 2 1]]

    2. axis = 1

[[1 2 3]          [[3 2 1]

 [4 5 6]    →    [6 5 4]

 [7 8 9]]          [9 8 7]]

    3. axis = 0

[[1 2 3]          [[7 8 9]

 [4 5 6]    →    [4 5 6]

 [7 8 9]]          [1 2 3]]

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
res = hp.flip(a)
print(ct.decrypt(res))
# 输出 [0.1 4.3 0.3 0.5]

# 数组, 不指定轴
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.flip(A)
print(ct.decrypt(res))
# 输出 [[ 4.  1.  3.]
#       [ 4. -3.  2.]
#       [ 3.  2.  1.]]

# 数组, axis = 1
res = hp.flip(A, 1)
print(ct.decrypt(res))
# 输出 [[ 3.  2.  1.]
#       [ 4. -3.  2.]
#       [ 4.  1.  3.]]

# 数组, axis = 0
res = hp.flip(A, 0)
print(ct.decrypt(res))
# 输出 [[ 3.  1.  4.]
#       [ 2. -3.  4.]
#       [ 1.  2.  3.]]
```
