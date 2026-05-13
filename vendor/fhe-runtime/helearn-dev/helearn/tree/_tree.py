import henumpy as hp
import numpy as np
from helearn.tree import ZERO, ONE

class SplitPoint(object):
    """
    分裂点数据结构，记录加密的分裂值和再排序数组中的位置
    """
    def __init__(self, val, pos):
        self.val = val
        self.pos = pos


class Node(object):
    """回归树节点，用于存放分裂条件
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
        loss=None,
        depth=None,
    ):
        self.loss = loss
        self.split_feature = split_feature
        self.split_value = split_value
        self.is_leaf = is_leaf
        self.depth = depth
        self.weight = None
        self.grad = None
        self.left_child = None
        self.right_child = None

    def get_split_points(self, v1):
        """ 朴素方式获取分裂点，计算中值
        """
        ret = []
        for i in range(1, v1.cipherShape()[0]):
            ret.append(SplitPoint((v1[i] + v1[i-1]) / 2.0, i))
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

    def build(self, X, y_pred, y, global_index, features_len, samples_len, max_depth, min_samples_split, loss, criterion, depth):
        """
        三个树继续生长的条件
        1: 深度没有到达最大
        2: 点样本数 >= min_samples_split
        3: 划分收益大于阈值
        """
        sum_total_sq = ZERO()
        parent_impurity = ZERO()
        if criterion == "square_error":
            parent_impurity = hp.sum(hp.square(y_pred - hp.mean(y_pred)))
            sum_total_sq = hp.sum(hp.square(y_pred)) # 总平方和
        sum_total = hp.sum(y_pred)  # 总和
        
        # 叶子结点
        if ( depth >= max_depth 
            or X.cipherShape()[0] < min_samples_split 
            or hp.unique(y_pred).cipherShape()[0] <= 1):
            self.is_leaf=True
            self.loss = loss
            self.leaf_weight(y_pred, y)
            G = hp.ones_array(samples_len) * self.weight
            # G_base_array = G.get_base_array()
            for i in range(samples_len):
                if i not in global_index:
                    G[i] = ZERO()
                    # G_base_array[i + 5] = 0.0
            # self.grad = hp.CipherArray(G_base_array)
            self.grad = G
            return

        best_gain = None
        impurity_gain = None
        split_feature = None
        split_value = None
        left_index = []
        right_index = []

        for feature_id in range(features_len):
            fea_series = X[:, feature_id]
            f_len = fea_series.cipherShape()[0]
            # ========================= 优化的分裂点选择 ==========================
            # 排序特征列 并返回与原列的对应关系
            # indices = cipher_argsort(fea_series)
            indices = hp.argsort(fea_series)
            y_ordered = hp.take(y_pred, indices)
            f_ordered = hp.take(fea_series, indices)

            cut_points = self.get_split_points(f_ordered)

            y_sqsum_left = []
            y_sqsum_right = []
            y_cumsum_left = hp.cumsum(y_ordered)
            y_cumsum_right = sum_total - y_cumsum_left

            # 均方误差计算前缀平方和
            if criterion == "square_error":
                sum_left_sq = ZERO()
                for vy in y_ordered:
                    sum_left_sq = sum_left_sq + vy * vy
                    y_sqsum_left.append(sum_left_sq)
                    y_sqsum_right.append(sum_total_sq - sum_left_sq)

            # 遍历所有切分点
            for cut_point in cut_points:
                feature_split_value = cut_point.val
                pos = cut_point.pos
                
                left_number = pos - 0 # 不包括pos元素
                right_number = f_len - pos

                left_part_weight = pos / f_len
                right_part_weight = 1 - left_part_weight
    
                if criterion == "square_error":
                    # 左右子树均方误差选择最小值
                    y_left = y_cumsum_left[pos-1]
                    left_impurity = y_sqsum_left[pos-1] - y_left * y_left / left_number
                    
                    y_right = y_cumsum_right[pos-1]
                    right_impurity =  y_sqsum_right[pos-1] - y_right * y_right / right_number

                    impurity_gain = parent_impurity - (left_impurity * left_part_weight  + right_impurity * right_part_weight)

                elif criterion == "friedman_mse": # friedman_mse
                    # [参考1]: http://www-personal.umich.edu/~jizhu/jizhu/wuke/Friedman-AoS01.pdf
                    # [参考2]: https://github.com/WonDerSoKo/GBDT_Binary_Classification/blob/master/gbdt_source.py
                    # 修正均方误差  FriedmanMSE(MSE)中重写了impurity_improvement
                    # 需要注意的是 friedman_mse 的 impurity_improvement 跟父节点无关，不需要parent - child，因此是选择最大值
                    left_mean = y_cumsum_left[pos-1] / left_number
                    right_mean = y_cumsum_right[pos-1] / right_number
            
                    diff = left_mean - right_mean
                    weight = left_number * right_number / (left_number + right_number)
                    impurity_gain = diff * diff * weight

                if best_gain is None or impurity_gain > best_gain:
                    split_feature = feature_id
                    split_value = feature_split_value
                    best_gain = impurity_gain
                    left_index = indices[:pos]
                    right_index = indices[pos:]

        if best_gain < ONE() * 1e-6:
            self.is_leaf = True
            self.loss = loss
            self.leaf_weight(y_pred, y)
            G = hp.ones_array(samples_len) * self.weight
            # G_base_array = G.get_base_array()
            for i in range(samples_len):
                if i not in global_index:
                    # G_base_array[i + 5] = 0.0
                    G[i] = ZERO()
            # self.grad = hp.CipherArray(G_base_array)
            self.grad = G
            return
        else:
            self.split_feature = split_feature
            self.split_value = split_value
            
            self.left_child = Node()
            self.left_child.build(
                hp.take(X, left_index, axis=0),
                hp.take(y_pred, left_index),
                hp.take(y, left_index),
                global_index[left_index],
                features_len,
                samples_len,
                max_depth, 
                min_samples_split, 
                loss,
                criterion,
                depth + 1
            )
            self.right_child = Node()
            self.right_child.build(
                hp.take(X, right_index, axis=0),
                hp.take(y_pred, right_index),
                hp.take(y, right_index),
                global_index[right_index],
                features_len,
                samples_len,
                max_depth, 
                min_samples_split, 
                loss,
                criterion,
                depth + 1
            )
    
    def leaf_weight(self, y_pred, y):
        """ 叶子节点权重计算
        """
        self.weight = self.loss.leaf_weight(y_pred, y)

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


class CipherTree(object):
    """
    Cipher Tree Builder
    基础加密GBDT树结构
    [参数]
    ------------------------
        X: 样本数据
        y: 标签列数据
        res: 残差数据
        loss: 损失函数
        max_depth:  树生长最大深度
        criterion: 分裂准则 信息增益  {'friedman_mse', 'square_error'}
    """
    def __init__(
            self, 
            X,
            res,
            y,
            max_depth, 
            min_samples_split, 
            criterion, 
            loss,
        ):
        self.loss = loss
        self.max_depth = max_depth
        self.criterion = criterion
        
        _shape = X.cipherShape()
        self.features_len = _shape[1]
        self.samples_len = _shape[0]

        self.y_pred = res   # 残差向量
        self.X = X
        self.y = y          # y列
        self.min_samples_split = min_samples_split # 每个节点最少样本数
        # 根节点
        self.root = None
        self.build_tree()

    def build_tree(self):
        self.root = Node()
        self.root.build(
            X=self.X, 
            y_pred=self.y_pred,
            y=self.y, 
            global_index=np.arange(self.samples_len),
            features_len=self.features_len, 
            samples_len=self.samples_len, 
            max_depth=self.max_depth, 
            min_samples_split=self.min_samples_split, 
            loss=self.loss, 
            criterion=self.criterion,
            depth=0
        )
    
    def predict(self, instance):
        """在树上进行一次预测
        """
        return self.root.predict(instance)

    def grad_on_tree(self):
        """ 获取树上的梯度值
        """
        return self.root.grad_on_tree()