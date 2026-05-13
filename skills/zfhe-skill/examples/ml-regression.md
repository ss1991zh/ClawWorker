# 示例：密文机器学习回归

> 用户需求："对加密的房价数据做回归预测"

**路由结果**：helearn 单独  
**数据源**：helearn 内置数据集  
**任务类型**：ML 回归

```python
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# ── 加载密文数据集 ──
data = hl.datasets.load_boston()
assert data.train_data is not None, "训练数据加载失败"
assert data.train_target is not None, "训练标签加载失败"

X_train = data.train_data
y_train = data.train_target
X_test = data.test_data

print("波士顿房价数据加载完成")

# ── 方案一：XGBoost 回归 ──
print("\n=== XGBoost 回归 ===")
xgb_model = hl.XGBRegressor(
    learning_rate=0.3,
    n_estimators=10,
    max_depth=6
)
xgb_model.fit(X=X_train, y=y_train)
xgb_pred = xgb_model.predict(X=X_test)

print(f"XGBoost 预测: {ct.decrypt_ndarray(xgb_pred)}")

# ── 方案二：GBRT 回归 ──
print("\n=== GBRT 回归 ===")
gbrt_model = hl.GradientBoostingRegressor(
    learning_rate=0.1,
    n_estimators=3,
    max_depth=6,
    criterion="friedman_mse"
)
gbrt_model.fit(X=X_train, y=y_train)
gbrt_pred = gbrt_model.predict(X=X_test)

print(f"GBRT 预测: {ct.decrypt_ndarray(gbrt_pred)}")

# ── 方案三：线性回归 ──
print("\n=== 线性回归 ===")
lr_model = hl.LinearRegression()
lr_model.set_params(iterations=100, w=0.01, learningrate=0.01)
lr_model.fit(X=X_train, y=y_train)
lr_pred = lr_model.predict(X=X_test)

print(f"线性回归预测: {ct.decrypt_ndarray(lr_pred)}")

# 注意：同态加密计算结果存在浮点精度误差，这是 FHE 的固有特性，非 bug。
```
