# nan_to_num

### 将 nan 替换为零，使用大的有限数替换 inf

## 参数

- `x`：标量密文或数组密文，输入元素
- `nan`：标量密文，可选 用于填充 NaN 值的值。如果未传递任何值，则 NaN 值将替换为 0.0。
- `posinf`：标量密文，可选 用于填充正无穷大值的值。如果未传递任何值，则正无穷大值将替换为非常大的数字。
- `neginf`：标量密文，可选 用于填充负无穷大值的值。如果未传递任何值，则负无穷大值将替换为非常小的数字。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `nan_to_num`：$ x $被全部替换为有效数值后的结果

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = hp.empty()		# nan
res = hp.nan_to_num(x)
print(ct.decrypt(res))
# 输出 9.999999999999999e-16

# 向量
aa_nan_inf = np.array([2.1, np.nan, 4.0, 5.2, np.inf])
a_nan_inf = ct.encrypt(aa_nan_inf)
res = hp.nan_to_num(a_nan_inf)
print(ct.decrypt(res))
# 输出 [2.10000000e+000 0.00000000e+000 4.00000000e+000 5.20000000e+000 4.98843893e+300]

# 向量, 指定替换数据
x1 = ct.encrypt(5)
res = hp.nan_to_num(a_nan_inf, posinf=x1)
print(ct.decrypt(res))
# 输出 [2.1 0.  4.  5.2 5. ]

# 数组
AA_nan_inf = np.array([[ 1.,  np.nan,  3.],[ np.inf, -3.,  4.],[ 3.,  1., np.nan]])
 = ct.encrypt(AA_nan_inf)
res = hp.nan_to_num(A_nan_inf)
print(ct.decrypt(res))
# 输出 [[ 1.00000000e+000  0.00000000e+000  3.00000000e+000]
#       [ 4.56094809e+300 -3.00000000e+000  4.00000000e+000]
#       [ 3.00000000e+000  1.00000000e+000  0.00000000e+000]]

# 数组, 指定替换数据
x2 = ct.encrypt(3)
res = hp.nan_to_num(A_nan_inf, nan=x1, posinf=x2)
print(ct.decrypt(res))
# 输出 [[ 1.  5.  3.]
#       [ 3. -3.  4.]
#		[ 3.  1.  5.]]
```
