# 测试行加密的效率
import henumpy as hp
import helearn as hl
from helearn.utils.gtimer import gt
import time

def trans_row(x):
    return x.transEncType()

def load():
    gt.start("helearn load data")
    breast_cancer = hl.datasets.load_breast_cancer(data_type="cipher")
    X_train = breast_cancer.train_data
    y_train = breast_cancer.train_target
    X_test = breast_cancer.test_data
    y_test = breast_cancer.test_target
    gt.stop("helearn load data")
    return trans_row(X_train), y_train, trans_row(X_test), y_test

def test_row_gbdt(X_train, y_train, X_test):
    gt.start("gbdt train and pred")
    model = hl.GradientBoostingClassifier(
        learning_rate=0.5,
        n_estimators=6,
        max_depth=8,
        criterion ="friedman_mse",
    )

    model.fit(X=X_train, y=y_train)
    pred, label = model.predict(X=X_test)
    gt.stop("gbdt train and pred")
    return pred, label

def test_row_xgbd(X_train, y_train, X_test):
    gt.start("xgbdt train and pred")
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

    model.fit(X=X_train, y=y_train)
    pred, label = model.predict(X=X_test)
    gt.stop("xgbdt train and pred")
    return pred, label

def test_row_gbrt(X_train, y_train, X_test):
    gt.start("gbrt train and pred")
    model = hl.GradientBoostingRegressor(
        learning_rate = 0.5,
        n_estimators = 6,
        max_depth = 8,
        criterion ="friedman_mse",
    )

    model.fit(X=X_train, y=y_train)
    pred = model.predict(X=X_test)
    gt.stop("gbrt train and pred")
    return pred

def test_row_xgbr(X_train, y_train, X_test):
    gt.start("xgbrt train and pred")
    model = hl.XGBRegressor(
        learning_rate = 0.3,
        n_estimators = 10,
        max_depth = 6,
        lambd = 0.1,
        gamma = 1e-6,
        min_child_weight = 1,
        min_samples_split = 2,
        n_jobs = 6,
    )

    model.fit(X=X_train, y=y_train)
    pred = model.predict(X=X_test)
    gt.stop("xgbrt train and pred")
    return pred

if  __name__ == '__main__':
    hp.initDict()
    X, y, X_t, y_t = load()
    test_row_gbdt(X, y, X_t)
    test_row_xgbd(X, y, X_t)
    test_row_gbrt(X, y, X_t)
    test_row_xgbr(X, y, X_t)
    gt.summary()