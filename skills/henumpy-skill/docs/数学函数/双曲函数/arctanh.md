# arctanh

### 反双曲正切函数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `arctanh`： $ x $的反双曲正切值 $ arctanh(x)=\frac{1}{2}\ln \frac{1+x}{1-x} $，$ x\in(-1,\ 1) $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(0.3)
res = hp.arctanh(x)
print(ct.decrypt(res))
# 输出  0.30951960420311303

# 向量
aa = np.array([0.5, 0.3])
a = ct.encrypt(aa)
res = hp.arctanh(a)
print(ct.decrypt(res))
# 输出 [0.54930614 0.3095196 ]

# 数组
AA = np.array([[0.04529455, 0.82642999, 0.39533218],
               [0.66946354, 0.60157516, 0.49374761],
               [0.16709517, 0.29711747, 0.60414683]])
A = ct.encrypt(AA)
res = hp.arctanh(A)
print(ct.decrypt(res))
# 输出 [[0.04532556 1.17676874 0.41810427]
#       [0.80977032 0.69561201 0.54100404]
#       [0.1686769  0.30635499 0.69965198]]
```
