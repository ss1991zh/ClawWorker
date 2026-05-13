# arcsin

### 反正弦函数

## 参数

标量密文或数组密文

- `x`：正弦值，定义域 [-1, 1]
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `arcsin`： $ x $所对应的角度，弧度制

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(0.3)
res = hp.arcsin(x)
print(ct.decrypt(res))
# 输出  0.3046926540153974  

# 向量
aa = np.array([0.5, 0.3])
a = ct.encrypt(aa)
res = hp.arcsin(a)
print(ct.decrypt(res))
# 输出 [0.52359878 0.30469265]

# 数组
AA = np.array([[0.04529455, 0.82642999, 0.39533218],
               [0.66946354, 0.60157516, 0.49374761],
               [0.16709517, 0.29711747, 0.60414683]])
A = ct.encrypt(AA)
res = hp.arcsin(A)
print(ct.decrypt(res))
# 输出 [[0.04531005 0.97273725 0.40642946]
#       [0.73348638 0.64547152 0.51639406]
#       [0.16788268 0.30167237 0.64869478]]
```
