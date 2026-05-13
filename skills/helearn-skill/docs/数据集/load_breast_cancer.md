# load_breast_cancer

加载乳腺癌数据集，支持密文和明文两种模式。

## 签名

```python
hl.datasets.load_breast_cancer(data_type="cipher")
```

也可使用旧版 API：

```python
hl.load_Breast_cancer()
```

## 参数

- `data_type`：str，数据类型。`"cipher"` 返回密文数据，省略则返回需要手动加密的数据。

## 返回值

数据集对象，包含以下属性：

- `train_data`：训练集特征（密文数组）
- `train_target`：训练集标签（密文数组）
- `test_data`：测试集特征（密文数组）
- `test_target`：测试集标签（密文数组，仅 `data_type="cipher"` 时）
- `feature_names`：特征名称列表（仅旧版 API）

## 示例

```python
import helearn as hl
import henumpy as hp

hp.initDict()

# 方式一：直接加载密文数据
data = hl.datasets.load_breast_cancer(data_type="cipher")
X_train = data.train_data
y_train = data.train_target

# 方式二：加载后手动处理
data = hl.load_Breast_cancer()
X_train = data.train_data
y_train = data.train_target
```
