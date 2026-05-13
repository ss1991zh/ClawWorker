import henumpy as hp
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import crypto_toolkit as ct
import helearn as hl
import time


# 调用sklearn库的实现
def gbrt_sklearn(train_data, train_target, test_data):
    model = GradientBoostingRegressor(
        learning_rate = 0.5, 
        n_estimators = 6,
        max_depth = 8,
        min_samples_split = 2,
        subsample = 1, 
    )
    s = time.time()
    model.fit(train_data, train_target)
    e = time.time()
    print(f"sklearn train time:{e - s:.6f}s")
    res = model.predict(test_data)
    return res

if __name__ == "__main__":
    # 初始化字典以及私钥
    hp.initDict()
    ct.initSK()

    # 加载密文数据
    s = time.time()
    breast_cancer = hl.datasets.load_breast_cancer(data_type="cipher")
    X_train = breast_cancer.train_data
    y_train = breast_cancer.train_target
    X_test = breast_cancer.test_data
    y_test = breast_cancer.test_target

    true_value = ct.decrypt(y_test)
    e = time.time()
    print(f"helearn load data time:{e - s:.6f}s")

    model = hl.GradientBoostingRegressor(
        learning_rate = 0.5,
        n_estimators = 6,
        max_depth = 8,
        criterion ="friedman_mse",
    )

    # helearn拟合
    s = time.time()
    model.fit(X=X_train, y=y_train)
    e = time.time()
    print(f"helearn train time:{e - s:.6f}s")

    # 计算预测值
    s = time.time()
    pred = model.predict(X=X_test)
    e = time.time()
    print(f"helearn predict time:{e - s:.6f}s")

    # 解密预测值以及真实值
    pre = ct.decrypt(pred)
    mae_cipher_gbdt = np.mean(np.abs(np.array(pre) - np.array(true_value)))
    mse_cipher_gbdt = np.mean((np.array(pre) - np.array(true_value))**2) / len(pre)
    print(f"基于 HEnumpy 的GBRT回归准确率: (mae) {mae_cipher_gbdt}, (mse) {mse_cipher_gbdt}")

    # 明文数据路径
    breast_plain = hl.datasets.load_breast_cancer(data_type="plain")
 
    # sklearn拟合
    res_sklearn = gbrt_sklearn(breast_plain.train_data, breast_plain.train_target.ravel(), breast_plain.test_data)
    res_sklearn = res_sklearn.reshape(1,len(res_sklearn))[0]
    mae_sklearn_gbrt = np.mean(np.abs(res_sklearn - true_value))
    mse_sklearn_gbrt = np.mean((res_sklearn - np.array(true_value))**2) / len(res_sklearn)
    print(f"基于 sklearn 的GBRT回归准确率: (mae) {mae_sklearn_gbrt}, (mse) {mse_sklearn_gbrt}")
