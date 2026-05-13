# 错误处理详解

本文档包含完整的错误处理规则，涵盖代码生成自检、防御性编程模板和易混淆 API 对照。

## 常见错误模式速查表

| 错误表现 | 原因 | 修复方法 |
|---------|------|---------|
| `initDict` 未调用导致运行时崩溃 | 遗漏初始化 | 确保所有用到的库都有对应的 initDict 调用 |
| `AttributeError: hp has no attribute 'multiply'` | numpy 命名习惯误用 | 改为 `hp.mul`，查 INDEX.md |
| DataFrame 传入 helearn `fit()` 报错 | 类型不匹配 | 先 `cdf.to_cipherarray()` 转为 CipherArray |
| GBDT/XGBoost 训练结果异常 | 未使用列加密 | 加密时加 `encrypt_by_column=True` |
| hetorch2 输出精度异常大 | dtype 不是 float64 | 确保输入 Tensor `dtype=torch.float64` |
| `fillna(0)` 报错 | 传入明文标量 | 改为 `fillna(ct.encrypt(0))` |
| `groupby('col')` 报错 | pandaseal 不支持按列名分组 | 改为 `groupby(level=0)` |
| `XGBClassifier` not found | 拼写错误 | 改为 `hl.XGBClassfier`（注意少一个 i） |
| hetorch2 和 henumpy 混用时部分功能失效 | initDict 不互通 | 必须同时调用 `hp.initDict()` 和 `hetorch2.initDict()` |
| `ct.decrypt()` 对 DataFrame 返回异常 | 加解密方法不匹配 | DataFrame 用 `ct.decrypt_df()`，不是 `ct.decrypt()` |

## 易混淆 API 对照表

### numpy vs henumpy

| numpy | henumpy | 备注 |
|-------|---------|------|
| `np.multiply(a, b)` | `hp.mul(a, b)` | 名称不同 |
| `np.subtract(a, b)` | `hp.sub(a, b)` | 名称不同 |
| `np.divide(a, b)` | `hp.div(a, b)` | 名称不同 |
| `np.power(a, b)` | `hp.pow(a, b)` | 名称不同 |
| `np.abs(x)` | `hp.absolute(x)` | 名称不同 |
| `np.linalg.inv(A)` | `hp.linalg.inv(A)` | 相同 |
| `np.round(x, n)` | `hp.round(x, n)` | 相同 |
| — | `hp.invers(x)` | henumpy 独有：求逆 |
| — | `hp.decimal(x)` | henumpy 独有：取小数部分 |
| — | `hp.rounding(x)` | henumpy 独有：四舍五入 |
| `scipy.special.expit(x)` | `hp.expit(x)` | sigmoid 函数 |

### pandas vs pandaseal

| pandas | pandaseal | 备注 |
|--------|-----------|------|
| `pd.read_csv()` | `ps.read_csv()` | 读密文 CSV |
| `pd.read_excel()` | `ps.read_excel()` | 读密文 Excel |
| `df.groupby('col')` | `cdf.groupby(level=0)` | 只能按索引分组 |
| `df.fillna(0)` | `cdf.fillna(ct.encrypt(0))` | fill_value 必须是密文 |
| `df.describe()` | 不存在 | 需手动组合 `mean/std/min/max/quantile` |
| `df.apply()` | 不存在 | 需手动逐列操作 |
| `df.pivot_table()` | 不存在 | 需手动 groupby + 重组 |

### torch vs hetorch2

| torch | hetorch2 | 备注 |
|-------|----------|------|
| `nn.Linear` | `hetorch2.nn.Linear` | 命名一致 |
| `nn.Embedding` | `hetorch2.nn.Embedding` | 命名一致 |
| `nn.BatchNorm1d` | `hetorch2.nn.BatchNorm1d` | 命名一致（仅推理） |
| `nn.BatchNorm2d` | `hetorch2.nn.BatchNorm2d` | 命名一致（仅推理） |
| `nn.LayerNorm` | `hetorch2.nn.LayerNorm` | 命名一致 |
| `nn.ReLU` | `hetorch2.nn.ReLU` | 命名一致 |
| `nn.SiLU` | `hetorch2.nn.SiLU` | 命名一致 |
| `F.relu` | `hetorch2.nn.functional.relu` | 命名一致 |
| `F.softmax` | `hetorch2.nn.functional.softmax` | 命名一致 |
| `torch.matmul` | `hetorch2.matmul` | 矩阵乘法 |
| `torch.mul` | `hetorch2.mul` | 逐元素乘法 |
| `torch.Tensor` | `hetorch2.CipherTensor` | 密文张量 |
| `nn.Conv2d` | 不支持 | hetorch2 已移除 Conv2d |
| `nn.LSTM` | 不支持 | hetorch2 已移除 LSTM |
| `nn.MultiheadAttention` | 不支持 | hetorch2 已移除，需手动实现 |

**关键区分**：hetorch2 的命名与 PyTorch 完全对齐，不再使用 `He`/`h` 前缀。`hetorch2.mul` 是逐元素乘法，`hetorch2.matmul` 是矩阵乘法。

### sklearn vs helearn

| sklearn | helearn | 备注 |
|---------|---------|------|
| `LogisticRegression()` | `hl.LogisticRegression()` | 相同 |
| `GradientBoostingClassifier()` | `hl.GradientBoostingClassifier()` | 相同 |
| `XGBClassifier()` | `hl.XGBClassfier()` | 拼写不同，少一个 i |
| `LinearRegression()` | `hl.LinearRegression()` | 相同 |
| `GradientBoostingRegressor()` | `hl.GradientBoostingRegressor()` | 相同 |
| `XGBRegressor()` | `hl.XGBRegressor()` | 相同 |
| `model.fit(X, y)` | `model.fit(X=X, y=y)` | 参数名显式传入 |
| `model.predict(X)` | `model.predict(X=X)` | 分类额外返回 label |
| `model.set_params(**kwargs)` | `model.set_params(iterations, w, learningrate)` | 仅 LR 类模型 |

## 加解密方法匹配决策树

```
数据来源是什么？
├── pandas DataFrame / Series
│   ├── 加密: ct.encrypt_df(df)
│   └── 解密: ct.decrypt_df(cdf)
├── numpy ndarray（给 henumpy 用）
│   ├── 加密: ct.encrypt(arr) 或 ct.encrypt_ndarray(arr)
│   └── 解密: ct.decrypt(cipher) 或 ct.decrypt_ndarray(cipher)
├── numpy ndarray（给 helearn 用）
│   ├── 加密: ct.encrypt_ndarray(arr)
│   │   └── GBDT/XGBoost: ct.encrypt_ndarray(arr, encrypt_by_column=True) 或加密时设置列加密
│   └── 解密: ct.decrypt_ndarray(cipher)
├── torch Tensor
│   ├── 加密: ct.encrypt_tensor(tensor)
│   └── 解密: ct.decrypt_tensor(cipher_tensor)
├── CSV 文件（文件级）
│   ├── 加密: ct.encrypt_csv(input, output)
│   └── 解密: ct.decrypt_csv(input, output)
├── Excel 文件（文件级）
│   ├── 加密: ct.encrypt_excel(input, output)
│   └── 解密: ct.decrypt_excel(input, output)
└── JSON 文件（文件级）
    ├── 加密: ct.encrypt_json(input, output)
    └── 解密: ct.decrypt_json(input, output)
```

## 防御性代码模板

### 文件存在性检查

```python
import os

file_path = 'encrypted_data.xlsx'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"加密文件不存在: {file_path}")

cdf = ps.read_excel(file_path, index_col=0)
```

### 文件扩展名校验

```python
import os

file_path = 'data.xlsx'
ext = os.path.splitext(file_path)[1].lower()
if ext in ['.xlsx', '.xls']:
    cdf = ps.read_excel(file_path, index_col=0)
elif ext == '.csv':
    cdf = ps.read_csv(file_path)
elif ext == '.json':
    cdf = ps.read_json(file_path)
else:
    raise ValueError(f"不支持的文件格式: {ext}")
```

### 密文形状确认

```python
cipher_data = ct.encrypt(np.array([[1, 2], [3, 4]]))
print(f"密文形状: {cipher_data.cipherShape()}")
print(f"密文类型: {cipher_data.get_cipher_type()}")  # 1=标量, 2=数组, 3=离散
```

### helearn 数据校验

```python
data = hl.datasets.load_breast_cancer(data_type="cipher")
assert data.train_data is not None, "训练数据加载失败"
assert data.train_target is not None, "训练标签加载失败"
```

### hetorch2 dtype 检查

```python
x = torch.randn(1, 3, 28, 28, dtype=torch.float64)
assert x.dtype == torch.float64, f"hetorch2 要求 float64，当前 dtype: {x.dtype}"
cx = ct.encrypt_tensor(x)
```

### 精度提示模板

在每个生成脚本末尾添加：

```python
# 注意：同态加密计算结果存在浮点精度误差，这是 FHE 的固有特性，非 bug。
# 如需高精度整数运算，考虑使用离散加密: ct.encrypt_ndarray(data, discrete=True)
```
