from functools import wraps
import henumpy as hp
from .gtimer import gt
from enum import Enum

class CipherType(Enum):
    '''
    enum for chiper type code
    '''
    ROW_CHIPER = 0
    COL_CHIPER = 1

def boolean_index_or(a1, a2):
    """bool索引与操作
    """
    len1 = len(a1)
    len2 = len(a2)
    if len1 != len2:
        raise ValueError("two array length must be same")
    r = []
    for k in range(len1):
        r.append(a1[k] or a2[k])
    return r

# def cipher_argsort(v1):
#     arr = v1.get_base_array()
#     arr_value = arr[5:]
#     return np.argsort(arr_value)

def ensure_col_encryption(func):
    """确保输入是列加密
    """
    @wraps(func)
    def _convert_2darray_input_to_col(self, *args, **kwargs):
        gt.start('perform transform')
        for idx, arg in enumerate(args):
            if isinstance(arg, hp.CipherArray):
                if len(arg.cipherShape()) > 1:  # 只对数组
                    if arg._check_encryption_type() != CipherType.COL_CHIPER:
                        args[idx] = arg.transEncType()
        
        for k, v in kwargs.items():
            if isinstance(v, hp.CipherArray):
                try:
                    if len(v.cipherShape()) > 1:  # 只对数组
                        if v._check_encryption_type() != CipherType.COL_CHIPER:
                            kwargs[k] = v.transEncType()
                except:
                    print(v.cipherShape())
        gt.stop('perform transform')
        return func(self, *args, **kwargs)

    return _convert_2darray_input_to_col

def to_cipher(func):
    """
    将当前返回封装为CipherArray对象
    """
    @wraps(func)
    def _convert_arr_to_cipher(self, *args, **kwargs):
        func_res = func(self, *args, **kwargs)
        if isinstance(func_res, tuple):
            ret = []
            for i in range(len(func_res)):
                res = hp.empty_array()
                for it in func_res[i]:
                    res = hp.append(res, it)
                ret.append(res)
            return tuple(ret)
        else:
            res = hp.empty_array()
            for it in func_res:
                res = hp.append(res, it)
            return res
    return _convert_arr_to_cipher