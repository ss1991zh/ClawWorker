# trunc

### 返回输入元素的截断值

## 参数

标量密文或数组密文

- `x`：待舍入的元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `trunc`：$ x $的舍入结果

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(10.123)
res = hp.trunc(x)		
print(ct.decrypt(res))
# 输出  9.999999999999982

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.trunc(a)	
print(ct.decrypt(res))
# 输出 [-1.07134820e-15 -3.21404461e-16  4.00000000e+00 -2.94620756e-16]

# 数组
AA = np.array([[6.42928142, 9.77273297, 4.93308361],
               [3.19938589, 6.71818304, 7.02042517],
               [8.82960339, 3.42430176, 7.42846012]])
A = ct.encrypt(AA)
res = hp.trunc(A)		
print(ct.decrypt(res))
# 输出 [[6. 9. 4.]
#       [3. 6. 7.]
#       [8. 3. 7.]]
```
