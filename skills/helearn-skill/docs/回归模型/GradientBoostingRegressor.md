# GradientBoostingRegressor

## 描述

密文 GBRT 梯度提升树回归模型。

## 构造函数签名

```text
hl.GradientBoostingRegressor(
    learning_rate=0.1,
    n_estimators=3,
    max_depth=6,
    criterion="friedman_mse",
    debug=False,
)
```

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `learning_rate` | float | 梯度下降学习率。默认 `0.1`。 |
| `n_estimators` | int | GBDT 树个数。默认 `3`。 |
| `max_depth` | int | 每棵树最大高度。默认 `6`。 |
| `criterion` | str | 分裂准则。默认 `"friedman_mse"`。 |
| `debug` | bool | 是否输出调试信息。默认 `False`。 |

## 方法

### fit

**签名：** `model.fit(X, y)`

与 `GradientBoostingClassifier` 相同：`X` 为二维密文数组（列加密），`y` 为密文因变量。

**返回值：** `self`。

### predict

**签名：** `model.predict(X)`

与 `GradientBoostingClassifier` 的输入形式相同。

**返回值：** 仅预测值，无分类标签（与分类器的 `(pred, label)` 不同）。

## 示例

```python
import numpy as np
import helearn as hl
import henumpy as hp

hp.initDict()

data = hl.datasets.load_breast_cancer()
X_train = hl.CipherDataFrame(data.train_data.get_base_array())
y_train = hl.CipherDataFrame(np.array([data.train_target.get_base_array()]).T)
X_test = hl.CipherDataFrame(data.test_data.get_base_array())

model = hl.GradientBoostingRegressor(learning_rate=0.5, n_estimators=6, max_depth=8, debug=False)
model.fit(X=X_train, y=y_train)
pred = model.predict(X=X_test)
```
