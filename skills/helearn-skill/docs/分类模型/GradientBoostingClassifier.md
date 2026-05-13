# GradientBoostingClassifier

## 描述

密文 GBDT 梯度提升树分类模型。

## 构造函数签名

```text
hl.GradientBoostingClassifier(
    learning_rate=0.1,
    n_estimators=3,
    max_depth=6,
    criterion="friedman_mse",
)
```

## 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `learning_rate` | float | 梯度下降学习率。默认 `0.1`。 |
| `n_estimators` | int | GBDT 树个数。默认 `3`。 |
| `max_depth` | int | 每棵树最大高度。默认 `6`。 |
| `criterion` | str | 分裂准则，可选 `"friedman_mse"` 或 `"square_error"`。默认 `"friedman_mse"`。 |

## 方法

### fit

**签名：** `model.fit(X, y)`

| 参数 | 类型 | 说明 |
|------|------|------|
| `X` | 二维密文数组（列加密） | 训练集自变量。 |
| `y` | 密文数组 | 训练集因变量。 |

**返回值：** `self`。

### predict

**签名：** `model.predict(X)`

| 参数 | 类型 | 说明 |
|------|------|------|
| `X` | 二维密文数组 | 测试集自变量。 |

**返回值：** 元组 `(pred, label)` — 预测值与标签。

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

model = hl.GradientBoostingClassifier(learning_rate=0.5, n_estimators=6, max_depth=8)
model.fit(X=X_train, y=y_train)
pred, label = model.predict(X=X_test)
```
