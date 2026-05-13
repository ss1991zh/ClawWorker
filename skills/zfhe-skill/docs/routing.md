# 路由逻辑详解

根据用户自然语言需求，确定应调用哪些子 skill 的完整规则。

## 数据源识别规则

按优先级从高到低匹配：

### 规则 1: 明确文件类型

用户提及具体文件格式或给出文件路径时，直接确定数据源。

| 关键词/模式 | 数据源 | 子 skill | 读取 API |
|------------|--------|---------|---------|
| `.xlsx`、`.xls`、`Excel` | 加密 Excel | pandaseal | `ps.read_excel(path, index_col=0)` |
| `.csv`、`CSV` | 加密 CSV | pandaseal | `ps.read_csv(path)` |
| `.json`、`JSON` | 加密 JSON | pandaseal | `ps.read_json(path)` |
| `表格`、`DataFrame`、`数据表` | 结构化数据 | pandaseal | `ct.encrypt_df(df)` |

**特殊情况**：如果同时提及 CSV + 机器学习训练（如"用 CSV 训练分类器"），优先路由到 helearn 的 `ct.encrypt_csv()`，因为 helearn 直接支持 CSV 文件级加密后训练。

### 规则 2: 数值/数组类型

| 关键词/模式 | 数据源 | 子 skill | 加密 API |
|------------|--------|---------|---------|
| `数组`、`向量`、`矩阵`、`ndarray` | 数值数组 | henumpy | `ct.encrypt(np_array)` |
| `列表`、`数值列表`、Python 字面量 | 数值数组 | henumpy | `ct.encrypt(np.array([...]))` |
| 需要按列加密 | 列加密数组 | henumpy | `ct.encrypt(data, encrypt_by_column=True)` |
| 需要离散加密 | 离散数组 | henumpy | `ct.encrypt_ndarray(data, discrete=True)` |

### 规则 3: 张量/模型类型

| 关键词/模式 | 数据源 | 子 skill | 加密 API |
|------------|--------|---------|---------|
| `Tensor`、`张量`、`图像`、`图片` | 张量 | hetorch2 | `ct.encrypt_tensor(tensor)` |
| `模型`、`权重`、`.pth`、`.pt` | 模型权重 | hetorch2 | `torch.load(path)` |

### 规则 4: 内置数据集

| 关键词/模式 | 数据源 | 子 skill | 加载 API |
|------------|--------|---------|---------|
| `breast_cancer`、`乳腺癌` | 分类数据集 | helearn | `hl.datasets.load_breast_cancer(data_type="cipher")` |
| `boston`、`波士顿`、`房价` | 回归数据集 | helearn | `hl.datasets.load_boston()` |

### 规则 5: 明文数据需先加密

如果用户提供的是明文数据（如 pandas DataFrame、numpy array、torch Tensor），需要先加密再分析：

| 明文类型 | 加密方法 |
|---------|---------|
| `pd.DataFrame` | `ct.encrypt_df(df)` → CipherDataFrame |
| `np.ndarray` | `ct.encrypt(arr)` 或 `ct.encrypt_ndarray(arr)` → CipherArray |
| `torch.Tensor` | `ct.encrypt_tensor(tensor)` → CipherTensor |
| 明文 CSV 文件 | `ct.encrypt_csv(input, output)` → 加密 CSV 文件 |
| 明文 Excel 文件 | `ct.encrypt_excel(input, output)` → 加密 Excel 文件 |

## 任务类型识别规则

### 数据探索（EDA）→ pandaseal

触发词：`探索`、`查看`、`描述`、`分组`、`聚合`、`EDA`、`筛选`、`排序`、`去重`、`缺失值`、`合并`、`头几行`、`统计概览`

典型操作：`cdf.head()`、`cdf.groupby()`、`cdf.mean()`、`cdf.sort_values()`、`ps.merge()`、`cdf.dropna()`

### 数值计算 → henumpy

触发词：`均值`、`方差`、`标准差`、`相关系数`、`协方差`、`线性代数`、`矩阵乘`、`多项式`、`插值`、`归一化`、`距离`、`范数`

典型操作：`hp.mean()`、`hp.std()`、`hp.corrcoef()`、`hp.matmul()`、`hp.polyfit()`、`hp.linalg.norm()`

### ML 分类 → helearn

触发词：`分类`、`逻辑回归`、`GBDT`、`梯度提升`、`XGBoost`、`二分类`、`多分类`、`训练分类器`

可用模型：
- `hl.LogisticRegression()` — 逻辑回归
- `hl.GradientBoostingClassifier()` — GBDT 分类
- `hl.XGBClassfier()` — XGBoost 分类（注意拼写）

### ML 回归 → helearn

触发词：`回归`、`线性回归`、`GBRT`、`预测数值`、`房价`、`价格预测`

可用模型：
- `hl.LinearRegression()` — 线性回归
- `hl.GradientBoostingRegressor()` — GBRT 回归
- `hl.XGBRegressor()` — XGBoost 回归

### DL 推理 → hetorch2

触发词：`深度学习`、`神经网络`、`MLP`、`Transformer`、`推理`、`图像识别`、`分类推理`、`文本生成`

可用 Layer：`nn.Linear`、`nn.Embedding`、`nn.ReLU`、`nn.SiLU`、`nn.BatchNorm1d`、`nn.BatchNorm2d`、`nn.LayerNorm` 等

## 组合模式判定

当数据源和任务类型分属不同子 skill 时，需要组合使用。

### pandaseal + henumpy

**触发**：读取表格数据后需要做深度数值计算（pandaseal 自带的 `mean/std/var` 不够用）。

**判定标准**：如果需求中出现 pandaseal 不支持的统计运算（如 `corrcoef`、`polyfit`、`linalg.norm`），需要组合 henumpy。

**数据流**：`ps.read_excel()` → `cdf.to_cipherarray()` → `hp.*(cipher_array)` → `ct.decrypt()`

### pandaseal + helearn

**触发**：从表格文件读取数据后训练机器学习模型。

**判定标准**：用户同时提及文件读取和模型训练。

**数据流**：`ps.read_csv()` → `cdf.to_cipherarray()` → `model.fit(X, y)` → `model.predict(X_test)`

### henumpy + helearn

**触发**：对数值数组做预处理后训练模型。

**数据流**：`ct.encrypt_ndarray(data)` → `hp.*(预处理)` → `model.fit(X, y)`

### hetorch2 独立

**触发**：纯深度学习推理场景。

**重要**：hetorch2 不依赖 henumpy，有独立的 `hetorch2.initDict()`。

## 兜底策略

当上述规则无法明确匹配时：

1. **提及表格/文件但任务不明** → 默认路由到 pandaseal 做 EDA（`cdf.head()` + `cdf.mean()` + 数据概览）
2. **提及训练/预测但模型不明** → 默认推荐 helearn，但**必须询问**用户是分类还是回归
3. **提及推理但模型结构不明** → 默认展示 hetorch2 MLP 模板，但**必须询问**具体模型架构
4. **完全无法判断** → **必须向用户提问澄清**，禁止猜测生成代码

## 冲突检测

以下为常见的矛盾需求，需要引导用户：

| 用户表述 | 矛盾点 | 引导方向 |
|---------|--------|---------|
| "用 hetorch2 训练 sklearn 模型" | hetorch2 做推理不做训练，sklearn 风格用 helearn | 引导到 helearn |
| "用 pandaseal 做矩阵求逆" | pandaseal 无矩阵求逆 | 引导 pandaseal 读取 + henumpy `hp.linalg.inv()` |
| "用 henumpy 读 Excel" | henumpy 不读文件 | 引导 pandaseal 读取 + henumpy 计算 |
| "用 helearn 做深度学习" | helearn 是传统 ML | 引导到 hetorch2 |
