# random.rand

### 随机生成一个给定形状的数组，其中每一个元素值在 0-1 之间

## 参数

- `n`：整型，数组的列数
- `m`：整型，可选 数组的行数，默认 m=1
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `random.rand`： 给定形状的数组，其中每一个元素值在 0-1 之间 $ \mathop{{random.rand(m,\ n)}}\nolimits={ \left[ {\begin{array}{*{20}{c}}
{\mathop{{a}}\nolimits_{{11}}}&{\mathop{{a}}\nolimits_{{12}}}&{ \cdots }&{\mathop{{a}}\nolimits_{{1n}}}\\
{\mathop{{a}}\nolimits_{{21}}}&{\mathop{{a}}\nolimits_{{22}}}&{ \cdots }&{\mathop{{a}}\nolimits_{{2n}}}\\
{ \vdots }&{ \vdots }&{ \ddots }&{ \vdots }\\
{\mathop{{a}}\nolimits_{{m1}}}&{\mathop{{a}}\nolimits_{{m2}}}&{ \cdots }&{\mathop{{a}}\nolimits_{{mn}}}
\end{array}} \right] } $，$ a_{ij}\in [cc0,\ cc1] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 创建随机密文向量
res = hp.random.rand(3)
print(ct.decrypt(res))
# 输出 [0.14328851 0.82226388 0.0219831 ]

# 创建随机密文数组
res = hp.random.rand(3, 3)
print(ct.decrypt(res))
# 输出 [[0.01887148 0.01215568 0.49147331]
#       [0.8374955  0.24036332 0.40615997]
#       [0.03287072 0.15305552 0.63741653]]
```
