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
from henumpy.base.cipher_array_operation import broadcast_arrays

__all__ = ["sin", "cos", "tan", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh", "arcsinh", 
           "arccosh", "arctanh", "arctan2", "hypot", "rad2deg", "deg2rad", "degrees", "radians", "unwrap", "cosine"]

# 求三角形斜边
def __hypot(c1, c2):

    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    hypot_func = get_func_name("hypot")
    hypot_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    hypot_func.restype = POINTER(c_double)

    res_ptr = hypot_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 求三角形斜边（密文数组）
def __hypot_array(c1, c2):

    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    hypot_array_func = get_func_name("hypot_array")
    hypot_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    hypot_array_func.restype = POINTER(c_double)

    res_ptr = hypot_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __hypot_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("hypot")
    hypot_array_array_func = get_func_name("hypot_array_array")
    hypot_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    hypot_array_array_func.restype = POINTER(c_double)
    res_ptr = hypot_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 将角度从弧度转换为度数
def __rad2deg(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    rad2deg_func = get_func_name("rad2deg")
    rad2deg_func.argtypes = [POINTER(c_double), c_int]
    rad2deg_func.restype = POINTER(c_double)

    res_ptr = rad2deg_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 将角度从弧度转换为度数（数组版）
def __rad2deg_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    rad2deg_array_func = get_func_name("rad2deg_array")
    rad2deg_array_func.argtypes = [POINTER(c_double), c_int]
    rad2deg_array_func.restype = POINTER(c_double)

    res_ptr = rad2deg_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __rad2deg_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    rad2deg_array_array_func = get_func_name("rad2deg_array_array")
    rad2deg_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    rad2deg_array_array_func.restype = POINTER(c_double)
    res_ptr = rad2deg_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 将度数转换为弧度
def __deg2rad(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)

    deg2rad_func = get_func_name("deg2rad")
    deg2rad_func.argtypes = [POINTER(c_double), c_int]
    deg2rad_func.restype = POINTER(c_double)

    res_ptr = deg2rad_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 将度数转换为弧度（数组）
def __deg2rad_array(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)

    deg2rad_array_func = get_func_name("deg2rad_array")
    deg2rad_array_func.argtypes = [POINTER(c_double), c_int]
    deg2rad_array_func.restype = POINTER(c_double)

    res_ptr = deg2rad_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __deg2rad_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    deg2rad_array_array_func = get_func_name("deg2rad_array_array")
    deg2rad_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    deg2rad_array_array_func.restype = POINTER(c_double)
    res_ptr = deg2rad_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 弧度转度数
def __degrees(c1):
    c1_double_array = (c_double *(len(c1)))(*c1)

    degrees_func = get_func_name("degrees")
    degrees_func.argtypes = [POINTER(c_double), c_int]
    degrees_func.restype = POINTER(c_double)

    res_ptr = degrees_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 弧度转度数（数组）
def __degrees_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    degrees_array_func = get_func_name("degrees_array")
    degrees_array_func.argtypes = [POINTER(c_double), c_int]
    degrees_array_func.restype = POINTER(c_double)

    res_ptr = degrees_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __degrees_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    degrees_array_array_func = get_func_name("degress_array_array")
    degrees_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    degrees_array_array_func.restype = POINTER(c_double)
    res_ptr = degrees_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 度数转弧度
def __radians(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    radians_func = get_func_name("radians")
    radians_func.argtypes = [POINTER(c_double), c_int]
    radians_func.restype = POINTER(c_double)

    res_ptr = radians_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 度数转弧度（数组）
def __radians_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    radians_array_func = get_func_name("radians_array")
    radians_array_func.argtypes = [POINTER(c_double), c_int]
    radians_array_func.restype = POINTER(c_double)

    res_ptr = radians_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __radians_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    radians_array_array_func = get_func_name("radians_array_array")
    radians_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    radians_array_array_func.restype = POINTER(c_double)
    res_ptr = radians_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sin(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    sin_func = get_func_name("sin")
    sin_func.argtypes = [POINTER(c_double), c_int]
    sin_func.restype = POINTER(c_double)

    res_ptr = sin_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sin_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    sin_array_func = get_func_name("sin_array")
    sin_array_func.argtypes = [POINTER(c_double), c_int]
    sin_array_func.restype = POINTER(c_double)
    res_ptr = sin_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sin_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("sin")
    sin_array_array_func = get_func_name("sin_array_array")
    sin_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    sin_array_array_func.restype = POINTER(c_double)
    res_ptr = sin_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cos(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    cos_func = get_func_name("cos")
    cos_func.argtypes = [POINTER(c_double), c_int]
    cos_func.restype = POINTER(c_double)

    res_ptr = cos_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cos_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    cos_array_func = get_func_name("cos_array")
    cos_array_func.argtypes = [POINTER(c_double), c_int]
    cos_array_func.restype = POINTER(c_double)
    res_ptr = cos_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cos_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("cos")
    cos_array_array_func = get_func_name("cos_array_array")
    cos_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    cos_array_array_func.restype = POINTER(c_double)
    res_ptr = cos_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __tan(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    tan_func = get_func_name("tan")
    tan_func.argtypes = [POINTER(c_double), c_int]
    tan_func.restype = POINTER(c_double)

    res_ptr = tan_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __tan_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    tan_array_func = get_func_name("tan_array")
    tan_array_func.argtypes = [POINTER(c_double), c_int]
    tan_array_func.restype = POINTER(c_double)
    res_ptr = tan_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __tan_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("tan")
    tan_array_array_func = get_func_name("tan_array_array")
    tan_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    tan_array_array_func.restype = POINTER(c_double)
    res_ptr = tan_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arcsin(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arcsin_func = get_func_name("arcsin")
    arcsin_func.argtypes = [POINTER(c_double), c_int]
    arcsin_func.restype = POINTER(c_double)
    res_ptr = arcsin_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arcsin_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arcsin_array_func = get_func_name("arcsin_array")
    arcsin_array_func.argtypes = [POINTER(c_double), c_int]
    arcsin_array_func.restype = POINTER(c_double)
    res_ptr = arcsin_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arcsin_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("arcsin")
    arcsin_array_array_func = get_func_name("arcsin_array_array")
    arcsin_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    arcsin_array_array_func.restype = POINTER(c_double)
    res_ptr = arcsin_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arccos(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arccos_func = get_func_name("arccos")
    arccos_func.argtypes = [POINTER(c_double), c_int]
    arccos_func.restype = POINTER(c_double)
    res_ptr = arccos_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arccos_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arccos_array_func = get_func_name("arccos_array")
    arccos_array_func.argtypes = [POINTER(c_double), c_int]
    arccos_array_func.restype = POINTER(c_double)
    res_ptr = arccos_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arccos_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("arccos")
    arccos_array_array_func = get_func_name("arccos_array_array")
    arccos_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    arccos_array_array_func.restype = POINTER(c_double)
    res_ptr = arccos_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctan(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arctan_func = get_func_name("arctan")
    arctan_func.argtypes = [POINTER(c_double), c_int]
    arctan_func.restype = POINTER(c_double)
    res_ptr = arctan_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctan_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arctan_array_func = get_func_name("arctan_array")
    arctan_array_func.argtypes = [POINTER(c_double), c_int]
    arctan_array_func.restype = POINTER(c_double)
    res_ptr = arctan_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctan_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("arctan")
    arctan_array_array_func = get_func_name("arctan_array_array")
    arctan_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    arctan_array_array_func.restype = POINTER(c_double)
    res_ptr = arctan_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sinh(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    sinh_func = get_func_name("sinh")
    sinh_func.argtypes = [POINTER(c_double), c_int]
    sinh_func.restype = POINTER(c_double)
    res_ptr = sinh_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sinh_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    sinh_array_func = get_func_name("sinh_array")
    sinh_array_func.argtypes = [POINTER(c_double), c_int]
    sinh_array_func.restype = POINTER(c_double)
    res_ptr = sinh_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res) 

def __sinh_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("sinh")
    sinh_array_array_func = get_func_name("sinh_array_array")
    sinh_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    sinh_array_array_func.restype = POINTER(c_double)
    res_ptr = sinh_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)   

def __cosh(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    cosh_func = get_func_name("cosh")
    cosh_func.argtypes = [POINTER(c_double), c_int]
    cosh_func.restype = POINTER(c_double)
    res_ptr = cosh_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cosh_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    cosh_array_func = get_func_name("cosh_array")
    cosh_array_func.argtypes = [POINTER(c_double), c_int]
    cosh_array_func.restype = POINTER(c_double)
    res_ptr = cosh_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cosh_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("cosh")
    cosh_array_array_func = get_func_name("cosh_array_array")
    cosh_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    cosh_array_array_func.restype = POINTER(c_double)
    res_ptr = cosh_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __tanh(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    tanh_func = get_func_name("tanh")
    tanh_func.argtypes = [POINTER(c_double), c_int]
    tanh_func.restype = POINTER(c_double)
    res_ptr = tanh_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __tanh_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    tanh_array_func = get_func_name("tanh_array")
    tanh_array_func.argtypes = [POINTER(c_double), c_int]
    tanh_array_func.restype = POINTER(c_double)
    res_ptr = tanh_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __tanh_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("tanh")
    tanh_array_array_func = get_func_name("tanh_array_array")
    tanh_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    tanh_array_array_func.restype = POINTER(c_double)
    res_ptr = tanh_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arcsinh(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arcsinh_func = get_func_name("arcsinh")
    arcsinh_func.argtypes = [POINTER(c_double), c_int]
    arcsinh_func.restype = POINTER(c_double)
    res_ptr = arcsinh_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arcsinh_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arcsinh_array_func = get_func_name("arcsinh_array")
    arcsinh_array_func.argtypes = [POINTER(c_double), c_int]
    arcsinh_array_func.restype = POINTER(c_double)
    res_ptr = arcsinh_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arcsinh_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("arcsinh")
    arcsinh_array_array_func = get_func_name("arcsinh_array_array")
    arcsinh_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    arcsinh_array_array_func.restype = POINTER(c_double)
    res_ptr = arcsinh_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arccosh(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arccosh_func = get_func_name("arccosh")
    arccosh_func.argtypes = [POINTER(c_double), c_int]
    arccosh_func.restype = POINTER(c_double)
    res_ptr = arccosh_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arccosh_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arccosh_array_func = get_func_name("arccosh_array")
    arccosh_array_func.argtypes = [POINTER(c_double), c_int]
    arccosh_array_func.restype = POINTER(c_double)
    res_ptr = arccosh_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arccosh_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("arccosh")
    arccosh_array_array_func = get_func_name("arccosh_array_array")
    arccosh_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    arccosh_array_array_func.restype = POINTER(c_double)
    res_ptr = arccosh_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctanh(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arctanh_func = get_func_name("arctanh")
    arctanh_func.argtypes = [POINTER(c_double), c_int]
    arctanh_func.restype = POINTER(c_double)
    res_ptr = arctanh_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctanh_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arctanh_array_func = get_func_name("arctanh_array")
    arctanh_array_func.argtypes = [POINTER(c_double), c_int]
    arctanh_array_func.restype = POINTER(c_double)
    res_ptr = arctanh_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctanh_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("arctanh")
    arctanh_array_array_func = get_func_name("arctanh_array_array")
    arctanh_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    arctanh_array_array_func.restype = POINTER(c_double)
    res_ptr = arctanh_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctan2(c1, c2):
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    arctan2_func = get_func_name("arctan2")
    arctan2_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    arctan2_func.restype = POINTER(c_double)
    res_ptr = arctan2_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctan2_array(c1, c2):
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    arctan2_array_func = get_func_name("arctan2_array")
    arctan2_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    arctan2_array_func.restype = POINTER(c_double)
    res_ptr = arctan2_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __arctan2_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("arctan2")
    arctan2_array_array_func = get_func_name("arctan2_array_array")
    arctan2_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    arctan2_array_array_func.restype = POINTER(c_double)
    res_ptr = arctan2_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __unwrap(c1, discont, period):
    c1_double_array = (c_double * (len(c1)))(*c1)

    unwrap_func = get_func_name("unwrap")
    unwrap_func.argtype = [POINTER(c_double), c_int, c_double, c_double]
    unwrap_func.restype = POINTER(c_double)

    res_ptr = unwrap_func(c1_double_array, c_int(len(c1)), c_double(discont), c_double(period))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __unwrap_array(c1, discont, period, axis, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("unwrap")
    if axis == 0:
        unwrap_array_func = get_func_name("unwrap_array_axis0")
    else:
        unwrap_array_func = get_func_name("unwrap_array_axis1")
    unwrap_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_double, c_bool]
    unwrap_array_func.restype = POINTER(c_double)

    res_ptr = unwrap_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]),
                                      c_int(encrypt_type), c_int(output_encrypt_type),
                                      c_double(discont), c_double(period), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# sin 标量
def sin(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __sin(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __sin_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __sin_array_array(c1, encrypt_type, output_encrypt_type)     

# cos 标量
def cos(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __cos(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __cos_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __cos_array_array(c1, encrypt_type, output_encrypt_type)

# tan 标量
def tan(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __tan(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __tan_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __tan_array_array(c1, encrypt_type, output_encrypt_type)

# arcsin 标量
def arcsin(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __arcsin(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __arcsin_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __arcsin_array_array(c1, encrypt_type, output_encrypt_type) 

# arccos 标量
def arccos(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __arccos(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __arccos_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __arccos_array_array(c1, encrypt_type, output_encrypt_type)

# arctan 标量
def arctan(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __arctan(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __arctan_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __arctan_array_array(c1, encrypt_type, output_encrypt_type)

# sinh 标量
def sinh(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __sinh(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __sinh_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __sinh_array_array(c1, encrypt_type, output_encrypt_type)

# cosh 标量
def cosh(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __cosh(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __cosh_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __cosh_array_array(c1, encrypt_type, output_encrypt_type)

# tanh 标量
def tanh(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __tanh(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __tanh_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __tanh_array_array(c1, encrypt_type, output_encrypt_type)

# arcsinh标量
def arcsinh(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __arcsinh(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __arcsinh_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __arcsinh_array_array(c1, encrypt_type, output_encrypt_type)

# arccosh标量
def arccosh(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __arccosh(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __arccosh_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __arccosh_array_array(c1, encrypt_type, output_encrypt_type) 

# arctanh标量
def arctanh(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __arctanh(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __arctanh_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __arctanh_array_array(c1, encrypt_type, output_encrypt_type)

# c1/c2的反正切，并正确选择象限
def arctan2(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __arctan2(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __arctan2_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        return __arctan2_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), output_encrypt_type)
    
def hypot(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
    if c1.get_cipher_type() == 1:
        return __hypot(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 1:
        return __hypot_array(c1.get_base_array(), c2.get_base_array())
    elif c1.get_cipher_type() == 2 and c1.ndim == 2:
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        return __hypot_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), output_encrypt_type)  

# 将弧度转换为度数 rad2deg 支持标量以及向量
def rad2deg(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __rad2deg(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __rad2deg_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __rad2deg_array_array(c1, encrypt_type, output_encrypt_type)

# 度数转换为弧度 deg2rad 支持标量以及向量
def deg2rad(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __deg2rad(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __deg2rad_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __deg2rad_array_array(c1, encrypt_type, output_encrypt_type)

# 将弧度转换为度数degrees 支持标量以及向量
def degrees(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __degrees(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __degrees_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __degrees_array_array(c1, encrypt_type, output_encrypt_type)

# 度数转换为弧度 radians 支持标量以及向量
def radians(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __radians(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __radians_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __radians_array_array(c1, encrypt_type, output_encrypt_type)

# # 通过将值之间的差值更改为 2*pi 补码来展开(平移相位角)
def unwrap(c1, discont=np.pi, axis=1, output_encrypt_type=-1):
    CHECK_ARRAY(c1, "c1")
    if discont < np.pi:
        discont = np.pi
    period = 2 * np.pi
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __unwrap(c1, discont, period)
    elif c1.ndim == 2:
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type            
        return __unwrap_array(c1, discont, period, axis, encrypt_type, output_encrypt_type)

def cosine(c1, c2):
    # 检查是否为离散密文
    if not c1.discrete:
        raise ValueError("Can only handle discrete cipher float array.(Param:c1)")
    if not c2.discrete:
        raise ValueError("Can only handle discrete cipher float array.(Param:c2)")
    
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)

    func = get_func_name("cosine")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    func.restype = POINTER(c_double)

    res_ptr = func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)
