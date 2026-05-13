# arcsinh

### 反双曲正弦函数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `arcsinh`： $ x $的反双曲正弦值 $ arcsinh(x)=\ln(x+\sqrt{x^2+1}) $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.arcsinh(x)
print(ct.decrypt(res))
# 输出  2.3124383412727556

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.arcsinh(a)
print(ct.decrypt(res))
# 输出 [0.48121183 0.29567305 2.16501676 0.09983408]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.arcsinh(A)
print(ct.decrypt(res))
# 输出 [[ 0.88137359  1.44363548  1.81844646]
#       [ 1.44363548 -1.81844646  2.09471255]
#       [ 1.81844646  0.88137359  2.09471255]]
```
