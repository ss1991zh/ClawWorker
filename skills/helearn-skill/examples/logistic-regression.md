# 逻辑回归 — 乳腺癌二分类

基于密文逻辑回归在乳腺癌数据上做二分类：加载密文特征与标签，训练后输出密文预测与阈值划分结果。

## 完整示例

```python
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 加载密文数据
data = hl.load_Breast_cancer()
train_data = data.train_data
train_target = data.train_target
test_data = data.test_data
num_test = test_data.cipherShape()[0]

# 初始密文权重（特征数 + 截距项）
Weight = hp.ones_array(len(data.feature_names) + 1)

# 初始化模型
lr = hl.LogisticRegression()
lr.set_params(iterations=50, w=Weight, learningrate=0.1)

# 密文训练
lr.fit(train_data, train_target)

# 密文预测
c_pre, c_rule = lr.predict(test_data)

# 分类阈值判断（0.5）
divide = hp.empty_array()
for i in range(num_test):
    if (c_rule >= hp.ones() * 0.5)[i]:
        divide = divide.append(hp.ones())
    else:
        divide = divide.append(hp.zeros())
```

## 算法与 API 对照表

| API | 用途 |
|-----|------|
| `hl.LogisticRegression()` | 创建逻辑回归模型 |
| `set_params()` | 设置迭代次数、初始权重、学习率等 |
| `fit()` | 密文模型训练 |
| `predict()` | 密文预测，返回预测值与规则得分等 |
| `hl.load_Breast_cancer()` | 加载乳腺癌数据集（旧版 API） |
| `hp.ones_array()` | 创建全 1 密文数组，用作初始权重 |
