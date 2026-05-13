# expm1

### 计算所有元素的$ e^x-1 $ 输入：标量密文或数组密文 `x`：输入元素 `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定$ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若$ output\_encrypt\_type=1 $，则返回的为列加密形式。 输出：标量密文或数组密文 `expm1`：数组中所有元素的$ e^x-1 $ $ expm1(x)=e^x-1 $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.expm1(x)
print(ct.decrypt(res))
# 输出  147.41315910257578

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.expm1(a)
print(ct.decrypt(res))
# 输出 [ 0.64872127  0.34985881 72.6997937   0.10517092]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.expm1(A)
print(ct.decrypt(res))
# 输出 [[ 1.71828183  6.3890561  19.08553692]
#       [ 6.3890561  -0.95021293 53.59815003]
#       [19.08553692  1.71828183 53.59815003]]
```
