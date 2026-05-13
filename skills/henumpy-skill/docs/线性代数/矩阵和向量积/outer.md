# outer

### 计算两个向量的外积

## 参数

- `a`：数组密文，第一个输入元素， $ 1\times M $维。如果输入不是 1 维输入，则平展。
- `b`：数组密文，第二个输入元素， $ 1\times N $维。如果输入不是 1 维输入，则平展。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

矩阵密文 `outer`：$ a $和$ b $的外积 $ {\mathop{{outer(a,b)}}\nolimits={ \left[ {\begin{array}{*{20}{c}}
{\mathop{{a_o*b_0}}\nolimits}&{\mathop{{a_o*b_1}}\nolimits}&{ \cdots }&{\mathop{{a_o*b_{N-1} }}\nolimits}\\
{\mathop{{a_1*b_0}}\nolimits}&{\mathop{{a_1*b_1}}\nolimits}&{ \cdots }&{\mathop{{a_1*b_{N-1} }}\nolimits}\\
{ \vdots }&{ \vdots }&{ \ddots }&{ \vdots }\\
{\mathop{{a_{M-1}*b_0}}\nolimits}&{\mathop{{a_{M-1}*b_1}}\nolimits}&{ \cdots }&{\mathop{{a_{M-1}*b_{N-1} }}\nolimits}
\end{array}} \right] }} _{{M \times N}} $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量和向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.outer(a, b)
print(ct.decrypt(res))
# 输出 [[  1.05   2.     2.6   20.25]
#       [  0.63   1.2    1.56  12.15]
#       [  9.03  17.2   22.36 174.15]
#       [  0.21   0.4    0.52   4.05]]
```
