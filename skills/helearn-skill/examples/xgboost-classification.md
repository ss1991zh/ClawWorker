# XGBoost 极限梯度提升树 — 分类

使用密文 XGBoost 分类器（类名 `XGBClassfier`）在乳腺癌密文数据上训练与预测，数据可直接以 `data_type="cipher"` 加载。

## 完整示例

```python
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 直接加载密文数据
data = hl.datasets.load_breast_cancer(data_type="cipher")
X_train = data.train_data
y_train = data.train_target
X_test = data.test_data

model = hl.XGBClassfier(
    learning_rate=0.3,
    n_estimators=10,
    max_depth=6,
    lambd=0.1,
    gamma=1e-6,
    min_samples_split=2,
    min_child_weight=1,
    n_jobs=6,
)

# 密文训练
model.fit(X=X_train, y=y_train)

# 密文预测
pred, label = model.predict(X=X_test)
```

## 算法与 API 对照表

| API | 用途 |
|-----|------|
| `hl.XGBClassfier()` | 创建密文 XGBoost 分类模型（注意拼写为 Classfier） |
| `hl.datasets.load_breast_cancer(data_type="cipher")` | 直接得到密文训练/测试特征与标签 |
| `fit()` / `predict()` | 密文训练与预测，返回 `(pred, label)` |
