# (linalg.)matrix_power

### 将方阵提高到（整数）幂 n

## 参数

- `A`：矩阵密文，输入元素， $ M\times M $维方阵
- `n`：标量明文，整型，指数
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

矩阵密文 `(linalg.)matrix_power`：$ A $的$ n $次幂 + $ n $为正整数 $ (linalg.)matrix\_power(A,\ n)=\underbrace{A*A*\dots*A}_n $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 矩阵
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.linalg.matrix_power(A, 3)
print(ct.decrypt(res))
# 输出 [[ 81.  54. 130.]
#       [ 72. -25. 132.]
#       [118.  42. 195.]]
```
