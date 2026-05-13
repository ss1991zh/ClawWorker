# arccosh

### 反双曲余弦函数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `arccosh`： $ x $的反双曲余弦值 $ arccosh(x)=\ln(x+\sqrt{x^2-1}) $，$ x\in[1,\  +\infty) $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.arccosh(x)
print(ct.decrypt(res))
# 输出  2.292431669561179

# 向量
aa = np.array([2.1, 4.0, 5.2, 40.5])
a = ct.encrypt(aa)
res = hp.arccosh(a)
print(ct.decrypt(res))
# 输出 [1.37285914 2.06343707 2.33242932 4.3942967 ]

# 数组
AA = np.array([[6.42928142, 9.77273297, 4.93308361],
               [3.19938589, 6.71818304, 7.02042517],
               [8.82960339, 3.42430176, 7.42846012]])
A = ct.encrypt(AA)
res = hp.arccosh(A)
print(ct.decrypt(res))
# 输出 [[2.54790629 2.97011537 2.27867629]
#       [1.83073596 2.59237926 2.63685953]
#       [2.86803505 1.90200826 2.6939042 ]]
```
