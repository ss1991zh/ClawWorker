# sinh

### 双曲正弦函数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `sinh`： $ x $的双曲正弦值 $ sinh(x)=\frac{e^x-e^{-x}}{2} $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.sinh(x)
print(ct.decrypt(res))
# 输出  74.20321057778862

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.sinh(a)
print(ct.decrypt(res))
# 输出 [ 0.52109531  0.30452029 36.84311257  0.10016675]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.sinh(A)
print(ct.decrypt(res))
# 输出 [[  1.17520119   3.62686041  10.01787493]
#       [  3.62686041 -10.01787493  27.2899172 ]
#       [ 10.01787493   1.17520119  27.2899172 ]]
```
