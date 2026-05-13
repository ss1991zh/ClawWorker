# 示例：混合流水线（读取 → 预处理 → 建模）

> 用户需求："从加密 CSV 读取数据，做特征工程后训练 XGBoost 分类器"

**路由结果**：pandaseal + henumpy + helearn 联合  
**数据源**：加密 CSV 文件  
**任务类型**：数据读取 → 预处理 → ML 分类

```python
import helearn as hl
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np
import os

hp.initDict()
ct.initSK()

# ══════════════════════════════════════
# 阶段 1: 数据读取（pandaseal）
# ══════════════════════════════════════

file_path = 'encrypted_dataset.csv'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"加密文件不存在: {file_path}")

cdf = ps.read_csv(file_path)
print(f"数据形状: {cdf.shape}")
print(f"列名: {cdf.columns}")
print(cdf.head(5))

# ══════════════════════════════════════
# 阶段 2: 数据探索与清洗（pandaseal）
# ══════════════════════════════════════

print("\n=== 数据概览 ===")
print(f"均值:\n{ct.decrypt_df(cdf.mean())}")
print(f"标准差:\n{ct.decrypt_df(cdf.std())}")

# 缺失值处理
cdf = cdf.fillna(ct.encrypt(0))

# 去重
cdf = cdf.drop_duplicates()

# ══════════════════════════════════════
# 阶段 3: 特征工程（pandaseal + henumpy）
# ══════════════════════════════════════

# 列运算：构造交叉特征
cdf['feature_cross'] = cdf['feature1'] * cdf['feature2']

# 提取特征和标签
feature_cols = ['feature1', 'feature2', 'feature_cross']
X_cipher = cdf[feature_cols].to_cipherarray()
y_cipher = cdf['label'].to_cipherarray()

# 用 henumpy 做 Z-score 归一化
X_mean = hp.mean(X_cipher, axis=0)
X_std = hp.std(X_cipher, axis=0)
X_normalized = hp.div(hp.sub(X_cipher, X_mean), X_std)

print(f"\n归一化后数据形状: {X_normalized.cipherShape()}")

# ══════════════════════════════════════
# 阶段 4: 模型训练与预测（helearn）
# ══════════════════════════════════════

print("\n=== XGBoost 分类训练 ===")
model = hl.XGBClassfier(
    learning_rate=0.3,
    n_estimators=10,
    max_depth=6
)
model.fit(X=X_normalized, y=y_cipher)

pred, label = model.predict(X=X_normalized)

# ══════════════════════════════════════
# 阶段 5: 结果输出（解密）
# ══════════════════════════════════════

print("\n=== 预测结果 ===")
print(f"预测值: {ct.decrypt_ndarray(pred)}")
print(f"预测标签: {ct.decrypt_ndarray(label)}")

# 注意：同态加密计算结果存在浮点精度误差，这是 FHE 的固有特性，非 bug。
# 如需高精度整数运算，考虑使用离散加密: ct.encrypt_ndarray(data, discrete=True)
```
