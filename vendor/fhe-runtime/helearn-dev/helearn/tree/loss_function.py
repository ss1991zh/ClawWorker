import henumpy as hp
import numpy as np
from helearn.tree import ONE, ZERO
from abc import ABCMeta, abstractmethod


class LossFunction(metaclass=ABCMeta):
    """
    损失函数基类
    ------------------
    [函数]
        initialize_f_0 :    初始化 F_0
        calculate_residual: 计算负梯度
        update_f_m:         计算 F_m
        leaf_weight:        更新叶子节点的预测值
        __call__:           计算训练损失
    """

    def __init__(self):
        pass

    @abstractmethod
    def initialize_f_0(self, y):
        raise NotImplementedError

    @abstractmethod
    def negative_gradient(self, y_pred, y):
        raise NotImplementedError

    def gradient(self, y_pred, y):
        return self.negative_gradient(y_pred, y) * -1

    @abstractmethod
    def hessian(self, y_pred, y):
        raise NotImplementedError

    @abstractmethod
    def leaf_weight(self, y_pred, y):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, y_pred, y):
        raise NotImplementedError


class SquareError(LossFunction):
    """
    均方差损失: 回归问题
    np.mean((y - pred)^2)

    [参考]
    ---------------------
    [1] initialize_f_0:  https://github.com/scikit-learn/scikit-learn/blob/
        093e0cf14aff026cca6097e8c42f83b735d26358/sklearn/ensemble/_gb.py#L499  get_init_raw_predictions
    [2] negative_gradient: https://github.com/scikit-learn/scikit-learn/blob/
        093e0cf14aff026cca6097e8c42f83b735d26358/sklearn/ensemble/_gb_losses.py line 690
    [3] update_f_m:     https://github.com/scikit-learn/scikit-learn/blob/
        093e0cf14aff026cca6097e8c42f83b735d26358/sklearn/ensemble/_gb.py#L499  _fit_stages
    """

    def __init__(self):
        super().__init__()

    def initialize_f_0(self, y):
        """计算f0初始拟合"""
        y_mean = hp.mean(y)
        init_raw_preditions = hp.ones_like(y) * y_mean
        return y_mean, init_raw_preditions

    def negative_gradient(self, y_pred, y):
        """残差"""
        residual = y - y_pred

        return residual

    def hessian(self, y_pred, y):
        """二阶导海森矩阵"""
        return hp.ones_like(y)

    def leaf_weight(self, y_pred, y):
        """(只在GBDT中使用) 回归树叶节点的预测值为均值"""
        return hp.mean(y_pred)

    def __call__(self, y_pred, y):
        """计算loss值"""
        loss = hp.mean(hp.square(y - y_pred))
        return loss


class BinomialDeviance(LossFunction):
    """
    对数似然损失: 二分类问题
    -2.0 * np.mean((y * pred) - np.logaddexp(0.0, pred))

    [参考]
    ---------------------
    [1] initialize_f_0:  https://github.com/scikit-learn/scikit-learn/blob/
        093e0cf14aff026cca6097e8c42f83b735d26358/sklearn/ensemble/_gb_losses.py get_init_raw_predictions
    [2] GBDT二分类算法完整的算法过程: https://zhuanlan.zhihu.com/p/89549390
    [3] negative_gradient:  https://github.com/scikit-learn/scikit-learn/blob/
        093e0cf14aff026cca6097e8c42f83b735d26358/sklearn/ensemble/_gb_losses.py line 690
    [4] scipy.special.expit -> 1/(1+exp(-x))
    [5] update_f_m: https://github.com/scikit-learn/scikit-learn/blob/
        093e0cf14aff026cca6097e8c42f83b735d26358/sklearn/ensemble/_gb.py#L499   _fit_stages
    [6] leaf_weight: 公式出自 https://zhuanlan.zhihu.com/p/89549390 中 c_{m, j} 的计算 "c) 对于J_m个叶子节点区域计算出最佳拟合值"
    [7] __call__: https://github.com/scikit-learn/scikit-learn/blob/
        093e0cf14aff026cca6097e8c42f83b735d26358/sklearn/ensemble/_gb_losses.py line 675
    """

    def __init__(self):
        super().__init__()

    def initialize_f_0(self, y):
        """计算f0初始拟合
        分类问题使用 F_0 = log( P(Y=1|x)/ (1 - P(Y=1|x)))
        # log(x / (1 - x)) is the inverse of the sigmoid (expit) function
        """
        prob_pos = hp.sum(y)
        prob_neg = y.cipherShape()[0] - prob_pos

        log_likehood = hp.log(prob_pos / prob_neg)
        init_ = hp.ones_like(y) * log_likehood

        return log_likehood, init_

    def negative_gradient(self, y_pred, y):
        """计算负梯度"""
        residual = y - hp.expit(y_pred)
        return residual

    def hessian(self, y_pred, y):
        """二阶导海森矩阵"""
        sigmod = hp.expit(y_pred)
        return sigmod * (ONE() - sigmod)

    def leaf_weight(self, y_pred, y):
        """分类树叶节点的预测值"""
        eps = np.finfo(np.float32).eps.item()
        numerator = hp.sum(y_pred)
        if hp.absolute(numerator) < ONE() * eps:
            return ZERO()
        denominator = hp.sum((y - y_pred) * (ONE() - y + y_pred))
        if hp.absolute(denominator) < ONE() * eps:
            return ZERO()
        else:
            return numerator / denominator

    # def __call__(self, y_pred, y): # 存在局限
    #     """计算loss值
    #     """
    #     # logger.info(ct.decode(y_pred))
    #     # logger.info(ct.decode(y))
    #     logaddexp = hp.log(hp.exp(y_pred) + ONE())
    #     negative_log = hp.mean(hp.mul(y, y_pred) - logaddexp)
    #     loss = negative_log * -2
    #     return loss

    def __call__(self, y_pred, y):
        # logger.info(ct.decode(y_pred))
        # logger.info(ct.decode(y))
        loss = -(y * hp.log(y_pred) + (1.0 - y) * hp.log(1.0 - y_pred))
        return hp.mean(loss)
