# degrees

### 将角度从弧度转换为度数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `degrees`：相应的以度为单位的$ x $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5.0)
res = hp.degrees(x)
print(ct.decrypt(res))
# 输出 286.4788975654116    

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.degrees(a)
print(ct.decrypt(res))
# 输出 [ 28.64788976  17.18873385 246.37185191   5.72957795]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.degrees(A)
print(ct.decrypt(res))
# 输出 [[  57.29577951  114.59155903  171.88733854]
#       [ 114.59155903 -171.88733854  229.18311805]
#       [ 171.88733854   57.29577951  229.18311805]]
```
