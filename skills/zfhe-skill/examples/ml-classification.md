# 示例：密文机器学习分类

> 用户需求："用加密数据训练一个乳腺癌分类器"

**路由结果**：helearn 单独  
**数据源**：helearn 内置数据集  
**任务类型**：ML 分类

```python
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# ── 加载密文数据集 ──
data = hl.datasets.load_breast_cancer(data_type="cipher")
assert data.train_data is not None, "训练数据加载失败"
assert data.train_target is not None, "训练标签加载失败"

X_train = data.train_data
y_train = data.train_target
X_test = data.test_data

print("数据加载完成")

# ── 方案一：XGBoost 分类 ──
print("\n=== XGBoost 分类 ===")
xgb_model = hl.XGBClassfier(
    learning_rate=0.3,
    n_estimators=10,
    max_depth=6
)
xgb_model.fit(X=X_train, y=y_train)
xgb_pred, xgb_label = xgb_model.predict(X=X_test)  # 分类模型返回 (预测值, 标签)

print(f"XGBoost 预测结果: {ct.decrypt_ndarray(xgb_pred)}")
print(f"XGBoost 预测标签: {ct.decrypt_ndarray(xgb_label)}")

# ── 方案二：GBDT 分类 ──
print("\n=== GBDT 分类 ===")
gbdt_model = hl.GradientBoostingClassifier(
    learning_rate=0.1,
    n_estimators=3,
    max_depth=6,
    criterion="friedman_mse"
)
gbdt_model.fit(X=X_train, y=y_train)
gbdt_pred, gbdt_label = gbdt_model.predict(X=X_test)

print(f"GBDT 预测结果: {ct.decrypt_ndarray(gbdt_pred)}")
print(f"GBDT 预测标签: {ct.decrypt_ndarray(gbdt_label)}")

# ── 方案三：逻辑回归 ──
print("\n=== 逻辑回归 ===")
lr_model = hl.LogisticRegression()
lr_model.set_params(iterations=100, w=0.01, learningrate=0.01)
lr_model.fit(X=X_train, y=y_train)
lr_pred, lr_label = lr_model.predict(X=X_test)

print(f"LR 预测结果: {ct.decrypt_ndarray(lr_pred)}")
print(f"LR 预测标签: {ct.decrypt_ndarray(lr_label)}")

# 注意：同态加密计算结果存在浮点精度误差，这是 FHE 的固有特性，非 bug。
```
