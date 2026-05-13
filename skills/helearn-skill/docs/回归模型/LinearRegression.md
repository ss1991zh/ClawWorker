# LinearRegression

## 描述

密文线性回归，通过梯度下降最小化均方误差。

## 构造函数签名

```text
hl.LinearRegression()
```

无构造参数。

## 参数

构造函数无额外参数。

## 方法

### set_params

**签名：** `model.set_params(iterations=500, w=None, learningrate=0.1)`

| 参数 | 类型 | 说明 |
|------|------|------|
| `iterations` | int | 梯度下降训练次数。默认 `500`。 |
| `w` | 离散密文数组 | 模型初始权重。默认 `None`。 |
| `learningrate` | float | 学习率。默认 `0.1`。 |

**返回值：** 无（就地设置参数）。

### fit

**签名：** `model.fit(X, y, calloss=False)`

| 参数 | 类型 | 说明 |
|------|------|------|
| `X` | 二维密文数组 | 训练集自变量。 |
| `y` | 密文数组 | 训练集因变量。 |
| `calloss` | bool | 是否计算训练损失。默认 `False`。 |

**返回值：** `self`。

### predict

**签名：** `model.predict(X)`

| 参数 | 类型 | 说明 |
|------|------|------|
| `X` | 二维密文数组 | 测试集自变量。 |

**返回值：** 预测值。

## 示例

```python
import helearn as hl
import henumpy as hp

hp.initDict()

boston = hl.datasets.load_boston()
Weight = hp.ones_array(len(boston.feature_names)+1)

lr = hl.LinearRegression()
lr.set_params(iterations=50, w=Weight, learningrate=0.1)
lr.fit(boston.train_data, boston.train_target)
pred = lr.predict(boston.test_data)
```
