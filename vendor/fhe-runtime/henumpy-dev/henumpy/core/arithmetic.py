import numpy as np
from ctypes import *
import os
import sys
import time
import weakref

current_dir = os.path.dirname(os.path.abspath(__file__))
henumpy_parent_dir = os.path.dirname(current_dir)
sys.path = list(set(sys.path))
if henumpy_parent_dir not in sys.path:
    sys.path.append(henumpy_parent_dir)

from henumpy.base.base_function import (
    get_func_name, 
    get_func_parallelization_config, 
    free_double_ptr,
    free_bool_ptr,
    free_int_ptr,
    CHECK_DISCRETE, 
    CHECK_ARRAY
)
from henumpy.base.cipher_array import CipherArray
from henumpy.base.cipher_array_operation import  broadcast_to, broadcast_arrays

__all__ = ["sum", "nansum", "add", "sub", "mul", "div", "invers", "reciprocal", "positive",
           "negative", "prod", "nanprod", "cumprod", "nancumprod", "cumsum", "nancumsum", 
           "diff", "ediff1d", "gradient", "cross", "trapz", "pow", "log", "log10", "log2",
           "exp", "expm1", "exp2", "floor_divide", "fmod", "mod", "remainder", "modf", "divmod",
           "float_power"]

# 标量密文加法
def __add(c1, c2):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)

    # 调用go函数
    add_func = get_func_name("add")
    add_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    add_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = add_func(c1_double_array, c2_double_array, c_int(len(c1)))

    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    # print("python back res: \n %d, %d, %d, %d, %.16f"% (res[0], res[1], res[2], res[3], res[4]))

    # 使用ctypes库创建C数组指针无须手动释放C数组的内存， 使用Cython或其他扩展库需要手动释放
    # freeMemory(c1_double_array)
    # freeMemory(c2_double_array)
    # freeMemory(res_ptr)
    # print(res)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文加明文
def __add_double(c1, m):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)

    # 调用go函数
    add_double_func = get_func_name("add_double")
    add_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    add_double_func.restype = POINTER(c_double)

    res_ptr = add_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文减法
def __sub(c1, c2):

    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)

    # 调用go函数
    sub_func = get_func_name("sub")
    sub_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    sub_func.restype = POINTER(c_double)
    # sub_func.restypes = POINTER(c_double)  加s出问题
    # 将数组传递给C函数，并获取返回指针
    res_ptr = sub_func(c1_double_array, c2_double_array, c_int(len(c1)))

    # 获取指针指向的数据内容并返回
    
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文减明文
def __sub_double(c1, m):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sub_double_func = get_func_name("sub_double")
    sub_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    sub_double_func.restype = POINTER(c_double)
    res_ptr =sub_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 明文减标量密文
def __sub_double_right(m, c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    sub_double_right_func = get_func_name("sub_double_right")
    sub_double_right_func.argtypes = [POINTER(c_double), c_int, c_double]
    sub_double_right_func.restype = POINTER(c_double)
    
    res_ptr = sub_double_right_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文乘法
def __mul(c1, c2):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)

    # 调用go函数
    mul_func = get_func_name("mul")
    mul_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    mul_func.restype = POINTER(c_double)

    # 将数组指针传递给函数，并接收返回指针
    res_ptr = mul_func(c1_double_array, c2_double_array, c_int(len(c1)))

    # 获取指针指向数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文乘明文
def __mul_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)

    mul_double_func = get_func_name("mul_double")
    mul_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    mul_double_func.restype = POINTER(c_double)

    res_ptr = mul_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文除法
def __div(c1, c2):

    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    # 调用go函数
    div_func = get_func_name("div")
    div_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    div_func.restype = POINTER(c_double)

    res_ptr = div_func(c1_double_array, c2_double_array, c_int(len(c1)))

    # 获取指针指向数据内容并将其转换为ndarray数组
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文除明文
def __div_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)

    div_double_func = get_func_name("div_double")
    div_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    div_double_func.restype = POINTER(c_double)

    res_ptr = div_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 明文除标量密文
def __div_double_right(m, c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    div_double_right_func = get_func_name("div_double_right")
    div_double_right_func.argtypes = [POINTER(c_double), c_int, c_double]
    div_double_right_func.restype = POINTER(c_double)

    res_ptr = div_double_right_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 数组密文加法
def __add_array(c1, c2):

    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    add_array_func =  get_func_name("add_array")
    add_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    add_array_func.restype = POINTER(c_double)

    res_ptr = add_array_func(c1_double_array, c2_double_array, c_int(len(c1)))

    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 数组密文加明文
def __add_array_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)

    add_array_double_func = get_func_name("add_array_double")
    add_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    add_array_double_func.restype = POINTER(c_double)

    res_ptr = add_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __add_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("add")
    add_array_array_func = get_func_name("add_array_array")
    add_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    add_array_array_func.restype = POINTER(c_double)
    res_ptr = add_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __add_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("add")    
    add_array_array_double_func = get_func_name("add_array_array_double")
    add_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
    add_array_array_double_func.restype = POINTER(c_double)
    res_ptr = add_array_array_double_func(c1_double_array, c_double(m), c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# 数组密文减法
def __sub_array(c1, c2):

    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    sub_array_func = get_func_name("sub_array")
    sub_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    sub_array_func.restype = POINTER(c_double)

    res_ptr = sub_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 数组密文减明文
def __sub_array_double(c1, m):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 调用go函数
    sub_array_double_func = get_func_name("sub_array_double")
    sub_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    sub_array_double_func.restype = POINTER(c_double)

    res_ptr = sub_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 明文减数组密文
def __sub_array_double_right(m, c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 调用go函数
    sub_array_double_right_func = get_func_name("sub_array_double_right")
    sub_array_double_right_func.argtypes = [POINTER(c_double), c_int, c_double]
    sub_array_double_right_func.restype = POINTER(c_double)

    res_ptr = sub_array_double_right_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sub_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("sub")
    sub_array_array_func = get_func_name("sub_array_array")      
    sub_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    sub_array_array_func.restype = POINTER(c_double)
    res_ptr = sub_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sub_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("sub")
    sub_array_array_double_func = get_func_name("sub_array_array_double")
    sub_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
    sub_array_array_double_func.restype = POINTER(c_double)
    res_ptr = sub_array_array_double_func(c1_double_array, c_double(m), c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sub_array_array_double_right(m, c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("sub")
    sub_array_array_double_right_func = get_func_name("sub_array_array_double_right")
    sub_array_array_double_right_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
    sub_array_array_double_right_func.restype = POINTER(c_double)
    res_ptr = sub_array_array_double_right_func(c1_double_array, c_double(m), c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# 数组密文乘法
def __mul_array(c1, c2, discrete):

    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    mul_array_func = get_func_name("mul_array")
    mul_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    mul_array_func.restype = POINTER(c_double)

    res_ptr = mul_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    if discrete:
        res = res.tolist()
        res_ = []
        for i in range(int(res[1])):
            res_ += res[:1]
            res_.append(res[i+2])
        res = np.array(res_)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res, discrete)

# 数组密文乘明文
def __mul_array_double(c1, m, discrete):
    c1_double_array = (c_double * (len(c1)))(*c1)

    mul_array_double_func = get_func_name("mul_array_double")
    mul_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    mul_array_double_func.restype = POINTER(c_double)

    res_ptr = mul_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    if discrete:
        res = res.tolist()
        res_ = []
        for i in range(int(res[1])):
            res_ += res[:1]
            res_.append(res[i+2])
        res = np.array(res_)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res, discrete)

def __mul_array_double_array(c1, arr, discrete=False):
    c1_double_array = (c_double * (len(c1)))(*c1)
    arr_double_array = (c_double * (len(arr)))(*arr)

    mul_array_double_array_func = get_func_name("mul_array_double_array")
    mul_array_double_array_func.argtypes = [POINTER(c_double), c_int, POINTER(c_double), c_int]
    mul_array_double_array_func.restype = POINTER(c_double)
    res_ptr = mul_array_double_array_func(c1_double_array, len(c1), arr_double_array, len(arr))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    if discrete:
        res = res.tolist()
        res_ = []
        for i in range(int(res[1])):
            res_ += res[:1]
            res_.append(res[i+2])
        res = np.array(res_)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res, discrete)

def __mul_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("mul")
    mul_array_array_func = get_func_name("mul_array_array")
    mul_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    mul_array_array_func.restype = POINTER(c_double)
    res_ptr = mul_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __mul_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("mul")
    mul_array_array_double_func = get_func_name("mul_array_array_double")
    mul_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
    mul_array_array_double_func.restype = POINTER(c_double)
    res_ptr = mul_array_array_double_func(c1_double_array, c_double(m), c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 数组密文除法
def __div_array(c1, c2):

    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    div_array_func = get_func_name("div_array")
    div_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    div_array_func.restype = POINTER(c_double)

    res_ptr = div_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 数组密文乘明文
def __div_array_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)

    div_array_double_func = get_func_name("div_array_double")
    div_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    div_array_double_func.restype = POINTER(c_double)

    res_ptr = div_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 明文除数组密文
def __div_array_double_right(m, c1):

    c1_double_array = (c_double * (len(c1)))(*c1)

    div_array_double_func = get_func_name("div_array_double_right")
    div_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    div_array_double_func.restype = POINTER(c_double)

    res_ptr = div_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __div_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("div")
    div_array_array_func = get_func_name("div_array_array")
    div_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    div_array_array_func.restype = POINTER(c_double)
    res_ptr = div_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res) 

def __div_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("div")
    div_array_array_double_func = get_func_name("div_array_array_double")
    div_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
    div_array_array_double_func.restype = POINTER(c_double)
    res_ptr = div_array_array_double_func(c1_double_array, c_double(m), c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __div_array_array_double_right(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("div")
    div_array_array_double_right_func = get_func_name("div_array_array_double_right")
    div_array_array_double_right_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
    div_array_array_double_right_func.restype = POINTER(c_double)
    res_ptr = div_array_array_double_right_func(c1_double_array, c_double(m), c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)   

# 逐元素返回参数的倒数
def __reciprocal(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    reciprocal_func = get_func_name("reciprocal")
    reciprocal_func.argtypes = [POINTER(c_double), c_int]
    reciprocal_func.restype = POINTER(c_double)

    res_ptr = reciprocal_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 逐元素返回参数的倒数(数组)
def __reciprocal_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    reciprocal_array_func = get_func_name("reciprocal_array")
    reciprocal_array_func.argtypes = [POINTER(c_double), c_int]
    reciprocal_array_func.restype = POINTER(c_double)

    res_ptr = reciprocal_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __reciprocal_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("reciprocal")
    reciprocal_array_array_func = get_func_name("reciprocal_array_array")
    reciprocal_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    reciprocal_array_array_func.restype = POINTER(c_double)

    res_ptr = reciprocal_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)
    
# 逐元素正数计算
def __positive(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    positive_func = get_func_name("positive")
    positive_func.argtypes = [POINTER(c_double), c_int]
    positive_func.restype = POINTER(c_double)

    res_ptr = positive_func(c1_double_array, c_int(len(c1)))
    res =np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 逐元素正数计算(数组)
def __positive_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    positive_array_func = get_func_name("positive_array")
    positive_array_func.argtypes = [POINTER(c_double), c_int]
    positive_array_func.restype = POINTER(c_double)

    res_ptr = positive_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __positive_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("positive")    
    positive_array_array_func = get_func_name("positive_array_array")
    positive_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    positive_array_array_func.restype = POINTER(c_double)

    res_ptr = positive_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# 逐元素负数计算
def __negative(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    negative_func = get_func_name("negative")
    negative_func.argtypes = [POINTER(c_double), c_int]
    negative_func.restype = POINTER(c_double)

    res_ptr = negative_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 逐元素负数计算
def __negative_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    negative_array_func = get_func_name("negative_array")
    negative_array_func.argtypes = [POINTER(c_double), c_int]
    negative_array_func.restype = POINTER(c_double)

    res_ptr = negative_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __negative_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("negative")
    negative_array_array_func = get_func_name("negative_array_array")
    negative_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    negative_array_array_func.restype = POINTER(c_double)

    res_ptr = negative_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文整数次幂
def __pow(c1,n):
    # 数据类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)

    pow_func = get_func_name("pow")
    pow_func.argtypes = [POINTER(c_double), c_int, c_int]
    pow_func.restype = POINTER(c_double)

    res_ptr = pow_func(c1_double_array, c_int(len(c1)), c_int(n))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文整数次幂
def __pow_array(c1,n):
    # 数据类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)

    pow_array_func = get_func_name("pow_array")
    pow_array_func.argtypes = [POINTER(c_double), c_int, c_int]
    pow_array_func.restype = POINTER(c_double)

    res_ptr = pow_array_func(c1_double_array, c_int(len(c1)), c_int(n))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __pow_array_array(c1, n, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("pow")
    pow_array_array_func = get_func_name("pow_array_array")
    pow_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
    pow_array_array_func.restype = POINTER(c_double)

    res_ptr = pow_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(n), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文分数次幂
def __pow_fractionorder(c1,n,m):
    # 数据类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)

    pow_fractionorder_func = get_func_name("pow_fractionorder")
    pow_fractionorder_func.argtypes = [POINTER(c_double), c_int , c_int, c_int]
    pow_fractionorder_func.restype = POINTER(c_double)

    res_ptr = pow_fractionorder_func(c1_double_array, c_int(len(c1)), c_int(n), c_int(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __pow_array_fractionorder(c1,n,m):
    # 数据类型转换python->C
    c1_double_array = (c_double * (len(c1)))(*c1)

    pow_array_fractionorder_func = get_func_name("pow_array_fractionorder")
    pow_array_fractionorder_func.argtypes = [POINTER(c_double), c_int , c_int, c_int]
    pow_array_fractionorder_func.restype = POINTER(c_double)

    res_ptr = pow_array_fractionorder_func(c1_double_array, c_int(len(c1)), c_int(n), c_int(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __pow_array_array_fractionorder(c1, n, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("pow")
    pow_array_array_fractionorder_func = get_func_name("pow_array_array_fractionorder")
    pow_array_array_fractionorder_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    pow_array_array_fractionorder_func.restype = POINTER(c_double)

    res_ptr = pow_array_array_fractionorder_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(n), c_int(m), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

# 标量密文指数运算
def __exp(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)

    exp_func = get_func_name("exp")
    exp_func.argtypes = [POINTER(c_double), c_int]
    exp_func.restype = POINTER(c_double)

    res_ptr = exp_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文指数运算
def __exp_array(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    exp_array_func = get_func_name("exp_array")
    exp_array_func.argtypes = [POINTER(c_double), c_int]
    exp_array_func.restype = POINTER(c_double)

    res_ptr = exp_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __exp_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("exp")
    exp_array_array_func = get_func_name("exp_array_array")
    exp_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    exp_array_array_func.restype = POINTER(c_double)
    res_ptr = exp_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

def __expm1(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    expm1_func = get_func_name("expm1")
    expm1_func.argtypes = [POINTER(c_double), c_int]
    expm1_func.restype = POINTER(c_double)
    res_ptr = expm1_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __expm1_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    expm1_array_func = get_func_name("expm1_array")
    expm1_array_func.argtypes = [POINTER(c_double), c_int]
    expm1_array_func.restype = POINTER(c_double)
    res_ptr = expm1_array_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __expm1_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("expm1")
    expm1_array_array_func = get_func_name("expm1_array_array")
    expm1_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    expm1_array_array_func.restype = POINTER(c_double)
    res_ptr = expm1_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __exp2(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    exp2_func = get_func_name("exp2")
    exp2_func.argtypes = [POINTER(c_double), c_int]
    exp2_func.restype = POINTER(c_double)
    res_ptr = exp2_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __exp2_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    exp2_array_func = get_func_name("exp2_array")
    exp2_array_func.argtypes = [POINTER(c_double), c_int]
    exp2_array_func.restype = POINTER(c_double)
    res_ptr = exp2_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __exp2_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("exp2")
    exp2_array_array_func = get_func_name("exp2_array_array")
    exp2_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    exp2_array_array_func.restype = POINTER(c_double)
    res_ptr = exp2_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文取对数运算
def __log(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)

    log_func = get_func_name("log")
    log_func.argtypes = [POINTER(c_double), c_int]
    log_func.restype = POINTER(c_double)

    res_ptr = log_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文取对数运算
def __log_array(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)

    log_array_func = get_func_name("log_array")
    log_array_func.argtypes = [POINTER(c_double), c_int]
    log_array_func.restype = POINTER(c_double)

    res_ptr = log_array_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __log_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("log")
    log_array_array_func = get_func_name("log_array_array")
    log_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    log_array_array_func.restype = POINTER(c_double)
    res_ptr = log_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

def __log10(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    log10_func = get_func_name("log10")
    log10_func.argtypes = [POINTER(c_double), c_int]
    log10_func.restype = POINTER(c_double)
    res_ptr = log10_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __log10_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    log10_array_func = get_func_name("log10_array")
    log10_array_func.argtypes = [POINTER(c_double), c_int]
    log10_array_func.restype = POINTER(c_double)
    res_ptr = log10_array_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __log10_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("log10")
    log10_array_array_func = get_func_name("log10_array_array")
    log10_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    log10_array_array_func.restype = POINTER(c_double)
    res_ptr = log10_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __log2(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    log2_func = get_func_name("log2")
    log2_func.argtypes = [POINTER(c_double), c_int]
    log2_func.restype = POINTER(c_double)
    res_ptr = log2_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __log2_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    log2_array_func = get_func_name("log2_array")
    log2_array_func.argtypes = [POINTER(c_double), c_int]
    log2_array_func.restype = POINTER(c_double)
    res_ptr = log2_array_func(c1_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __log2_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0: # 行加密
        c1_new_shape = (c1_shape[0], c1_shape[1]-2)
    else: # 列加密
        c1_new_shape = (c1_shape[0]-2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("log2")
    log2_array_array_func = get_func_name("log2_array_array")
    log2_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    log2_array_array_func.restype = POINTER(c_double)
    res_ptr = log2_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 小数次幂
def __float_power(c1, m):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)

    float_power_func = get_func_name("float_power")
    float_power_func.argtypes = [POINTER(c_double), c_int, c_double]
    float_power_func.restype = POINTER(c_double)

    res_ptr = float_power_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __float_power_array(c1, m):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)

    float_power_array_func = get_func_name("float_power_array")
    float_power_array_func.argtypes = [POINTER(c_double), c_int, c_double]
    float_power_array_func.restype = POINTER(c_double)

    res_ptr = float_power_array_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __float_power_array_array(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("float_power")
    float_power_array_array_func = get_func_name("float_power_array_array")
    float_power_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_bool]
    float_power_array_array_func.restype = POINTER(c_double)

    res_ptr = float_power_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_double(m), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)  

def __fmod(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 获取函数
    fmod_func = get_func_name("fmod")
    fmod_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    fmod_func.restype = POINTER(c_double)
    res_ptr = fmod_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fmod_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    fmod_double_func = get_func_name("fmod_double")
    fmod_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    fmod_double_func.restype = POINTER(c_double)
    res_ptr = fmod_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fmod_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 获取函数
    fmod_array_func = get_func_name("fmod_array")
    fmod_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    fmod_array_func.restype = POINTER(c_double)
    res_ptr = fmod_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fmod_array_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    fmod_array_double_func = get_func_name("fmod_array_double")
    fmod_array_double_func.argtypes = [POINTER(c_double), c_int,c_double]
    fmod_array_double_func.restype = POINTER(c_double)
    res_ptr = fmod_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __fmod_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("fmod")
    fmod_array_array_func = get_func_name("fmod_array_array")
    fmod_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    fmod_array_array_func.restype = POINTER(c_double)
    res_ptr = fmod_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res) 

def __fmod_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("fmod")
    fmod_array_array_double_func = get_func_name("fmod_array_array_double")
    fmod_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_bool]
    fmod_array_array_double_func.restype = POINTER(c_double)
    res_ptr = fmod_array_array_double_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_double(m), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)  

def __mod(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 获取函数
    mod_func = get_func_name("mod")
    mod_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    mod_func.restype = POINTER(c_double)
    res_ptr = mod_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __mod_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    mod_double_func = get_func_name("mod_double")
    mod_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    mod_double_func.restype = POINTER(c_double)

    res_ptr = mod_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __mod_array(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 获取函数
    mod_array_func = get_func_name("mod_array")
    mod_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    mod_array_func.restype = POINTER(c_double)
    res_ptr = mod_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __mod_array_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    mod_array_double_func = get_func_name("mod_array_double")
    mod_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    mod_array_double_func.restype = POINTER(c_double)
    res_ptr = mod_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __mod_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("mod")
    fmod_array_array_func = get_func_name("mod_array_array")
    fmod_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    fmod_array_array_func.restype = POINTER(c_double)
    res_ptr = fmod_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res) 

def __mod_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("mod")
    mod_array_array_double_func = get_func_name("mod_array_array_double")
    mod_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_bool]
    mod_array_array_double_func.restype = POINTER(c_double)
    res_ptr = mod_array_array_double_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_double(m), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res) 

def __modf(c1):
    # 类型转换
    c1_double_array = (c_double *(len(c1)))(*c1)
    # 调用go函数
    modf_func = get_func_name("modf")
    modf_func.argtypes = [POINTER(c_double), c_int]
    modf_func.restype = POINTER(c_double)
    res_ptr = modf_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(4,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    # 将结果组装成元组
    res_decimal = CipherArray(res[:2])
    res_fix = CipherArray(res[2:])
    return (res_decimal, res_fix)

def __modf_array(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    modf_array_func = get_func_name("modf_array")
    modf_array_func.argtypes = [POINTER(c_double), c_int]
    modf_array_func.restype = POINTER(c_double)
    res_ptr = modf_array_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2*len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    res0 = res[:len(c1)]
    res1 = res[len(c1):]
    return (CipherArray(res0), CipherArray(res1))

def __modf_array_array(c1, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("modf")
    modf_array_array_func = get_func_name("modf_array_array")
    modf_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    modf_array_array_func.restype = POINTER(c_double)

    res_ptr = modf_array_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]*2, c1_new_shape[1]+2))
        res0 = res[:c1_new_shape[0],:]
        res1 = res[c1_new_shape[0]:,:]
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]*2))
        res0 = res[:,:c1_new_shape[1]]
        res1 = res[:,c1_new_shape[1]:]
    weakref.finalize(res, free_double_ptr, res_ptr)
    return (CipherArray(res0), CipherArray(res1))

def __divmod(c1,c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 调用go函数
    divmod_func = get_func_name("divmod")
    divmod_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    divmod_func.restype = POINTER(c_double)
    res_ptr = divmod_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(4,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    # 将结果组装成元组
    res_floor_div = CipherArray(res[:2])
    res_mod = CipherArray(res[2:])
    return (res_floor_div, res_mod)

def __divmod_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    divmod_func = get_func_name("divmod_double")
    divmod_func.argtypes = [POINTER(c_double), c_int, c_double]
    divmod_func.restype = POINTER(c_double)
    res_ptr = divmod_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(4,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    # 将结果组装成元组
    res_floor_div = CipherArray(res[:2])
    res_mod = CipherArray(res[2:])
    return (res_floor_div, res_mod)    

def __divmod_array(c1, c2):
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    divmod_array_func = get_func_name("divmod_array")
    divmod_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    divmod_array_func.restype = POINTER(c_double)
    res_ptr = divmod_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2*len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    res0 = res[:len(c1)]
    res1 = res[len(c1):]
    return (CipherArray(res0), CipherArray(res1))

def __divmod_array_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    divmod_array_double = get_func_name("divmod_array_double")
    divmod_array_double.argtypes = [POINTER(c_double), c_int, c_double]
    divmod_array_double.restype = POINTER(c_double)
    res_ptr = divmod_array_double(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(2*len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    res0 = res[:len(c1)]
    res1 = res[len(c1):]
    return (CipherArray(res0), CipherArray(res1))

def __divmod_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("divmod")
    divmod_array_array_func = get_func_name("divmod_array_array")
    divmod_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    divmod_array_array_func.restype = POINTER(c_double)
    res_ptr = divmod_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]*2, c1_new_shape[1]+2))
        res0 = res[:c1_new_shape[0],:]
        res1 = res[c1_new_shape[0]:,:]
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]*2+2, c1_new_shape[1]))
        head = res[:1,:]
        list_ = [c1_new_shape[0]] * c1_new_shape[1]
        array = np.array(list_)
        head = np.vstack((head, array))
        res0 = np.vstack((head, res[2:2+c1_new_shape[0],:]))
        res1 = np.vstack((head, res[2+c1_new_shape[0]:,:]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return (CipherArray(res0), CipherArray(res1))

def __divmod_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("divmod")
    divmod_array_array_double_func = get_func_name("divmod_array_array_double")
    divmod_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_bool]
    divmod_array_array_double_func.restype = POINTER(c_double)
    res_ptr = divmod_array_array_double_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_double(m), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]*2, c1_new_shape[1]+2))
        res0 = res[:c1_new_shape[0],:]
        res1 = res[c1_new_shape[0]:,:]
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]*2+2, c1_new_shape[1]))
        head = res[:1,:]
        list_ = [c1_new_shape[0]] * c1_new_shape[1]
        array = np.array(list_)
        head = np.vstack((head, array))
        res0 = np.vstack((head, res[2:2+c1_new_shape[0],:]))
        res1 = np.vstack((head, res[2+c1_new_shape[0]:,:]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return (CipherArray(res0), CipherArray(res1))

def __floor_div(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 获取函数
    floor_divide_func = get_func_name("floor_divide")
    floor_divide_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    floor_divide_func.restype = POINTER(c_double)

    res_ptr = floor_divide_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __floor_div_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    floor_div_double_func = get_func_name("floor_divide_double")
    floor_div_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    floor_div_double_func.restype = POINTER(c_double)
    res_ptr = floor_div_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __floor_div_array(c1, c2):
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    floor_div_array_func = get_func_name("floor_divide_array")
    floor_div_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    floor_div_array_func.restype = POINTER(c_double)

    res_ptr = floor_div_array_func(c1_double_array, c2_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __floor_div_array_double(c1, m):
    c1_double_array = (c_double * (len(c1)))(*c1)
    floor_div_array_double_func = get_func_name("floor_divide_array_double")
    floor_div_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
    floor_div_array_double_func.restype = POINTER(c_double)
    res_ptr = floor_div_array_double_func(c1_double_array, c_int(len(c1)), c_double(m))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __floor_div_array_array(c1, c2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("floor_divide")
    floor_div_array_array_func = get_func_name("floor_divide_array_array")
    floor_div_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    floor_div_array_array_func.restype = POINTER(c_double)

    res_ptr = floor_div_array_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __floor_div_array_array_double(c1, m, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("floor_divide")
    floor_div_array_array_double_func = get_func_name("floor_divide_array_array_double")
    floor_div_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_bool]
    floor_div_array_array_double_func.restype = POINTER(c_double)

    res_ptr = floor_div_array_array_double_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_double(m), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)            

def __prod(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    prod_func = get_func_name("prod")
    prod_func.argtypes = [POINTER(c_double), c_int]
    prod_func.restype = POINTER(c_double)
    res_ptr = prod_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __prod_array(c1, axis, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("prod")
    if axis is None:
        prod_array_func = get_func_name("prod_array_none")
    elif axis == 0:
        prod_array_func = get_func_name("prod_array_0")
    else:
        prod_array_func = get_func_name("prod_array_1")
    prod_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    prod_array_func.restype = POINTER(c_double)
    res_ptr = prod_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1] + 2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nanprod(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    prod_func = get_func_name("nanprod")
    prod_func.argtypes = [POINTER(c_double), c_int]
    prod_func.restype = POINTER(c_double)
    res_ptr = prod_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nanprod_array(c1, axis, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("nanprod")
    if axis is None:
        nanprod_array_func = get_func_name("nanprod_array_none")
    elif axis == 0:
        nanprod_array_func = get_func_name("nanprod_array_0")
    else:
        nanprod_array_func = get_func_name("nanprod_array_1")

    nanprod_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    nanprod_array_func.restype = POINTER(c_double)
    res_ptr = nanprod_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1] + 2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sum(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    sum_func = get_func_name("sum")
    sum_func.argtypes = [POINTER(c_double), c_int]
    sum_func.restype = POINTER(c_double)
    res_ptr = sum_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __sum_array(c1, axis, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("sum")
    if axis is None:
        sum_array_func = get_func_name("sum_array_none")
    elif axis == 0:
        sum_array_func = get_func_name("sum_array_0")
    else:
        sum_array_func = get_func_name("sum_array_1")

    sum_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    sum_array_func.restype = POINTER(c_double)
    res_ptr = sum_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1] + 2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nansum(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)
    nansum_func = get_func_name("nansum")
    nansum_func.argtypes = [POINTER(c_double), c_int]
    nansum_func.restype = POINTER(c_double)
    res_ptr = nansum_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nansum_array(c1, axis, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("nansum")
    if axis is None:
        nansum_array_func = get_func_name("nansum_array_none")
    elif axis == 0:
        nansum_array_func = get_func_name("nansum_array_0")
    else:
        nansum_array_func = get_func_name("nansum_array_1")

    nansum_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    nansum_array_func.restype = POINTER(c_double)
    res_ptr = nansum_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1] + 2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0] + 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cumprod(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    cumprod_func = get_func_name("cumprod")
    cumprod_func.argtypes = [POINTER(c_double), c_int]
    cumprod_func.restype = POINTER(c_double)

    res_ptr = cumprod_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cumprod_array(c1, axis, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    if axis is None:
        cumprod_array_func = get_func_name("cumprod_array_none")
        cumprod_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
        cumprod_array_func.restype = POINTER(c_double)
        res_ptr = cumprod_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type))
    else:
        if axis == 0:
            cumprod_array_func = get_func_name("cumprod_array_0")
        else:
            cumprod_array_func = get_func_name("cumprod_array_1")
        cumprod_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
        cumprod_array_func.restype = POINTER(c_double)
        res_ptr = cumprod_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type)) 
    
    if axis is None: # 轴为none则结果数组为向量
        res = np.ctypeslib.as_array(res_ptr, shape=(2+c1_new_shape[0]*c1_new_shape[1],))
    else:
        if output_encrypt_type == 0: # 行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
        else: # 列加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nancumprod(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    cumprod_func = get_func_name("nancumprod")
    cumprod_func.argtypes = [POINTER(c_double), c_int]
    cumprod_func.restype = POINTER(c_double)

    res_ptr = cumprod_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nancumprod_array(c1, axis, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    if axis is None:
        nancumprod_array_func = get_func_name("nancumprod_array_none")
        nancumprod_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
        nancumprod_array_func.restype = POINTER(c_double)
        res_ptr = nancumprod_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type))
    else:
        if axis == 0:
            nancumprod_array_func = get_func_name("nancumprod_array_0")
        else:
            nancumprod_array_func = get_func_name("nancumprod_array_1")
        nancumprod_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
        nancumprod_array_func.restype = POINTER(c_double)
        res_ptr = nancumprod_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type)) 
    
    if axis is None: # 轴为none则结果数组为向量
        res = np.ctypeslib.as_array(res_ptr, shape=(2+c1_new_shape[0]*c1_new_shape[1],))
    else:
        if output_encrypt_type == 0: # 行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
        else: # 列加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cumsum(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    cumsum_func = get_func_name("cumsum")
    cumsum_func.argtypes = [POINTER(c_double), c_int]
    cumsum_func.restype = POINTER(c_double)

    res_ptr = cumsum_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cumsum_array(c1, axis, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    if axis is None:
        cumsum_array_func = get_func_name("cumsum_array_none")
        cumsum_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
        cumsum_array_func.restype = POINTER(c_double)
        res_ptr = cumsum_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type))
    else:
        if axis == 0:
            cumsum_array_func = get_func_name("cumsum_array_0")
        else:
            cumsum_array_func = get_func_name("cumsum_array_1")
        cumsum_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
        cumsum_array_func.restype = POINTER(c_double)
        res_ptr = cumsum_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type)) 
    
    if axis is None: # 轴为none则结果数组为向量
        res = np.ctypeslib.as_array(res_ptr, shape=(2+c1_new_shape[0]*c1_new_shape[1],))
    else:
        if output_encrypt_type == 0: # 行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
        else: # 列加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)   

def __nancumsum(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    cumsum_func = get_func_name("nancumsum")
    cumsum_func.argtypes = [POINTER(c_double), c_int]
    cumsum_func.restype = POINTER(c_double)

    res_ptr = cumsum_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __nancumsum_array(c1, axis, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    if axis is None:
        nancumsum_array_func = get_func_name("nancumsum_array_none")
        nancumsum_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
        nancumsum_array_func.restype = POINTER(c_double)
        res_ptr = nancumsum_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type))
    else:
        if axis == 0:
            nancumsum_array_func = get_func_name("nancumsum_array_0")
        else:
            nancumsum_array_func = get_func_name("nancumsum_array_1")
        nancumsum_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
        nancumsum_array_func.restype = POINTER(c_double)
        res_ptr = nancumsum_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type)) 
    
    if axis is None: # 轴为none则结果数组为向量
        res = np.ctypeslib.as_array(res_ptr, shape=(2+c1_new_shape[0]*c1_new_shape[1],))
    else:
        if output_encrypt_type == 0: # 行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]+2))
        else: # 列加密
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)            

def __diff(c1, n):
    c1_double_array = (c_double * (len(c1)))(*c1)

    diff_func = get_func_name("diff")
    diff_func.argtypes = [POINTER(c_double), c_int, c_int]
    diff_func.restype = POINTER(c_double)

    res_ptr = diff_func(c1_double_array, c_int(len(c1)), c_int(n))
    res = np.ctypeslib.as_array(res_ptr, shape=((len(c1)-n),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __diff_array(c1, n, axis, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("diff")
    if axis == 0:
        diff_array_func = get_func_name("diff_array_axis0")
    else:
        diff_array_func = get_func_name("diff_array_axis1")
    diff_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
    diff_array_func.restype = POINTER(c_double)
    res_ptr = diff_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(n), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        if axis == 0:
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]-n, c1_new_shape[1]+2))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]-n+2))
    else:
        if axis == 0:
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2-n, c1_new_shape[1]))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2, c1_new_shape[1]-n))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __ediff1d(c1, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    ediff1d_func = get_func_name("ediff1d")    
    ediff1d_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
    ediff1d_func.restype = POINTER(c_double)

    res_ptr = ediff1d_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type))
    res = np.ctypeslib.as_array(res_ptr, shape=(2+c1_new_shape[0]*c1_new_shape[1]-1,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __gradient(c1):
    c1_double_array = (c_double * (len(c1)))(*c1)

    gradient_func = get_func_name("gradient")
    gradient_func.argtypes = [POINTER(c_double), c_int]
    gradient_func.restype = POINTER(c_double)

    res_ptr = gradient_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __gradient_array(c1, axis, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("gradient")
    gradient_array_axis0_func = get_func_name("gradient_axis0")
    gradient_array_axis0_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    gradient_array_axis0_func.restype = POINTER(c_double)
    gradient_array_axis1_func = get_func_name("gradient_axis1")
    gradient_array_axis1_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    gradient_array_axis1_func.restype = POINTER(c_double)
    if axis is None:
        # if output_encrypt_type == 0:
        res_ptr0 = gradient_array_axis0_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        res_ptr1 = gradient_array_axis1_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        if output_encrypt_type == 0:
            res0 = np.ctypeslib.as_array(res_ptr0, shape=(c1_new_shape[0],2+c1_new_shape[1]))
            res1 = np.ctypeslib.as_array(res_ptr1, shape=(c1_new_shape[0],2+c1_new_shape[1]))
        else:
            res0 = np.ctypeslib.as_array(res_ptr0, shape=(c1_new_shape[0]+2,c1_new_shape[1]))
            res1 = np.ctypeslib.as_array(res_ptr1, shape=(c1_new_shape[0]+2,c1_new_shape[1]))
        res = (CipherArray(res0), CipherArray(res1))
        weakref.finalize(res0, free_double_ptr, res_ptr0)
        weakref.finalize(res1, free_double_ptr, res_ptr1)
    elif axis == 0:
        res_ptr0 = gradient_array_axis0_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        if output_encrypt_type == 0:
            resarr = np.ctypeslib.as_array(res_ptr0, shape=(c1_new_shape[0],2+c1_new_shape[1]))
        else:
            resarr = np.ctypeslib.as_array(res_ptr0, shape=(c1_new_shape[0]+2,c1_new_shape[1]))
        res = CipherArray(resarr)
        weakref.finalize(resarr, free_double_ptr, res_ptr0)
    else:
        res_ptr1 = gradient_array_axis1_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        if output_encrypt_type == 0:
            resarr = np.ctypeslib.as_array(res_ptr1, shape=(c1_new_shape[0],2+c1_new_shape[1]))
        else:
            resarr = np.ctypeslib.as_array(res_ptr1, shape=(c1_new_shape[0]+2,c1_new_shape[1]))
        res = CipherArray(resarr)
        weakref.finalize(resarr, free_double_ptr, res_ptr1)
    return res

def __trapz(c1, x, dx):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    if x is None:
        trapz_func = get_func_name("trapzdx")
        trapz_func.argtypes = [POINTER(c_double), c_int, c_double]
        trapz_func.restype = POINTER(c_double)
        if dx is None:
            res_ptr = trapz_func(c1_double_array, c_int(len(c1)), c_double(1))
        else:
            res_ptr = trapz_func(c1_double_array, c_int(len(c1)), c_double(dx))
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    else:
        x_double_array = (c_double * (len(x)))(*x)
        trapz_func = get_func_name("trapz")
        trapz_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        trapz_func.restype = POINTER(c_double)
        res_ptr = trapz_func(c1_double_array, x_double_array, c_int(len(c1)))
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __trapz_array(c1, x, dx, axis, encrypt_type):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("trapz")
    if x is None:
        if axis == 0:
            trapz_array_func = get_func_name("trapz_array_dx_axis0") 
        else: # axis = 1
            trapz_array_func = get_func_name("trapz_array_dx_axis1")
        trapz_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
        trapz_array_func.restype = POINTER(c_double)
        if dx is None:
            res_ptr = trapz_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_double(1), c_bool(parallel))
        else:
            res_ptr = trapz_array_func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_double(dx), c_bool(parallel))
    else: # x != None
        x = x.reshape(-1,)
        x_double_array = (c_double * (len(x)))(*x)
        if axis == 0:
            trapz_array_func = get_func_name("trapz_array_axis0")
        else:
            trapz_array_func = get_func_name("trapz_array_axis1")
        trapz_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
        trapz_array_func.restype = POINTER(c_double)
        res_ptr = trapz_array_func(c1_double_array, x_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type))
    if axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(2+c1_new_shape[1],))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(2+c1_new_shape[0],))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cross(c1, c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 获取函数并设置函数入参以及返回值
    cross_func = get_func_name("cross")
    cross_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
    cross_func.restype = POINTER(c_double)
    # 调用函数，并将返回C指针转换为ndarray
    res_ptr = cross_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(len(c2)))
    # 密文长度为2则将返回值转换为标量密文，密文长度为3则将返回值转换为长度为3的密文数组
    if int(c1[1]) == 2 and int(c2[1]) == 2:
        res = np.ctypeslib.as_array(res_ptr, shape=(3,))
        # 数组切片
        res1 = res[:1]
        res2 = res[2:]
        res = np.append(res1, res2)
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(5,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cross_array(c1, c2, axis1, axis2, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    c2_shape = c2.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
        c2_new_shape = (c2_shape[0], c2_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])
        c2_new_shape = (c2_shape[0] - 2, c2_shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    cross_array_func = get_func_name("cross_array")
    cross_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int]
    cross_array_func.restype = POINTER(c_double)
    res_ptr = cross_array_func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(c2_shape[0]), c_int(c2_shape[1]), c_int(axis1), c_int(axis2), c_int(encrypt_type), c_int(output_encrypt_type))
    if c1_new_shape[axis1] == 2 and c2_new_shape[axis2] == 2:
        if axis1 == 0:
            res_shape = (1, c1_new_shape[1])
        else:
            res_shape = (1, c1_new_shape[0])
    else:
        if axis1 == 0:
            res_shape = (c1_new_shape[1], 3)
        else:
            res_shape = (c1_new_shape[0], 3)
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(res_shape[0], res_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(res_shape[0]+2, res_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 数组密文的组内求和
def sum(c1, axis=None):
    CHECK_ARRAY(c1, "c1") # 检查输入
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __sum(c1)
    else:
        return __sum_array(c1, axis, encrypt_type)    

# 数组密文的组内求和（将nan视为0）
def nansum(c1, axis=None):
    CHECK_ARRAY(c1, "c1") # 检查输入
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __nansum(c1)
    else:
        return __nansum_array(c1, axis, encrypt_type)

# 密文加法包含 标量加标量、标量加向量、向量加标量、向量加向量
def add(c1, c2, output_encrypt_type=-1):
    if isinstance(c1, CipherArray) and isinstance(c2, CipherArray):
        CHECK_DISCRETE(c1, "c1")
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = c1._broadcast_arrays(c2)
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        c_type1 = c1.get_cipher_type()
        c_type2 = c2.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        c2 = c2.get_base_array()
        if c_type1 == 1 and c_type2 == 1:
            return __add(c1, c2)
        if c1.ndim == 1 and c2.ndim == 1:
            return __add_array(c1, c2)
        if output_encrypt_type != 0 or output_encrypt_type != 1:
            output_encrypt_type = c1_encrypt_type        
        return __add_array_array(c1, c2, c1_encrypt_type, output_encrypt_type)
    elif isinstance(c1, CipherArray) and isinstance(c2, (int, float, np.number)):
        CHECK_DISCRETE(c1, "c1")
        c_type = c1.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        if c_type == 1:
            return __add_double(c1, c2)
        if c1.ndim == 1:
            return __add_array_double(c1, c2)
        else:
            if output_encrypt_type != 0 or output_encrypt_type != 1:
                output_encrypt_type = c1_encrypt_type            
            return __add_array_array_double(c1, c2, c1_encrypt_type, output_encrypt_type)
    elif isinstance(c1, (int, float, np.number)) and isinstance(c2, CipherArray):
        return add(c2, c1, output_encrypt_type=output_encrypt_type)
    else:
        raise ValueError("At least one of c1 and c2 must be of CipherArray type")

# 密文减法 包含 标量减标量、标量减向量、向量减标量、向量减向量
def sub(c1, c2, output_encrypt_type=-1):
    if isinstance(c1, CipherArray) and isinstance(c2, CipherArray):
        CHECK_DISCRETE(c1, "c1")
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = c1._broadcast_arrays(c2)
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        c_type1 = c1.get_cipher_type()
        c_type2 = c2.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        c2 = c2.get_base_array()
        if c_type1 == 1 and c_type2 == 1:
            return __sub(c1, c2)
        if c1.ndim == 1 and c2.ndim == 1:
            return __sub_array(c1, c2)
        if output_encrypt_type != 0 or output_encrypt_type != 1:
            output_encrypt_type = c1_encrypt_type
        return __sub_array_array(c1, c2, c1_encrypt_type, output_encrypt_type)
    elif isinstance(c1, CipherArray) and isinstance(c2, (int, float, np.number)):
        CHECK_DISCRETE(c1, "c1")
        c_type = c1.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        if c_type == 1:
            return __sub_double(c1, c2)
        if c1.ndim == 1:
            return __sub_array_double(c1, c2)
        else:
            if output_encrypt_type != 0 or output_encrypt_type != 1:
                output_encrypt_type = c1_encrypt_type        
            return __sub_array_array_double(c1, c2, c1_encrypt_type, output_encrypt_type)
    elif isinstance(c1, (int, float, np.number)) and isinstance(c2, CipherArray):
        CHECK_DISCRETE(c2, "c2")
        check_res2 = c2.get_cipher_type()
        c2_encrypt_type = c2.get_encryption_type()
        c2 = c2.get_base_array()
        if check_res2 == 1:
            return __sub_double_right(c1, c2) 
        elif check_res2 == 2:
            if c2.ndim == 1:
                return __sub_array_double_right(c1, c2)
            elif c2.ndim == 2:
                if output_encrypt_type == -1:
                    output_encrypt_type = c2_encrypt_type
                return __sub_array_array_double_right(c1, c2, c2_encrypt_type, output_encrypt_type)
    raise ValueError("The input is neither a ciphertext type nor a numerical type.(Param:c1)")
    
# 密文乘法 包含 标量乘标量、标量乘向量、向量乘标量、向量乘向量
def mul(c1, c2, output_encrypt_type=-1, discrete=False):

    if isinstance(c1, CipherArray) and isinstance(c2, CipherArray):
        CHECK_DISCRETE(c1, "c1")
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = c1._broadcast_arrays(c2)
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        c_type1 = c1.get_cipher_type()
        c_type2 = c2.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        c2 = c2.get_base_array()
        if c_type1 == 1 and c_type2 == 1:
            return __mul(c1, c2)
        if c1.ndim == 1 and c2.ndim == 1:
            return __mul_array(c1, c2, discrete)
        
        if output_encrypt_type != 0 or output_encrypt_type != 1:
            output_encrypt_type = c1_encrypt_type

        return __mul_array_array(c1, c2, c1_encrypt_type, output_encrypt_type)
    if isinstance(c1, CipherArray) and isinstance(c2, (int, float, np.number, list, np.ndarray)): 
        CHECK_DISCRETE(c1, "c1")
        c_type = c1.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        # c1 = c1.get_base_array()
        if c_type == 1:
            if isinstance(c2, (int, float, np.number)):
                return __mul_double(c1.get_base_array(), c2)
            else:
                # c1 = broadcast_(c1, (len(c2),), 0)
                c1 = broadcast_to(c1, (len(c2),))
                return __mul_array_double_array(c1.get_base_array(), c2, discrete)
        if c1.ndim == 1:
            if isinstance(c2, (int, float, np.number)):
                return __mul_array_double(c1.get_base_array(), c2, discrete)
            if isinstance(c2, (list, np.ndarray)):
                return __mul_array_double_array(c1.get_base_array(), c2, discrete)
        else:
            if isinstance(c2, (int, float, np.number)):
                if output_encrypt_type != 0 or output_encrypt_type != 1:
                    output_encrypt_type = c1_encrypt_type
                return __mul_array_array_double(c1.get_base_array(), c2, c1_encrypt_type, output_encrypt_type)
            if isinstance(c2, (list, np.ndarray)):
                raise NotImplementedError("Not implemented yet")
    if isinstance(c2, CipherArray) and isinstance(c1, (int, float, np.number, list, np.ndarray)):
        return mul(c2, c1, output_encrypt_type, discrete)
    raise ValueError("The input is neither a ciphertext type nor a numerical type.(Param:c1)")   

# 密文除法 包含 标量除标量、标量除向量、向量除标量、向量除向量
def div(c1, c2, output_encrypt_type=-1):
    if isinstance(c1, CipherArray) and isinstance(c2, CipherArray):
        CHECK_DISCRETE(c1, "c1")
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = c1._broadcast_arrays(c2)
        if c1.get_encryption_type() != c2.get_encryption_type():
            c2 = c2.transEncType()
        c_type1 = c1.get_cipher_type()
        c_type2 = c2.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        c2 = c2.get_base_array()
        if c_type1 == 1 and c_type2 == 1:
            return __div(c1, c2)
        if c1.ndim == 1 and c2.ndim == 1:
            return __div_array(c1, c2)
        if output_encrypt_type != 0 or output_encrypt_type != 1:
            output_encrypt_type = c1_encrypt_type        
        return __div_array_array(c1, c2, c1_encrypt_type, output_encrypt_type)
    elif isinstance(c1, CipherArray) and isinstance(c2, (int, float, np.number)):
        CHECK_DISCRETE(c1, "c1")
        c_type = c1.get_cipher_type()
        c1_encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        if c_type == 1:
            return __div_double(c1, c2)
        if c1.ndim == 1:
            return __div_array_double(c1, c2)
        else:
            if output_encrypt_type != 0 or output_encrypt_type != 1:
                output_encrypt_type = c1_encrypt_type
            return __div_array_array_double(c1, c2, c1_encrypt_type, output_encrypt_type)
    elif isinstance(c1, (int, float, np.number)) and isinstance(c2, CipherArray):
        CHECK_DISCRETE(c2, "c2")
        check_res2 = c2.get_cipher_type()
        c2_encrypt_type = c2.get_encryption_type()
        c2 = c2.get_base_array()
        if check_res2 == 1:
            return __div_double_right(c1, c2) 
        elif check_res2 == 2:
            if c2.ndim == 1:
                return __div_array_double_right(c1, c2)
            elif c2.ndim == 2:
                if output_encrypt_type == -1:
                    output_encrypt_type = c2_encrypt_type
                return __div_array_array_double_right(c2, c1, c2_encrypt_type, output_encrypt_type)
    raise ValueError("The input is neither a ciphertext type nor a numerical type.(Param:c1)")    


# 密文invers(反转之后再做除法运算运算), 包含 标量除标量、标量除向量、向量除标量、向量除向量
def invers(c1, c2, output_encrypt_type=-1):
    return div(c2, c1, output_encrypt_type)

# 逐元素返回倒数 reciprocal 支持标量以及向量
def reciprocal(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __reciprocal(c1)
    else:
        if c1.ndim == 1:
            return __reciprocal_array(c1)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __reciprocal_array_array(c1, encrypt_type, output_encrypt_type)

# 逐元素正数计算 positive 支持标量以及向量
def positive(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __positive(c1)
    else:
        if c1.ndim == 1:
            return __positive_array(c1)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __positive_array_array(c1, encrypt_type, output_encrypt_type)

# 逐元素负数计算 negative 支持标量以及向量
def negative(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __negative(c1)
    else:
        if c1.ndim == 1:
            return __negative_array(c1)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __negative_array_array(c1, encrypt_type, output_encrypt_type)

# 组内乘法
def prod(c1, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __prod(c1)
    else:
        return __prod_array(c1, axis, encrypt_type)    

def nanprod(c1, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __nanprod(c1)
    else:
        return __nanprod_array(c1, axis, encrypt_type)    

# 返回给定轴上元素的累积乘积
def cumprod(c1, axis=None, output_encrypt_type=-1):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __cumprod(c1)
    else:
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type
        return __cumprod_array(c1, axis, encrypt_type, output_encrypt_type)  

# 返回给定轴上元素的累积乘积(将nan视为1)   
def nancumprod(c1, axis=None, output_encrypt_type=-1):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __nancumprod(c1)
    else:
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type
        return __nancumprod_array(c1, axis, encrypt_type, output_encrypt_type)   

# 返回给定轴上元素的累积和
def cumsum(c1, axis=None, output_encrypt_type=-1):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __cumsum(c1)
    else:
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type
        return __cumsum_array(c1, axis, encrypt_type, output_encrypt_type)      

# 返回给定轴上元素的累积和(将nan视为0)
def nancumsum(c1, axis=None, output_encrypt_type=-1):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __nancumsum(c1)
    else:
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type
        return __nancumsum_array(c1, axis, encrypt_type, output_encrypt_type)      

# 计算沿给定轴的第 n 个离散差
def diff(c1, n=1, axis=1, output_encrypt_type=-1):
    CHECK_ARRAY(c1, "c1")
    c1_shape = c1.cipherShape()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        if c1_shape[0] <= n:
            raise ValueError("N must be smaller than the shape of the array!")
        else:
            return __diff(c1, n)
    else:
        if axis == 0:
            if c1_shape[0] <= n:
                raise ValueError("N must be smaller than the shape of the array!")
        else:
            if c1_shape[1] <= n:
                raise ValueError("N must be smaller than the shape of the array!")
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type
        return __diff_array(c1, n, axis, encrypt_type, output_encrypt_type)

# 数组的连续元素之间的差异,并在数组的前后添加指定密文
def ediff1d(c1):
    CHECK_ARRAY(c1, "c1")
    if c1.ndim == 1:
        return diff(c1,1)
    else:
        encrypt_type = c1.get_encryption_type()
        c1 = c1.get_base_array()
        return __ediff1d(c1, encrypt_type)

# 返回数组的梯度
def gradient(c1, axis=None, output_encrypt_type=-1):
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __gradient(c1)
    else:
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type
        return __gradient_array(c1, axis, encrypt_type, output_encrypt_type)

# # 返回两个向量的叉积
def cross(c1, c2, axis1=1, axis2=1, output_encrypt_type=-1):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    CHECK_ARRAY(c2, "c2")
    encrypt_type1 = c1.get_encryption_type()
    if encrypt_type1 != c2.get_encryption_type():
        c2 = c2.transEncType()
    else:pass
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    if c1.ndim == 1:
        return __cross(c1, c2)
    else:
        output_encrypt_type = encrypt_type1 if output_encrypt_type == -1 else output_encrypt_type
        return __cross_array(c1, c2, axis1, axis2, encrypt_type1, output_encrypt_type)
       
# 使用复合梯形规则沿给定轴积分
def trapz(c1, x=None, dx=None, axis=1):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    shape_c1 = c1.cipherShape()
    c1 = c1.get_base_array()
    if c1.ndim==1:
        if x is not None:
            shape_x = x.cipherShape()
            if len(shape_x) != len(shape_c1) or shape_c1[0] != shape_x[0]:
                raise ValueError(f"c1 and x has different shape.[shape of c1 = {shape_c1},shape of x = {shape_x}]")
            else: pass
            x = x.get_base_array()
        else:pass
        return __trapz(c1, x, dx)
    else:
        if x is not None:
            shape_x = x.cipherShape()
            if (len(shape_x) != len(shape_c1) and shape_c1[-1] != shape_x[-1]) or (shape_c1[0] != shape_x[0] and shape_c1[1] != shape_x[1]):
                raise ValueError(f"c1 and x has different shape.[shape of c1 = {shape_c1},shape of x = {shape_x}]")
            else:
                if len(shape_x) == 1 and shape_x[0] == shape_c1[0]:
                    # x = x.get_base_array()
                    # x = broadcast_(x, shape_c1, 3, encrypt_type)
                    # x = CipherArray(x)
                    x = broadcast_to(x, shape_c1, encrypt_type)
                if encrypt_type != x.get_encryption_type():
                    x = x.transEncType()
                else:pass
                x = x.get_base_array()
        else:pass
        return __trapz_array(c1, x, dx, axis, encrypt_type)

# 幂运算
def pow(c1, n, m=1, output_encrypt_type=-1):
    if type(n) != int or type(m) != int:
        raise ValueError("Parameter n or m must be Integer.")
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        if m == 1:
            return __pow(c1, n)
        else:
            return __pow_fractionorder(c1, n, m)
    else:
        if c1.ndim == 1:
            if m == 1:
                return __pow_array(c1, n)
            else:
                return __pow_array_fractionorder(c1, n, m)
        else:
            if m == 1:
                return __pow_array_array(c1, n, encrypt_type, encrypt_type if output_encrypt_type == -1 else output_encrypt_type)
            else:
                return __pow_array_array_fractionorder(c1, n, m, encrypt_type, encrypt_type if output_encrypt_type == -1 else output_encrypt_type)      

# 自然底数对数
def log(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __log(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __log_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __log_array_array(c1, encrypt_type, output_encrypt_type)

# log以10为底对数
def log10(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __log10(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __log10_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __log10_array_array(c1, encrypt_type, output_encrypt_type)
    
# log以2为底
def log2(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __log2(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __log2_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __log2_array_array(c1, encrypt_type, output_encrypt_type)

# 指数运算
def exp(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __exp(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __exp_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __exp_array_array(c1, encrypt_type, output_encrypt_type)

# exp(c) -1
def expm1(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __expm1(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __expm1_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __expm1_array_array(c1, encrypt_type, output_encrypt_type)

# 2^c
def exp2(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array() 
    if check_res == 1:
        return __exp2(c1)
    elif check_res == 2:
        if c1.ndim == 1:
            return __exp2_array(c1)
        elif c1.ndim == 2:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __exp2_array_array(c1, encrypt_type, output_encrypt_type)

# 返回小于或等于输入除法的最大整数（输入中可能包含明文）
def floor_divide(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    if isinstance(c2, (int, float, np.number)):
        if c1.get_cipher_type() == 1:
            return __floor_div_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __floor_div_array_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __floor_div_array_array_double(c1.get_base_array(), c2, c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)
    elif isinstance(c2, CipherArray):
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
        if c1.get_cipher_type() == 1:
            return __floor_div(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __floor_div_array(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __floor_div_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)

# 返回除法的余数
def fmod(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    if isinstance(c2, (int, float, np.number)):
        if c1.get_cipher_type() == 1:
            return __fmod_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __fmod_array_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __fmod_array_array_double(c1.get_base_array(), c2, c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)
    elif isinstance(c2, CipherArray):
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
        if c1.get_cipher_type() == 1:
            return __fmod(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __fmod_array(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __fmod_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)


# 返回除法元素的余数
def mod(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    if isinstance(c2, (int, float, np.number)):
        if c1.get_cipher_type() == 1:
            return __mod_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __mod_array_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __mod_array_array_double(c1.get_base_array(), c2, c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)
    elif isinstance(c2, CipherArray):
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
        if c1.get_cipher_type() == 1:
            return __mod(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __mod_array(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __mod_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)

# remainder函数与mod函数功能相同
def remainder(c1,c2, output_encrypt_type=-1):
    return mod(c1,c2, output_encrypt_type)

def modf(c1, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return __modf(c1)
    else:
        if c1.ndim == 1:
            return __modf_array(c1)
        else:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type
            return __modf_array_array(c1, encrypt_type, output_encrypt_type)

# 同时返回逐元素的商和余数
def divmod(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    if isinstance(c2, (int, float, np.number)):
        if c1.get_cipher_type() == 1:
            return __divmod_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __divmod_array_double(c1.get_base_array(), c2)
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __divmod_array_array_double(c1.get_base_array(), c2, c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)
    elif isinstance(c2, CipherArray):
        CHECK_DISCRETE(c2, "c2")
        c1, c2 = broadcast_arrays(c1, c2, c1.get_encryption_type())
        if c1.get_cipher_type() == 1:
            return __divmod(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 1:
            return __divmod_array(c1.get_base_array(), c2.get_base_array())
        elif c1.get_cipher_type() == 2 and c1.ndim == 2:
            return __divmod_array_array(c1.get_base_array(), c2.get_base_array(), c1.get_encryption_type(), c1.get_encryption_type() if output_encrypt_type == -1 else output_encrypt_type)


def float_power(c1, m, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")    
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1: # 标量密文
        return __float_power(c1, m)
    else:
        if c1.ndim == 1:
            return __float_power_array(c1, m)
        else:
            return __float_power_array_array(c1, m, encrypt_type, encrypt_type if output_encrypt_type==-1 else output_encrypt_type)