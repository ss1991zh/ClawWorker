import helearn as hl
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
import henumpy as hp
import crypto_toolkit as ct
from sklearn import linear_model
warnings.filterwarnings("ignore")

# 调用sklearn库的实现
def logicalregression_sklearn(train_data, train_target, test_data):
    model = linear_model.LogisticRegression()
    model.fit(train_data, train_target)
    res = model.predict(test_data)
    return res


if __name__ == "__main__":
    # 初始化字典以及私钥
    hp.initDict()
    ct.initSK()

    # 加载密文数据
    begin_time = time.time() # 计时开始
    Breast_cancer = hl.load_breast_cancer(data_type="cipher")
    end_time = time.time() # 计时结束
    load_data_time_helearn = end_time - begin_time

    # 初始权重明文
    init_w = np.asarray([0.5]*(len(Breast_cancer.feature_names)+1))
    # 加密明文权重
    Weight = ct.encrypt(init_w, discrete=True)
    # 初始化类参数
    lr = hl.LogisticRegression()
    lr.set_params(iterations=50,w=Weight,learningrate=0.1)

    # helearn拟合
    begin_time = time.time() # 计时开始
    l, loss = lr.fit(Breast_cancer.train_data, Breast_cancer.train_target, True)
    end_time = time.time() # 计时结束
    loss_plain = ct.decrypt(hp.CipherArray(loss, discrete=True), discrete=True)
    train_time_helearn = end_time-begin_time

    # 计算得分
    begin_time = time.time() # 计时开始
    c_pre, c_rule = lr.predict(Breast_cancer.test_data)
    end_time = time.time() # 计时结束
    predict_time_helearn = end_time-begin_time

    # 分类
    divide = hp.empty_array()
    num_test = Breast_cancer.test_data.cipherShape()[0]
    for i in range(num_test): 
        if (c_rule >= hp.ones()*0.5)[i]:
            divide = divide.append(hp.ones())
        else :
            divide = divide.append(hp.zeros())

    # 计算准确率
    temp = 0
    for i in range(num_test):
        if divide[i] == Breast_cancer.test_target[i]:
                temp = temp + 1
    helearn_accuracy = temp / num_test

    # sklearn拟合并预测
    breast_cancer_plain = hl.datasets.load_breast_cancer(data_type="plain")
    y_pred = logicalregression_sklearn(breast_cancer_plain.train_data, 
                                                 breast_cancer_plain.train_target, 
                                                 breast_cancer_plain.test_data)
    #计算准确率
    temp = 0
    for i in range(50):
        if y_pred[i] == breast_cancer_plain.test_target[i]:
            temp = temp + 1
    sklearn_accuracy = temp / 50

    # 打印Helearn计算时间
    print("helearn load data time:\t%fs"%load_data_time_helearn)
    print("helearn train time:\t%fs"%train_time_helearn)
    print("helearn predict time:\t%fs"%predict_time_helearn)
    print("基于 HENumpy 的逻辑回归准确率:\t%f"%helearn_accuracy)
    print("基于 sklearn 的逻辑回归准确率:\t%f"%sklearn_accuracy)

    # 打印损失函数
    plt.plot(loss_plain)
    plt.show()

