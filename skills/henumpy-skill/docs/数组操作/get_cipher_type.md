# a.get_cipher_type

获取密文对象的类型。

## 签名

```python
a.get_cipher_type()
```

## 参数

- `a`: 密文对象 — 需要查询类型的密文

## 返回值

int (明文)：
- `1` = 标量密文
- `2` = 数组密文（连续）
- `3` = 离散数组密文

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量密文
x = ct.encrypt(5.0)
print(x.get_cipher_type())
# 输出 1

# 数组密文
arr = ct.encrypt(np.array([[1., 2., 3.], [4., 5., 6.]]))
print(arr.get_cipher_type())
# 输出 2

# 离散数组密文
discrete_arr = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]), discrete=True)
print(discrete_arr.get_cipher_type())
# 输出 3
```
