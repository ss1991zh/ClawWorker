# 示例：密文统计分析报告

> 用户需求："计算加密数据的相关性矩阵、协方差矩阵和 Z-score 归一化"

**路由结果**：pandaseal + henumpy 联合  
**数据源**：加密 CSV 文件  
**任务类型**：数值计算（pandaseal 的基本统计不够，需 henumpy 高级统计）

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np
import os

hp.initDict()
ct.initSK()

# ── 数据读取（pandaseal） ──
file_path = 'encrypted_metrics.csv'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"加密文件不存在: {file_path}")

cdf = ps.read_csv(file_path)
print(f"数据形状: {cdf.shape}")
print(f"列名: {cdf.columns}")

# ── 基本统计（pandaseal） ──
print("\n=== 基本统计（pandaseal） ===")
mean_vals = cdf.mean()
std_vals = cdf.std()
print(f"均值: {ct.decrypt_df(mean_vals)}")
print(f"标准差: {ct.decrypt_df(std_vals)}")

# ── 转换为 CipherArray 进行高级计算（henumpy） ──
cipher_array = cdf.to_cipherarray()

# ── 相关系数矩阵（henumpy） ──
print("\n=== 相关系数矩阵 ===")
corr_matrix = hp.corrcoef(cipher_array)
print(ct.decrypt(corr_matrix))

# ── 协方差矩阵（henumpy） ──
print("\n=== 协方差矩阵 ===")
cov_matrix = hp.cov(cipher_array)
print(ct.decrypt(cov_matrix))

# ── Z-score 归一化（henumpy） ──
print("\n=== Z-score 归一化 ===")
z_scores = hp.div(hp.sub(cipher_array, hp.mean(cipher_array, axis=0)), hp.std(cipher_array, axis=0))
print(ct.decrypt(z_scores))

# ── Min-Max 归一化（henumpy） ──
print("\n=== Min-Max 归一化 ===")
x_min = hp.min(cipher_array, axis=0)
x_max = hp.max(cipher_array, axis=0)
normalized = hp.div(hp.sub(cipher_array, x_min), hp.sub(x_max, x_min))
print(ct.decrypt(normalized))

# ── 欧几里得距离（第一行与第二行） ──
print("\n=== 欧几里得距离（行0 vs 行1） ===")
dist = hp.sqrt(hp.sum(hp.square(hp.sub(cipher_array[0], cipher_array[1]))))
print(ct.decrypt(dist))

# 注意：同态加密计算结果存在浮点精度误差，这是 FHE 的固有特性，非 bug。
```
