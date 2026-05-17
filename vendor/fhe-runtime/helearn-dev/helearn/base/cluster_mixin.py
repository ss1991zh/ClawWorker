class ClusterMixin:
    def fit(self, X):
        """
        在输入数据上拟合聚类模型。

        参数: 
        - X: array-like 或 pd.DataFrame, 形状为 (n_samples, n_features)
            用于聚类的输入数据。
        """
        raise NotImplementedError("Subclasses must implement the fit method")

    def predict(self, X):
        """
        为新数据点预测聚类标签。

        参数: 
        - X: array-like 或 pd.DataFrame, 形状为 (n_samples, n_features)
            要预测聚类标签的输入数据。

        返回: 
        - labels: array, 形状为 (n_samples,)
            每个数据点的聚类标签。
        """
        raise NotImplementedError("Subclasses must implement the predict method")

    def fit_predict(self, X):
        """
        在输入数据上拟合聚类模型并预测聚类标签。

        参数: 
        - X: array-like 或 pd.DataFrame, 形状为 (n_samples, n_features)
            用于聚类的输入数据。

        返回: 
        - labels: array, 形状为 (n_samples,)
            每个数据点的聚类标签。
        """
        self.fit(X)
        return self.predict(X)

    def fit_transform(self, X):
        """
        在输入数据上拟合聚类模型并返回转换后的数据。

        参数: 
        - X: array-like 或 pd.DataFrame, 形状为 (n_samples, n_features)
            用于聚类的输入数据。

        返回: 
        - transformed_data: array, 形状为 (n_samples, n_clusters)
            转换后的数据, 通常为聚类中心或聚类成员。
        """
        self.fit(X)
        return self.transform(X)

    def transform(self, X):
        """
        将输入数据转换为聚类成员或聚类中心。

        参数: 
        - X: array-like 或 pd.DataFrame, 形状为 (n_samples, n_features)
            要进行转换的输入数据。

        返回: 
        - transformed_data: array, 形状为 (n_samples, n_clusters)
            转换后的数据, 通常为聚类中心或聚类成员。
        """
        raise NotImplementedError("Subclasses must implement the transform method")