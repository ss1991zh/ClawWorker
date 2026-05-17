import henumpy as hp
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
import crypto_toolkit as ct
import helearn as hl
import time


# 调用sklearn库的实现
def gbdt_sklearn(train_data, train_target, test_data):
    model = GradientBoostingClassifier(
        learning_rate = 0.5, 
        n_estimators = 6,
        max_depth = 8,
        min_samples_split = 2,
        subsample = 1, 
    )
    model.fit(train_data, train_target)
    s = time.time()
    res = model.predict(test_data)
    e = time.time()
    print(f"sklearn train time:{e - s:.6f}s")
    return res

if __name__ == "__main__":
    # 初始化字典以及私钥
    hp.initDict()
    ct.initSK()

    # 加载密文数据
    breast_cancer = hl.datasets.load_breast_cancer(data_type="cipher")
    X_train = breast_cancer.train_data
    y_train = breast_cancer.train_target
    X_test = breast_cancer.test_data
    y_test = breast_cancer.test_target
 
    true_value = ct.decrypt(y_test)
    true_value = [int(s) for s in true_value]

    model = hl.GradientBoostingClassifier(
        learning_rate=0.5,
        n_estimators=6,
        max_depth=8,
        criterion ="friedman_mse",
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
    lab = [1 if s > 0.5 else 0 for s in lab] 
    p_cipher = metrics.accuracy_score(np.array(true_value), np.array(lab))
    r_cipher = metrics.recall_score(np.array(true_value), np.array(lab))
    print(f"基于 HEnumpy 的GBDT分类准确率: (accuracy) {p_cipher}, (recall) {r_cipher}")

    # 明文数据路径
    breast_plain = hl.datasets.load_breast_cancer(data_type="plain")
    
    # sklearn拟合
    res_sklearn = gbdt_sklearn(breast_plain.train_data, breast_plain.train_target.ravel(), breast_plain.test_data)
    res_sklearn = res_sklearn.reshape(1, len(res_sklearn))[0]
    p_sklearn = metrics.accuracy_score(np.array(true_value), res_sklearn)
    r_sklearn = metrics.recall_score(np.array(true_value), res_sklearn)
    print(f"基于 sklearn 的GBDT分类准确率: (accuracy) {p_sklearn}, (recall) {r_sklearn}")

