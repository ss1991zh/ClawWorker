import henumpy as hp

class ONE(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = hp.ones()
        return cls._instance

class ZERO(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = hp.zeros()
        return cls._instance
 
class EMPTY(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = hp.empty_array()
        return cls._instance