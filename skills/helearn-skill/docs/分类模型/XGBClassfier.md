# XGBClassfier

## 描述

密文 XGBoost 极限梯度提升树分类模型。注意类名拼写为 `XGBClassfier`（非 Classifier）。

## 构造函数签名

```text
hl.XGBClassfier(
    learning_rate=0.1,
    n_estimators=10,
    max_depth=6,
    base_score=0.5,
    lambd=1e-6,
    gamma=1e-6,
    min_child_weight=1,
    min_samples_split=2,
    n_jobs=cpu_count,
)
```

其中 `cpu_count` 表示 CPU 核心数（与运行环境一致）。

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `learning_rate` | float | 学习率。默认 `0.1`。 |
| `n_estimators` | int | 树个数。默认 `10`。 |
| `max_depth` | int | 每棵树最大高度。默认 `6`。 |
| `base_score` | float | 初始化权重。默认 `0.5`。 |
| `lambd` | float | 正则化参数。默认 `1e-6`。 |
| `gamma` | float | 限制节点生长。默认 `1e-6`。 |
| `min_child_weight` | float | 叶节点二阶导和阈值。默认 `1`。 |
| `min_samples_split` | int | 节点最少样本数。默认 `2`。 |
| `n_jobs` | int | 并行进程数。默认 CPU 核心数。 |

## 方法

### fit

**签名：** `model.fit(X, y)`

与 `GradientBoostingClassifier` 相同：`X` 为训练特征，`y` 为训练标签。

**返回值：** `self`。

### predict

**签名：** `model.predict(X)`

与 `GradientBoostingClassifier` 相同。

**返回值：** 元组 `(pred, label)` — 预测值与标签。

## 示例

```python
import helearn as hl
import henumpy as hp

hp.initDict()

data = hl.datasets.load_breast_cancer(data_type="cipher")
model = hl.XGBClassfier(learning_rate=0.3, n_estimators=10, max_depth=6, lambd=0.1)
model.fit(X=data.train_data, y=data.train_target)
pred, label = model.predict(X=data.test_data)
```
