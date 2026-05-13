# arctan

### 反正切函数

## 参数

标量密文或数组密文

- `x`：正切值
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `arctan`：$ x $所对应的角度，弧度制

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5)
res = hp.arctan(x)
print(ct.decrypt(res))
# 输出  1.3734007669450157

# 验证 tan(res) = x
print(ct.decrypt(hp.tan(res)))
# 输出 5.000000000000016

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.arctan(a)
print(ct.decrypt(res))
# 输出 [0.46364761 0.29145679 1.34229969 0.09966865]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.arctan(A)
print(ct.decrypt(res))
# 输出 [[ 0.78539816  1.10714872  1.24904577]
#       [ 1.10714872 -1.24904577  1.32581766]
#       [ 1.24904577  0.78539816  1.32581766]]
```
