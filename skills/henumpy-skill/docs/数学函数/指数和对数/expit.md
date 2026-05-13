# expit

### 计算 sigmod 函数

## 参数

标量密文或数组密文

- `x`：输入元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `expit`：数组中所有元素的 sigmod 函数值 $ expit(x)=\frac{cc1}{cc1+exp(-x)} $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.expit(x)
print(ct.decrypt(res))
# 输出  0.9933071490757157

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.expit(a)
print(ct.decrypt(res))
# 输出 [0.62245933 0.57444252 0.98661308 0.52497919]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.expit(A)
print(ct.decrypt(res))
# 输出 [[0.73105858 0.88079708 0.95257413]
#       [0.88079708 0.04742587 0.98201379]
#       [0.95257413 0.73105858 0.98201379]]
```
