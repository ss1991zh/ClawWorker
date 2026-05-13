# reciprocal

### 返回输入元素的倒数

## 参数

标量密文或数组密文

`x`：待求倒数的元素

`output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定$ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若$ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `reciprocal`：$ x $的倒数

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.reciprocal(x)		
print(ct.decrypt(res))
# 输出  0.20000000000000004

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.reciprocal(a)		
print(ct.decrypt(res))
# 输出 [ 2.          3.33333333  0.23255814 10.        ]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.reciprocal(A)		
print(ct.decrypt(res))
# 输出 [[ 1.          0.5         0.33333333]
#       [ 0.5        -0.33333333  0.25      ]
#       [ 0.33333333  1.          0.25      ]]
```
