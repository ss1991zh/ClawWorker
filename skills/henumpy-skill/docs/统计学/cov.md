# cov

### 返回估计协方差矩阵
协方差表示两个变量一起变化的水平。

## 参数

`A`：数组密文 包含多个变量和观测值的二维数组。每行$ a
 $代表一个变量，每列代表所有这些变量的单个观察。

- `B`：数组密文，可选 一组额外的变量和观测值。 $ B $与 $ A $具有相同的形状。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

矩阵密文 `cov`：$ A $和$ B $的估计协方差矩阵 $ cov(A,\ B)=\frac{\sum{(A-\bar{A})(B-\bar{B})}}{n-1} $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa, discrete=True)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb, discrete=True)
res = hp.cosine(a, b)
print(ct.decrypt(res)) 
# 输出 [[  4.02666667 -12.89333333]
#		[-12.89333333 338.96333333]]

# 数组
AA = np.array([[ 1.,  2.],[ 2., -3.]])
A = ct.encrypt(AA)
BB = np.array([[ 0.5,  4.],[ 4., 5.],])
B = ct.encrypt(BB)
res = hp.cov(A, B)
print(ct.decrypt(res))
# 输出 [[ 0.5   -2.5    1.75   0.5  ]
#       [-2.5   12.5   -8.75  -2.5  ]
#       [ 1.75  -8.75   6.125  1.75 ]
#       [ 0.5   -2.5    1.75   0.5  ]]
```
