# deg2rad

### 将角度从度数转换为弧度

## 参数

标量密文或数组密文

- `x`：以度为单位的角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `deg2rad`：相应的以弧度为单位的$ x $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5.0)
res = hp.deg2rad(x)
print(ct.decrypt(res))
# 输出 0.08726646259971649    

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.deg2rad(a)
print(ct.decrypt(res))
# 输出 [0.00872665 0.00523599 0.07504916 0.00174533]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.deg2rad(A)
print(ct.decrypt(res))
# 输出 [[ 0.01745329  0.03490659  0.05235988]
#       [ 0.03490659 -0.05235988  0.06981317]
#       [ 0.05235988  0.01745329  0.06981317]]
```
