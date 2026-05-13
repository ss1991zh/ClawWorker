# hp.clip

将数组中的值限制在指定范围内。

## 签名

```python
hp.clip(a, a_min, a_max, output_encrypt_type=None)
```

## 参数

- `a`: 数组密文 — 待限制的数组
- `a_min`: 标量密文/数组密文 — 下限
- `a_max`: 标量密文/数组密文 — 上限
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

数组密文 — 值被裁剪后的数组。小于 `a_min` 的替换为 `a_min`，大于 `a_max` 的替换为 `a_max`。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量裁剪
x = ct.encrypt(5)
a_min = ct.encrypt(0.2)
a_max = ct.encrypt(3.1)
print(ct.decrypt(hp.clip(x, a_min, a_max)))
# 输出 3.1

# 向量裁剪（标量边界）
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
print(ct.decrypt(hp.clip(a, a_min, a_max)))
# 输出 [0.5 0.3 3.1 0.2]

# 向量裁剪（向量边界）
lo = ct.encrypt(np.array([0.6, 0.1, 3.2, 0.4]))
hi = ct.encrypt(np.array([0.8, 0.2, 4.1, 0.9]))
print(ct.decrypt(hp.clip(a, lo, hi)))
# 输出 [0.6 0.2 4.1 0.4]
```
