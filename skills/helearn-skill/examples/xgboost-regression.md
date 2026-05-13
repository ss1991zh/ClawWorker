# XGBoost 极限梯度提升树 — 回归

使用密文 XGBoost 回归器在乳腺癌数据上训练与预测；通过 `data_type="cipher"` 直接获得密文特征与标签，无需再手动封装为 `CipherDataFrame`。

## 完整示例

以下脚本从数据加载到预测可在同一环境中直接运行；需先完成同态环境初始化。

```python
import helearn as hl
import henumpy as hp

hp.initDict()

data = hl.datasets.load_breast_cancer(data_type="cipher")
X_train = data.train_data
y_train = data.train_target
X_test = data.test_data

model = hl.XGBRegressor(
    learning_rate=0.3,
    n_estimators=10,
    max_depth=6,
    lambd=0.1,
    gamma=1e-6,
    min_samples_split=2,
    min_child_weight=1,
    n_jobs=6,
)

model.fit(X=X_train, y=y_train)

pred = model.predict(X=X_test)
```

## 使用的 API

| API | 用途 |
|-----|------|
| `hp.initDict()` | 初始化 henumpy 同态字典（脚本入口必调） |
| `hl.datasets.load_breast_cancer(data_type="cipher")` | 直接加载密文特征与标签，便于与 XGB 回归器对接 |
| `hl.XGBRegressor()` | 创建密文 XGBoost 回归模型 |
| `fit()` | 密文训练 |
| `predict()` | 密文回归预测 |
