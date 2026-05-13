# 加解密基础操作

演示 `crypto_toolkit` 对数值数组与 CSV 文件的加解密；与 `henumpy` 同态字典初始化配合使用。

## 完整示例

```python
import os

import crypto_toolkit as ct
import henumpy as hp
import numpy as np

hp.initDict()
ct.initSK()

# ---------- 数值数组 ----------
# 单值加密
a = 5
A = ct.encrypt_ndarray(a)
print("解密:", ct.decrypt_ndarray(A))  # 5.0

# 二维数组 — 按行加密
x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
X = ct.encrypt_ndarray(x)
print("按行解密:", ct.decrypt_ndarray(X))

# 二维数组 — 按列加密
X_col = ct.encrypt_ndarray(x, encrypt_by_column=True)
print("按列解密:", ct.decrypt_ndarray(X_col, decrypt_by_column=True))

# 离散形式加密
X_disc = ct.encrypt_ndarray(x, discrete=True)
print("离散解密:", ct.decrypt_ndarray(X_disc, discrete=True))

# ---------- CSV 文件（运行前生成示例输入文件）----------
with open("input.csv", "w", encoding="utf-8") as f:
    f.write("col1,col2,col3\n1.0,2.0,3.0\n4.0,5.0,6.0\n")

ct.encrypt_csv("input.csv", "encrypted.csv", encrypt_by_column=True)
ct.decrypt_csv("encrypted.csv", "decrypted.csv", decrypt_by_column=True)

for name in ("input.csv", "encrypted.csv", "decrypted.csv"):
    if os.path.isfile(name):
        os.remove(name)
```

## 加密模式说明

| 模式 | 参数 | 适用场景 |
|------|------|----------|
| 按行加密 | `encrypt_by_column=False` | 列维度不变，行维度变化 |
| 按列加密 | `encrypt_by_column=True` | 行维度不变，列维度变化 |
| 连续形式 | `discrete=False` | 数组元素批量运算，有加速效果 |
| 离散形式 | `discrete=True` | 元素独立运算或频繁变更值 |
