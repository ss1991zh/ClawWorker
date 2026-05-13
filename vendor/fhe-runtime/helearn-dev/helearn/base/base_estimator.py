class BaseEstimator:
    def __init__(self):
        pass
    
    def fit(self, X, y=None, **fit_params):
        """
        将模型拟合到数据。

        参数:
        -----------
        X : array-like 或 pd.DataFrame
            训练数据。
        y : array-like 或 pd.Series, 默认=None
            目标值。
        **fit_params : dict
            附加的拟合参数。

        返回:
        --------
        self : object
            返回实例本身。
        """
        return self
    
    def predict(self, X):
        """
        预测给定输入数据的目标值。

        参数:
        -----------
        X : array-like 或 pd.DataFrame
            输入数据。
            
        返回:
        --------
        y_pred : array-like
            预测的目标值。
        """
        pass
    
    def score(self, X, y=None):
        """
        返回预测的决定系数 R^2。

        参数:
        -----------
        X : array-like 或 pd.DataFrame
            输入数据。
        y : array-like 或 pd.Series, 默认=None
            目标值。

        返回:
        --------
        score : float
            R^2, 相对于 y 的 self.predict(X)。
        """
        # 自定义计算分数的逻辑
        pass
    
    def get_params(self, deep=True):
        """
        获取此估计器的参数。
        
        参数:
        -----------
        deep : bool, 默认=True
            如果为True, 将返回此估计器和包含的子对象的参数, 
            这些子对象是估计器。

        返回:
        --------
        params : dict
            将参数名称映射到它们的值。
        """
        out = {}
        for key in self._get_param_names():
            value = getattr(self, key)
            if deep and hasattr(value, 'get_params'):
                deep_items = value.get_params().items()
                out.update((key + '__' + k, val) for k, val in deep_items)
            out[key] = value
        return out
    
    def set_params(self, **params):
        """
        设置此估计器的参数。
        
        参数:
        -----------
        **params : dict
            估计器参数。
        """
        if not params:
            return self
        valid_params = self.get_params(deep=True)
        for key, value in params.items():
            key, delim, sub_key = key.partition('__')
            if key not in valid_params:
                raise ValueError(f'Invalid parameter {key} for estimator {self.__class__.__name__}')
            if delim:
                setattr(getattr(self, key), sub_key, value)
            else:
                setattr(self, key, value)
        return self

    def _get_param_names(self):
        """
        获取估计器的参数名称。
        """
        return sorted(self.__dict__.keys())