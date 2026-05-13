# 线性回归 — 波士顿房价预测

使用密文线性回归在加密特征上训练模型，并预测波士顿房价测试集。

## 完整示例

以下脚本从数据加载到预测可在同一环境中直接运行；需先完成同态环境初始化。

```python
import helearn as hl
import henumpy as hp

hp.initDict()

boston = hl.datasets.load_boston()
train_data = boston.train_data
train_target = boston.train_target
test_data = boston.test_data

Weight = hp.ones_array(len(boston.feature_names) + 1)

lr = hl.LinearRegression()
lr.set_params(iterations=50, w=Weight, learningrate=0.1)

lr.fit(train_data, train_target)

pred = lr.predict(test_data)
```

## 使用的 API

| API | 用途 |
|-----|------|
| `hp.initDict()` | 初始化 henumpy 同态字典（脚本入口必调） |
| `hl.datasets.load_boston()` | 加载波士顿房价密文数据集 |
| `hp.ones_array()` | 构造全 1 密文向量，作为初始权重 |
| `hl.LinearRegression()` | 创建密文线性回归模型 |
| `set_params()` | 设置迭代次数、初始权重、学习率等训练参数 |
| `fit()` | 在密文训练集上训练 |
| `predict()` | 对密文测试特征做预测 |
