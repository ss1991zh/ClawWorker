# GBDT 梯度提升树 — 分类

使用密文 GBDT（`GradientBoostingClassifier`）在乳腺癌数据上完成分类：将数据集包装为 `CipherDataFrame` 后训练与预测。

## 完整示例

```python
import numpy as np
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 加载数据并包装为 CipherDataFrame
data = hl.datasets.load_breast_cancer()
X_train = hl.CipherDataFrame(data.train_data.get_base_array())
y_train = hl.CipherDataFrame(np.array([data.train_target.get_base_array()]).T)
X_test = hl.CipherDataFrame(data.test_data.get_base_array())

model = hl.GradientBoostingClassifier(
    learning_rate=0.5,
    n_estimators=6,
    max_depth=8,
    criterion="friedman_mse",
)

# 密文训练
model.fit(X=X_train, y=y_train)

# 密文预测
pred, label = model.predict(X=X_test)
```

## 算法与 API 对照表

| API | 用途 |
|-----|------|
| `hl.GradientBoostingClassifier()` | 创建 GBDT 分类模型 |
| `hl.CipherDataFrame()` | 将密文底层数组包装为二维密文 DataFrame |
| `hl.datasets.load_breast_cancer()` | 加载乳腺癌数据集（默认非 cipher 时需再包装） |
| `fit()` / `predict()` | 密文训练与预测，返回 `(pred, label)` |
