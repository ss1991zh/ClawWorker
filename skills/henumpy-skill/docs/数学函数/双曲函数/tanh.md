# tanh

### 双曲正切函数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `tanh`： $ x $的双曲正切值 $ tanh(x)=\frac{e^x-e^{-x}}{e^x+e^{-x}} $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.tanh(x)
print(ct.decrypt(res))
# 输出  0.9999092042625947

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.tanh(a)
print(ct.decrypt(res))
# 输出 [0.46211716 0.29131261 0.99963186 0.09966799]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.tanh(A)
print(ct.decrypt(res))
# 输出 [[ 0.76159416  0.96402758  0.99505475]
#       [ 0.96402758 -0.99505475  0.9993293 ]
#       [ 0.99505475  0.76159416  0.9993293 ]]
```
