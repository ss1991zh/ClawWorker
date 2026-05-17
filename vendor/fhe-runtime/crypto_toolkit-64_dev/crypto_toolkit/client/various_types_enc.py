# Contains functions for encrypting and decrypting multiple data types
# currently supported: float, int, bool, str
import numpy as np
from .base import (
    _encrypt_float,
    _encrypt_int,
    _encrypt_bool,
    _encrypt_str,
    _decrypt_float, 
    _decrypt_int, 
    _decrypt_bool,
    _decrypt_str,
)

def encrypt_various_type(data, cipher_type='float'):
    """
    将输入数据当做浮点数数组加密

    参数：
    data: 输入数据，可以是浮点数、整数、布尔值、字符串等类型
    cipher_type: 加密后的密文类型，可选值为'float'、'int'、'bool'、'str'
        - 'int'：整数加密的范围是int32的范围 即-2^31 到 2^31-1
    返回：
    加密后的数据，类型为numpy.ndarray
    """

    # 检查输入数据类型
    if isinstance(data, (tuple, dict, set)):
        raise TypeError("Currently, encryption of tuple, dict, and set types is not supported.")
    
    # 字符串类型单独处理
    if cipher_type == 'str':
        if not isinstance(data, str):
            raise ValueError("Only string types can be processed in the manner of string encryption")        
        return _encrypt_str(data).reshape((len(data), 2))
    
    # 其他类型的通用处理流程
    type_mapping = {
        'float': {'func': _encrypt_float, 'dtype': np.float64},
        'int': {'func': _encrypt_int, 'dtype': np.int32},
        'bool': {'func': _encrypt_bool, 'dtype': np.bool_}
    }
    
    if cipher_type not in type_mapping:
        raise ValueError("Invalid cipher_type")
    
    # 获取当前类型的处理函数和数据类型
    encrypt_func = type_mapping[cipher_type]['func']
    target_dtype = type_mapping[cipher_type]['dtype']
    
    # 标量检测和数组转换
    is_scalar = False
    if not isinstance(data, (list, np.ndarray)):
        data = np.array([data])
        is_scalar = True
    elif isinstance(data, list):
        data = np.array(data)
    
    # 类型转换
    try:
        data = data.astype(target_dtype)
    except:
        raise TypeError(f"This data type '{data.dtype}' cannot use {cipher_type} type encryption methods")
    
    # 加密处理
    res = encrypt_func(data)
    if is_scalar:
        return res
    else:
        return res.reshape(data.shape + (2,))


def decrypt_various_type(c):
    """
    假设数组中的密文都是同一个类型的密文，比如都是float或者都是int
    """
    cipher_type = _get_cipher_type(c)
    if cipher_type == 'float':
        shape = c.shape
        res = _decrypt_float(c)
        if len(shape) == 1:
            return res
        else:
            return res.reshape(shape[:-1])
        # return _decrypt_float(c)
    elif cipher_type == 'int':
        shape = c.shape
        res = _decrypt_int(c)
        if len(shape) == 1:
            return res
        else:
            return res.reshape(shape[:-1])
        # return _decrypt_int(c)
    elif cipher_type == 'bool':
        shape = c.shape
        res = _decrypt_bool(c)
        if len(shape) == 1:
            return res
        else:
            return res.reshape(shape[:-1])
        # return _decrypt_bool(c)
    elif cipher_type == 'str':
        return _decrypt_str(c)


def _float64_to_bytes_and_uint16_numpy(f):
    """
    使用numpy实现相同功能
    """
    # 将float64转换为字节（大端模式）
    bytes_array = np.array([f], dtype='>f8').tobytes()
    
    # 取出前两个字节，以小端模式解释为uint16
    x1 = np.frombuffer(bytes_array[0:2], dtype='<u2')[0]
    
    return x1

def _get_cipher_type(c):
    """
    工具函数，从密文中获取密文类型
    """
    prefix = c.reshape(-1,)[0]
    x1 = _float64_to_bytes_and_uint16_numpy(prefix)
        # 获取二进制表示，并确保是16位长度
    bit_pattern = format(x1, '016b')
    
    # 检查前四位
    if bit_pattern[0] == '1':  # 第一位为1
        return "float"
    elif bit_pattern[1] == '1':  # 第二位为1
        return "int"
    elif bit_pattern[2] == '1':  # 第三位为1
        return "bool"
    elif bit_pattern[3] == '1':  # 第四位为1
        return "str"
    else:
        # 如果前四位都不是1，返回默认类型或抛出异常
        raise ValueError("Not any kind of legal ciphertext")