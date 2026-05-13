# 示例：二元运算与比较

在加密 DataFrame 上进行加减乘除和比较操作。

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np

hp.initDict()
ct.initSK()

df = pd.DataFrame({'angles': [0, 3, 4], 'degrees': [360, 180, 360]},
                   index=['circle', 'triangle', 'rectangle'])
cdf = ct.encrypt_df(df)

# ── 运算符方式（推荐） ──
res_add = cdf + 1                     # 每个元素 +1
res_sub = cdf - 1                     # 每个元素 -1
res_mul = cdf * 2                     # 每个元素 *2
res_div = cdf / 2                     # 每个元素 /2
print(ct.decrypt_df(res_add))
#            angles  degrees
# circle        1.0    361.0
# triangle      4.0    181.0
# rectangle     5.0    361.0

# ── 方法调用方式 ──
res_add2 = cdf.add(1)                # 等价于 cdf + 1
res_sub2 = cdf.sub(1)                # 等价于 cdf - 1

# ── 两个 CipherDataFrame 运算 ──
df2 = pd.DataFrame({'angles': [1, 1, 1], 'degrees': [10, 10, 10]},
                    index=['circle', 'triangle', 'rectangle'])
cdf2 = ct.encrypt_df(df2)
result = cdf + cdf2
print(ct.decrypt_df(result))

# ── fill_value 处理缺失值 ──
df_nan = pd.DataFrame({'a': [1, np.nan], 'b': [3, 4]}, index=['x', 'y'])
cdf_nan = ct.encrypt_df(df_nan)
one = ct.encrypt(1)
res_fill = cdf_nan.add(cdf_nan, fill_value=one)
print(ct.decrypt_df(res_fill))

# ── CipherArray 与 CipherDataFrame 运算 ──
arr = ct.encrypt(np.array([[1, 2], [3, 6], [5, 4]]))
res_arr = cdf + arr
print(ct.decrypt_df(res_arr))

# ── 比较运算 ──
gt_result = cdf.gt(3)                # 或 cdf > 3
lt_result = cdf.lt(100)              # 或 cdf < 100
eq_result = cdf.eq(cdf2)             # 或 cdf == cdf2

# 比较返回布尔值，可用于筛选
mask = cdf['angles'] > 2
filtered = cdf[mask]
print(ct.decrypt_df(filtered))
#            angles  degrees
# triangle      3.0    180.0
# rectangle     4.0    360.0
```
