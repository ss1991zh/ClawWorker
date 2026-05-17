# 前5位的复制还没写
import numpy as np

def train_test_split(X, y, test_size=0.2, random_state=None):
    
    if random_state is not None:
        np.random.seed(random_state)

    X = X.T
    num_samples = X.shape[0]
    print("num_samples: ", num_samples)
    num_test_samples = int(test_size * num_samples)

    # 随机打乱数据
    indices = np.random.permutation(num_samples)
    X = X[indices]
    y = y[indices]

    # 划分数据集
    X_train, X_test = X[:-num_test_samples], X[-num_test_samples:]
    y_train, y_test = y[:-num_test_samples], y[-num_test_samples:]

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":

    from helearn.datasets import *

    # 初始化字典以及私钥
    hp.initDict()

    # 加载密文数据
    boston = load_boston()
    X, y = boston.train_data, boston.train_target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
    print("y_train shape:", y_train.shape)
    print("y_test shape:", y_test.shape)
    