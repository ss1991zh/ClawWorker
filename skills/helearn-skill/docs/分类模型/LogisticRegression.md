# LogisticRegression

密文逻辑回归（二分类），使用 sigmoid 激活函数，通过梯度下降最小化交叉熵损失。

## 初始化

```python
hl.LogisticRegression()
```

## 方法

### set_params

```python
model.set_params(iterations=500, w=None, learningrate=0.1)
```

- `iterations`：int，梯度下降训练次数。默认 `500`。
- `w`：离散密文数组，模型初始权重。默认 `None`。
- `learningrate`：float，学习率。默认 `0.1`。

### fit

```python
model.fit(X, y, calloss=False)
```

- `X`：二维密文数组，训练集自变量。
- `y`：密文数组，训练集因变量。
- `calloss`：bool，是否计算训练过程中的损失。默认 `False`。
- **返回值**：self。

### predict

```python
model.predict(X)
```

- `X`：二维密文数组，测试集自变量。
- **返回值**：`(predict_result, activation)` — 预测值和激活函数值（sigmoid 输出）。

## 示例

```python
import helearn as hl
import henumpy as hp

hp.initDict()

data = hl.load_Breast_cancer()
Weight = hp.ones_array(len(data.feature_names) + 1)

lr = hl.LogisticRegression()
lr.set_params(iterations=50, w=Weight, learningrate=0.1)
lr.fit(data.train_data, data.train_target)
pred, activation = lr.predict(data.test_data)
```
