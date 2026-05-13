import henumpy as hp
from helearn.base.base_estimator import BaseEstimator
from helearn.tree._tree import CipherTree
from helearn.tree._constant import ONE, ZERO
from helearn.tree.loss_function import SquareError, BinomialDeviance
from helearn.utils.cipher_tools import to_cipher, ensure_col_encryption
from tqdm import trange


class BaseGradientBoosting(BaseEstimator):
    """树模型基类，主要完成深度优先遍历的特征分裂与节点构建过程
    [参数]
    ------------------
        loss: helearn.tree.loss_function.LossFunction
            树模型loss对象
        learning_rate: float, 默认 0.3
            学习率
        n_estimators: int, 默认 10
            基学习树总数
        max_depth: int, 默认6
            树生长最大深度
        criterion: str, 可选 friedman_mse, square_error, 默认 friedman_mse
            分裂准则 信息增益的计算方式
        min_samples_split: int, 默认 2
            每个节点允许的最少样本数
    """

    def __init__(
        self,
        loss,
        learning_rate,
        n_estimators,
        max_depth,
        criterion,
        min_samples_split=2,
    ):
        super().__init__()
        self.loss = loss
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.criterion = criterion
        self.min_samples_split = min_samples_split

        if not isinstance(self.min_samples_split, int):
            raise ValueError("min_samples_split must be integer")
        if self.min_samples_split < 2:
            raise ValueError("min_samples_split must >= 2")
        
        self.trees = {}
        self.f_0 = None

    @ensure_col_encryption
    def fit(self, X, y):
        self.f_0, raw_predictions = self.loss.initialize_f_0(y)  # 计算初始F_0
        with trange(1, self.n_estimators + 1) as t:
            t.set_description(f"fit tree (No.0): ")
            t.set_postfix(loss=ZERO())
            for iter in t:  # 对 m = 1, 2, ..., M  构造每一棵树
                # 计算负梯度 对于平方差来说就是残差 residual对于回归问题就是残差
                residual = self.loss.negative_gradient(raw_predictions, y)
                # 利用残差构建下一棵树
                self.trees[iter] = CipherTree(
                    X=X,
                    res=residual,
                    y=y,
                    max_depth=self.max_depth,
                    min_samples_split=self.min_samples_split,
                    criterion=self.criterion,
                    loss=self.loss,
                )

                grad_on_tree = self.trees[iter].grad_on_tree()  # 更新新一轮拟合值prediction F_m
                grad_on_tree = grad_on_tree * self.learning_rate
                raw_predictions = hp.add(raw_predictions, grad_on_tree)

                # 利用new_predictions获取当前的loss
                if isinstance(self.loss, BinomialDeviance):
                    loss_val = self.loss(hp.expit(raw_predictions), y)
                    t.set_description(f"fit tree (No.{iter}): ")
                    t.set_postfix(loss=loss_val)
                else:
                    loss_val = self.loss(raw_predictions, y)
                    t.set_description(f"fit tree (No.{iter}): ")
                    t.set_postfix(loss=loss_val)


class GradientBoostingRegressor(BaseGradientBoosting):
    """回归树， 分裂点采用friedman均方差与sklearn中一致
    [参数]
    ------------------
        learning_rate: float, 默认 0.3
            学习率
        n_estimators: int, 默认 10
            基学习树总数
        max_depth: int, 默认6
            树生长最大深度
        criterion: str, 可选 friedman_mse, square_error, 默认 friedman_mse
            分裂准则 信息增益的计算方式
        min_samples_split: int, 默认 2
            每个节点允许的最少样本数
    """

    def __init__(
        self,
        learning_rate=0.3,
        n_estimators=10,
        max_depth=6,
        criterion="friedman_mse",
        min_samples_split=2,
    ):
        super().__init__(
            SquareError(),
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            criterion=criterion,
        )

    @to_cipher
    def predict(self, X):
        """在树上找到对应的路径计算predict值的和, 这里采用固定步长"""
        samples = X.cipherShape()[0]
        res = [self.f_0 * ONE() for _ in range(samples)]

        for i in range(samples):
            for iter in range(1, self.n_estimators + 1):
                tree_pred = self.trees[iter].predict(X[i, :])
                res[i] = res[i] + tree_pred * self.learning_rate
        return res


class GradientBoostingClassifier(BaseGradientBoosting):
    """GBDT分类问题 原则上也是回归树,分裂方式完全一直。
        但是损失计算在这里使用 BinomialDeviance (交叉熵)
    [参数]
    ------------------
        learning_rate: float, 默认 0.3
            学习率
        n_estimators: int, 默认 10
            基学习树总数
        max_depth: int, 默认6
            树生长最大深度
        criterion: str, 可选 friedman_mse, square_error, 默认 friedman_mse
            分裂准则 信息增益的计算方式
        min_samples_split: int, 默认 2
            每个节点允许的最少样本数
    """

    def __init__(
        self,
        learning_rate=0.3,
        n_estimators=10,
        max_depth=6,
        criterion="friedman_mse",
        min_samples_split=2,
    ):
        super().__init__(
            BinomialDeviance(),
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            criterion=criterion,
        )

    @to_cipher
    def predict(self, X):
        """在树上找到对应的路径计算predict值的和， 这里采用固定步长"""
        samples = X.cipherShape()[0]
        res = [self.f_0 * ONE() for _ in range(samples)]

        for i in range(samples):
            for iter in range(1, self.n_estimators + 1):
                tree_pred = self.trees[iter].predict(X[i, :])
                res[i] = res[i] + tree_pred * self.learning_rate

        proba = [0] * samples
        label = [None] * samples

        for i in range(samples):
            proba[i] = hp.expit(res[i])
            if proba[i] > 0.5 * ONE():
                label[i] = ONE()
            else:
                label[i] = ZERO()

        return proba, label
