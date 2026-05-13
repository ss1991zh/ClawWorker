# load_boston

加载波士顿房价数据集。

## 签名

```python
hl.datasets.load_boston()
```

## 参数

无。

## 返回值

数据集对象，包含以下属性：

- `train_data`：训练集特征（密文数组）
- `train_target`：训练集标签（密文数组）
- `test_data`：测试集特征（密文数组）
- `feature_names`：特征名称列表

## 示例

```python
import helearn as hl
import henumpy as hp

hp.initDict()

boston = hl.datasets.load_boston()
print(boston.feature_names)
X_train = boston.train_data
y_train = boston.train_target
X_test = boston.test_data
```
