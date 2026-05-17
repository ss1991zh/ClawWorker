import henumpy as hp
import numpy as np
from helearn.tree import ZERO, ONE
from helearn.tree._tree import SplitPoint
from functools import partial


def get_split_points(v1):
    """ 朴素方式获取分裂点，计算中值
    """
    ret = []
    for i in range(1, v1.cipherShape()[0]):
        ret.append(SplitPoint((v1[i] + v1[i-1]) / 2, i))
    return ret

    # ret = []
    # cipher_array = v1.get_base_array()
    # cipher_signature = cipher_array[:4]
    # cipher_data_array = cipher_array[5:]
    # len_cipher_array = len(cipher_data_array)
    # v1 = hp.CipherArray(
    #     np.hstack((
    #         cipher_signature, np.asarray([len_cipher_array]), cipher_data_array
    #     ))
    # )
    # v2 = hp.CipherArray(
    #     np.hstack((
    #         cipher_signature, np.asarray([len_cipher_array, 0.0]), cipher_data_array[:-1]
    #     ))
    # )

    # middle = (v1 + v2) / 2.0
    # for idx, it in enumerate(middle):
    #     if idx > 0:
    #         ret.append(SplitPoint(it, idx))
    # return ret

def find_best_split(
        instances, 
        g_series, 
        h_series, 
        g_sum_total, 
        h_sum_total, 
        min_child_weight,
        lambd,
        gamma,
        parent_impurity,
        feature_id,
    ):
    """分裂点计算
    """
    split_feature = None
    split_value = None
    best_gain = None
    left_index = []
    right_index = []

    impurity_gain = None

    fea_series = instances[:, feature_id]
    # indices = cipher_argsort(fea_series)
    indices = hp.argsort(fea_series)
        
    g_ordered = hp.take(g_series, indices)
    h_ordered = hp.take(h_series, indices)
    f_ordered = hp.take(fea_series, indices)

    cut_points = get_split_points(f_ordered)

    g_cumsum_left = hp.cumsum(g_ordered)
    g_cumsum_right = []

    h_cumsum_left = hp.cumsum(h_ordered)
    h_cumsum_right = []

    for i in range(len(indices)):
        g_cumsum_right.append(g_sum_total - g_cumsum_left[i])
        h_cumsum_right.append(h_sum_total - h_cumsum_left[i])
    
    for cut_point in cut_points:
        feature_split_value = cut_point.val
        pos = cut_point.pos

        if h_cumsum_left[pos-1] < min_child_weight  or h_cumsum_right[pos-1] < min_child_weight:
            impurity_gain = ZERO()
        else:
            g_left = g_cumsum_left[pos-1]
            left_impurity = g_left * g_left / (h_cumsum_left[pos-1] + lambd)

            g_right = g_cumsum_right[pos-1]
            right_impurity =  g_right * g_right / (h_cumsum_right[pos-1] +  lambd)

            impurity_gain = left_impurity + right_impurity - parent_impurity -  gamma

        if best_gain is None or impurity_gain > best_gain:
            split_feature = feature_id
            split_value = feature_split_value
            best_gain = impurity_gain
            left_index = indices[:pos]
            right_index = indices[pos:]
        
    return (split_feature, split_value, best_gain, left_index, right_index)

class XgbNode(object):
    """ XGB节点, 用于存放分裂条件以及节点索引值
    [参数]
    ----------------
        split_feature: 分裂特征
        split_value: 该特征选择值
        is_leaf: 是否叶节点
        loss: 损失计算函数
        grad: 梯度向量
        weight: 叶子节点权重
        depth: 该节点深度
    """
    def __init__(
            self,
            split_feature=None,
            split_value=None,
            is_leaf=False,
            depth=None,
        ):
        self.split_feature = split_feature
        self.split_value = split_value
        self.is_leaf = is_leaf
        self.depth = depth
        self.weight = None
        self.grad = None
        self.left_child = None
        self.right_child = None
    
    def build(
            self, 
            instances, 
            global_index,
            features_len, 
            samples_len,
            g_series, 
            h_series, 
            depth, 
            min_child_weight, 
            lambd, 
            gamma, 
            min_samples_split, 
            max_depth,
            execute_pool,
        ):
        """ 建树过程, 递归构建子树
        """
        if depth >= max_depth or instances.cipherShape()[0] < min_samples_split:
            self.is_leaf = True
            self.leaf_weight(g_series, h_series, min_child_weight, lambd)
            G = hp.ones_array(samples_len) * self.weight
            # G_base_array = G.get_base_array()
            for i in range(samples_len):
                if i not in global_index:
                    # G_base_array[i + 5] = 0.0
                    G[i] = ZERO()
            # self.grad = hp.CipherArray(G_base_array)
            self.grad = G
            return
        
        g_sum_total = hp.sum(g_series)
        h_sum_total = hp.sum(h_series)
        
        parent_impurity = g_sum_total * g_sum_total / (h_sum_total + lambd)

        best_gain = None
        split_feature = None
        split_value = None
        left_index = []
        right_index = []
        
        func = partial(find_best_split, 
                instances, g_series, 
                h_series, 
                g_sum_total, 
                h_sum_total, 
                min_child_weight,
                lambd,
                gamma,
                parent_impurity
            )

        rets = []
        if execute_pool is not None:
            rets = execute_pool.map(func, [i for i in range(features_len)])
        else:
            for i in range(features_len):
                rets.append(func(i))

        for ech_r in rets:
            # split_feature, split_value, best_gain, left_index, right_index
            if best_gain is None or ech_r[2] > best_gain:
                best_gain = ech_r[2]
                split_feature = ech_r[0]
                split_value = ech_r[1]
                left_index = ech_r[3]
                right_index = ech_r[4]

        if best_gain <= ZERO(): # 此判断阈值在于gamma
            self.is_leaf = True
            self.leaf_weight(g_series, h_series, min_child_weight, lambd)
            G = hp.ones_array(samples_len) * self.weight
            # G_base_array = G.get_base_array()
            for i in range(samples_len):
                if i not in global_index:
                    # G_base_array[i + 5] = 0.0
                    G[i] = ZERO()
            # self.grad = hp.CipherArray(G_base_array)
            self.grad = G
        else:
            self.split_feature = split_feature
            self.split_value = split_value

            self.left_child = XgbNode()
            self.left_child.build(
                hp.take(instances, left_index, axis=0), 
                global_index[left_index],
                features_len,
                samples_len,
                hp.take(g_series, left_index),
                hp.take(h_series, left_index), 
                depth+1, 
                min_child_weight, 
                lambd, 
                gamma,
                min_samples_split,
                max_depth,
                execute_pool,
            )

            self.right_child = XgbNode()
            self.right_child.build(
                hp.take(instances, right_index, axis=0), 
                global_index[right_index],
                features_len,
                samples_len,
                hp.take(g_series, right_index), 
                hp.take(h_series, right_index), 
                depth+1, 
                min_child_weight, 
                lambd, 
                gamma,
                min_samples_split,
                max_depth,
                execute_pool,
            )

    def leaf_weight(self, gradient, hessian, min_child_weight, lambd):
        """ 叶子节点权重计算
        """
        _gradient = hp.sum(gradient)
        _hessian = hp.sum(hessian)
        if _hessian < min_child_weight:
            self.weight = ZERO()
        else:
            self.weight = _gradient / (_hessian + lambd) * -1

    def grad_on_tree(self):
        """ 计算树上的梯度提升
        """
        if self.is_leaf:
            return self.grad
        else:
            left_weight = self.left_child.grad_on_tree()
            right_weight = self.right_child.grad_on_tree()
            return hp.add(left_weight, right_weight)
        
    def predict(self, instance):
        """获取某条样本的预测值
        """
        if self.is_leaf:
            return self.weight
        if instance[self.split_feature] < self.split_value:
            return self.left_child.predict(instance)
        else:
            return self.right_child.predict(instance)
        
class XgbCipherTree(object):
    """ XGB Cipher Tree Builder
    XGB加密树结构

    [参数]
    -------------
        X: 样本数据
        res: 拟合数据
        grad: 一阶导
        hes: 二阶导
        loss: 损失函数
        max_depth: 树生长最大深度
        min_samples_split: 最少叶节点样本数
        min_child_weight: 正则参数
        lambd: 正则参数
        gamma: 限制因子
        pool: 进程池
    """
    def __init__(
            self, 
            X, 
            res,
            grad,
            hes,
            loss, 
            max_depth, 
            min_samples_split,
            min_child_weight,
            lambd,
            gamma,
            pool,
        ):
        self.loss = loss
        self.max_depth = max_depth
        _shape = X.cipherShape()
        self.features_len = _shape[1]
        self.samples_len = _shape[0]
        self.residual = res
        self.gradient = grad 
        self.hessian = hes
        self.X = X
        self.min_samples_split = min_samples_split # 每个节点最少样本数
        self.min_child_weight = min_child_weight * ONE()
        self.lambd = lambd
        self.gamma = gamma
        self.pool = pool
        self.root = None
        self.build_tree()

    def build_tree(self):
        """ 建树过程
        """      
        self.root = XgbNode()
        self.root.build(
            instances=self.X,
            global_index=np.arange(self.samples_len),
            features_len=self.features_len,
            samples_len=self.samples_len,
            g_series=self.gradient, 
            h_series=self.hessian,
            depth=0,
            min_child_weight=self.min_child_weight, 
            lambd=self.lambd, 
            gamma=self.gamma,
            min_samples_split=self.min_samples_split,
            max_depth=self.max_depth,
            execute_pool=self.pool
        )
        
    def predict(self, instance):
        """ 预测一次样本
        """
        return self.root.predict(instance)
    
    def grad_on_tree(self):
        """ 获取树上的梯度值
        """
        return self.root.grad_on_tree()