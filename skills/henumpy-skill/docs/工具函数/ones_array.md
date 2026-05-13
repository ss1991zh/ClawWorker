# ones_array

### 创建给定形状的全 1 密文数组

## 参数

- `n`：整型，数组的列数
- `m`：整型，可选 数组的行数，默认 m=1
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `ones_array`： 给定形状的全 1 密文数组 $ {\mathop{{ones\_array(m, \ n)}}\nolimits={ \left[ {\begin{array}{*{20}{c}}
{\mathop{{cc1}}\nolimits}&{\mathop{{cc1}}\nolimits}&{ \cdots }&{\mathop{{cc1}}\nolimits}\\
{\mathop{{cc1}}\nolimits}&{\mathop{{cc1}}\nolimits}&{ \cdots }&{\mathop{{cc1}}\nolimits}\\
{ \vdots }&{ \vdots }&{ \ddots }&{ \vdots }\\
{\mathop{{cc1}}\nolimits}&{\mathop{{cc1}}\nolimits}&{ \cdots }&{\mathop{{cc1}}\nolimits}
\end{array}} \right] }} _{{m \times n}} $

注：cc1为 1 的密文，随计算字典的不同而改变

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 向量
res = hp.ones_array(3)
print(ct.decrypt(res))
# 输出 [1. 1. 1.]

# 数组
res = hp.ones_array(2, 3)
print(ct.decrypt(res))
# 输出 [[1. 1. 1.]
#       [1. 1. 1.]]
```
