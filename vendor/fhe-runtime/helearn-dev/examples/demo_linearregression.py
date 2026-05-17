import numpy as np
import henumpy as hp
import crypto_toolkit as ct
import helearn as hl
import time
from sklearn import linear_model

# 调用sklearn库的实现做对比
def linearregression_sklearn(train_data, train_target, test_data):
    model = linear_model.LinearRegression()
    model.fit(train_data, train_target)
    res = model.predict(test_data)
    return res

if __name__ == "__main__":
    
    # 初始化字典以及私钥
    hp.initDict()
    ct.initSK()

    # 加载密文数据
    begin_time = time.time()
    boston = hl.datasets.load_boston(data_type="cipher")
    end_time = time.time()
    t_load_cipher_data = end_time - begin_time # 加载数据时间
    
    # 初始权重明文
    init_w = np.asarray([0.5]*(len(boston.feature_names)+1))
    # 加密明文权重
    Weight = ct.encrypt(init_w, discrete=True)
    # 初始化类参数
    lr = hl.LinearRegression()
    lr.set_params(iterations=50,w=Weight,learningrate=0.1)
    
    # helearn拟合
    begin_time = time.time() # 计时开始
    lr.fit(boston.train_data, boston.train_target)
    end_time = time.time() # 计时结束
    t_train = end_time - begin_time # 模型训练时间

    # 计算预测值
    begin_time = time.time() # 计时开始
    c_pre = lr.predict(boston.test_data)
    end_time = time.time() # 计时结束
    t_predict = end_time - begin_time

    # 解密预测值以及真实值
    pre = ct.decrypt(c_pre)
    true_value = ct.decrypt(boston.test_target)
    
    # sklearn拟合
    boston_plain = hl.datasets.load_boston(data_type="plain")
    res_sklearn = linearregression_sklearn(boston_plain.train_data, 
                                           boston_plain.train_target, 
                                           boston_plain.test_data)

    # 计算MAE
    res_sklearn = res_sklearn.reshape(1,len(res_sklearn))[0]
    mae_cipher_lr = np.mean(np.abs(pre - true_value))
    mae_sklearn_lr = np.mean(np.abs(res_sklearn - true_value))

    # 输出结果
    print("helearn load data time:\t%fs"%(t_load_cipher_data))
    print("helearn train time:\t%fs"%(t_train))
    print("helearn predict time:\t%fs"%(t_predict))
    print("helearn MAE:\t%f"%(mae_cipher_lr))
    print("sklearn MAE:\t%f"%(mae_sklearn_lr))
    print("Detailed comparison:\nhelearn_lr_result\tsklearn_lr_result\treal_value")
    for i in range(len(pre)):
        print("%.16f\t%.16f\t%.16f"%(pre[i], res_sklearn[i], true_value[i]))