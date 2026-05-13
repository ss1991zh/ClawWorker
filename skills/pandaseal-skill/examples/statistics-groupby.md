# 示例：统计运算与分组聚合

在加密 DataFrame 上进行统计计算和 groupby 聚合。

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np

hp.initDict()
ct.initSK()

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}, index=['x', 'y', 'z'])
cdf = ct.encrypt_df(df)

# ── 基本统计 ──
print(ct.decrypt_df(cdf.mean()))       # 列均值：a=2.0, b=5.0
print(ct.decrypt_df(cdf.std()))        # 列标准差
print(ct.decrypt_df(cdf.var()))        # 列方差
print(ct.decrypt_df(cdf.max()))        # 列最大值：a=3.0, b=6.0
print(ct.decrypt_df(cdf.min()))        # 列最小值：a=1.0, b=4.0

# 行方向统计
print(ct.decrypt_df(cdf.mean(axis=1)))   # 行均值

# 分位数
q75 = cdf.quantile(0.75)
print(ct.decrypt_df(q75))

# 协方差矩阵
print(ct.decrypt_df(cdf.cov()))

# 累积求和
print(ct.decrypt_df(cdf.cumsum()))

# 百分比变化
print(ct.decrypt_df(cdf.pct_change()))

# 数据偏移
print(ct.decrypt_df(cdf.shift(1)))

# ── 分组聚合 ──
df2 = pd.DataFrame(
    {'max_speed': [6, 4, 7, 6, np.nan, 6],
     'shield':    [2, 5, 8, 4, 5, 3],
     'age':       [11, 6, 13, 4, 8, 4]},
    index=['cobra', 'viper', 'sidewinder', 'cobra', 'cobra', 'cobra']
)
cdf2 = ct.encrypt_df(df2)

# 按索引分组
grouped = cdf2.groupby(level=0)

# 分组均值
avg = grouped.mean()
print(ct.decrypt_df(avg))

# 分组求和
total = grouped.sum()
print(ct.decrypt_df(total))

# 分组中位数
med = grouped.median()
print(ct.decrypt_df(med))

# 分组标准差
sd = grouped.std()
print(ct.decrypt_df(sd))

# 分组分位数
q = grouped.quantile(0.3)
print(ct.decrypt_df(q))

# ── 实际场景：按房龄统计平均收入 ──
# avg_income = ct.decrypt_df(c_df.groupby(level=0).mean()['MedInc'])
```
