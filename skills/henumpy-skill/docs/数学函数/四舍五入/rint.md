# rint

### 将输入元素舍入为最接近的整数（四舍六入五留双）

## 参数

标量密文或数组密文

- `x`：待舍入的元素
- `m`：整型，可选 五留双精度，默认 $ m=0 $
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `rint`：$ x $的舍入结果

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(1.145)
res = hp.round(x)		
print(ct.decrypt(res))
# 输出  1.0000000000000004

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.round(a)	
print(ct.decrypt(res))
# 输出 [-4.85439899e-16  3.64079924e-16  4.00000000e+00 -2.42719949e-16]

# 数组
AA = np.array([[6.42928142, 9.77273297, 4.93308361],
               [3.19938589, 6.71818304, 7.02042517],
               [8.82960339, 3.42430176, 7.42846012]])
A = ct.encrypt(AA)
res = hp.round(A)		
print(ct.decrypt(res))
# 输出 [[ 6. 10.  5.]
#       [ 3.  7.  7.]
#       [ 9.  3.  7.]]
```
