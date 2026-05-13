# 示例：选择与索引

在加密 DataFrame 上使用 `[]`、`loc`、`iloc`、`at`、`iat` 和布尔索引。

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd

hp.initDict()
ct.initSK()

df = pd.DataFrame(
    [[1, 2], [4, 5], [7, 8]],
    index=['cobra', 'viper', 'sidewinder'],
    columns=['max_speed', 'shield']
)
cdf = ct.encrypt_df(df)

# ── 列选择 [] ──
col = cdf['max_speed']              # 返回 CipherSeries
print(ct.decrypt_df(col))
# cobra         1.0
# viper         4.0
# sidewinder    7.0

# ── loc：基于标签 ──
row = cdf.loc['viper']              # 返回 CipherSeries
print(ct.decrypt_df(row))
# max_speed    4.0
# shield       5.0

cell = cdf.loc['cobra', 'shield']   # 返回标量密文
print(ct.decrypt(cell))             # 2.0

subset = cdf.loc[['viper', 'sidewinder']]  # 返回 CipherDataFrame
print(ct.decrypt_df(subset))

# ── iloc：基于整数位置 ──
row0 = cdf.iloc[0]                  # 第 0 行
print(ct.decrypt_df(row0))

cell_ij = cdf.iloc[1, 0]           # 第 1 行第 0 列
print(ct.decrypt(cell_ij))         # 4.0

# ── at / iat：访问单个值 ──
val = cdf.at['cobra', 'shield']
print(ct.decrypt(val))              # 2.0

val2 = cdf.iat[2, 1]
print(ct.decrypt(val2))             # 8.0

# ── 布尔索引 ──
mask = df['shield'] > 4             # 布尔条件（明文比较）
filtered = cdf.loc[mask]
print(ct.decrypt_df(filtered))
# viper         4.0   5.0
# sidewinder    7.0   8.0

# 密文比较也可直接用
filtered2 = cdf[cdf['shield'] > 4]
print(ct.decrypt_df(filtered2))
```
