# GBRT 梯度提升树 — 回归

在乳腺癌数据集上，使用密文 GBRT（梯度提升回归树）完成回归训练与预测；特征与标签通过 `CipherDataFrame` 与数据集提供的密文数组对接。

## 完整示例

以下脚本从数据加载到预测可在同一环境中直接运行；需先完成同态环境初始化。

```python
import numpy as np
import helearn as hl
import henumpy as hp

hp.initDict()

data = hl.datasets.load_breast_cancer()
X_train = hl.CipherDataFrame(data.train_data.get_base_array())
y_train = hl.CipherDataFrame(np.array([data.train_target.get_base_array()]).T)
X_test = hl.CipherDataFrame(data.test_data.get_base_array())

model = hl.GradientBoostingRegressor(
    learning_rate=0.5,
    n_estimators=6,
    max_depth=8,
    criterion="friedman_mse",
    debug=False,
)

model.fit(X=X_train, y=y_train)

pred = model.predict(X=X_test)
```

## 使用的 API

| API | 用途 |
|-----|------|
| `hp.initDict()` | 初始化 henumpy 同态字典（脚本入口必调） |
| `hl.datasets.load_breast_cancer()` | 加载乳腺癌数据集（默认非 `cipher` 时需配合 `CipherDataFrame` 使用） |
| `hl.CipherDataFrame()` | 将密文底层数组包装为 GBRT 所需的二维密文表结构 |
| `hl.GradientBoostingRegressor()` | 创建密文 GBRT 回归模型 |
| `fit()` | 密文训练 |
| `predict()` | 密文回归预测 |
