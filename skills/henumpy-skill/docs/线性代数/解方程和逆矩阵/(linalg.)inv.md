# (linalg.)inv

### 求矩阵的逆矩阵

## 参数

矩阵密文

- `A`：输入元素， $ n\times n $维方阵
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

矩阵密文 `inv`：$ A $的逆矩阵

> **备注**: .I 运算符可以用作 hp.inv 的简写

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.inv(A)     # 等价于 res = A.I
print(ct.decrypt(res))
# 输出 [[-0.64 -0.2   0.68]
#       [ 0.16 -0.2   0.08]
#       [ 0.44  0.2  -0.28]]
```
