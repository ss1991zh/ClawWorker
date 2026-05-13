# square

### 返回输入元素的平方

## 参数

标量密文或数组密文

- `x`：待求平方的元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `square`：$ x $的平方

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.square(x)
print(ct.decrypt(res))
# 输出  24.999999999999996

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.square(a)
print(ct.decrypt(res))
# 输出 [2.500e-01 9.000e-02 1.849e+01 1.000e-02]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.square(A)
print(ct.decrypt(res))
# 输出 [[ 1.  4.  9.]
#       [ 4.  9. 16.]
#       [ 9.  1. 16.]]
```
