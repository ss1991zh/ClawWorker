# float_power

### 浮点型幂运算

## 参数

- `x`：标量密文或数组密文，底数 `alpha`：标量明文，浮点型，指数
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `float_power`：$ x $的$ \alpha $次幂，即$ float\_power(x,\ \alpha)=x^{\alpha} $

> **备注**: ** 运算符可以用作 hp.float_power 的简写

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.float_power(x, 2.2)		# 等价于 res = x**2.2
print(ct.decrypt(res))
# 输出  34.49324153653046

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.float_power(a, 1.7)		# 等价于 res = a**1.7
print(ct.decrypt(res))
# 输出 [ 0.3077861   0.12915349 11.93703245  0.01995262]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.float_power(A, 3.4)		# 等价于 res = A**3.4
print(ct.decrypt(res))
# 输出 [[  1.          10.55606329  41.8998305 ]
#       [ 10.55606329          nan 111.4304721 ]
#       [ 41.8998305    1.         111.4304721 ]]
```
