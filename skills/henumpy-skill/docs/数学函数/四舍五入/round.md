# round

### 将输入元素舍入到给定的小数位数（四舍六入五留双）

## 参数

标量密文或数组密文

- `x`：待舍入的元素
- `n`：整型，可选 舍入到的小数位数，默认舍入为整数，即 $ n=0 $
- `m`：整型，可选 五留双精度，默认 $ m=12-n $
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `round`：$ x $的舍入结果

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量, n = 2
x = ct.encrypt(1.145)
res = hp.round(x, 2)		
print(ct.decrypt(res))
# 输出  1.149999999999998

# 标量, n = 2, m = 2
res = hp.round(x, 2, 2)
print(ct.decrypt(res))
# 输出  1.1399999999999977

# 向量, n = 2, m = 2
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.round(a, 2, 2)	
print(ct.decrypt(res))
# 输出 [0.5 0.3 4.3 0.1]

# 数组, n = 1, 即舍入到小数点后第一位
AA = np.array([[6.42928142, 9.77273297, 4.93308361],
               [3.19938589, 6.71818304, 7.02042517],
               [8.82960339, 3.42430176, 7.42846012]])
A = ct.encrypt(AA)
res = hp.round(A, 1)		
print(ct.decrypt(res))
# 输出 [[6.4 9.8 4.9]
#       [3.2 6.7 7. ]
#       [8.8 3.4 7.4]]
```
