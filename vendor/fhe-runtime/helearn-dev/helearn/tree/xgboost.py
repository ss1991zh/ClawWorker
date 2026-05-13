import henumpy as hp
from helearn.tree._constant import ONE, ZERO
from helearn.base.base_estimator import BaseEstimator
from helearn.tree.loss_function import SquareError, BinomialDeviance
from helearn.tree._xgbtree import XgbCipherTree
from helearn.utils.cipher_tools import to_cipher, ensure_col_encryption
from multiprocessing import Pool, cpu_count
from tqdm import trange


class XGBBaseGradientBoosting(BaseEstimator):
    """XGB基学习器, 用于定义XGB训练过程
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
        base_score: float, 默认 0.5
            初始化第一轮权重
        lambd: float, 默认 1e-6
            正则化参数
        gamma: float, 默认 1e-6
            限制叶节点分裂参数，信息增益的小于此值会停止增长
        min_child_weight: int or float, 默认 1
            叶节点的h二阶导和小于此值会停止增长
        min_samples_split: int, 默认 2
            每个节点允许的最少样本数
        n_jobs: int, 默认 核心数
            并行进程数量
    """

    def __init__(
        self,
        loss,
        learning_rate,
        n_estimators,
        max_depth,
        base_score=0.5,
        lambd=1.0,
        gamma=1e-6,
        min_child_weight=1,
        min_samples_split=2,
        n_jobs=cpu_count(),
    ):
        super().__init__()
        self.loss = loss
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.base_score = base_score
        self.lambd = lambd
        self.gamma = gamma
        self.min_samples_split = min_samples_split
        if not isinstance(self.min_samples_split, int):
            raise ValueError("min_samples_split must be integer")
        if self.min_samples_split < 2:
            raise ValueError("min_samples_split must >= 2")
        
        self.min_child_weight = min_child_weight
        if self.min_child_weight < 1:
            raise ValueError("min_child_weight < 1 is not suggested")
        
        self.trees = {}
        self.n_jobs = n_jobs
        if not isinstance(n_jobs, int):
            raise ValueError("n_jobs must be integer")
        if n_jobs < -1 or n_jobs > cpu_count():
            raise ValueError("can not set processes out of range [1, cpus]")
        self.f_0 = None

    @ensure_col_encryption
    def fit(self, X, y):
        pool = Pool(initializer=hp.initDict, processes=self.n_jobs)
        raw_predictions = hp.ones_array(y.cipherShape()[0]) * self.base_score  # 计算初始F_0
        self.f_0 = raw_predictions

        with trange(1, self.n_estimators + 1) as t:  # 对 m = 1, 2, ..., M  构造每一棵树
            t.set_description(f"fit tree (No.0): ")
            t.set_postfix(loss=ZERO())
            for iter in t:
                residual = self.loss.negative_gradient(raw_predictions, y)
                gradient = -1 * residual
                hessian = self.loss.hessian(raw_predictions, y)

                # 利用残差构建下一棵树
                self.trees[iter] = XgbCipherTree(
                    X=X,
                    res=residual,
                    grad=gradient,
                    hes=hessian,
                    max_depth=self.max_depth,
                    lambd=self.lambd,
                    gamma=self.gamma,
                    min_samples_split=self.min_samples_split,
                    min_child_weight=self.min_child_weight,
                    loss=self.loss,
                    pool=pool,
                )

                # 更新新一轮拟合值prediction F_m
                grad_on_tree = self.trees[iter].grad_on_tree()
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

        pool.close()


class XGBRegressor(XGBBaseGradientBoosting):
    """XGB回归学习
    [参数]
    ------------------
        learning_rate: float, 默认 0.3
            学习率
        n_estimators: int, 默认 10
            基学习树总数
        max_depth: int, 默认6
            树生长最大深度
        base_score: float, 默认 0.5
            初始化第一轮权重
        lambd: float, 默认 1e-6
            正则化参数
        gamma: float, 默认 1e-6
            限制叶节点分裂参数，信息增益的小于此值会停止增长
        min_child_weight: int or float, 默认 1
            叶节点的h二阶导和小于此值会停止增长
        min_samples_split: int, 默认 2
            每个节点允许的最少样本数
        n_jobs: int, 默认 核心数
            并行进程数量
    """

    def __init__(
        self,
        learning_rate=0.3,
        n_estimators=10,
        max_depth=6,
        base_score=0.5,
        lambd=1e-6,
        gamma=1e-6,
        min_child_weight=1,
        min_samples_split=2,
        n_jobs=cpu_count(),
    ):
        super().__init__(
            loss=SquareError(),
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            base_score=base_score,
            lambd=lambd,
            gamma=gamma,
            min_child_weight=min_child_weight,
            min_samples_split=min_samples_split,
            n_jobs=n_jobs,
        )

    @to_cipher
    def predict(self, X):
        """在树上找到对应的路径计算predict值的和, 这里采用固定步长"""
        samples = X.cipherShape()[0]
        ret = [self.base_score * ONE() for _ in range(samples)]

        for i in range(samples):
            for iter in range(1, self.n_estimators + 1):
                tree_pred = self.trees[iter].predict(X[i, :])
                ret[i] = ret[i] + tree_pred * self.learning_rate

        return ret


class XGBClassfier(XGBBaseGradientBoosting):
    """XGB分类学习
    [参数]
    ------------------
        learning_rate: float, 默认 0.3
            学习率
        n_estimators: int, 默认 10
            基学习树总数
        max_depth: int, 默认6
            树生长最大深度
        base_score: float, 默认 0.5
            初始化第一轮权重
        lambd: float, 默认 1e-6
            正则化参数
        gamma: float, 默认 1e-6
            限制叶节点分裂参数，信息增益的小于此值会停止增长
        min_child_weight: int or float, 默认 1
            叶节点的h二阶导和小于此值会停止增长
        min_samples_split: int, 默认 2
            每个节点允许的最少样本数
        n_jobs: int, 默认 核心数
            并行进程数量
    """

    def __init__(
        self,
        learning_rate=0.3,
        n_estimators=10,
        max_depth=6,
        base_score=0.5,
        lambd=1e-6,
        gamma=1e-6,
        min_child_weight=1,
        min_samples_split=2,
        n_jobs=cpu_count(),
    ):
        super().__init__(
            loss=BinomialDeviance(),
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            base_score=base_score,
            lambd=lambd,
            gamma=gamma,
            min_child_weight=min_child_weight,
            min_samples_split=min_samples_split,
            n_jobs=n_jobs,
        )

    @to_cipher
    def predict(self, X):
        """在树上找到对应的路径计算predict值的和, 这里采用固定步长"""
        samples = X.cipherShape()[0]
        res = [self.base_score * ONE() for _ in range(samples)]

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
