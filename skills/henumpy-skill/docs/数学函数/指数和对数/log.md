# log

### 自然对数

## 参数

标量密文或数组密文

- `x`：待求自然对数的元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `log`：数组中所有元素的自然对数 $ log(x)=ln \ x $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.log(x)
print(ct.decrypt(res))
# 输出  1.609437912434101

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.log(a)
print(ct.decrypt(res))
# 输出 [-0.69314718 -1.2039728   1.45861502 -2.30258509]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.log(A)
print(ct.decrypt(res))
# 输出 [[4.94961759e-16 6.93147181e-01 1.09861229e+00]
#       [6.93147181e-01            nan 1.38629436e+00]
#       [1.09861229e+00 2.31755161e-15 1.38629436e+00]]
```
