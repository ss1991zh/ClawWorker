import henumpy as hp
import numpy as np
from xgboost import XGBClassifier
from sklearn import metrics
import crypto_toolkit as ct
import helearn as hl
import time


# 调用xgboost库的实现
def xgboost_sk(train_data, train_target, test_data):
    model = XGBClassifier(
        learning_rate = 0.3, 
        n_estimators = 10,
        max_depth = 6,
        reg_lambda = 0.1,
        gamma = 1e-6,
        min_child_weight = 1,
        subsample = 1, 
    )
    model.fit(train_data, train_target)
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
    true_value = [int(s) for s in true_value]
    e = time.time()
    print(f"helearn load data time:{e - s:.6f}s")

    model = hl.XGBClassfier(
        learning_rate = 0.3,
        n_estimators =10,
        max_depth=6,
        lambd=0.1,
        gamma=1e-6,
        min_samples_split = 2,
        min_child_weight = 1,
        n_jobs=6,
    )

    # helearn拟合
    s = time.time()
    model.fit(X=X_train, y=y_train)
    e = time.time()
    print(f"helearn train time:{e - s:.6f}s")

    # 计算预测值
    s = time.time()
    pred, label = model.predict(X=X_test)
    e = time.time()
    print(f"helearn predict time:{e - s:.6f}s")

    # 解密预测值以及真实值
    pre = ct.decrypt(pred)
    lab = ct.decrypt(label)
    # print(pre, lab)
    lab = [1 if s > 0.5 else 0 for s in lab]
    # print(lab)
    p_cipher = metrics.accuracy_score(np.array(true_value), np.array(lab))
    r_cipher = metrics.recall_score(np.array(true_value), np.array(lab))
    print(f"基于 HEnumpy 的XGBOOST分类准确率: (accuracy) {p_cipher}, (recall) {r_cipher}")

    # 明文数据路径
    breast_plain = hl.datasets.load_breast_cancer(data_type="plain")
 
    # sklearn拟合
    res_sklearn = xgboost_sk(breast_plain.train_data, breast_plain.train_target.ravel(), breast_plain.test_data)
    res_sklearn = res_sklearn.reshape(1,len(res_sklearn))[0]
    p_sklearn = metrics.accuracy_score(np.array(true_value), res_sklearn)
    r_sklearn = metrics.recall_score(np.array(true_value), res_sklearn)
    print(f"基于 Xgboost 原生的分类准确率: (accuracy) {p_sklearn}, (recall) {r_sklearn}")
