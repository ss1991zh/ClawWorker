# unwrap

### 通过将值之间的差值更改为$ 2\pi $补码来展开(平移相位角) 每当连续相位角之间的跳跃大于$ discont $时，$ unwrap $就会通过增加$ 2\pi $的整数倍来平移相位角，直到跳跃小于$ discont $。 输入： `x`：数组密文，输入数组 `discont`：None 或整数，可选 值之间的最大不连续性，默认为$ \pi $，用户自定义$ discont $需大于 $ \pi $。 `axis`：None 或整数，可选 要操作的轴，默认为最后一个轴。 `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定$ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若$ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `unwrap`：平移相位角后的$ x $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK() 

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.unwrap(a)
print(ct.decrypt(res))
# 输出 [ 0.5         0.3        -1.98318531  0.1       ]

# 数组
AA = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
A = ct.encrypt(AA)
res = hp.unwrap(A)
print(ct.decrypt(res))
# 输出 [[ 0.5        -2.28318531 -4.28318531]
# 		[ 4.          5.          6.56637061]
#		[-0.1         0.7         2.2       ]]

# 数组, 指定discont和axis
BB = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
B = ct.encrypt(BB)
res = hp.unwrap(B, discont=4, axis=0)
print(ct.decrypt(res))
# 输出 [[1.         2.         3.        ]
#       [2.         3.28318531 4.        ]
#       [3.         1.         4.        ]]
```
