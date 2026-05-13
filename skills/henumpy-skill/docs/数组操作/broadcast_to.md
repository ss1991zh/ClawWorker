# broadcast_to

### 将数组广播到新的形状

## 参数

- `A`： 数组密文，要广播的数组
- `shape`：整数，目标数组的形状。 若提供单个整数 `i`，将被解释为 `(i,)`。
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `broadcast_to`： 一个具有指定形状的原始数组的只读视图。此数组通常是非连续的。此外，广播后的数组中可能有多个元素引用同一内存位置。

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.broadcast_to(a, (3, 4))
print(ct.decrypt(res))
# 输出 [[0.5 0.3 4.3 0.1]
#		[0.5 0.3 4.3 0.1]
#		[0.5 0.3 4.3 0.1]]
```
