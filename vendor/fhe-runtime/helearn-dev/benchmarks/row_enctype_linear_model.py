# 测试行加密的效率
import henumpy as hp
import helearn as hl
import time

def load_boston():
    start_time_load = time.time()
    breast_cancer = hl.datasets.load_boston(data_type="cipher")
    X_train = (breast_cancer.train_data).transEncType()
    y_train = breast_cancer.train_target
    X_test = (breast_cancer.test_data).transEncType()
    y_test = breast_cancer.test_target
    end_time_load = time.time()
    print("load boston data time:\t%fs"%(end_time_load - start_time_load) )
    return X_train, y_train, X_test, y_test

def load_breast_cancer():
    start_time_load = time.time()
    breast_cancer = hl.datasets.load_breast_cancer(data_type="cipher")
    X_train = (breast_cancer.train_data).transEncType()
    y_train = breast_cancer.train_target
    X_test = (breast_cancer.test_data).transEncType()
    y_test = breast_cancer.test_target
    end_time_load = time.time()
    print("load breast cancer data time:\t%fs"%(end_time_load - start_time_load) )
    return X_train, y_train, X_test, y_test

def test_row_lr(X_train, y_train, X_test):
    start_time_train_and_pre = time.time()
    model = hl.LinearRegression(
        iterations=50
    )
    model.fit(X_train, y_train)
    pre = model.predict(X_test)
    end_time_train_and_pre = time.time()
    print("LinearRegression model train and predict time:\t%fs"%(end_time_train_and_pre - start_time_train_and_pre))
    return model, pre

def test_row_logicalr(X_train, y_train, X_test):
    start_time_train_and_pre = time.time()
    model = hl.LogisticRegression(
        iterations=50
    )
    model.fit(X_train, y_train)
    pre = model.predict(X_test)
    end_time_train_and_pre = time.time()
    print("LogisticRegression model train and predict time:\t%fs"%(end_time_train_and_pre - start_time_train_and_pre))
    return model, pre

if __name__ == "__main__":
    hp.initDict()
    # 测试线性回归
    X_train, Y_train, X_test, Y_test = load_boston()
    test_row_lr(X_train, Y_train, X_test)
    # 测试逻辑回归
    X_train, Y_train, X_test, Y_test = load_breast_cancer()
    test_row_logicalr(X_train, Y_train, X_test)
