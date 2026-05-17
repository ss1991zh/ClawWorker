#逻辑回归模型

import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path = list(set(sys.path))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import henumpy as hp

from helearn.base.base_estimator import *
from helearn.utils.csv_parsers import *
from helearn.base.base_function import *


class LogisticRegression(BaseEstimator):

    def __init__(
        self,
        # penalty="L2",
        # dual=False,
        # tol=1e-4,
        # C=1.0
        # fit_intercept=True,
        # intercept_scaling=1,
        # class_weight=None,
        # random_state=Noen,
        # solver="lbfgs",
        # multi_class="auto",
        # verbose=0,
        # warm_start=False,
        # n_jobs=None,
        # l1_ratio=None,
        iterations=500,
        learningrate=0.1,
        w=None
    ):
        '''
        初始化逻辑回归模型。
        
        已支持参数：
        ---------
        iterations : int, default=500
            梯度下降训练次数
        learningrate : float, default=0.1
            学习率, 用于更新权重
        w : ndarray(离散密文数组), default=None
            线性模型权重

        未支持参数：
        ----------
        penalty : {'L1', 'L2', 'elasticnet', 'none'}, default='L2'
            用于指定处罚中使用的规范。'newton-cg','sag'和'lbfgs'求解器仅支持L2惩罚。仅'saga'求解器支持'elasticnet'。如果为'none'(liblinear求解器不支持),则不应用任何正则化。
        dual : bool, 默认值False
            是否对偶化。仅对liblinear求解器使用L2惩罚时进行对偶化。当n_samples > n_features时,首选dual = False。
        tol : float,默认值1e-4
            停止迭代的容差标准。
        C : float, default=1.0
            正则强度的倒数；必须为正浮点数。与支持向量机一样,较小的值指定更强的正则化。
        fit_intercept : bool, default=True
            是否将常量(aka偏置或截距)添加到决策函数。
        intercept_scaling : float, default=1
            仅在使用求解器'liblinear'并将self.fit_intercept设置为True时有用。在这种情况下,x变为[x,self.intercept_scaling],即将常量值等于intercept_scaling的'合成'特征附加到实例矢量。截距变为intercept_scaling * synthetic_feature_weight。        
        class_weight : dict or 'balanced', default=None
            以{class_label: weight}的形式与类别关联的权重。如果没有给出,所有类别的权重都应该是1。
            'balanced'模式使用y的值来自动调整为与输入数据中的类频率成反比的权重。如n_samples / (n_classes * np.bincount(y))。
        random_state : int, RandomState instance, default=None
            在solver=='sag','saga'或'liblinear'时,用于随机整理数据。
        solver : {'newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'}, default='lbfgs'
            用于优化问题的算法。
            - 对于小型数据集,' liblinear'是一个不错的选择,而对于大型数据集,' sag'和' saga'更快。
            - 对于多类分类问题,只有'newton-cg' ,'sag','saga' 和 'lbfgs' 处理多项式损失。'liblinear'仅限于'一站式'计划。
            - 'newton-cg','lbfgs','sag'和'saga'处理L2或不惩罚。
            - 'liblinear'和'saga'也可以处理L1罚款。
            - ' saga'还支持' elasticnet'惩罚。
            - 'liblinear'不支持设置 penalty='none'。
        multi_class : {'auto', 'ovr', 'multinomial'}, default='auto'
            如果选择的选项是' ovr',则每个标签都看做二分类问题。对于'multinomial',即使数据是二分类的,损失最小是多项式损失拟合整个概率分布。当solver ='liblinear' 时, 'multinomial' 不可用。如果数据是二分类的,或者如果Solver ='liblinear',则'auto'选择'ovr',否则选择'multinomial'。
        verbose : int, default=0
            对于liblinear和lbfgs求解器,将verbose设置为任何正数以表示输出日志的详细程度。
        warm_start : bool, default=False
            设置为True时,重用前面调用的解决方案来进行初始化,否则,只清除前面的解决方案。这个参数对于线性求解器无用。
        n_jobs : int, default=None
            当multi_class ='ovr',在对类进行并行化时使用的CPU内核数。将solver设置为'liblinear'时,无论是否指定'multi_class' ,都将忽略此参数。除非设置了joblib.parallel_backend 参数,否则None表示1 。 -1表示使用所有处理器。
        l1_ratio : float, default=None
            Elastic-Net混合参数,取值范围0 <= l1_ratio <= 1。仅在penalty='elasticnet'时使用。设置l1_ratio=0等同于使用penalty='l2',而设置l1_ratio=1等同于使用penalty='l1'。对于0 < l1_ratio <1,惩罚是L1和L2的组合。
        返回值：
        ---------
        无返回值
        '''
        self.__w = w if w is not None else np.array([])
        self.__iterations = iterations
        self.__learningrate = learningrate
    

    # 拟合函数
    def fit(self, X, y, calloss=False):
        '''
        参数:
        -----------
        X : 二维密文数组,CipherArray
            因变量
        y : 密文数组类型,CipherArray
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
        X = hp.CipherArray(X)
        # 检查是否传入初始权重密文
        # 初始化权重
        if len(self.__w) == 0:
            cc1 = hp.ones()
            self.__init_weight(cc1, feature_num)
        
        # 训练参数
        if calloss == True:# 需要计算每次迭代的损失
            loss = hp.zeros()
            loss_array = []
            for i in range(0, self.__iterations):
                self.__w = self.__cipher_gradient_descent(X, y, self.__w, self.__learningrate)
                wx = hp.zeros_array(data_rows)
                for i in range(0, feature_num):
                    # 获取权重密文
                    wi = self.__w[i]
                    # wi = hp.CipherArray([self.__w[i*5+0], self.__w[i*5+1], self.__w[i*5+2], self.__w[i*5+3], self.__w[i*5+4]])
                    # 计算w*x,输入值（标量密文,向量密文）
                    temp = hp.mul(wi, X[:,i])
                    # 计算Σw*x
                    wx = hp.add(temp, wx)
                # 计算损失
                """
                for i in range(0, data_rows):
                    loss = loss + (y[i] * wx[i] - hp.log(hp.exp(wx[i]) + hp.ones()))
                loss = - loss / data_rows 
                """
                loss = - hp.sum(y * wx - hp.log(hp.exp(wx)+hp.ones()))/data_rows
                loss_array = loss_array + loss.tolist()
            return self, np.array(loss_array)
        else:
            for i in range(0, self.__iterations):
                self.__w = self.__cipher_gradient_descent(X, y, self.__w, self.__learningrate)
            return self

    # 计算得分, 激活函数
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
            # 计算w*x,输入值（标量密文,向量密文）
            temp = hp.mul(wi, X[:,i])
            # 计算Σw*x
            wx = hp.add(temp, wx)
        """
        relu = hp.empty_array()
        for i in range(0, data_rows):
            relu = relu.append(hp.ones() / (hp.ones() + hp.exp((-wx[i]))))
        """
        relu = hp.ones() / (hp.exp((-wx)) + hp.ones())
        return wx, relu

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
        # X.shape = (特征值个数,数据条数+5)
        data_rows = X.cipherShape()[0] # 数据条数
        feature_num = X.cipherShape()[1] # 特征数
        # 新建一个长度为数据条数的密文0数组 用于保存fx 
        wx = hp.zeros_array(data_rows)
        # 计算fx
        for i in range(0, feature_num):
            # 获取权重密文
            wi = Weight[i]
            # wi = hp.CipherArray([self.__w[i*5+0], self.__w[i*5+1], self.__w[i*5+2], self.__w[i*5+3], self.__w[i*5+4]])
            # 计算w*x,输入值（标量密文,向量密文）
            temp = hp.mul(wi, X[:,i])
            # 计算Σw*x
            wx = hp.add(temp, wx)

        # 计算激活函数
        """
        relu = hp.empty_array()
        for i in range(0, data_rows):
            relu = relu.append(hp.ones() / (hp.ones() + hp.exp((-wx[i]))))
        """
        relu = hp.ones() / (hp.exp((-wx)) + hp.ones())

        # 计算wi的梯度,然后更新梯度
        temp = hp.sub(relu, Y)
        for i in range(0, feature_num):
            temp1 = hp.mul(X[:,i], temp)
            # 组内求和计算梯度
            gradient = hp.sum(temp1)
            # 乘以1/n
            gradient = hp.mul(gradient, 1/data_rows)
            Wi = Weight[i]
            # Wi = hp.CipherArray([Weight[i*5+0], Weight[i*5+1], Weight[i*5+2], Weight[i*5+3], Weight[i*5+4]])
            # 梯度乘以学习率(密文,明文)
            gradient = hp.mul(gradient, LearningRate)
            # 更新权重
            Wi = hp.sub(Wi, gradient)
            Weight[i] = Wi
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
    Breast_cancer = load_breast_cancer()
    train_data = Breast_cancer.train_data
    train_target = Breast_cancer.train_target
    test_data = Breast_cancer.test_data
    test_target = Breast_cancer.test_target
    num_test = test_data.cipherShape()[0]
    
    # 初始权重明文
    init_w = np.asarray([0.5]*(len(Breast_cancer.feature_names)+1))
    # 加密明文权重
    Weight = ct.encrypt(init_w, discrete=True)
    # 初始化类参数
    lr = LogisticRegression()
    lr.set_params(iterations=50,w=Weight,learningrate=0.1)
    
    # helearn拟合
    begin_time = time.time() # 计时开始
    l, loss = lr.fit(train_data, train_target, True)
    end_time = time.time() # 计时结束
    loss_plain = ct.decrypt(loss, discrete=True)
    time = end_time-begin_time
    
    # 计算得分
    c_pre, c_rule = lr.predict(test_data)
    #print(c_rule)

    # 分类
    divide = hp.empty_array()
    for i in range(num_test): 
        if (c_rule >= hp.ones()*0.5)[i]:
            divide = divide.append(hp.ones())
        else :
            divide = divide.append(hp.zeros())

    
    # 计算准确率
    temp = 0
    for i in range(num_test):
        if divide[i] == test_target[i]:
             temp = temp + 1
        accuracy = temp / num_test

    print("cipher running time:%fs"%time)
    print("基于 HENumpy 的逻辑回归准确率:%f"%accuracy)
    # 打印损失函数
    plt.plot(loss_plain)
    plt.show()