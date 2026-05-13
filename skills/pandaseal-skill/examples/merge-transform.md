# 示例：合并、缺失值、去重与分桶

在加密 DataFrame 上进行数据合并、缺失值处理、去重和分桶操作。

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np

hp.initDict()
ct.initSK()

# ── merge 合并 ──
df1 = pd.DataFrame({'key': [1, 2, 3], 'val_a': [10, 20, 30]})
df2 = pd.DataFrame({'key': [1, 2, 4], 'val_b': [40, 50, 60]})
cdf1 = ct.encrypt_df(df1)
cdf2 = ct.encrypt_df(df2)

inner = ps.merge(cdf1, cdf2)                          # 默认 inner join
print(ct.decrypt_df(inner))

left = ps.merge(cdf1, cdf2, how='left', on='key')     # left join
print(ct.decrypt_df(left))

# ── concat 拼接 ──
combined = ps.concat([cdf1, cdf1], ignore_index=True)
print(ct.decrypt_df(combined))

# ── join 按索引合并 ──
df_a = pd.DataFrame({'a': [1, 2]}, index=['x', 'y'])
df_b = pd.DataFrame({'b': [3, 4]}, index=['x', 'y'])
cdf_a = ct.encrypt_df(df_a)
cdf_b = ct.encrypt_df(df_b)
joined = cdf_a.join(cdf_b)
print(ct.decrypt_df(joined))

# ── 缺失值处理 ──
df_nan = pd.DataFrame({'a': [1, np.nan, 3], 'b': [np.nan, 5, 6]})
cdf_nan = ct.encrypt_df(df_nan)

print(cdf_nan.isna())                    # 检测缺失值

dropped = cdf_nan.dropna()               # 删除含 NaN 的行
print(ct.decrypt_df(dropped))

zero = ct.encrypt(0)
filled = cdf_nan.fillna(zero)            # 用密文 0 填充 NaN
print(ct.decrypt_df(filled))

# ── 去重 ──
df_dup = pd.DataFrame({'a': [1, 1, 2], 'b': [3, 3, 4]})
cdf_dup = ct.encrypt_df(df_dup)
deduped = cdf_dup.drop_duplicates()
print(ct.decrypt_df(deduped))

# ── 分桶 (cut) ──
s = pd.Series([1, 7, np.nan, 4, 6, 3], name='price')
cs = ct.encrypt_df(s)

# 等宽分桶
res1 = ps.cut(cs, 3, labels=["bad", "medium", "good"])
print(res1)
# 0       bad
# 1      good
# 2       NaN
# 3    medium
# 4      good
# 5       bad

# 自定义区间分桶
bins = ct.encrypt([1, 3, 4, 7])
res2 = ps.cut(cs, bins, labels=["bad", "medium", "good"])
print(res2)
```
