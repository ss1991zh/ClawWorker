# vander

## 参数

- `x`：数组密文，输入数组 输入的一维数组，用作构建范德蒙德矩阵的向量。
- `N`： $ None $或整数，可选 可选参数，指定生成的范德蒙德矩阵的列数（默认为 len(x)）。
- `increasing`：布尔型，可选 可选参数，控制每一行的幂次顺序是否递增（默认为 False）.
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

矩阵密文 `vander`：根据参数 x、N 和 increasing 生成的范德蒙德矩阵，其中矩阵的每一列是输入向量的幂。

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

xx = np.array([0.5, 0.3, 4.3, 0.1])
x = ct.encrypt(xx)
res = hp.vander(x, 3)
print(ct.decrypt(res))
# 输出 [[2.500e-01 5.000e-01 1.000e+00]
#       [9.000e-02 3.000e-01 1.000e+00]
#       [1.849e+01 4.300e+00 1.000e+00]
#       [1.000e-02 1.000e-01 1.000e+00]]
```
