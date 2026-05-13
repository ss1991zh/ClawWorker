# helearn API 索引

> 仅签名 + 一句话描述 + 文档路径。详细参数说明请按需读取对应文档。

## 加解密 API（`crypto_toolkit`）

| API | 签名 | 描述 | 文档 |
|-----|------|------|------|
| encrypt_ndarray | `ct.encrypt_ndarray(input_array, encrypt_by_column=False, discrete=False)` | 数值数组加密（支持单值/一维/二维） | `docs/加解密/encrypt_ndarray.md` |
| decrypt_ndarray | `ct.decrypt_ndarray(input_array, decrypt_by_column=False, discrete=False)` | 数值数组解密 | `docs/加解密/decrypt_ndarray.md` |
| encrypt_csv | `ct.encrypt_csv(input_file, output_file, encrypt_by_column=True, extract_header=True)` | CSV 文件加密 | `docs/加解密/encrypt_csv.md` |
| decrypt_csv | `ct.decrypt_csv(input_file, output_file, decrypt_by_column=True, extract_header=True)` | CSV 文件解密 | `docs/加解密/decrypt_csv.md` |

## 分类模型

| 模型 | 签名 | 描述 | 文档 |
|------|------|------|------|
| LogisticRegression | `hl.LogisticRegression()` + `set_params(iterations, w, learningrate)` | 密文逻辑回归（二分类） | `docs/分类模型/LogisticRegression.md` |
| GradientBoostingClassifier | `hl.GradientBoostingClassifier(learning_rate=0.1, n_estimators=3, max_depth=6, criterion="friedman_mse")` | 密文 GBDT 梯度提升树分类 | `docs/分类模型/GradientBoostingClassifier.md` |
| XGBClassfier | `hl.XGBClassfier(learning_rate=0.1, n_estimators=10, max_depth=6, ...)` | 密文 XGBoost 分类 | `docs/分类模型/XGBClassfier.md` |

## 回归模型

| 模型 | 签名 | 描述 | 文档 |
|------|------|------|------|
| LinearRegression | `hl.LinearRegression()` + `set_params(iterations, w, learningrate)` | 密文线性回归 | `docs/回归模型/LinearRegression.md` |
| GradientBoostingRegressor | `hl.GradientBoostingRegressor(learning_rate=0.1, n_estimators=3, max_depth=6, criterion="friedman_mse")` | 密文 GBRT 梯度提升树回归 | `docs/回归模型/GradientBoostingRegressor.md` |
| XGBRegressor | `hl.XGBRegressor(learning_rate=0.1, n_estimators=10, max_depth=6, ...)` | 密文 XGBoost 回归 | `docs/回归模型/XGBRegressor.md` |

## 数据集

| API | 签名 | 描述 | 文档 |
|-----|------|------|------|
| load_breast_cancer | `hl.datasets.load_breast_cancer(data_type="cipher")` | 加载乳腺癌数据集（密文/明文） | `docs/数据集/load_breast_cancer.md` |
| load_boston | `hl.datasets.load_boston()` | 加载波士顿房价数据集 | `docs/数据集/load_boston.md` |

## 通用方法（所有模型共享）

| 方法 | 签名 | 描述 |
|------|------|------|
| fit | `model.fit(X, y)` | 密文模型训练（X 为密文特征，y 为密文标签） |
| predict | `model.predict(X)` | 密文模型预测（返回预测值，分类模型额外返回标签/激活值） |
| set_params | `model.set_params(iterations, w, learningrate)` | 设置模型参数（仅 LR 类模型） |
