# 示例：CipherDataFrame/CipherSeries 创建与基本操作

从 ndarray 或 CipherArray 构建加密 DataFrame，并进行基本查看操作。

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import numpy as np
import pandas as pd

hp.initDict()
ct.initSK()

# ── 方式一：先用 pandas 创建 DataFrame，再加密 ──
df = pd.DataFrame(
    np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    columns=['a', 'b', 'c']
)
cipher_df = ct.encrypt_df(df)
print(ct.decrypt_df(cipher_df))
#      a    b    c
# 0  1.0  2.0  3.0
# 1  4.0  5.0  6.0
# 2  7.0  8.0  9.0

# ── 方式二：从 CipherArray 直接构造 CipherDataFrame ──
A = np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]])
cipher_A = ct.encrypt(A, encrypt_by_column=True)
df2 = ps.CipherDataFrame(data=cipher_A, columns=['A', 'B', 'C'])
print(ct.decrypt_df(df2))
#      A    B    C
# 0  1.0  2.0  3.0
# 1  2.0 -3.0  4.0
# 2  3.0  1.0  4.0

# ── CipherSeries ──
s = pd.Series([1, 2, 3, 4, 5], index=["r1", "r2", "r3", "r4", "r5"])
cs = ct.encrypt_df(s)
print(ct.decrypt_df(cs))
# r1    1.0
# r2    2.0
# r3    3.0
# r4    4.0
# r5    5.0

# ── 基本查看 ──
print(cipher_df.head(2))       # 前 2 行
print(cipher_df.tail(2))       # 后 2 行
print(cipher_df.shape)         # (3, 3)
print(cipher_df.size)          # 9
print(cipher_df.ndim)          # 2
print(cipher_df.columns)       # Index(['a', 'b', 'c'], dtype='object')
print(cipher_df.index)         # RangeIndex(start=0, stop=3, step=1)
```
