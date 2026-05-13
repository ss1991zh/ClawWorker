# cbrt

### 返回输入元素的立方根

## 参数

标量密文或数组密文

- `x`：待求立方根的元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `cbrt`：$ x $的立方根

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.cbrt(x)
print(ct.decrypt(res))
# 输出  1.709975946676697

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.cbrt(a)
print(ct.decrypt(res))
# 输出 [0.79370053 0.66943295 1.62613333 0.46415888]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.cbrt(A)
print(ct.decrypt(res))
# 输出 [[ 1.          1.25992105  1.44224957]
#       [ 1.25992105 -1.44224957  1.58740105]
#       [ 1.44224957  1.          1.58740105]]
```
