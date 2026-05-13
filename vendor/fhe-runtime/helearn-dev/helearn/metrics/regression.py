import henumpy as hp
 
def square_error(array=None):
    """
    计算均方误差
    """
    mean = hp.mean(array)
    _square_error = hp.sum(hp.square(array - mean))
    return _square_error
