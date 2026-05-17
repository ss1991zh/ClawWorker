#线性回归模型

import numpy as np
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path = list(set(sys.path))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import henumpy as hp

from helearn.base.base_estimator import *
from helearn.utils.csv_parsers import *
from helearn.base.base_function import *


class LinearRegression(BaseEstimator):

    def __init__(
        self,
        # fit_intercept=True,
        # normalize="deprecated",
        # copy_X=True,
        # n_jobs=None,
        # positive=False,
        iterations=500,
        learningrate=0.1,
        w=None
    ):
        '''
        初始化线性回归模型。
        
        已支持参数：
        ---------
        iterations : int, default=500
            梯度下降训练次数
        learningrate : float, 默认值0.1
            学习率, 用于更新权重
        w : CipherArray(离散密文数组), 默认值为None
            线性模型权重

        未支持参数：
        ---------
        fit_intercept : bool,  默认值True
            是否计算此模型的截距。如果设置为False,则在计算中将不使用截距(即数据应居中)。
        normalize : bool, 默认值False
            当'fit_intercept'设置为False时,此参数将被忽略。
            如果为True,则回归量X将在回归前通过减去平均值并除以l2-norm.进行标准化。
        copy_X : bool, 默认值True
            如果为True,则X将被复制;否则,它可能会被覆盖。
        n_jobs : int, 默认值None
            用于计算的作业数。这只会在足够大的问题的情况下提供加速，
            即如果首先'n_targets>1',其次'X'是稀疏的,或者如果'positive'设置为'True'``无``表示1,
            除非在:obj:`joblib.pallel_backend`上下文中``-1''表示使用所有处理器。
        positive : bool, 默认值False
            当设置为'True'时,强制系数为正。此选项仅适用于密集阵列。
        
        返回值：
        ---------
        无返回值
        '''
        # self.fit_intercept = fit_intercept
        # self.normalize = normalize
        # self.copy_X = copy_X
        # self.n_jobs = n_jobs
        # self.positive = positive
        self.__w = w if w is not None else np.array([])
        self.__iterations = iterations
        self.__learningrate = learningrate
    

    # 拟合函数
    def fit(self, X, y, calloss=False):
        '''
        参数:
        -----------
        X : 一维数组类型的密文数组 [[cipherfloatarray1], [cipherfloatarray2]] 不包含全1列
            因变量
        y : 密文数组类型 [cipherfloatarray]
            自变量
        calloss: bool 型，是否计算训练过程中的损失，默认为 False
            
        返回值:
        --------
        self : object
            返回自身
        '''
        data_rows = X.cipherShape()[0] # 数据条数
        feature_num = X.cipherShape()[1] # 特征数
        # 在训练数据的最后一列插入1的密文
        ones = hp.ones_array(data_rows)
        X = hp.insert(X, feature_num, ones, axis=1)
        feature_num += 1
        # X = hp.CipherArray(X)
        # 检查是否传入初始权重密文
        # 初始化权重
        if len(self.__w) == 0:
            cc1 = hp.ones()
            self.__init_weight(cc1, feature_num)
        
        # 训练参数
        if calloss == True:# 需要计算每次迭代的损失
            loss_array = []
            for i in range(0, self.__iterations):
                self.__w = self.__cipher_gradient_descent(X, y, self.__w, self.__learningrate)
                wx = hp.zeros_array(data_rows)
                for i in range(0, feature_num):
                    # 获取权重密文
                    wi = self.__w[i]
                    # wi = hp.CipherArray([self.__w[i*5+0], self.__w[i*5+1], self.__w[i*5+2], self.__w[i*5+3], self.__w[i*5+4]])
                    # 计算w*x,输入值（标量密文，向量密文）
                    temp = hp.mul(wi, X[:,i])
                    # 计算Σw*x
                    wx = hp.add(temp, wx)
                #loss = hp.div(hp.sum(hp.mul(hp.sub(wx, y), hp.sub(wx, y))), float(data_rows))
                #loss = hp.sum((wx-y)**2)/float(data_rows)
                loss = hp.sum((wx-y)*(wx-y))/float(data_rows)
                loss_array = loss_array + loss.tolist()
            return self, np.array(loss_array)
        else:
            for i in range(0, self.__iterations):
                self.__w = self.__cipher_gradient_descent(X, y, self.__w, self.__learningrate)
            return self

    # 预测函数
    def predict(self, X):
        '''
        参数:
        -----------
        X:CipherFloat-array [cipherfloat1, cipherfloat2, cipherfloat3]
        返回值:
        --------
        predict result:cipherfloat
        '''
        data_rows = X.cipherShape()[0] # 数据条数
        feature_num = X.cipherShape()[1] # 特征数
        # 在X的末尾插入1的密文
        ones = hp.ones_array(data_rows)
        X = hp.insert(X, feature_num, ones, axis=1)
        feature_num += 1
        X = hp.CipherArray(X)
        wx = hp.zeros_array(data_rows)
        for i in range(0, feature_num):
            # 获取权重密文
            wi = self.__w[i]
            # wi = hp.CipherArray([self.__w[i*5+0], self.__w[i*5+1], self.__w[i*5+2], self.__w[i*5+3],self.__w[i*5+4]])
            # 计算w*x,输入值（标量密文，向量密文）
            temp = hp.mul(wi, X[:,i])
            # 计算Σw*x
            wx = hp.add(temp, wx)
        return wx

    def get_params(self, deep=True):
        '''获取模型参数'''
        return self.__w
    
    def set_params(self, **params):
        '''设置模型参数'''
        for key in params:
            if key == "iterations":
                self.__iterations = params[key]
            if key == "learningrate":
                self.__learningrate = params[key]
            if key == "w":
                self.__w = params[key]

    def __cipher_gradient_descent(self, X, Y, Weight, LearningRate):
        """
        密文梯度下降算法
        参数
        -------
        X:密文训练数据的因变量  n列数据(n,l)
        Y:密文训练数据的自变量
        Weight:密文权重 为一维数组[c1.X1,c1.X2,c1.Y1,c1.Y2,c1.A,c2.X1,c2.X2,c2.Y1,c2.Y2,c2.A] 
        LearningRate:学习率

        返回值
        -------
        更新后的权重
        """
        # X.shape = (特征值个数，数据条数+5)
        data_rows = X.cipherShape()[0] # 数据条数
        feature_num = X.cipherShape()[1] # 特征数
        # 新建一个长度为数据条数的密文0数组 用于保存fx 
        wx = hp.zeros_array(data_rows)
        # 计算fx
        for i in range(0, feature_num):
            # 获取权重密文
            #print(self.__w, i)
            wi = Weight[i]
            # wi = hp.CipherArray([self.__w[i*5+0], self.__w[i*5+1], self.__w[i*5+2], self.__w[i*5+3], self.__w[i*5+4]])
            # 计算w*x,输入值（标量密文，向量密文）
            temp = hp.mul(wi, X[:,i])
            # 计算Σw*x
            wx = hp.add(temp, wx)

        # 计算wi的梯度(2/n)*x(wx-y),然后更新梯度
        temp = hp.sub(wx, Y)
        for i in range(0, feature_num):
            temp1 = hp.mul(X[:,i], temp)
            # 组内求和计算梯度
            gradient = hp.sum(temp1)
            # 乘以2/n
            gradient = hp.mul(gradient, 2/data_rows)
            Wi = Weight[i]
            # Wi = hp.CipherArray([Weight[i*5+0], Weight[i*5+1], Weight[i*5+2], Weight[i*5+3], Weight[i*5+4]])
            # 梯度乘以学习率(密文，明文)
            gradient = hp.mul(gradient, LearningRate)
            # 更新权重
            Wi = hp.sub(Wi, gradient)
            # Wi = Wi.get_base_array()
            # for j in range(0,5):
                # Weight[i*5+j] = Wi[j]
            Weight[i] = Wi
            #print("权重", Weight)
        return Weight
    
    def __init_weight(self, cc1, n):
        """
        初始化初始权重密文[0.5]
        参数
        -------
        cc1:1的标量密文 ndarray
        n: 权重的个数 int

        返回值
        -------
        self
        """
        c = hp.mul(cc1, 0.5)
        for i in range(n):
            self.__w = np.append(self.__w, c)
        self.__w = hp.CipherArray(self.__w, discrete=True)
        return self

if __name__ == "__main__":
    
    from helearn.datasets import *
    import crypto_toolkit as ct
    # 初始化字典以及私钥
    hp.initDict()
    ct.initSK()

    # 加载密文数据
    boston = load_boston()
    train_data = boston.train_data
    train_target = boston.train_target
    test_data = boston.test_data
    test_target = boston.test_target
    
    # 初始权重明文
    init_w = np.asarray([0.5]*(len(boston.feature_names)+1))
    # 加密明文权重
    Weight = ct.encrypt(init_w, discrete=True)
    # 初始化类参数
    lr = LinearRegression()
    lr.set_params(iterations=10,w=Weight,learningrate=0.1)
    
    # helearn拟合
    lr.fit(train_data, train_target)
    
    # 计算预测值
    c_pre = lr.predict(test_data)
    
    # 解密预测值以及真实值
    pre = ct.decrypt(c_pre)
    true_value = ct.decrypt(test_target)
    
    mae_cipher_lr = np.mean(np.abs(pre - true_value))
    print("helearn MAE:%f"%(mae_cipher_lr))