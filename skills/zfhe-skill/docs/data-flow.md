# 数据格式转换

子 skill 间传递数据时需要显式进行格式转换。本文档说明各密文数据类型之间的转换方法。

## 密文数据类型总览

| 数据类型 | 所属子 skill | 说明 |
|---------|------------|------|
| CipherArray（标量/数组/矩阵） | henumpy | `ct.encrypt()` 生成，支持 `hp.*` 运算 |
| CipherDataFrame | pandaseal | `ct.encrypt_df()` 生成，支持 `cdf.*` 和 `ps.*` 操作 |
| CipherSeries | pandaseal | CipherDataFrame 的单列，支持列级操作 |
| CipherTensor | hetorch2 | `ct.encrypt_tensor()` 生成，支持 hetorch2 Layer/Function |
| ndarray 密文 | helearn | `ct.encrypt_ndarray()` 生成，供 helearn 模型使用 |

## 转换路径

### CipherDataFrame → CipherArray

```python
cipher_array = cdf.to_cipherarray()
```

**用途**：从 pandaseal 读取的表格数据转为 henumpy 可计算的数组。

**注意**：转换后不可再使用 pandaseal 的 DataFrame 方法（如 `head()`、`groupby()`）。

### CipherDataFrame 单列 → CipherArray

```python
col_cipher = cdf['column_name']          # CipherSeries
col_array = cdf['column_name'].values    # 底层 CipherArray
```

### CipherArray → CipherDataFrame

```python
import pandaseal as ps
cdf = ps.CipherDataFrame(cipher_array, columns=['col1', 'col2', ...])
```

**用途**：henumpy 计算结果转回 pandaseal 进行 DataFrame 操作或导出文件。

### 明文 numpy → CipherArray（henumpy）

```python
cipher = ct.encrypt(np.array([1.0, 2.0, 3.0]))
```

按列加密（部分场景需要）：

```python
cipher = ct.encrypt(data, encrypt_by_column=True)
```

### 明文 numpy → ndarray 密文（helearn）

```python
cipher = ct.encrypt_ndarray(np_array)
```

离散加密：

```python
cipher = ct.encrypt_ndarray(np_array, discrete=True)
```

### 明文 DataFrame → CipherDataFrame

```python
import pandas as pd
df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
cdf = ct.encrypt_df(df)
```

### 明文 Tensor → CipherTensor

```python
import torch
x = torch.randn(1, 3, 28, 28, dtype=torch.float64)
cx = ct.encrypt_tensor(x)
```

**注意**：dtype 必须是 `torch.float64`，这是 hetorch2 的要求。

### CipherTensor → 明文 Tensor

```python
result = ct.decrypt_tensor(cipher_tensor)
```

## 跨 skill 数据流模式

### 模式 A: pandaseal → henumpy → 解密

读取表格 → 提取数据 → 数值计算 → 解密输出。

```python
cdf = ps.read_excel('encrypted.xlsx', index_col=0)
cipher_array = cdf.to_cipherarray()

result = hp.corrcoef(cipher_array)

print(ct.decrypt(result))
```

### 模式 B: pandaseal → helearn → 解密

读取表格 → 提取特征/标签 → ML 训练 → 预测 → 解密。

```python
cdf = ps.read_csv('encrypted.csv')
X = cdf[['feature1', 'feature2']].to_cipherarray()
y = cdf['label'].to_cipherarray()

model = hl.XGBClassfier(learning_rate=0.3, n_estimators=10, max_depth=6)
model.fit(X=X, y=y)
pred, label = model.predict(X=X)

print(ct.decrypt(pred))
```

### 模式 C: 明文加密 → henumpy → helearn → 解密

先加密数值数据 → 预处理 → 训练 → 预测。

```python
X_enc = ct.encrypt_ndarray(X_plain, encrypt_by_column=True)
y_enc = ct.encrypt_ndarray(y_plain)

model = hl.GradientBoostingClassifier(learning_rate=0.1, n_estimators=3, max_depth=6)
model.fit(X=X_enc, y=y_enc)
pred, label = model.predict(X=X_enc)
```

### 模式 D: hetorch2 独立

加密 Tensor → 模型推理 → 解密。

```python
x = torch.randn(1, 3, 28, 28, dtype=torch.float64)
cx = ct.encrypt_tensor(x)

model = CipherCNN()
model.load_state_dict(torch.load('model.pth'))
output = model(cx)

result = ct.decrypt_tensor(output)
```

## 不兼容的转换

以下转换路径 **不存在**，不要尝试：

| 源类型 | 目标类型 | 原因 |
|--------|---------|------|
| CipherArray → CipherTensor | 无直接转换 API | hetorch2 和 henumpy 的密文格式不互通 |
| CipherTensor → CipherArray | 无直接转换 API | 同上 |
| CipherDataFrame → CipherTensor | 无直接转换 API | 需先解密再加密为 Tensor |
| CipherTensor → CipherDataFrame | 无直接转换 API | 需先解密再加密为 DataFrame |

如果流水线确实需要跨越 henumpy/pandaseal 和 hetorch2 的数据格式，必须通过解密-再加密中转：

```python
plain = ct.decrypt(cipher_array)
tensor = torch.tensor(plain, dtype=torch.float64)
cipher_tensor = ct.encrypt_tensor(tensor)
```
