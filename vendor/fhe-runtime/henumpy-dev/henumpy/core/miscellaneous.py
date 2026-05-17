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
    free_int_ptr, 
    free_double_ptr,
    free_bool_ptr,
    cipherLen, 
    get_func_parallelization_config, 
    CHECK_DISCRETE, 
    CHECK_ARRAY
)
from henumpy.base.cipher_array import CipherArray
from henumpy.base.cipher_array_operation import  ones, zeros, broadcast_arrays, broadcast_to

__all__ = ["cbrt", "heaviside", "square", "sqrt", "compare", "equal", "not_equal", "greater_equal",
           "less_equal", "greater", "less", "absolute", "convolve", "clip", "sign", "maximum", "minimum", 
           "fmax", "fmin", "interp", "nan_to_num", "isclose", "sort", "expit", "map_cipher", "flip", 
           "where", "map_cipher_inv"]

def __cbrt(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    cbrt_func = get_func_name("cbrt")
    cbrt_func.argtypes = [POINTER(c_double), c_int]
    cbrt_func.restype = POINTER(c_double)

    res_ptr = cbrt_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cbrt_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    cbrt_array_func = get_func_name("cbrt_array")
    cbrt_array_func.argtypes = [POINTER(c_double), c_int]
    cbrt_array_func.restype = POINTER(c_double)
    res_ptr = cbrt_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cbrt_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("cbrt")
    cbrt_array_array_func = get_func_name("cbrt_array_array")
    cbrt_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    cbrt_array_array_func.restype = POINTER(c_double)
    res_ptr = cbrt_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 返回输入数的平方
def __square(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    square_func = get_func_name("square")
    square_func.argtypes = [POINTER(c_double), c_int]
    square_func.restype = POINTER(c_double)

    res_ptr = square_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 逐个返回输入数的平方
def __square_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    square_array_func = get_func_name("square_array")
    square_array_func.argtypes = [POINTER(c_double), c_int]
    square_array_func.restype = POINTER(c_double)

    res_ptr = square_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __square_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("square")
    square_array_array_func = get_func_name("square_array_array")
    square_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    square_array_array_func.restype = POINTER(c_double)
    res_ptr = square_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文开平方根
def __sqrt(c1):
    # 类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)

    sqrt_func = get_func_name("sqrt")
    sqrt_func.argtypes = [POINTER(c_double), c_int]
    sqrt_func.restype = POINTER(c_double)

    res_ptr = sqrt_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 数组密文开平方根
def __sqrt_array(c1):
    # 类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)

    sqrt_array_func = get_func_name("sqrt_array")
    sqrt_array_func.argtypes = [POINTER(c_double), c_int]
    sqrt_array_func.restype = POINTER(c_double)

    res_ptr = sqrt_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sqrt_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("sqrt")
    sqrt_array_array_func = get_func_name("sqrt_array_array")
    sqrt_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    sqrt_array_array_func.restype = POINTER(c_double)
    res_ptr = sqrt_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# 标量密文比较
def __compare(c1, c2):

    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    # 获取函数
    compare_func = get_func_name("compare")
    compare_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    compare_func.restype = c_int

    # 调用函数并返回
    res = compare_func(c1_double_array, c2_double_array, c_int(len(c1)))
    return res

# 数组密文比较
def __compare_array(c1, c2):

    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    compare_array_func = get_func_name("compare_array")
    compare_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    compare_array_func.restype = POINTER(c_int)

    res_ptr = compare_array_func(c1_double_array, c2_double_array, c_int(len(c1)))

    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1)-2,))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __compare_array_array(c1, c2, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("compare")
    compare_array_array_func = get_func_name("compare_array_array")
    compare_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    compare_array_array_func.restype = POINTER(c_int)
    res_ptr = compare_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

# 标量密文绝对值
def __absolute(c1):
    # 数据类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)

    absolute_func = get_func_name("absolute")
    absolute_func.argtypes = [POINTER(c_double), c_int]
    absolute_func.restype = POINTER(c_double)

    res_ptr = absolute_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文绝对值
def __absolute_array(c1):
    # 数据类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)
    absolute_array_func = get_func_name("absolute_array")
    absolute_array_func.argtypes = [POINTER(c_double), c_int]
    absolute_array_func.restype = POINTER(c_double)

    res_ptr = absolute_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __absolute_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    absolute_array_array_func = get_func_name("absolute_array_array")
    absolute_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    absolute_array_array_func.restype = POINTER(c_double)
    res_ptr = absolute_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 比较相等函数equal
def __equal(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    equal_func = get_func_name("equal")
    equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    equal_func.restype = c_bool

    res = equal_func(c1_double_array, c2_double_array, c_int(len(c1)))

    return res

# 数组版比较相等函数
def __equal_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    equal_array_func = get_func_name("equal_array")
    equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    equal_array_func.restype = POINTER(c_bool)

    res_ptr = equal_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __equal_array_array(c1, c2, encrypt_type):
    # 密文数组的形状
    shape_c1 = c1.shape
    if encrypt_type == 0:
        shape_new = (shape_c1[0], shape_c1[1]-2)
    else:
        shape_new = (shape_c1[0]-2, shape_c1[1])
    # ndarray转c数组
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("equal")
    # 调用go函数
    equal_array_array_func = get_func_name("equal_array_array")
    equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    equal_array_array_func.restype = POINTER(c_bool)
    res_ptr = equal_array_array_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

# 标量密文不等于
def __not_equal(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    not_equal_func = get_func_name("not_equal")
    not_equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    not_equal_func.restype = c_bool
    res = not_equal_func(c1_double_array, c2_double_array, c_int(len(c1)))
    return res

# 向量密文不等于
def __not_equal_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    not_equal_array_func = get_func_name("not_equal_array")
    not_equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    not_equal_array_func.restype = POINTER(c_bool)

    res_ptr = not_equal_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __not_equal_array_array(c1, c2, encrypt_type):
    # 密文数组的形状
    shape_c1 = c1.shape
    if encrypt_type == 0:
        shape_new = (shape_c1[0], shape_c1[1]-2)
    else:
        shape_new = (shape_c1[0]-2, shape_c1[1])
    # ndarray转c数组
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("not_equal")
    # 调用go函数
    not_equal_array_array_func = get_func_name("not_equal_array_array")
    not_equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    not_equal_array_array_func.restype = POINTER(c_bool)
    res_ptr = not_equal_array_array_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

# 标量密文大于等于
def __greater_equal(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    greater_equal_func = get_func_name("greater_equal")
    greater_equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    greater_equal_func.restype = c_bool
    res = greater_equal_func(c1_double_array, c2_double_array, c_int(len(c1)))
    return res

# 向量密文大于等于
def __greater_equal_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    greater_equal_array_func = get_func_name("greater_equal_array")
    greater_equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    greater_equal_array_func.restype = POINTER(c_bool)

    res_ptr = greater_equal_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __greater_equal_array_array(c1, c2, encrypt_type):
    # 密文数组的形状
    shape_c1 = c1.shape
    if encrypt_type == 0:
        shape_new = (shape_c1[0], shape_c1[1]-2)
    else:
        shape_new = (shape_c1[0]-2, shape_c1[1])
    # ndarray转c数组
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("greater_equal")
    # 调用go函数
    greater_equal_array_array_func = get_func_name("greater_equal_array_array")
    greater_equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    greater_equal_array_array_func.restype = POINTER(c_bool)
    res_ptr = greater_equal_array_array_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

# 标量密文小于等于
def __less_equal(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    less_equal_func = get_func_name("less_equal")
    less_equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    less_equal_func.restype = c_bool
    res = less_equal_func(c1_double_array, c2_double_array, c_int(len(c1)))
    return res

# 向量密文小于等于
def __less_equal_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    less_equal_array_func = get_func_name("less_equal_array")
    less_equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    less_equal_array_func.restype = POINTER(c_bool)

    res_ptr = less_equal_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __less_equal_array_array(c1, c2, encrypt_type):
    # 密文数组的形状
    shape_c1 = c1.shape
    if encrypt_type == 0:
        shape_new = (shape_c1[0], shape_c1[1]-2)
    else:
        shape_new = (shape_c1[0]-2, shape_c1[1])
    # ndarray转c数组
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("less_equal")
    # 调用go函数
    less_equal_array_array_func = get_func_name("less_equal_array_array")
    less_equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    less_equal_array_array_func.restype = POINTER(c_bool)
    res_ptr = less_equal_array_array_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

# 标量密文大于
def __greater(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    greater_func = get_func_name("greater")
    greater_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    greater_func.restype = c_bool
    res = greater_func(c1_double_array, c2_double_array, c_int(len(c1)))
    return res

# 向量密文大于
def __greater_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    greater_array_func = get_func_name("greater_array")
    greater_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    greater_array_func.restype = POINTER(c_bool)

    res_ptr = greater_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __greater_array_array(c1, c2, encrypt_type):
    shape_c1 = c1.shape
    if encrypt_type == 0:
        shape_new = (shape_c1[0], shape_c1[1]-2)
    else:
        shape_new = (shape_c1[0]-2, shape_c1[1])
    # ndarray转c数组
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("greater")
    # 调用go函数
    greater_array_array_func = get_func_name("greater_array_array")
    greater_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    greater_array_array_func.restype = POINTER(c_bool)
    res_ptr = greater_array_array_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

# 标量密文小于
def __less(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    less_func = get_func_name("less")
    less_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    less_func.restype = c_bool
    res = less_func(c1_double_array, c2_double_array, c_int(len(c1)))
    return res

# 向量密文小于
def __less_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    less_array_func = get_func_name("less_array")
    less_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    less_array_func.restype = POINTER(c_bool)

    res_ptr = less_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __less_array_array(c1, c2, encrypt_type):
    shape_c1 = c1.shape
    if encrypt_type == 0:
        shape_new = (shape_c1[0], shape_c1[1]-2)
    else:
        shape_new = (shape_c1[0]-2, shape_c1[1])
    # ndarray转c数组
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("less")
    # 调用go函数
    less_array_array_func = get_func_name("less_array_array")
    less_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    less_array_array_func.restype = POINTER(c_bool)
    res_ptr = less_array_array_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

# 标量密文sign函数
def __sign(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 调用go函数
    sign_func = get_func_name("sign")
    sign_func.argtypes = [POINTER(c_double), c_int]
    sign_func.restype = POINTER(c_double)
    res_ptr = sign_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文sign函数
def __sign_array(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 调用go函数
    sign_array_func = get_func_name("sign_array")
    sign_array_func.argtypes = [POINTER(c_double), c_int]
    sign_array_func.restype = POINTER(c_double)
    res_ptr = sign_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sign_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("sign")
    clip_array_array_func = get_func_name("sign_array_array") 
    clip_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]  
    clip_array_array_func.restype = POINTER(c_double)

    res_ptr = clip_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res) 

# 标量密文maximum函数
def __maximum(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    maximum_func = get_func_name("maximum")
    maximum_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    maximum_func.restype = POINTER(c_double)

    res_ptr = maximum_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文maximum函数
def __maximum_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    maximum_array_func = get_func_name("maximum_array")
    maximum_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    maximum_array_func.restype = POINTER(c_double)

    res_ptr = maximum_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __maximum_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("maximum")
    maximum_array_array_func = get_func_name("maximum_array_array")
    maximum_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    maximum_array_array_func.restype = POINTER(c_double)
    res_ptr = maximum_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文minimum函数
def __minimum(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    minimum_func = get_func_name("minimum")
    minimum_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    minimum_func.restype = POINTER(c_double)

    res_ptr = minimum_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文minimum函数
def __minimum_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    minimum_array_func = get_func_name("minimum_array")
    minimum_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    minimum_array_func.restype = POINTER(c_double)

    res_ptr = minimum_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __minimum_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("minimum")
    minimum_array_array_func = get_func_name("minimum_array_array")
    minimum_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    minimum_array_array_func.restype = POINTER(c_double)
    res_ptr = minimum_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文fmax函数
def __fmax(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    fmax_func = get_func_name("fmax")
    fmax_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    fmax_func.restype = POINTER(c_double)

    res_ptr = fmax_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文fmax函数
def __fmax_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    fmax_array_func = get_func_name("fmax_array")
    fmax_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    fmax_array_func.restype = POINTER(c_double)

    res_ptr = fmax_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fmax_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("fmax")
    fmax_array_array_func = get_func_name("fmax_array_array")
    fmax_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    fmax_array_array_func.restype = POINTER(c_double)
    res_ptr = fmax_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文fminx函数
def __fmin(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    fmin_func = get_func_name("fmin")
    fmin_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    fmin_func.restype = POINTER(c_double)

    res_ptr = fmin_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文fmin函数
def __fmin_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    fmin_array_func = get_func_name("fmin_array")
    fmin_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    fmin_array_func.restype = POINTER(c_double)

    res_ptr = fmin_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fmin_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("fmin")
    fmin_array_array_func = get_func_name("fmin_array_array")
    fmin_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    fmin_array_array_func.restype = POINTER(c_double)
    res_ptr = fmin_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __clip(c1, min, max):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    min_double_array = (c_double * (len(min)))(*min)
    max_double_array = (c_double * (len(max)))(*max)
    # 调用go函数
    clip_func = get_func_name("clip")
    clip_func.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
    clip_func.restype = POINTER(c_double)
    res_ptr = clip_func(c1_double_array, min_double_array, max_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __clip_array(c1, min, max):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    min_double_array = (c_double * (len(min)))(*min)
    max_double_array = (c_double * (len(max)))(*max)
    # 调用go函数
    clip_array_func = get_func_name("clip_array")
    clip_array_func.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
    clip_array_func.restype = POINTER(c_double)
    res_ptr = clip_array_func(c1_double_array, min_double_array, max_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __clip_array_array(c1, min, max, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    min = min.reshape(-1,)
    max = max.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    min_double_array = (c_double * len(min))(*min)
    max_double_array = (c_double * len(max))(*max)
    parallel = get_func_parallelization_config("clip")
    clip_array_array_func = get_func_name("clip_array_array") 
    clip_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]  
    clip_array_array_func.restype = POINTER(c_double)

    res_ptr = clip_array_array_func(c1_double_array, min_double_array, max_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# 标量密文线性插值
def __interp(c1, xp, fp, left, right):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    xp_double_array = (c_double * (len(xp)))(*xp)
    fp_double_array = (c_double * (len(fp)))(*fp)
    left_double_array = (c_double * (len(left)))(*left)
    right_double_array = (c_double * (len(right)))(*right)
    # 调用go函数
    interp_func = get_func_name("interp")
    interp_func.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int]
    interp_func.restype = POINTER(c_double)
    res_ptr = interp_func(c1_double_array, xp_double_array, fp_double_array, left_double_array, right_double_array, c_int(len(c1)), c_int(len(xp)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文线性插值
def __interp_array(c1, xp, fp, left, right):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    xp_double_array = (c_double * (len(xp)))(*xp)
    fp_double_array = (c_double * (len(fp)))(*fp)
    left_double_array = (c_double * (len(left)))(*left)
    right_double_array = (c_double * (len(right)))(*right)
    # 调用go函数
    interp_array_func = get_func_name("interp_array")
    interp_array_func.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
    interp_array_func.restype = POINTER(c_double)
    res_ptr = interp_array_func(c1_double_array, xp_double_array, fp_double_array, left_double_array, right_double_array, c_int(len(c1)), c_int(len(xp)), c_int(len(left)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __interp_array_array(c1, xp, fp, left, right, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    xp_double_array = (c_double * (len(xp)))(*xp)
    fp_double_array = (c_double * (len(fp)))(*fp) 
    left_double_array = (c_double * (len(left)))(*left) 
    right_double_array = (c_double * (len(right)))(*right) 
    parallel = get_func_parallelization_config("interp")
    interp_array_array_func = get_func_name("interp_array_array")
    interp_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    interp_array_array_func.restype = POINTER(c_double)

    res_ptr = interp_array_array_func(c1_double_array, xp_double_array, fp_double_array, left_double_array, right_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(len(xp)), c_int(len(left)), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文nan_to_num
def __nan_to_num(c1, nan, posinf, neginf):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    nan_double_array = (c_double * (len(nan)))(*nan)
    posinf_double_array = (c_double * (len(posinf)))(*posinf)
    neginf_double_array = (c_double * (len(neginf)))(*neginf)
    # 调用go函数
    nan_to_num_func = get_func_name("nan_to_num")
    nan_to_num_func.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
    nan_to_num_func.restype = POINTER(c_double)

    res_ptr = nan_to_num_func(
        c1_double_array, 
        nan_double_array, 
        posinf_double_array, 
        neginf_double_array,
        c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文nan_to_num
def __nan_to_num_array(c1, nan, posinf, neginf):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    nan_double_array = (c_double * (len(nan)))(*nan)
    posinf_double_array = (c_double * (len(posinf)))(*posinf)
    neginf_double_array = (c_double * (len(neginf)))(*neginf)    
    # 调用go函数
    nan_to_num_array_func = get_func_name("nan_to_num_array")
    nan_to_num_array_func.argtypes = [POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
    nan_to_num_array_func.restype = POINTER(c_double)

    res_ptr = nan_to_num_array_func(
        c1_double_array, 
        c_int(len(c1)),
        nan_double_array,
        posinf_double_array,
        neginf_double_array,
        c_int(len(nan)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nan_to_num_array_array(c1, encrypt_type, nan, posinf, neginf, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    nan_double_array = (c_double * len(nan))(*nan)
    posinf_double_array = (c_double * len(posinf))(*posinf)
    neginf_double_array = (c_double * len(neginf))(*neginf)
    nan_to_num_array_array_func = get_func_name("nan_to_num_array_array")
    nan_to_num_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
    nan_to_num_array_array_func.restype = POINTER(c_double)
    res_ptr = nan_to_num_array_array_func(
        c1_double_array, 
        c_int(c1_shape[0]), 
        c_int(c1_shape[1]), 
        c_int(encrypt_type), 
        c_int(output_encrypt_type),
        nan_double_array,
        posinf_double_array,
        neginf_double_array,
        c_int(len(nan)))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __isclose(c1, c2, rtol, atol):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    # 调用go函数
    isclose_func = get_func_name("isclose")
    isclose_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_double, c_double]
    isclose_func.restype = c_bool

    res = isclose_func(c1_double_array, c2_double_array, c_int(len(c1)), c_double(rtol), c_double(atol))
    return bool(res)

def __isclose_array(c1, c2, rtol, atol):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    # 调用go函数
    isclose_array_func = get_func_name("isclose_array")
    isclose_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_double, c_double]
    isclose_array_func.restype = POINTER(c_bool)

    res_ptr = isclose_array_func(c1_double_array, c2_double_array, c_int(len(c1)), c_double(rtol), c_double(atol))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __isclose_array_array(c1, c2, rtol, atol, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("isclose")
    isclose_array_array_func = get_func_name("isclose_array_array")
    isclose_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_double, c_double, c_bool]
    isclose_array_array_func.restype = POINTER(c_bool)
    res_ptr = isclose_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_double(rtol), c_double(atol), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def __expit(c1):
    # 类型转换
    c1_double_array = (c_double *len(c1))(*c1)
    # 调用go函数
    expit_func = get_func_name("expit")
    expit_func.argtypes = [POINTER(c_double), c_int]
    expit_func.restype = POINTER(c_double)

    res_ptr = expit_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sort(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sort_func = get_func_name("sort")
    sort_func.argtypes = [POINTER(c_double), c_int]
    sort_func.restype = POINTER(c_double)

    res_ptr = sort_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sort_decrement(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sort_decrement_func = get_func_name("sort_decrement")
    sort_decrement_func.argtypes = [POINTER(c_double), c_int]
    sort_decrement_func.restype = POINTER(c_double)

    res_ptr = sort_decrement_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sort_array_array_one(c1, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1] - 2)
    else:
        shape_c1_new = (shape_c1[0] - 2, shape_c1[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sort_array_array_one_func = get_func_name("sort_array_array_one")
    sort_array_array_one_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    sort_array_array_one_func.restype = POINTER(c_double)
    res_ptr = sort_array_array_one_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sort_array_array_one_decrement(c1, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1] - 2)
    else:
        shape_c1_new = (shape_c1[0] - 2, shape_c1[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sort_array_array_one_decrement_func = get_func_name("sort_array_array_one_decrement")
    sort_array_array_one_decrement_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    sort_array_array_one_decrement_func.restype = POINTER(c_double)
    res_ptr = sort_array_array_one_decrement_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)
    
def __sort_array_array_zero(c1, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1] - 2)
    else:
        shape_c1_new = (shape_c1[0] - 2, shape_c1[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sort_array_array_zero_func = get_func_name("sort_array_array_zero")
    sort_array_array_zero_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    sort_array_array_zero_func.restype = POINTER(c_double)
    res_ptr = sort_array_array_zero_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sort_array_array_zero_decrement(c1, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1] - 2)
    else:
        shape_c1_new = (shape_c1[0] - 2, shape_c1[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sort_array_array_zero_decrement_func = get_func_name("sort_array_array_zero_decrement")
    sort_array_array_zero_decrement_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    sort_array_array_zero_decrement_func.restype = POINTER(c_double)
    res_ptr = sort_array_array_zero_decrement_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __expit_array(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    expit_func_array = get_func_name("expit_array")
    expit_func_array.argtypes = [POINTER(c_double), c_int]
    expit_func_array.restype = POINTER(c_double)

    res_ptr = expit_func_array(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __expit_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("expit")
    expit_array_array_func = get_func_name("expit_array_array")
    expit_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    expit_array_array_func.restype = POINTER(c_double)
    res_ptr = expit_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __map_cipher(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    map_cipher_func = get_func_name("map_cipher")
    map_cipher_func.argtypes = [POINTER(c_double), c_int]
    map_cipher_func.restype = c_double

    res = map_cipher_func(c1_double_array, c_int(len(c1)))
    res = float(res)
    return res

def __map_cipher_array(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    map_cipher_array_func = get_func_name("map_cipher_array")
    map_cipher_array_func.argtypes = [POINTER(c_double), c_int]
    map_cipher_array_func.restype = POINTER(c_double)

    res_ptr = map_cipher_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return res

def __flip_array(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    flip_array_func = get_func_name("flip_array")
    flip_array_func.argtypes = [POINTER(c_double), c_int]
    flip_array_func.restype = POINTER(c_double)

    res_ptr = flip_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 默认情况
def __flip_array_array(c1, encrypt_type, output_encrypt_type=-1):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0]-2, shape_c1[1])
    # 类型转换
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    flip_array_array_func = get_func_name("flip_array_array")
    flip_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    flip_array_array_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1:
        output_encrypt_type = encrypt_type
    res_ptr = flip_array_array_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0: # 行加密
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# asix = 0
def __flip_array_array_zero(c1, encrypt_type, output_encrypt_type=-1):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0]-2, shape_c1[1])
    # 类型转换
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    flip_array_array_zero_func = get_func_name("flip_array_array_zero")
    flip_array_array_zero_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    flip_array_array_zero_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1:
        output_encrypt_type = encrypt_type
    res_ptr = flip_array_array_zero_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0: # 行加密
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        print(1)
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# axis = 1
def __flip_array_array_one(c1, encrypt_type, output_encrypt_type=-1):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0]-2, shape_c1[1])
    # 类型转换
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    flip_array_array_one_func = get_func_name("flip_array_array_one")
    flip_array_array_one_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    flip_array_array_one_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1:
        output_encrypt_type = encrypt_type
    res_ptr = flip_array_array_one_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0: # 行加密
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __where_array(condition, c1, c2):
    condition_bool_array = (c_bool * len(condition))(*condition)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    # 调用go函数
    where_array_func = get_func_name("where_array")
    where_array_func.argtypes = [POINTER(c_bool), c_int, POINTER(c_double), POINTER(c_double), c_int]
    where_array_func.restype = POINTER(c_double)
    res_ptr = where_array_func(condition_bool_array, c_int(len(condition)), c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __where_array_array(condition, c1, c2, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0]-2, shape_c1[1])
    # 类型转换
    condition = condition.reshape(-1,)
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    condition_bool_array = (c_bool * len(condition))(*condition)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("where")
    where_array_array_func = get_func_name("where_array_array")
    where_array_array_func.argtypes = [POINTER(c_bool), c_int, c_int, POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    where_array_array_func.restype = POINTER(c_double)

    res_ptr = where_array_array_func(condition_bool_array, c_int(shape_c1_new[0]), c_int(shape_c1_new[1]), c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if encrypt_type == 0: # 行加密
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __map_cipher_inv_double(a):
    map_cipher_inv_double_func = get_func_name("map_cipher_inv_double")
    map_cipher_inv_double_func.argtype = c_double
    map_cipher_inv_double_func.restype = POINTER(c_double)

    res_ptr = map_cipher_inv_double_func(c_double(a))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __map_cipher_inv_double_array(a):
    a_double_array = (c_double * len(a))(*a)
    map_cipher_inv_double_array_func = get_func_name("map_cipher_inv_double_array")
    map_cipher_inv_double_array_func.argtypes = [POINTER(c_double), c_int]
    map_cipher_inv_double_array_func.restype = POINTER(c_double)
    res_ptr = map_cipher_inv_double_array_func(a_double_array, c_int(len(a)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(a)+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __heaviside(c1, c2):
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    heaviside_func = get_func_name("heaviside")
    heaviside_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    heaviside_func.restype = POINTER(c_double)
    res_ptr = heaviside_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __heaviside_array(c1, c2):
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    heaviside_array_func = get_func_name("heaviside_array")
    heaviside_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    heaviside_array_func.restype = POINTER(c_double)
    res_ptr = heaviside_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __heaviside_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("heaviside")
    heaviside_array_array_func = get_func_name("heaviside_array_array")
    heaviside_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    heaviside_array_array_func.restype = POINTER(c_double)
    res_ptr = heaviside_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 逐元素返回立方根
def cbrt(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __cbrt(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __cbrt_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __cbrt_array_array(c1, encrypt_type, output_encrypt_type)

# 阶跃函数
def heaviside(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")    
    CHECK_DISCRETE(c2, "c2")    
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __heaviside(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __heaviside_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        return __heaviside_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), output_encrypt_type)


# 逐个返回输入数的平方 支持标量以及数组类型
def square(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __square(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __square_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __square_array_array(c1, encrypt_type, output_encrypt_type)

# 密文开平方根运算sqrt
def sqrt(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __sqrt(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __sqrt_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __sqrt_array_array(c1, encrypt_type, output_encrypt_type)

# 比较函数，能够处理（标量，标量）,（向量，向量）,(标量，向量)，(向量，标量)
def compare(c1, c2):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())

    if c1.get_cipher_type() == 1:
        return __compare(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __compare_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()        
        return __compare_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type())

# 按元素返回(x1 == x2)
def equal(c1, c2):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())

    if c1.get_cipher_type() == 1:
        return __equal(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __equal_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()        
        return __equal_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type())

def not_equal(c1, c2):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())

    if c1.get_cipher_type() == 1:
        return __not_equal(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __not_equal_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()        
        return __not_equal_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type())

def greater_equal(c1, c2):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())

    if c1.get_cipher_type() == 1:
        return __greater_equal(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __greater_equal_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()        
        return __greater_equal_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type())

# 按元素返回(x1 <= x2)
def less_equal(c1, c2):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())

    if c1.get_cipher_type() == 1:
        return __less_equal(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __less_equal_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()        
        return __less_equal_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type())


# 按元素返回(x1 > x2)
def greater(c1, c2):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())

    if c1.get_cipher_type() == 1:
        return __greater(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __greater_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()        
        return __greater_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type())

# 按元素返回(x1 < x2)
def less(c1, c2):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())

    if c1.get_cipher_type() == 1:
        return __less(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __less_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()        
        return __less_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type())

# 绝对值函数
def absolute(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __absolute(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __absolute_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __absolute_array_array(c1, encrypt_type, output_encrypt_type)

# 卷积函数
def convolve(c1, c2 ,mode="full"):
    # 检查输入
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    if check_res1 != 2 and c1.ndim != 1:
        raise ValueError("Can only handle vector ciphertext, please enter vector ciphertext!(Param:c1)")
    if check_res2 != 2 and c2.ndim != 1:
        raise ValueError("Can only handle vector ciphertext, please enter vector ciphertext!(Param:c2)")
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 根据mode调用不同的函数
    if mode == "full":
        convolve_func = get_func_name("convolve")
        convolve_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
        convolve_func.restype = POINTER(c_double)
        # 获取结果并将结果转为ndarray类型
        res_ptr = convolve_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(len(c2)))
        res = np.ctypeslib.as_array(res_ptr, shape=((len(c1)+int(c2[1])-1),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    elif mode == "same":
        convolve_same_func = get_func_name("convolve_same")
        convolve_same_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
        convolve_same_func.restype = POINTER(c_double)
        # 调用go函数
        res_ptr = convolve_same_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(len(c2)))
        # 计算max(M,N)
        length = np.max([int(c1[1]), int(c2[1])])
        res = np.ctypeslib.as_array(res_ptr, shape=(2+length,))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    elif mode == "valid":
        convolve_valid_func = get_func_name("convolve_valid")
        convolve_valid_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
        convolve_valid_func.restype = POINTER(c_double)
        res_ptr = convolve_valid_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(len(c2)))
        # 计算max(M,N)-min(M,N)+1
        length = np.max(([int(c1[1]), int(c2[1])])) - np.min(([int(c1[1]), int(c2[1])])) + 1
        res = np.ctypeslib.as_array(res_ptr, shape=(2+length,))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    else:
        raise ValueError("mode error!(Param:mode)")

#  clip函数限制数组的值位于[a_min, a_max]
def clip(c1, min, max, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(min, "min")
    CHECK_DISCRETE(max, "max")
    if c1.get_cipher_type() == 1: # c1为标量密文
        if min.get_cipher_type() == 1 and max.get_cipher_type() == 1:
            min = min.get_base_array()
            max = max.get_base_array()    
            return __clip(c1, min, max)
        else:
            s = ""
            if min.get_cipher_type() != 1:
                s += "min "
            if max.get_cipher_type() != 1:
                s += "max "
            raise ValueError(f"Can only handle scalar ciphertext, please enter scalar ciphertext!(Param:{s})")    
    elif c1.get_cipher_type() == 2:
        min = broadcast_to(min, c1.cipherShape())
        max = broadcast_to(max, c1.cipherShape())
        if c1.ndim == 1:
            return __clip_array(c1.get_base_array(), min.get_base_array(), max.get_base_array())
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = c1.get_encryption_type()
            if min.get_encryption_type() != c1.get_encryption_type():
                min = min.transEncType()
            if max.get_encryption_type() != c1.get_encryption_type():
                max = max.transEncType()
            return __clip_array_array(c1.get_base_array(), min.get_base_array(), max.get_base_array(), c1.get_encryption_type(), output_encrypt_type)

# sign函数 返回数字符号的元素指示
def sign(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __sign(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __sign_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __sign_array_array(c1, encrypt_type, output_encrypt_type)

# 取数组中最大值如果有Nan则返回Nan
def maximum(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __maximum(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __maximum_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        return __maximum_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), output_encrypt_type)

# 取数组中最小值如果有Nan则返回Nan
def minimum(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __minimum(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __minimum_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        return __minimum_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), output_encrypt_type)

# 取数组中最大的元素
def fmax(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __fmax(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __fmax_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        return __fmax_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), output_encrypt_type)

# 取数组中最小的元素
def fmin(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __fmin(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __fmin_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        return __fmin_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), output_encrypt_type)

# 线性差值
def interp(c1, xp, fp, left="", right="", output_encrypt_type=-1):
    # 检查输入
    CHECK_ARRAY(xp, "xp")
    CHECK_ARRAY(fp, "fp")
    check_res1 = c1.get_cipher_type()
    check_res2 = xp.get_cipher_type()
    check_res3 = fp.get_cipher_type()
    if type(left) != CipherArray:
        left = fp[0]
    if type(right) != CipherArray:
        right = fp[cipherLen(fp)-1]
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    xp = xp.get_base_array()
    fp = fp.get_base_array()
    check_res4 = left.get_cipher_type()
    check_res5 = right.get_cipher_type()
    left = left.get_base_array()
    right = right.get_base_array()
    if check_res4 != 1:
        raise ValueError("Can only handle scalar ciphertext, please enter scalar ciphertext!(Param:left)")
    if check_res5 != 1:
        raise ValueError("Can only handle scalar ciphertext, please enter scalar ciphertext!(Param:right)")
    if check_res1 == 1:# c1为标量密文
        return __interp(c1, xp, fp, left, right)
    elif check_res1 == 2:# c1为向量密文
        if c1.ndim == 1:
            return __interp_array(c1, xp, fp, left, right)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __interp_array_array(c1, xp, fp, left, right, encrypt_type, output_encrypt_type)

# 将 nan 替换为零，使用大的有限数替换 inf
def nan_to_num(c1, nan=None, posinf=None, neginf=None, output_encrypt_type=-1):
    if nan is None:
        nan = zeros()
    if posinf is None:
        posinf = ones() * 1e300
    if neginf is None:
        neginf = ones() * -1e300
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    nan = nan.get_base_array()
    posinf = posinf.get_base_array()
    neginf = neginf.get_base_array()
    if check_res == 1:
        return __nan_to_num(c1, nan, posinf, neginf)
    elif check_res == 2:
        if c1.ndim == 1:
            return __nan_to_num_array(c1, nan, posinf, neginf)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __nan_to_num_array_array(c1, encrypt_type, nan, posinf, neginf, output_encrypt_type)
    
def isclose(c1, c2, rtol=1e-5, atol=1e-8):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __isclose(c1.get_base_array(), c2.get_base_array(), rtol, atol)
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __isclose_array(c1.get_base_array(), c2.get_base_array(), rtol, atol)
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        return __isclose_array_array(c1.get_base_array(), c2.get_base_array(), rtol, atol, c1.get_encryption_type())

def sort(c1, output_encrypt_type=-1, axis=1, decrement=False):
    CHECK_ARRAY(c1, "c1")
    # 判断c1的类型
    ndim = c1.ndim
    encrypt_type = c1.encryption_type
    c1 = c1.get_base_array()
    if ndim == 2:
        if output_encrypt_type != 0 and output_encrypt_type != 1:
            output_encrypt_type = encrypt_type
        if axis == 1:
            if decrement:
                return __sort_array_array_one_decrement(c1, encrypt_type, output_encrypt_type)
            else:
                return __sort_array_array_one(c1, encrypt_type, output_encrypt_type)
        else:
            if decrement:
                return __sort_array_array_zero_decrement(c1, encrypt_type, output_encrypt_type)
            else:
                return __sort_array_array_zero(c1, encrypt_type, output_encrypt_type)
    else:
        if decrement : # 降序
            return __sort_decrement(c1)
        else: # 升序
            return __sort(c1)

# 激活函数
def expit(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")    
    # 检查输入
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __expit(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __expit_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __expit_array_array(c1, encrypt_type, output_encrypt_type)

def map_cipher(c1):
    CHECK_DISCRETE(c1, "c1")
    # 检查输入
    check_res = c1.get_cipher_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __map_cipher(c1)
    elif check_res == 2:
        return __map_cipher_array(c1)

# 翻转数组元素
def flip(c1, axis=None, output_encrypt_type=-1):
    CHECK_ARRAY(c1, "c1")
    # 根据c1的类型选择执行的函数
    shape_c1 = c1.cipherShape()
    if len(shape_c1) == 1: # 标量或向量密文
        c1 = c1.get_base_array()
        return __flip_array(c1)
    else:
        # 根据axis的类型选择不同的函数
        encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        if axis == None:
            return __flip_array_array(c1, encrypt_type, output_encrypt_type)
        elif axis == 0:
            return __flip_array_array_zero(c1, encrypt_type, output_encrypt_type)
        elif axis == 1:
            return __flip_array_array_one(c1, encrypt_type, output_encrypt_type)
        else:
            raise ValueError("Axis can only be 0 or 1!(Param:axis)")
        
# 根据条件从多个选择中选择元素
def where(condition, c1=None, c2=None, output_encrypt_type=-1):
    if c1 is None and c2 is None: # 如果c1，c2为空则直接调用np.where
        return np.where(condition)
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    shape = condition.shape
    if len(shape) == 1: # condition是一个向量
        # c1 = c1.get_base_array()
        # c2 = c2.get_base_array()
        if check_res1 == 1: # c1是标量密文
            # c1 = broadcast_(c1, (shape[0],), 0)
            c1 = broadcast_to(c1, shape)
        if check_res2 == 1: # c2是标量密文
            c2 = broadcast_to(c2, shape)       
        if c1.cipherShape()[0] != len(condition):
            raise ValueError(f"The lengths of two vectors are different.[len(condition)={len(condition)-2}, len(c1)={len(c1)-2}]")
        if c2.cipherShape()[0] != len(condition):
            raise ValueError(f"The lengths of two vectors are different.[len(condition)={len(condition)-2}, len(c1)={len(c2)-2}]")
        return __where_array(condition, c1.get_base_array(), c2.get_base_array())
    else: # 数组
        # c1 = c1.get_base_array()
        # c2 = c2.get_base_array()
        if check_res1 == 1:
            c1 = broadcast_to(c1, condition.shape)
        if check_res2 == 1:
            c2 = broadcast_to(c2, condition.shape)
        if check_res1 == 2 and c1.ndim == 1:
            raise ValueError("One-dimensional to two-dimensional broadcasting is currently not supported!(Param:c1)")
        if check_res2 == 2 and c2.ndim == 1:
            raise ValueError("One-dimensional to two-dimensional broadcasting is currently not supported!(Param:c2)")
        if output_encrypt_type != 0 and output_encrypt_type != 1:
            output_encrypt_type = encrypt_type
        return __where_array_array(condition, c1.get_base_array(), c2.get_base_array(), encrypt_type, output_encrypt_type)

def map_cipher_inv(a):
    # 类型判断
    if type(a) == float or type(a) == int or isinstance(a, np.number):
        return __map_cipher_inv_double(a)
    elif type(a) == np.ndarray:
        return __map_cipher_inv_double_array(a)
    else:
        raise ValueError("Illegal parameter type!(Param:a)")