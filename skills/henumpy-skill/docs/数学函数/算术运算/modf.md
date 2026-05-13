# modf

### 返回输入元素的小数和整数部分

## 参数

标量密文或数组密文

`x`：输入元素

`output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定$ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若$ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

元组密文 $ modf(x)=(out1,\ out2) $ `out1`：数组密文，$ x $的小数部分 `out2`：数组密文，$ x $的整数部分

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(10.123)
res = hp.modf(x)		
print(ct.decrypt(res))
# 输出  (array(0.123), array(10.))

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.modf(a)		
print(ct.decrypt(res))
# 输出 (array([0.5, 0.3, 0.3, 0.1]), array([ 2.54293423e-16,  2.54293423e-16,  4.00000000e+00, -6.03946880e-16]))

# 数组
AA = np.array([[6.42928142, 9.77273297, 4.93308361],
               [3.19938589, 6.71818304, 7.02042517],
               [8.82960339, 3.42430176, 7.42846012]])
A = ct.encrypt(AA)
res = hp.modf(A)		
print(ct.decrypt(res))
# 输出 (array([[0.42928142, 0.77273297, 0.93308361],
#              [0.19938589, 0.71818304, 0.02042517],
#              [0.82960339, 0.42430176, 0.42846012]]),
#       array([[6., 9., 4.],
#              [3., 6., 7.],
#              [8., 3., 7.]]))
```
