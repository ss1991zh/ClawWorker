import numpy as np
from ctypes import *
import os
import sys
import weakref

current_dir = os.path.dirname(os.path.abspath(__file__))
henumpy_parent_dir = os.path.dirname(current_dir)
sys.path = list(set(sys.path))
if henumpy_parent_dir not in sys.path:
    sys.path.append(henumpy_parent_dir)

from henumpy.base.base_function import (
    get_func_name, 
    free_bool_ptr,
    free_double_ptr,
    free_int_ptr,
    get_func_parallelization_config, 
    CHECK_DISCRETE, 
    CHECK_ARRAY
)
from henumpy.base.cipher_array import CipherArray

__all__ = ["round", "rounding", "rint", "fix", "trunc", "floor", "ceil", "decimal"]

# 取整
def __round(c1, n, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    round_func = get_func_name("round")
    round_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
    round_func.restype = POINTER(c_double)
    res_ptr = round_func(c1_double_array, c_int(len(c1)), c_int(n), c_int(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __round_array(c1, n, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    round_array_func = get_func_name("round_array")
    round_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
    round_array_func.restype = POINTER(c_double)
    res_ptr = round_array_func(c1_double_array, c_int(len(c1)), c_int(n), c_int(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __round_array_array(c1, n, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("round")
    round_array_array_func = get_func_name("round_array_array")
    round_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    round_array_array_func.restype = POINTER(c_double)
    res_ptr = round_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_int(n), c_int(m), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# 取整，指定小数位
def __rounding(c1, n):
    c1_double_array = (c_double * (len(c1)))(*c1)
    round_n_func = get_func_name("rounding")
    round_n_func.argtypes = [POINTER(c_double), c_int, c_int]
    round_n_func.restype = POINTER(c_double)
    res_ptr = round_n_func(c1_double_array, c_int(len(c1)), c_int(n))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __rounding_array(c1, n):
    c1_double_array = (c_double * (len(c1)))(*c1)
    round_n_array_func = get_func_name("rounding_array")
    round_n_array_func.argtypes = [POINTER(c_double), c_int, c_int]
    round_n_array_func.restype = POINTER(c_double)
    res_ptr = round_n_array_func(c1_double_array, c_int(len(c1)), c_int(n))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __rounding_array_array(c1, n, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("rounding")
    rounding_array_array_func = get_func_name("rounding_array_array")
    rounding_array_array_func.argtypes = [POINTER(c_double),  c_int, c_int, c_int, c_int, c_int, c_bool]
    rounding_array_array_func.restype = POINTER(c_double)
    res_ptr = rounding_array_array_func(c1_double_array,  c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_int(n), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)   

def __fix(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)
    fix_func = get_func_name("fix")
    fix_func.argtypes = [POINTER(c_double), c_int]
    fix_func.restype = POINTER(c_double)
    res_ptr = fix_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fix_array(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)
    fix_array_func = get_func_name("fix_array")
    fix_array_func.argtypes = [POINTER(c_double), c_int]
    fix_array_func.restype = POINTER(c_double)
    res_ptr = fix_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fix_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("fix")
    fix_array_array_func = get_func_name("fix_array_array")
    fix_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    fix_array_array_func.restype = POINTER(c_double)
    res_ptr = fix_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

def __floor(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)
    floor_func = get_func_name("floor")
    floor_func.argtypes = [POINTER(c_double), c_int]
    floor_func.restype = POINTER(c_double)
    res_ptr = floor_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __floor_array(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)
    floor_array_func = get_func_name("floor_array")
    floor_array_func.argtypes = [POINTER(c_double), c_int]
    floor_array_func.restype = POINTER(c_double)
    res_ptr = floor_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __floor_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("floor")
    floor_array_array_func = get_func_name("floor_array_array")
    floor_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    floor_array_array_func.restype = POINTER(c_double)
    res_ptr = floor_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __ceil(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)
    ceil_func = get_func_name("ceil")
    ceil_func.argtypes = [POINTER(c_double), c_int]
    ceil_func.restype = POINTER(c_double)
    res_ptr = ceil_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __ceil_array(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)
    ceil_array_func = get_func_name("ceil_array")
    ceil_array_func.argtypes = [POINTER(c_double), c_int]
    ceil_array_func.restype = POINTER(c_double)
    res_ptr = ceil_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __ceil_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("ceil")
    ceil_array_array_func = get_func_name("ceil_array_array")
    ceil_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    ceil_array_array_func.restype = POINTER(c_double)
    res_ptr = ceil_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __decimal(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置入参以及返回值
    decimal_func = get_func_name("decimal")
    decimal_func.argtypes = [POINTER(c_double), c_int]
    decimal_func.restype = POINTER(c_double)
    # 执行函数
    res_ptr = decimal_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __decimal_array(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置入参以及返回值
    decimal_array_func = get_func_name("decimal_array")
    decimal_array_func.argtypes = [POINTER(c_double), c_int]
    decimal_array_func.restype = POINTER(c_double)
    # 执行函数
    res_ptr = decimal_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __decimal_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("decimal")
    decimal_array_array_func = get_func_name("decimal_array_array")
    decimal_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    decimal_array_array_func.restype = POINTER(c_double)
    res_ptr = decimal_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 取整函数round
def round(c1, n=0, m=-1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if m == -1:
        m = 12 - 0
    else:pass
    if check_res == 1:
        return __round(c1, n, m)
    elif check_res == 2:
        if c1.ndim == 1:
            return __round_array(c1, n, m)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __round_array_array(c1, n, m, encrypt_type, output_encrypt_type)

def rounding(c1, n=0, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __rounding(c1, n)
    elif check_res == 2:
        if c1.ndim == 1:
            return __rounding_array(c1, n)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __rounding_array_array(c1, n, encrypt_type, output_encrypt_type)            

# 将元素舍入为最接近的整数
def rint(c1, m=-1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    return round(c1, 0, m, output_encrypt_type)

# 向零舍入到最接近的整数
def fix(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __fix(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __fix_array(c1)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __fix_array_array(c1, encrypt_type, output_encrypt_type)

# 与fix功能相同
def trunc(c1, output_encrypt_type=-1):
    return fix(c1, output_encrypt_type)

# 朝负无穷大四舍五入
def floor(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __floor(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __floor_array(c1)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __floor_array_array(c1, encrypt_type, output_encrypt_type)

# 朝正无穷四舍五入
def ceil(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __ceil(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __ceil_array(c1)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __ceil_array_array(c1, encrypt_type, output_encrypt_type)

# 取小数函数
def decimal(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __decimal(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __decimal_array(c1)
        else:
            return __decimal_array_array(c1, encrypt_type, encrypt_type if output_encrypt_type==-1 else output_encrypt_type)

