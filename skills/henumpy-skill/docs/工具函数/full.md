# full

### 根据指定的形状、数据类型和填充值来创建数组

## 参数

- `shape`：整型，指定输出数组的形状，可以是一个整数、元组或列表，表示数组的维度大小。
- `fill_value`：密文标量，指定填充数组的元素值。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `full`：给定形状和填充值的密文数组

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

x1 = ct.encrypt(5.0)
res = hp.full((2, 2), x1)
print(ct.decrypt(res))
# 输出 [[5. 5.]
#		[5. 5.]]
```
