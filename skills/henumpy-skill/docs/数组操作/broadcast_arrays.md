# broadcast_arrays

### 将两个数组进行广播，使它们对齐到兼容的形状

## 参数

标量密文或数组密文

- `a`：第一个输入元素
- `b`：第二个输入元素
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `broadcast_arrays`： 一个由数组组成的 `tuple`。

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

xx = np.array([[1,2,3]])
x = ct.encrypt(xx)
yy = np.array([[4],[5]])
y = ct.encrypt(yy)
res = hp.broadcast_arrays(x, y)
print(ct.decrypt(res))
# 输出	(array([[1., 2., 3.],
#               [1., 2., 3.]]), 
#		 array([[4., 4., 4.],
#       		[5., 5., 5.]]))
```
