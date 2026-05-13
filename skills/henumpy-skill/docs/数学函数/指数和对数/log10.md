# log10

### 以 10 为底的对数函数

## 参数

标量密文或数组密文

- `x`：输入元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `log10`：数组中所有元素以 10 为底的对数 $ log10(x)=\log_{10}x $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.log10(x)
print(ct.decrypt(res))
# 输出  0.6989700043360185

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.log10(a)
print(ct.decrypt(res))
# 输出 [-0.30103    -0.52287875  0.63346846 -1.        ]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.log10(A)
print(ct.decrypt(res))
# 输出 [[0.00000000e+00 3.01029996e-01 4.77121255e-01]
#       [3.01029996e-01            nan 6.02059991e-01]
#       [4.77121255e-01 3.50843249e-16 6.02059991e-01]]
```
