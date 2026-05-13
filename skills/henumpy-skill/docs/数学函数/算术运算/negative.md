# negative

### 对输入元素做负数计算

## 参数

标量密文或数组密文

- `x`：待做负数运算的元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `negative`： $ x $负数运算的结果

> **备注**: - 运算符可以用作 hp.negative 的简写

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.negative(x)		# 等价于 res = -x
print(ct.decrypt(res))
# 输出  -4.999999999999999

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)  
res = hp.negative(a)		# 等价于 res = -a
print(ct.decrypt(res))
# 输出 [-0.5 -0.3 -4.3 -0.1]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.negative(A)		# 等价于 res = -A
print(ct.decrypt(res))
# 输出 [[-1. -2. -3.]
#       [-2.  3. -4.]
#       [-3. -1. -4.]]
```
