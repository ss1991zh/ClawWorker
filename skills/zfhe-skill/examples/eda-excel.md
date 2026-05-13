# 示例：加密 Excel 数据探索分析

> 用户需求："分析这份加密 Excel 中各部门的销售数据"

**路由结果**：pandaseal 单独  
**数据源**：加密 Excel 文件  
**任务类型**：数据探索（EDA）

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np
import os

hp.initDict()
ct.initSK()

# ── 数据读取 ──
file_path = 'encrypted_sales.xlsx'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"加密文件不存在: {file_path}")

cdf = ps.read_excel(file_path, index_col=0)

# ── 数据概览 ──
print("=== 数据概览 ===")
print(f"形状: {cdf.shape}")
print(f"列名: {cdf.columns}")
print(f"前 5 行:")
print(cdf.head(5))

# ── 基本统计 ──
print("\n=== 基本统计 ===")
print(f"均值:\n{ct.decrypt_df(cdf.mean())}")
print(f"标准差:\n{ct.decrypt_df(cdf.std())}")
print(f"最大值:\n{ct.decrypt_df(cdf.max())}")
print(f"最小值:\n{ct.decrypt_df(cdf.min())}")

# ── 按部门分组统计（假设部门为索引） ──
print("\n=== 分组统计 ===")
grouped = cdf.groupby(level=0)
group_mean = grouped.mean()
group_sum = grouped.sum()
print(f"分组均值:\n{ct.decrypt_df(group_mean)}")
print(f"分组求和:\n{ct.decrypt_df(group_sum)}")

# ── 列运算：计算利润率 ──
cdf['profit_rate'] = cdf['profit'] / cdf['revenue']
print(f"\n利润率:\n{ct.decrypt_df(cdf['profit_rate'])}")

# ── 条件筛选：高销售额 ──
q75 = cdf['revenue'].quantile(0.75)
high_sales = cdf[cdf['revenue'] > q75]
print(f"\n高销售额（>75 分位）:\n{ct.decrypt_df(high_sales)}")

# ── 排序 ──
sorted_cdf = cdf.sort_values(by='revenue', ascending=False)
print(f"\n按销售额降序:\n{ct.decrypt_df(sorted_cdf.head(10))}")

# ── 导出结果 ──
cdf.to_excel('analysis_result.xlsx', index=True)
print("\n分析结果已导出到 analysis_result.xlsx")

# 注意：同态加密计算结果存在浮点精度误差，这是 FHE 的固有特性，非 bug。
```
