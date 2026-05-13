# zeros_like

### 创建与输入数组形状相同的全 0 密文数组

## 参数

- `a`：数组密文，输入数组
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `zeros_like`： 与输入数组形状相同的全 0 密文数组 A 为 m×n 维数组 $ {\mathop{{zeros\_like(A)}}\nolimits={ \left[ {\begin{array}{*{20}{c}}
{\mathop{{cc0}}\nolimits}&{\mathop{{cc0}}\nolimits}&{ \cdots }&{\mathop{{cc0}}\nolimits}\\
{\mathop{{cc0}}\nolimits}&{\mathop{{cc0}}\nolimits}&{ \cdots }&{\mathop{{cc0}}\nolimits}\\
{ \vdots }&{ \vdots }&{ \ddots }&{ \vdots }\\
{\mathop{{cc0}}\nolimits}&{\mathop{{cc0}}\nolimits}&{ \cdots }&{\mathop{{cc0}}\nolimits}
\end{array}} \right] }} _{{m \times n}} $

注：cc0为 0 的密文，随计算字典的不同而改变

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.zeros_like(A)
print(ct.decrypt(res))
# 输出 [[1.e-15 1.e-15 1.e-15]
#       [1.e-15 1.e-15 1.e-15]
#       [1.e-15 1.e-15 1.e-15]]
```
