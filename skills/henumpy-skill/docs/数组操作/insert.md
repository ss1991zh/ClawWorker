# insert

### 在数组的指定位置插入元素

## 参数

- `A`：数组密文 待插入的数组， $ m\times n $维数组
- `index`：整型 向数组中插入值的位置
- `values`：数组密文 往数组中插入的值
- `axis`： $ None $或整数，可选 要操作的轴，默认情况 $ None $按行插入， $ axis=1 $按列插入
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `insert`：向$ A $中插入$ values $后的数组

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 默认按行插入
AA = np.array([[ 1.,  2.],[ 2., -3.]])
A = ct.encrypt(AA)
aa = np.array([0.5, 0.3])
a = ct.encrypt(aa)
res = hp.insert(A, 1, a)
print(ct.decrypt(res))
# 输出 [[ 1.   2. ]
#       [ 0.5  0.3]
#       [ 2.  -3. ]]

# 按列插入
res = hp.insert(c1 = A, index = 1, c2 = a, axis = 1)
print(ct.decrypt(res))
# 输出 [[ 1.   0.5  2. ]
#       [ 2.   0.3 -3. ]]
```
