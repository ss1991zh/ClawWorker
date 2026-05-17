import numpy as np
import math
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
    free_int_ptr, 
    free_double_ptr, 
    cipherLen, 
    get_func_parallelization_config, 
    CHECK_ARRAY
)
from henumpy.base.cipher_array import CipherArray

__all__ = ["min", "max", "nanmin", "nanmax", "ptp", "percentile", "nanpercentile", "quantile", "nanquantile",
        "median", "nanmedian", "average", "mean", "nanmean", "std", "nanstd", "var", "nanvar", "corrcoef",
        "correlate", "cov", "digitize"]

# digitize
def __digitize(c1, c2, b):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    if b :
        digitize_func = get_func_name("digitize_true")
    else:
        digitize_func = get_func_name("digitize_false")
    digitize_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
    digitize_func.restype = POINTER(c_int)

    res_ptr = digitize_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(len(c2)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __digitize_array(c1, c2, encrypt_type, b):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])   
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("digitize")
    if b:
        func = get_func_name("digitize_array_true")
    else:
        func = get_func_name("digitize_array_false")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_int)
    res_ptr = func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(len(c2)), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0], c1_new_shape[1]))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __vector_func(c1, func_name):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置参数以及返回值
    func = get_func_name(func_name)
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = POINTER(c_double)
    
    res_ptr = func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __2darray_func(c1, axis, encrypt_type, func_name):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])    
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config(func_name)
    if axis is None: # 根据轴拼接函数名
        func_name += "_array_axisnone"
    elif axis == 0:
        func_name += "_array_axis0"
    else:
        func_name += "_array_axis1"
    func = get_func_name(func_name)
    func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1]+2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __varstd_func(c1, ddof, func_name):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置参数以及返回值
    func = get_func_name(func_name)
    func.argtypes = [POINTER(c_double), c_int, c_int]
    func.restype = POINTER(c_double)
    
    res_ptr = func(c1_double_array, c_int(len(c1)), c_int(ddof))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __varstd_2darray_func(c1, axis, encrypt_type, ddof, func_name):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])    
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config(func_name)
    if axis is None: # 根据轴拼接函数名
        func_name += "_array_axisnone"
    elif axis == 0:
        func_name += "_array_axis0"
    else:
        func_name += "_array_axis1"
    func = get_func_name(func_name)
    func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_int(ddof), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1]+2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

def __vector_func_q(c1, func_name, q):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置参数以及返回值
    func = get_func_name(func_name)
    func.argtypes = [POINTER(c_double), c_int, c_double]
    func.restype = POINTER(c_double)
    
    res_ptr = func(c1_double_array, c_int(len(c1)), c_double(q))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __2darray_func_q(c1, axis, encrypt_type, func_name, q):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])    
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config(func_name)
    if axis is None: # 根据轴拼接函数名
        func_name += "_array_axisnone"
    elif axis == 0:
        func_name += "_array_axis0"
    else:
        func_name += "_array_axis1"
    func = get_func_name(func_name)
    func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_double(q), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1]+2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)        

def __average(c1, weights):
    c1_double_array = (c_double * len(c1))(*c1)
    weights_double_array = (c_double * len(weights))(*weights)
    func = get_func_name("average")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, weights_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

def __average_double(c1, weights):
    c1_double_array = (c_double * len(c1))(*c1)
    weights_double_array = (c_double * len(weights))(*weights)
    func = get_func_name("average_double")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, weights_double_array, c_int(len(c1)), c_int(len(weights)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __average_array(c1, weights, axis, encrypt_type):
    parallel = get_func_parallelization_config("average")
    if axis is None:
        func = get_func_name("average_array_axisnone")
    elif axis == 0:
        func = get_func_name("average_array_axis0")
    else:
        func = get_func_name("average_array_axis1")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_double)
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])    
    c1 = c1.reshape(-1,)
    weights = weights.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    weights_double_array = (c_double * len(weights))(*weights)
    res_ptr = func(c1_double_array, weights_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1]+2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __average_array_double(c1, weights, axis, encrypt_type):
    parallel = get_func_parallelization_config("average")
    if axis is None:
        func = get_func_name("average_array_double_axisnone")
    elif axis == 0:
        func = get_func_name("average_array_double_axis0")
    else:
        func = get_func_name("average_array_double_axis1")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_double)
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])  
    c1 = c1.reshape(-1,)
    weights = weights.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    weights_double_array = (c_double * len(weights))(*weights)
    res_ptr = func(c1_double_array, weights_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(c1_new_shape[0]), c_int(c1_new_shape[1]), c_int(encrypt_type), c_bool(parallel))    
    if axis is None:
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1]+2,))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0]+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

def __cov_one_input(c1):
    c1_double_array = (c_double * len(c1))(*c1)
    func = get_func_name("cov_one_input")
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cov_two_input(c1, c2, output_encrypt_type):
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    func = get_func_name("cov_two_input")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res_shape = (2, 4)
    else:
        res_shape = (4, 2)
    res = np.ctypeslib.as_array(res_ptr, shape=res_shape)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cov_2darray_one_input(c1, c1_cipherShape, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    x_c1 = c1_shape[0] # 数组c1的行数
    y_c1 = c1_shape[1] # 数组c1的列数
    c1 = c1.reshape(-1,)
    # 将一维ndarray转换为c数组
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("cov")
    # 调用go函数
    cov_func = get_func_name("cov_2darray_one_input")
    cov_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    cov_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = encrypt_type
    res_ptr = cov_func(c1_double_array, c_int(x_c1), c_int(y_c1), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))

    if output_encrypt_type == 0:
        res_shape = (c1_cipherShape[0], c1_cipherShape[0]+2)
    else:
        res_shape = (c1_cipherShape[0]+2, c1_cipherShape[0])
    res=  np.ctypeslib.as_array(res_ptr, shape=res_shape)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __cov_2darray_two_input(c1, c2, c1_cipherShape, c2_cipherShape, encrypt_type, output_encrypt_type):
    c1_shape = c1.shape
    c2_shape = c2.shape
    x_c1 = c1_shape[0] # 数组c1的行数
    y_c1 = c1_shape[1] # 数组c1的列数
    x_c2 = c2_shape[0] # 数组c2的行数
    y_c2 = c2_shape[1] # 数组c2的列数
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    # 将一维ndarray转换为c数组
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("cov")
    # 调用go函数
    cov_func = get_func_name("cov_2darray_two_input")
    cov_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    cov_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = encrypt_type
    res_ptr = cov_func(c1_double_array, c2_double_array, c_int(x_c1), c_int(y_c1), c_int(x_c2), c_int(y_c2), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))

    if output_encrypt_type == 0:
        res_shape = (c1_cipherShape[0]+c2_cipherShape[0], c1_cipherShape[0]+c2_cipherShape[0]+2)
    else:
        res_shape = (c1_cipherShape[0]+c2_cipherShape[0]+2, c1_cipherShape[0]+c2_cipherShape[0])
    res = np.ctypeslib.as_array(res_ptr, shape=res_shape)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def min(c1, axis=None):
    # 输入检测
    CHECK_ARRAY(c1, "c1")
    encrypt = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __vector_func(c1, "min")
    else:
        return __2darray_func(c1, axis, encrypt, "min")
        
# 返回密文数组的最大值
def max(c1, axis=None):
    # 输入检测
    CHECK_ARRAY(c1, "c1")
    encrypt = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __vector_func(c1, "max")
    else:
        return __2darray_func(c1, axis, encrypt, "max")            

# 返回数组的最小值，忽略Nan
def nanmin(c1, axis=None):
    # 输入检测
    CHECK_ARRAY(c1, "c1")
    encrypt = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __vector_func(c1, "nanmin")
    else:
        return __2darray_func(c1, axis, encrypt, "nanmin")    

# 返回数组的最大值，忽略Nan
def nanmax(c1, axis=None):
    # 输入检测
    CHECK_ARRAY(c1, "c1")
    encrypt = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if c1.ndim == 1:
        return __vector_func(c1, "nanmax")
    else:
        return __2darray_func(c1, axis, encrypt, "nanmax")    

# # 沿轴的值的范围
def ptp(c1, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "ptp"
    if c1.ndim == 1:
        return __vector_func(c1, func_name)
    else:
        return __2darray_func(c1, axis, encrypt_type, func_name)

# 沿着指定的轴计算数据的第 q 个百分位数
def percentile(c1, q, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()  
    func_name = "percentile"
    if q < 0.0 or q > 100.0:
        raise ValueError("q's value must be between 0 and 100 (inclusive)")
    if c1.ndim == 1:
        return __vector_func_q(c1, func_name, q)
    else:
        return __2darray_func_q(c1, axis, encrypt_type, func_name, q)    

# 沿着指定的轴计算数据的第 q 个百分位数,忽略Nan
def nanpercentile(c1, q, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()  
    func_name = "nanpercentile"
    if q < 0.0 or q > 100.0:
        raise ValueError("q's value must be between 0 and 100 (inclusive)")
    if c1.ndim == 1:
        return __vector_func_q(c1, func_name, q)
    else:
        return __2darray_func_q(c1, axis, encrypt_type, func_name, q)  

# 沿着指定的轴计算数据的第 q 个分位数
def quantile(c1, q, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()  
    func_name = "quantile"
    if q < 0.0 or q > 1.0:
        raise ValueError("q's value must be between 0 and 1 (inclusive)")
    if c1.ndim == 1:
        return __vector_func_q(c1, func_name, q)
    else:
        return __2darray_func_q(c1, axis, encrypt_type, func_name, q)  

# 沿着指定的轴计算数据的第 q 个分位数，忽略Nan
def nanquantile(c1, q, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()  
    func_name = "nanquantile"
    if q < 0.0 or q > 1.0:
        raise ValueError("q's value must be between 0 and 1 (inclusive)")
    if c1.ndim == 1:
        return __vector_func_q(c1, func_name, q)
    else:
        return __2darray_func_q(c1, axis, encrypt_type, func_name, q)  

# 沿指定轴计算中位数
def median(c1, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "median"
    if c1.ndim == 1:
        return __vector_func(c1, func_name)
    else:
        return __2darray_func(c1, axis, encrypt_type, func_name)    

# 沿指定轴计算中位数，忽略nan
def nanmedian(c1, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "nanmedian" 
    if c1.ndim == 1:
        return __vector_func(c1, func_name)
    else:
        return __2darray_func(c1, axis, encrypt_type, func_name)  

def average(c1, weight=None, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    if weight is None:
        return mean(c1, axis)
    else:
        encrypt_type = c1.get_encryption_type()
        c1_shape = c1.cipherShape()
        c1 = c1.get_base_array()
        if type(weight) == np.ndarray:
            if c1.ndim == 1 and weight.ndim == 1:
                if len(c1) != len(weight):
                    raise ValueError("The length of c1 is not equal to the length of weights.")
                else:
                    return __average_double(c1, weight)
            elif c1.ndim == 2:
                if weight.ndim == 2:
                    if c1_shape[0] != weight.shape[0] or c1_shape[1] != weight.shape[1]:
                        raise ValueError(f"c1 and weight has different shape.[shape of c1 = {c1_shape},shape of weight = {weight.shape}]")
                    else:
                        pass
                else:
                    if axis is None:
                        raise TypeError("Axis must be specified when shapes of a and weights differ.")
                    elif axis == 0:
                        if c1_shape[0] != weight.shape[0]:
                            raise ValueError("Length of weights not compatible with specified axis.")
                        else:
                            tmp = weight.tolist()
                            weight = []
                            for element in tmp:
                                l = [element] * c1_shape[1]
                                weight.append(l)
                            weight = np.array(weight)
                    else:
                        if c1_shape[1] != weight.shape[0]:
                            raise ValueError("Length of weights not compatible with specified axis.")
                        else:
                            tmp = weight.tolist()
                            weight = []
                            for i in range(c1_shape[0]):
                                weight.append(tmp)
                            weight = np.array(weight)                            
                return __average_array_double(c1, weight, axis, encrypt_type)
            else:
                raise ValueError("1D weights expected when shapes of c1 and weights differ.")
        elif type(weight) == CipherArray:
            CHECK_ARRAY(weight, "c2")
            if weight.ndim == 1:
                weight_shape = weight.cipherShape()
                weight = weight.get_base_array()
                if c1.ndim == 1:
                    if len(c1) != len(weight):
                        raise ValueError("The length of c1 is not equal to the length of weights.")
                    else:
                        return __average(c1, weight)
                else: # c1.ndim == 2
                    if axis is None:
                        raise TypeError("Axis must be specified when shapes of a and weights differ.")
                    elif axis == 0:
                        if c1_shape[0] != weight_shape[0]:
                            raise ValueError("Length of weights not compatible with specified axis.")
                        else: # 广播
                            if encrypt_type == 0:
                                head = weight[:1].tolist()
                                A = weight[2:].tolist()
                                l = []
                                for element in A:
                                    tmp = head + [c1_shape[1]] + [element]*c1_shape[1] # 返回一个新对象
                                    l.append(tmp)
                                weight = np.array(l)
                            else: # encrypt_type = 1
                                weight = weight.reshape(-1,1)
                                weight = weight.tolist()
                                l = []
                                for element in weight:
                                    tmp = element * c1_shape[1]
                                    l.append(tmp)
                                weight = np.array(l)
                    else: # axis == 1
                        if c1_shape[1] != weight_shape[0]:
                            raise ValueError("Length of weights not compatible with specified axis.")
                        else: # 广播
                            if encrypt_type == 0:
                                l = [weight.tolist()]
                                l = l * c1_shape[0]
                                weight = np.array(l)
                            else: # 列加密
                                l = []
                                x1 = [weight[0]] * weight_shape[0]
                                x2 = [weight[1]] * weight_shape[0]
                                y1 = [weight[2]] * weight_shape[0]
                                y2 = [weight[3]] * weight_shape[0]
                                L = [weight[1]] * weight_shape[0]
                                l.append(x1)
                                l.append(x2)
                                l.append(y1)
                                l.append(y2)
                                l.append(L)
                                A = weight[2:].tolist()
                                for i in range(c1_shape[0]):
                                    l.append(A)
                                weight = np.array(l)
                    return __average_array(c1, weight, axis, encrypt_type)
            else: # weight.ndim = 2
                weight_shape = weight.cipherShape()
                if c1.ndim == 1:                
                    raise ValueError("1D weights expected when shapes of c1 and weights differ.")
                else:
                    if c1_shape[0] != weight_shape[0] or c1_shape[1] != weight_shape[1]:
                        raise ValueError(f"The shapes of the two array are inconsistent and cannot be calculated.[c1_shape={c1_shape}, weights_shape={weight_shape}]")
                    else:
                        if weight.get_encryption_type() != encrypt_type:
                            weight = weight.transEncType()
                        weight = weight.get_base_array()
                return __average_array(c1, weight, axis, encrypt_type)

def mean(c1, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "mean"
    if c1.ndim == 1:
        return __vector_func(c1, func_name)
    else:
        return __2darray_func(c1, axis, encrypt_type, func_name)    

# 计算算术平均 忽略nan
def nanmean(c1, axis=None):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "nanmean"
    if c1.ndim == 1:
        return __vector_func(c1, func_name)
    else:
        return __2darray_func(c1, axis, encrypt_type, func_name)    

# 计算沿指定轴的标准差
def std(c1, axis=None, ddof=0):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "std"
    if c1.ndim == 1:
        return __varstd_func(c1, ddof, func_name)
    else:
        return __varstd_2darray_func(c1, axis, encrypt_type, ddof, func_name)

# 计算沿指定轴的标准差,忽略nan
def nanstd(c1, axis=None, ddof=0):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "nanstd"
    if c1.ndim == 1:
        return __varstd_func(c1, ddof, func_name)
    else:
        return __varstd_2darray_func(c1, axis, encrypt_type, ddof, func_name)

# 计算沿指定轴的方差
def var(c1, axis=None, ddof=0):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "var"
    if c1.ndim == 1:
        return __varstd_func(c1, ddof, func_name)
    else:
        return __varstd_2darray_func(c1, axis, encrypt_type, ddof, func_name)    

# 计算沿指定轴的方差，忽略nan
def nanvar(c1, axis=None, ddof=0):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    func_name = "nanvar"
    if c1.ndim == 1:
        return __varstd_func(c1, ddof, func_name)
    else:
        return __varstd_2darray_func(c1, axis, encrypt_type, ddof, func_name)

# 返回皮尔逊乘积矩相关系数
def corrcoef(c1, c2, output_encrypt_type=-1):
    # 输入检测，检测维度是否相同
    c1_cipherShape = c1.cipherShape()
    c2_cipherShape = c2.cipherShape()
    if c1_cipherShape[0] != c2_cipherShape[0] or c2_cipherShape[1] != c2_cipherShape[1]:
        raise ValueError("The shapes of the input two arrays are not consistent, please check the input.")
    encrypt_type = c1.encryption_type # 默认c1与c2具有相同的加密类型
    c1_shape = c1.shape
    c2_shape = c2.shape
    x_c1 = c1_shape[0] # 数组c1的行数
    y_c1 = c1_shape[1] # 数组c1的列数
    x_c2 = c2_shape[0] # 数组c2的行数
    y_c2 = c2_shape[1] # 数组c2的列数
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    # 将一维ndarray转换为c数组
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("corrcoef")
    # 调用go函数
    corrcoef_func = get_func_name("corrcoef")
    corrcoef_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    corrcoef_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = encrypt_type
    res_ptr = corrcoef_func(c1_double_array, c2_double_array, c_int(x_c1), c_int(y_c1), c_int(x_c2), c_int(y_c2), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(2*c1_cipherShape[0], 2*c1_cipherShape[0]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(2*c1_cipherShape[0]+2, 2*c1_cipherShape[0]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 返回两个一维序列的互相关
def correlate(c1, c2, mode="valid"):
    # 输入检测
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    if check_res1 != 2 or c1.ndim != 1:
        raise ValueError("Can only handle vector ciphertext, please enter vector ciphertext!(Param:c1)")
    if check_res2 != 2 or c2.ndim != 1:
        raise ValueError("Can only handle vector ciphertext, please enter vector ciphertext!(Param:c2)")
    # 类型转换
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 根据mode选择执行函数,并设置返回值长度
    if mode == "valid":
        correlate_func = get_func_name("correlate_valid")
        length = 3 + int(abs(c1[1]-c2[1]))
    elif mode == "full":
        correlate_func = get_func_name("correlate_full")
        length = 1 + int(c1[1] + c2[1])
    elif mode =="same":
        correlate_func = get_func_name("correlate_same")
        maxmn = c1[1]
        if c1[1] < c2[1]:
            maxmn = c2[1]
        length = 2 + int(maxmn)
    else:
        raise ValueError("The parameter 'mode' must be one of valid, same, or full!")
    # 调用go函数
    correlate_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
    correlate_func.restype = POINTER(c_double)
    res_ptr = correlate_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(len(c2)))
    res = np.ctypeslib.as_array(res_ptr, shape=(length,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 估计协方差矩阵
def cov(c1, c2=None, output_encrypt_type=-1):
    if c2 is None:
        if c1.get_cipher_type() != 2 :
            raise ValueError("Can only handle vector ciphertext, please enter vector ciphertext!(Param:c1)")
        if c1.ndim == 1:
            c1 = c1.get_base_array()
            return __cov_one_input(c1)
        elif c1.ndim == 2:
            # 如果c1的形状为(1，n)则将其转换为向量
            if c1.cipherShape()[0] == 1:
                c1 = c1[0]
                return __cov_one_input(c1.get_base_array())
            encrypt_type = c1.get_encryption_type()
            if output_encrypt_type != 0 or output_encrypt_type != 1:
                output_encrypt_type = encrypt_type
            c1_cipherShape = c1.cipherShape()
            c1 = c1.get_base_array()
            return __cov_2darray_one_input(c1, c1_cipherShape, encrypt_type, output_encrypt_type)
        else:
            raise ValueError("The parameter c1 must be a 1D or 2D array.")

    else:
        if c1.get_cipher_type() != 2 or c2.get_cipher_type() != 2:
            raise ValueError(f"Can only handle vector ciphertext, please enter vector ciphertext!{'(Param:c1)' if c1.get_cipher_type() != 2 else '(Param:c2)'}")
        if c1.ndim == 1:
            if c2.ndim == 1:
                if cipherLen(c2) != cipherLen(c1):
                    raise ValueError("The length of c1 is not equal to the length of c2.")
                c1 = c1.get_base_array()
                c2 = c2.get_base_array()
                return __cov_two_input(c1, c2, 0)
            elif c2.ndim == 2:
                if c2.cipherShape()[1] != cipherLen(c1):
                    raise ValueError(f"The length of c1 is {cipherLen(c1)}, but zhe length of c2 with axis1 is {c2.cipherShape()[1]}.")
                c1 = c1.cipherReshape(1, cipherLen(c1), c2.get_encryption_type())
                c1_cipherShape = c1.cipherShape()
                c2_cipherShape = c2.cipherShape()
                if output_encrypt_type != 0 and output_encrypt_type != 1:
                    output_encrypt_type = c1.get_encryption_type()
                return __cov_2darray_two_input(c1.get_base_array(), c2.get_base_array(), c1_cipherShape, c2_cipherShape, c1.get_encryption_type(), output_encrypt_type)
        elif c1.ndim == 2:
            if c2.ndim == 1:
                if cipherLen(c2) != c1.cipherShape()[1]:
                    raise ValueError(f"The length of c2 is {cipherLen(c2)}, but zhe length of c1 with axis1 is {c1.cipherShape()[1]}.")
                c2 = c2.cipherReshape(1, cipherLen(c2), c1.get_encryption_type())
            elif c2.ndim == 2:
                if c1.cipherShape()[1] != c2.cipherShape()[1]:
                    raise ValueError(f"The length of c1 with axis1 is {c1.cipherShape()[1]}, but the length of c2 with axis1 is {c2.cipherShape()[1]}.")
                if c1.get_encryption_type() != c2.get_encryption_type():
                   c2 = c2.transEncType()

            if output_encrypt_type != 0 and output_encrypt_type != 1:
                output_encrypt_type = c1.get_encryption_type()
            return __cov_2darray_two_input(c1.get_base_array(), c2.get_base_array(), c1.cipherShape(), c2.cipherShape(), c1.get_encryption_type(), output_encrypt_type)

# 返回输入数组中每个值所属的 bin 的索引
def digitize(c1, c2, right=False):
    # 类型检测
    CHECK_ARRAY(c1, "c1")
    CHECK_ARRAY(c2, "c2")
    encrypt_type1 = c1.get_encryption_type()
    encrypt_type2 = c2.get_encryption_type()
    if c1.ndim == 1:
        if c2.ndim == 1:
            if cipherLen(c2) < 2:
                raise ValueError(f"The length must be greater than 2.[len(c2)={cipherLen(c2)}]")
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            return __digitize(c1, c2, right)
        else: # c2.ndim = 2
            raise ValueError("The parameter c2 must be a 1D vector.")            
    else: # c1.ndim = 2
        if c2.ndim == 1:
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            return __digitize_array(c1, c2, encrypt_type1, right)
        else:
            raise ValueError("The parameter c2 must be a 1D vector.")                            