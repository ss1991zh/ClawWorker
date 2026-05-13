---
name: pandaseal-skill
description: >
  同态加密 DataFrame 数据分析代码生成。使用 pandaseal (ps) 和 crypto_toolkit (ct) 在密文上
  执行 Pandas 风格的数据分析操作。
  触发条件：用户提及 pandaseal、PandaSeal、密文 DataFrame、CipherDataFrame、CipherSeries、
  加密数据分析、encrypted DataFrame、ciphertext data analysis，
  或需要在加密数据上做 Pandas 风格的操作（ps.read_csv、cdf.groupby、ps.merge 等）。
  不适用于：普通 pandas 明文操作。
user-invocable: true
metadata: {"openclaw":{"emoji":"🔒"}}
---

# pandaseal — 同态加密 DataFrame 数据分析

基于 `pandaseal` 的同态加密 DataFrame 数据分析代码生成 Skill。

三个核心库协同工作：
- **`pandaseal`**（别名 `ps`）— 密文上的 Pandas 风格数据分析算子
- **`crypto_toolkit`**（别名 `ct`）— 加解密操作
- **`henumpy`**（别名 `hp`）— 底层密文计算字典（必须初始化）

## 何时使用

当用户请求满足以下任一条件时激活此 skill：
- 提及 pandaseal、PandaSeal、CipherDataFrame、CipherSeries
- 提及加密数据分析、密文 DataFrame、encrypted data analysis
- 需要在加密数据上做 Pandas 风格的操作
- 使用 `ps.*`、`cdf.*`（CipherDataFrame 方法）或 `ct.encrypt_df` / `ct.decrypt_df` API

**不适用于**：普通 pandas 明文操作、非加密场景。

## 快速参考

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np

hp.initDict()
ct.initSK()

# 加密 DataFrame
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
cdf = ct.encrypt_df(df)

# pandaseal 操作
print(cdf.head())
col_a = cdf['a']
result = cdf['a'] + cdf['b']
avg = cdf.mean()
grouped = cdf.groupby(level=0).mean()

# 解密查看结果
print(ct.decrypt_df(cdf))
print(ct.decrypt(result))
```

## 常见计算模式

| 目标 | 实现方式 |
|------|---------|
| 查看前 N 行 | `cdf.head(n)` |
| 列运算 | `cdf['new_col'] = cdf['a'] * cdf['b']` |
| 条件筛选 | `cdf[cdf['col'] > cdf['col'].quantile(0.75)]` |
| 分组统计 | `cdf.groupby(level=0).mean()` |
| 数据合并 | `ps.merge(cdf1, cdf2, how='inner', on='key')` |
| 缺失值填充 | `cdf.fillna(ct.encrypt(0))` |
| 分桶 | `ps.cut(cdf['col'], bins=ct.encrypt([0,10,20]), labels=['low','high'])` |
| 排序 | `cdf.sort_values(by='col')` |
| 读取加密文件 | `cdf = ps.read_excel('cipher.xlsx', index_col=0)` |
| 导出加密文件 | `cdf.to_csv('output.csv')` |

## 代码生成工作流

处理用户请求时按以下步骤执行：

1. **分解需求** — 将用户需求拆解为 DataFrame 操作序列。
2. **映射 API** — 将每个操作映射到 `ps.*` 或 `cdf.*` API。
   - 在上方快速参考中？直接使用
   - 不在？查阅 `{baseDir}/INDEX.md` 获取函数签名和文档路径
   - INDEX.md 中无直接对应？用已有 API 组合
3. **查阅文档** — 对非基础 API，读取 `{baseDir}/docs/` 下的具体文档确认参数和行为。仅读取所需文档（2-5 个），不要批量加载。
4. **生成代码** — 组合 API 生成完整代码。必须包含初始化（`hp.initDict()` + `ct.initSK()`）。
5. **自检** — 对照下方硬性规则检查。

## 硬性规则

1. **必须初始化** — 每个脚本以 `hp.initDict()` + `ct.initSK()` 开头。
2. **禁止编造 API** — `{baseDir}/INDEX.md` 中找不到的 API 不存在。
3. **加解密方法区分** — 数值数组用 `ct.encrypt()` / `ct.decrypt()`；DataFrame/Series 用 `ct.encrypt_df()` / `ct.decrypt_df()`。
4. **运算符已重载** — `+` `-` `*` `/` `>` `<` `>=` `<=` `==` `!=` 可直接在 CipherDataFrame/CipherSeries 上使用。
5. **`_P` / `_L` 行是正常现象** — CipherDataFrame 打印时会显示 `_P`（加密参数）和 `_L`（长度）行，属于加密元数据，解密后不会出现。
6. **fill_value 必须是密文** — 二元操作的 `fill_value` 参数需传入密文标量（如 `ct.encrypt(0)`），不能传明文。
7. **groupby 基于索引** — `cdf.groupby(level=0)` 按索引分组，不支持按列名分组。
8. **比较操作返回布尔值** — `>` `<` 等比较返回普通布尔值，可直接用于布尔索引。

## 错误处理

- 如果用户请求的操作在 INDEX.md 中不存在，明确告知并建议可用的替代组合。
- 如果参数类型不确定，查阅对应文档的参数说明。
- 如果涉及精度问题，提醒用户同态加密存在固有浮点误差。

## 参考文件

- API 索引：`{baseDir}/INDEX.md`
- API 文档目录：`{baseDir}/docs/`
- 完整示例：`{baseDir}/examples/`
