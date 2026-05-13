# log2

### 以 2 为底的对数函数

## 参数

标量密文或数组密文

- `x`：输入元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `log2`：数组中所有元素以 2 为底的对数 $ log2(x)=\log_{2}x $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.log2(x)
print(ct.decrypt(res))
# 输出  2.321928094887363

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.log2(a)
print(ct.decrypt(res))
# 输出 [-1.         -1.73696559  2.10433666 -3.32192809]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.log2(A)
print(ct.decrypt(res))
# 输出 [[2.50404895e-15 1.00000000e+00 1.58496250e+00]
#       [1.00000000e+00            nan 2.00000000e+00]
#       [1.58496250e+00 1.88111102e-11 2.00000000e+00]]
```
