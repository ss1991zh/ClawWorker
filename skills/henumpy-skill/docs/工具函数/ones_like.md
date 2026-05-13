# hp.ones_like

创建与输入数组形状相同的全 1 密文数组。

## 签名

```python
hp.ones_like(a, output_encrypt_type=None)
```

## 参数

- `a`: 数组密文 — 参考数组（用于确定输出形状）
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

数组密文 — 与 `a` 形状相同的全 1 密文数组。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
res = hp.ones_like(A)
print(ct.decrypt(res))
# 输出 [[1. 1. 1.]
#       [1. 1. 1.]
#       [1. 1. 1.]]
```
