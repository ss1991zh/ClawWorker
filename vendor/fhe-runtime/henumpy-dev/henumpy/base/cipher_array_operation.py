from typing import List
import numpy as np
from ctypes import *
from .base_function import (
    get_func_name, 
    get_func_parallelization_config, 
    free_bool_ptr, 
    free_double_ptr, 
    free_int_ptr
)
import weakref
from .cipher_array import CipherArray
import copy

__all__ = ["take", "unique", "empty", "empty_array", "argmin", "argmax", "ones", "ones_array",
           "ones_like", "zeros", "zeros_array", "zeros_like", "full", "arange", "linspace", "append", 
           "argsort", "insert", "broadcast_to", "broadcast_arrays"]

# 获取指定索引位置列表的元素
def take(cipher_array, indices, axis=None):
    cipher_type = cipher_array.get_cipher_type()
    encryption_type = cipher_array.get_encryption_type()
    cipher_base_array = cipher_array.get_base_array()
    if isinstance(indices, List):
        indices = np.asarray(indices)
    else:
        if not isinstance(indices, np.ndarray):
            raise ValueError("must use array like indices, both list or ndarray obj")
    # if cipher_base_array.ndim > 1:
    #     raise ValueError("Arrays with dimensions greater than 1 are not currently supported")

    if cipher_type == 1 : # 标量密文
        raise ValueError("Take operation is not allowed to permit on scalar value")
        # return CipherArray(np.insert(cipher_base_array, 4, 1))
    
    elif cipher_type == 2 : # 数组密文
        if cipher_base_array.ndim == 1: # 一维数组
            res = [cipher_base_array[0], float(len(indices))]
            res += np.take(cipher_base_array[2:], indices).tolist()
            return CipherArray(np.array(res))
        elif cipher_base_array.ndim == 2: # 二维数组
            if encryption_type == 0:
                # 行加密
                if indices.ndim == 1:
                    # 按照axis取
                    res = None
                    if axis is None or axis == 0: # 按行取
                        res = cipher_base_array[indices, :]
                    elif axis == 1: # 按列区
                        indices = indices + 2 # 由于是ndarray会自动广播
                        ret = cipher_base_array[:, indices]
                        head = cipher_base_array[:, :2]
                        head[:, 1] = float(len(indices))
                        res = np.hstack((head, ret))
                    return CipherArray(res)
                elif indices.ndim == 2:
                    # 由于可能取到不同列的值 所以需要重新构造
                    raise ValueError("Not implemented now")
                else:
                    raise ValueError("dimensions higher not allowed")
            else:
                # 列加密
                if indices.ndim == 1:
                    # 按照axis取
                    res = None
                    if axis is None or axis == 0: # 按行取
                        indices = indices + 2
                        ret = cipher_base_array[indices, :]
                        head = cipher_base_array[:2, :]
                        head[1, :] = float(len(indices))
                        res = np.vstack((head, ret))
                    elif axis == 1: # 按列区
                        res = cipher_base_array[:, indices]
                    return CipherArray(res)
                elif indices.ndim == 2:
                    # 由于可能取到不同列的值 所以需要重新构造
                    raise ValueError("Not implemented now")
                else:
                    raise ValueError("dimensions higher not allowed")
        else:
            raise ValueError("Arrays with dimensions greater than 2 are not currently supported")
            
    elif cipher_type == 3 : # 离散数组密文
        raise ValueError("Discrete arrays are not currently supported")
    
    else:
        raise ValueError("Cipher type error")

# 获取一个 cipher对象的unique列表
def unique(c1):
    # 输入检测
    check_res = c1.get_cipher_type()
    c1 = c1.get_base_array()
    if check_res == 1:
        return c1
    elif check_res == 2:
        if c1.ndim == 1:
            res = [c1[0]]
            uni = np.unique(c1[2:])
            res += [float(len(uni))]
            res += uni.tolist()
            return CipherArray(res)
        elif c1.ndim == 2:
            raise ValueError("2-d cihper array not currently supported")
        else:
            raise ValueError("dimensions higher not currently supported")
    else:
        raise ValueError("Discrete arrays are not currently supported")

def __argsort(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    argsort_func = get_func_name("argsort")
    argsort_func.argtypes = [POINTER(c_double), c_int]
    argsort_func.restype = POINTER(c_int)
    res_ptr = argsort_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __argsort_decrement(c1):
    # 类型转换
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    argsort_decrement_func = get_func_name("argsort_decrement")
    argsort_decrement_func.argtypes = [POINTER(c_double), c_int]
    argsort_decrement_func.restype = POINTER(c_int)
    res_ptr = argsort_decrement_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __argsort_array_one(c1, encrypt_type):
    shape_c1 = c1.shape
    # 计算密文形状
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0]-2, shape_c1[1])
    c1 = c1.reshape(-1,) # 将二维数组转为一维
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("argsort")
    # 调用go函数
    argsort_array_one_func = get_func_name("argsort_array_one")
    argsort_array_one_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    argsort_array_one_func.restype = POINTER(c_int)
    res_ptr = argsort_array_one_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __argsort_array_one_decrement(c1, encrypt_type):
    shape_c1 = c1.shape
    # 计算密文形状
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0]-2, shape_c1[1])
    c1 = c1.reshape(-1,) # 将二维数组转为一维
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("argsort")
    # 调用go函数
    argsort_array_one_decrement_func = get_func_name("argsort_array_one_decrement")
    argsort_array_one_decrement_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    argsort_array_one_decrement_func.restype = POINTER(c_int)
    res_ptr = argsort_array_one_decrement_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __argsort_array_zero(c1, encrypt_type):
    shape_c1 = c1.shape
    # 计算密文形状
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0]-2, shape_c1[1])
    c1 = c1.reshape(-1,) # 将二维数组转为一维
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("argsort")
    # 调用go函数
    argsort_array_zero_func = get_func_name("argsort_array_zero")
    argsort_array_zero_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    argsort_array_zero_func.restype = POINTER(c_int)
    res_ptr = argsort_array_zero_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __argsort_array_zero_decrement(c1, encrypt_type):
    shape_c1 = c1.shape
    # 计算密文形状
    if encrypt_type == 0: # 行加密
        shape_c1_new = (shape_c1[0], shape_c1[1]-2)
    else: # 列加密
        shape_c1_new = (shape_c1[0] - 2, shape_c1[1])
    c1 = c1.reshape(-1,) # 将二维数组转为一维
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("argsort")
    # 调用go函数
    argsort_array_zero_decrement_func = get_func_name("argsort_array_zero_decrement")
    argsort_array_zero_decrement_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    argsort_array_zero_decrement_func.restype = POINTER(c_int)
    res_ptr = argsort_array_zero_decrement_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def __insert(c1, index, c2, axis, encrypt_type, output_encrypt_type):
    if encrypt_type == 0:
        shape_c1 = (c1.shape[0], c1.shape[1]-2)
    else:
        shape_c1 = (c1.shape[0]-2, c1.shape[1])        
    if output_encrypt_type == 0 and axis == 0:
        shape_c1_new = (shape_c1[0]+1, shape_c1[1]+2)
    elif output_encrypt_type == 0 and axis == 1:
        shape_c1_new = (shape_c1[0], shape_c1[1]+3)
    elif output_encrypt_type == 1 and axis == 0:
        shape_c1_new = (shape_c1[0]+3, shape_c1[1])
    else:
        shape_c1_new = (shape_c1[0]+2, shape_c1[1]+1)
    shape_c1 = c1.shape
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    insert_func = get_func_name("insert")
    insert_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, POINTER(c_double), c_int, c_int]
    insert_func.restype = POINTER(c_double)
    res_ptr = insert_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_int(output_encrypt_type), c2_double_array, c_int(len(c2)), c_int(index))
    res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __argminmax(c1, func_name):
    c1_double_array = (c_double * (len(c1)))(*c1)

    func = get_func_name(func_name)
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = c_int

    res = func(c1_double_array, c_int(len(c1)))
    return int(res)  

def __argminmax_array(c1, axis, encrypt_type, func_name):
    c1_shape = c1.shape
    if encrypt_type == 0:
        c1_new_shape = (c1_shape[0], c1_shape[1] - 2)
    else:
        c1_new_shape = (c1_shape[0] - 2, c1_shape[1])   
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config(func_name)
    if axis is None:
        name = func_name + "_array_axisnone"
        func = get_func_name(name)
        func.restype = c_int
    elif axis == 0 :
        name = func_name + "_array_axis0" 
        func = get_func_name(name)
        func.restype = POINTER(c_int)   
    else:
        name = func_name + "_array_axis1" 
        func = get_func_name(name)
        func.restype = POINTER(c_int)
    func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    res_ptr = func(c1_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(encrypt_type), c_bool(parallel))
    if axis is None:
        return int(res_ptr)
    elif axis == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[1],))
        weakref.finalize(res, free_int_ptr, res_ptr)
        return res
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(c1_new_shape[0],))
        weakref.finalize(res, free_int_ptr, res_ptr)
        return res

# 标量密文添加到向量密文
def __append(c1,c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    append_func = get_func_name("append")
    append_func.argtypes = [POINTER(c_double), c_int, POINTER(c_double), c_int]
    append_func.restype = POINTER(c_double)

    res_ptr = append_func(c1_double_array, c_int(len(c1)), c2_double_array, c_int(len(c2)))
    if c1[1] == 0 and c1[2] == 0.0:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(len(c1)),))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(len(c1)+1),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量密文添加到向量密文
def __append_array(c1,c2):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)

    append_array_func = get_func_name("append_array")
    append_array_func.argtypes = [POINTER(c_double), c_int, POINTER(c_double), c_int]
    append_array_func.restype = POINTER(c_double)

    res_ptr = append_array_func(c1_double_array, c_int(len(c1)), c2_double_array, c_int(len(c2)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(len(c1)+c2[1]),))
    if c1[1] == 0 and c1[2] == 0.0:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(len(c2)),))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(len(c1)+c2[1]),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __append_1d_2d(c1, c2, encrypt_type, cipher_shape_c2):
    c2_shape = c2.shape
    c1_double_array = (c_double * len(c1))(*c1)
    c2 = c2.reshape(-1,)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("append")
    func = get_func_name("append_1d_2d")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(c2_shape[0]), c_int(c2_shape[1]), c_int(encrypt_type), c_bool(parallel))
    # 检查向量是否为空向量
    if int(c1[1]) == 0 and c1[2] == 0.0: # 空向量
        length = cipher_shape_c2[0] * cipher_shape_c2[1]
    else:
        length = int(c1[1]) + cipher_shape_c2[0] * cipher_shape_c2[1]
    res = np.ctypeslib.as_array(res_ptr, shape=(length + 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __append_2d_scalar(c1, c2, encrypt_type, cipher_shape_c1):
    c1_shape = c1.shape
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("append")
    func = get_func_name("append_2d_scalar")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(len(c2)), c_int(encrypt_type), c_bool(parallel))
    length = cipher_shape_c1[0] * cipher_shape_c1[1] + 1
    res = np.ctypeslib.as_array(res_ptr, shape=(length+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __append_2d_1d(c1, c2, encrypt_type, cipher_shape_c1):
    c1_shape = c1.shape
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("append")
    func = get_func_name("append_2d_1d")
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    func.restype = POINTER(c_double)
    res_ptr = func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(len(c2)), c_int(encrypt_type), c_bool(parallel))
    length = cipher_shape_c1[0] * cipher_shape_c1[1] + int(c2[1])
    res = np.ctypeslib.as_array(res_ptr, shape=(length+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __append_2d_2d(c1, c2, axis, encrypt_type, output_encrypt_type, cipher_shape_c1, cipher_shape_c2):
    c1_shape = c1.shape
    c2_shape = c2.shape
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("append")
    if axis is None:
        func = get_func_name("append_2d_2d_axisnone")
        func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
        func.restype = POINTER(c_double)
        res_shape = (cipher_shape_c1[0] * cipher_shape_c1[1] + cipher_shape_c2[0] * cipher_shape_c2[1] + 2,)
        res_ptr = func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(c2_shape[0]), c_int(c2_shape[1]), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=res_shape)
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    elif axis == 0:
        func = get_func_name("append_2d_2d_axis0")
        res_shape = (cipher_shape_c1[0] + cipher_shape_c2[0], cipher_shape_c1[1])
    else:
        func = get_func_name("append_2d_2d_axis1")
        res_shape = (cipher_shape_c1[0], cipher_shape_c1[1] + cipher_shape_c2[1]) 
    if output_encrypt_type == 0:
        res_shape = (res_shape[0], res_shape[1] +2)
    else:
        res_shape = (res_shape[0]+2, res_shape[1])
    func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool] 
    func.restype = POINTER(c_double)
    res_ptr =func(c1_double_array, c2_double_array, c_int(c1_shape[0]), c_int(c1_shape[1]), c_int(c2_shape[0]), c_int(c2_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=res_shape)
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 获取一个空CipherFloat
def empty():

    empty_func = get_func_name("empty")
    empty_func.argtype = None
    empty_func.restype = POINTER(c_double)

    res_ptr = empty_func()
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 获取一个空CipherFloatArray
def empty_array():

    empty_array_func = get_func_name("empty_array")
    empty_array_func.argtype = None
    empty_array_func.restype = POINTER(c_double)
    res_ptr = empty_array_func()
    res = np.ctypeslib.as_array(res_ptr, shape=(3,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 返回最小值对应索引
def argmin(c1, axis=None):
    # 输入检测
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res != 2:
        raise ValueError("Can only handle array ciphertext, please enter array ciphertext.(Param:c1)!")
    if c1.ndim == 1:
        return __argminmax(c1, "argmin")
    else:
        return __argminmax_array(c1, axis, encrypt_type, "argmin")

# 返回最大值对应索引
def argmax(c1, axis=None):
    # 输入检测
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res != 2:
        raise ValueError("Can only handle array ciphertext, please enter array ciphertext.(Param:c1)!")
    if c1.ndim == 1:
        return __argminmax(c1, "argmax")
    else:
        return __argminmax_array(c1, axis, encrypt_type, "argmax")

# 获取标量cc1
def ones():
    # 获取函数并设置返回值
    ones_func = get_func_name("ones")
    ones_func.argtype = None
    ones_func.restype = POINTER(c_double)
    res_ptr = ones_func()
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 获取向量cc1
def ones_array(m, n=1, output_encrypt_type=0):
    # 获取函数并设置返回值
    if n == 1: # 返回向量
        ones_array_func = get_func_name("ones_array")
        ones_array_func.argtype = c_int
        ones_array_func.restype = POINTER(c_double)
        res_ptr = ones_array_func(c_int(m))
        res = np.ctypeslib.as_array(res_ptr, shape=((2+m),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    else:
        ones_array_func = get_func_name("ones_array_array")
        ones_array_func.argtypes = [c_int, c_int, c_int]
        ones_array_func.restype = POINTER(c_double)
        res_ptr = ones_array_func(c_int(m), c_int(n), c_int(output_encrypt_type))
        if output_encrypt_type == 0: # 行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(m,n+2))
        elif output_encrypt_type == 1: # 列加密
            res = np.ctypeslib.as_array(res_ptr, shape=(m+2,n))
        else:
            raise ValueError("Param 'output_encrypt_type' can only be 0 or 1!")
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

def ones_like(c1, output_encrypt_type=-1):
    # 获取密文c1的形状
    shape = c1.cipherShape()
    if len(shape) == 1:
        return ones_array(shape[0])
    else:
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        elif output_encrypt_type != 0 or output_encrypt_type != 1:
            raise ValueError("Param 'output_encrypt_type' can only be 0 or 1!")
        return ones_array(shape[0], shape[1], output_encrypt_type)

# 获取标量cc0
def zeros():
    # 获取函数并设置返回值
    zeros_func = get_func_name("zeros")
    zeros_func.argtype = None
    zeros_func.restype = POINTER(c_double)
    res_ptr = zeros_func()
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 获取向量cc0
def zeros_array(m, n=1, output_encrypt_type=0):
    # 获取函数并设置返回值
    if n == 1: # 返回向量
        zeros_array_func = get_func_name("zeros_array")
        zeros_array_func.argtype = c_int
        zeros_array_func.restype = POINTER(c_double)
        res_ptr = zeros_array_func(c_int(m))
        res = np.ctypeslib.as_array(res_ptr, shape=((2+m),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    else:
        zeros_array_func = get_func_name("zeros_array_array")
        zeros_array_func.argtypes = [c_int, c_int, c_int]
        zeros_array_func.restype = POINTER(c_double)
        res_ptr = zeros_array_func(c_int(m), c_int(n), c_int(output_encrypt_type))
        if output_encrypt_type == 0: # 行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(m,n+2))
        elif output_encrypt_type == 1: # 列加密
            res = np.ctypeslib.as_array(res_ptr, shape=(m+2,n))
        else:
            raise ValueError("Param 'output_encrypt_type' can only be 0 or 1!")
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
def zeros_like(c1, output_encrypt_type=-1):
    # 获取密文c1的形状
    shape = c1.cipherShape()
    if len(shape) == 1:
        return zeros_array(shape[0])
    else:
        if output_encrypt_type == -1:
            output_encrypt_type = c1.get_encryption_type()
        elif output_encrypt_type != 0 or output_encrypt_type != 1:
            raise ValueError("Param 'output_encrypt_type' can only be 0 or 1!")
        return zeros_array(shape[0], shape[1], output_encrypt_type)

def full(shape, fill_value, output_encrypt_type=0):
    """
    仅支持标量密文
    """
    if not isinstance(shape, (int, tuple, list)):
        raise ValueError("Param 'shape' can only be int or sequence of ints.")
    if not isinstance(fill_value, CipherArray):
        raise ValueError("Param 'fill_value' can only be a CipherArray.")

    if isinstance(shape, int):
        shape = (shape,)
    if isinstance(shape, list):
        shape = tuple(shape)

    # fill_value = fill_value.get_base_array()

    if len(shape) == 1:
        # res = CipherArray(broadcast_(fill_value, shape, 0))
        res = broadcast_to(fill_value, shape, output_encrypt_type)
        if output_encrypt_type == 1:
            res = res.transEncType()
    elif len(shape) == 2:
        # res = CipherArray(broadcast_(fill_value, shape, 1))
        res = broadcast_to(fill_value, shape, output_encrypt_type)
        if output_encrypt_type == 1:
            res = res.transEncType()
    else:
        raise ValueError(f"The length of shape must be 1 or 2, but got {len(shape)}.")
    
    return res

# 生成一系列连续的整数arange
def arange(stop_,start_=0,step_=1):
    # 调用numpy arange函数生成一系列连续的整数
    arr = np.arange(stop=stop_, start=start_, step=step_)
    c_double_array = (c_double * (len(arr)))(*arr)
    # 获取函数并设置返回值
    arange_func = get_func_name("plain_to_cipher")
    arange_func.argtypes = [POINTER(c_double), c_int]
    arange_func.restype = POINTER(c_double)

    res_ptr = arange_func(c_double_array, c_int(len(arr)))
    res = np.ctypeslib.as_array(res_ptr, shape=((len(arr)+2),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 返回指定间隔内均匀分布的数字
def linspace(start, stop, num=50, endpoint=True):
    start = start.get_base_array()
    stop  = stop.get_base_array()
    start_double_array = (c_double * (len(start)))(*start)
    stop_double_array = (c_double * (len(stop)))(*stop)

    linspace_func = get_func_name("linspace")
    linspace_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_bool]
    linspace_func.restype = POINTER(c_double)

    res_ptr = linspace_func(start_double_array, stop_double_array, c_int(len(start)), c_int(num), c_bool(endpoint))
    res = np.ctypeslib.as_array(res_ptr, shape=(num + 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 标量密文添加到向量密文中
def append(c1, c2, axis=None, output_encrypt_type=-1):
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    cipher_shape1 = c1.cipherShape()
    cipher_shape2 = c2.cipherShape()
    encrypt_type1 = c1.get_encryption_type()
    encrypt_type2 = c2.get_encryption_type()
    if check_res1 == 2: # 向量或数组
        c1 = c1.get_base_array()
        if c1.ndim == 1:
            c2 = c2.get_base_array()
            if check_res2 == 1:
                return __append(c1, c2)
            elif check_res2 == 2:
                if c2.ndim == 1:
                    return __append_array(c1, c2)
                else:
                    return __append_1d_2d(c1, c2, encrypt_type2, cipher_shape2)
            else:
                raise ValueError("Unable to handle discrete ciphertext array type, please enter scalar or array ciphertext.(Param:c2)")
        else: # c1.ndim = 2
            if check_res2 == 1:
                c2 = c2.get_base_array()
                return __append_2d_scalar(c1, c2, encrypt_type1, cipher_shape1)
            elif check_res2 == 2:
                if c2.ndim == 1:
                    c2 = c2.get_base_array()
                    return __append_2d_1d(c1, c2, encrypt_type1, cipher_shape1)
                else:
                    if encrypt_type1 != encrypt_type2:
                        c2 = c2.transEncType()
                    c2 = c2.get_base_array()
                    if output_encrypt_type == -1:
                        output_encrypt_type = encrypt_type1
                    if axis == 0 and (cipher_shape1[1] != cipher_shape2[1]):
                        raise ValueError(f"Axis 1 has different lengths.[c1.shape={cipher_shape1}, c2.shape={cipher_shape2}]")
                    if axis == 1 and (cipher_shape1[0] != cipher_shape2[0]):
                        raise ValueError(f"Axis 0 has different lengths.[c1.shape={cipher_shape1}, c2.shape={cipher_shape2}]")                        
                    return __append_2d_2d(c1, c2, axis, encrypt_type1, output_encrypt_type, cipher_shape1, cipher_shape2)

# 从向量密文中获取指定索引的密文
def getCipher(c1, index):
    if type(c1) == CipherArray:
        c1 = c1.get_base_array()
    # 检查index是否超过c1中包含的密文个数
    if index < 0 or index + 1 > c1[1]:# 数组越界
        raise IndexError(f"Index out of range with {index}")
    if type(index) != int:# 非法输入
        raise ValueError("Parameter index must be integer!")
    return CipherArray([c1[0], c1[2+index]])


def broadcast_to(c : CipherArray, shape, output_encrypt_type=-1) -> CipherArray:
    """
    通用广播函数，类似 numpy.broadcast_to
    参数：
    c: CipherArray类型，需要广播的数组
    shape: tuple类型，广播到的目标形状
    output_encrypt_type: int类型，加密类型，0为行加密，1为列加密
    """

    if c.cipherShape() == shape:
        return c
    encrypt_type = c.get_encryption_type()
    cipher_type = c.get_cipher_type()
    array = c.get_base_array()
    cipher_shape = c.cipherShape()
    if len(cipher_shape) > len(shape):
        raise (f"Can not broadcast shape :{cipher_shape} to shape :{shape}.")
    
    if output_encrypt_type == -1:
        output_encrypt_type = encrypt_type
    
    # 目前只支持二维，情况较少, 使用穷举的方式来确定如何广播

    # 标量密文
    if cipher_type == 1:
        if len(shape) == 1:
            res_list = [array[0], shape[0]] + [array[1]] * int(shape[0])
        elif len(shape) == 2:
            # 区分行列加密
            if output_encrypt_type == -1 or output_encrypt_type == 0:
                res_list_single = [array[0], shape[0]] + [array[1]] * int(shape[0])
                res_list = [res_list_single] * int(shape[1])
            else:
                res_p = [array[0]] * int(shape[1])
                res_L = [shape[0]] * int(shape[1])
                res_list = [res_p, res_L] + [[array[1]] * int(shape[1])] * int(shape[0])
        res_array = np.array(res_list)
        return CipherArray(res_array)
    elif cipher_type == 2:
        # 向量密文
        if len(cipher_shape) == 1:
            # 目标形状为一维
            if len(shape) == 1 :
                if shape[0] == cipher_shape[0]:
                    return CipherArray(array)
                elif cipher_shape[0] != 1:
                    raise ValueError(f"Can not broadcast shape :{cipher_shape} to shape :{shape}.")
                else:
                    # 满足广播条件
                    res_list = [array[0], shape[0]] + [array[2]] * int(shape[0])
                    return CipherArray(np.array(res_list))
            elif len(shape) == 2:
                # 目标形状为二维
                if cipher_shape[0] != 1 and cipher_shape[0] != shape[1]:
                    raise ValueError(f"Can not broadcast shape :{cipher_shape} to shape :{shape}.")
                if cipher_shape[0] == 1:
                    # 行加密
                    if output_encrypt_type == -1 or output_encrypt_type == 0:
                        res_list_single = [array[0], shape[1]] + [array[2]] * int(shape[1])
                        res_list = [res_list_single] * int(shape[0])
                    # 列加密
                    else:
                        res_p = [array[0]] * int(shape[1])
                        res_L = [shape[0]] * int(shape[1])
                        res_list = [res_p, res_L] + [[array[2]] * int(shape[1])] * int(shape[0])
                    
                    res_array = np.array(res_list)
                    return CipherArray(res_array)
                # 向量密文的形状与目标形状的最后一维相同
                else:
                    res_list_single = array.tolist()
                    res_list = [res_list_single] * int(shape[0])
                    res = CipherArray(np.array(res_list))
                    # 如果是列加密则执行行列加密转换
                if output_encrypt_type != encrypt_type:
                    res = res.transEncType()
                return res

        # 矩阵类型密文
        else:
            # 不需要广播
            if cipher_shape == shape:
                if output_encrypt_type == -1 or output_encrypt_type == encrypt_type:
                    return c
                else:
                    return c.transEncType()
            
            # 需要广播
            # 检查密文形状与目标形状是否满足广播条件
            CHECK_BROADCAST = True
            if  cipher_shape[0] != 1 and cipher_shape[0] != shape[0]:
                CHECK_BROADCAST = False
            if  cipher_shape[1] != 1 and cipher_shape[1] != shape[1]:
                CHECK_BROADCAST = False
            # 不满足广播条件
            if not CHECK_BROADCAST:
                raise ValueError(f"Can not broadcast shape :{cipher_shape} to shape :{shape}.")
            # 行加密密文
            if encrypt_type == 0:
                P = array[:, 0]
                P_broad = np.broadcast_to(P, (shape[0],))
                L = np.array([shape[1]])
                L_broad = np.broadcast_to(L, (shape[0],))
                A = array[:, 2:]
                A_broad = np.broadcast_to(A, shape)
                res_array = np.concatenate([P_broad.reshape(-1, 1), L_broad.reshape(-1, 1), A_broad], axis=1)
                res = CipherArray(res_array)
            # 列加密密文
            else:
                P = array[0]
                P_broad = np.broadcast_to(P, (shape[1],))
                L = np.array([shape[0]])
                L_broad = np.broadcast_to(L, (shape[1],))
                A = array[2:]
                A_broad = np.broadcast_to(A, shape)
                res_array = np.concatenate([P_broad.reshape(1, -1), L_broad.reshape(1, -1), A_broad], axis=0)
                res = CipherArray(res_array)
            if output_encrypt_type != encrypt_type:
                res = res.transEncType()
            return res


def broadcast_arrays(c1, c2, output_encrypt_type=-1):
    """
    将两个密文数组广播到相同的形状，可以指定输出的加密类型
    """
    if not isinstance(c1, CipherArray) or not isinstance(c2, CipherArray):
        raise ValueError("Parameters must be CipherArray.")
    c1_new, c2_new = c1._broadcast_arrays(c2)
    c1_new_encrypt_type = c1.get_encryption_type()
    c2_new_encrypt_type = c2.get_encryption_type()
    if output_encrypt_type == -1:
        return c1_new, c2_new
    if c1_new_encrypt_type != output_encrypt_type:
        c1_new = c1_new.transEncType()
    if c2_new_encrypt_type != output_encrypt_type:
        c2_new = c2_new.transEncType()
    return c1_new, c2_new

def argsort(c1, axis=1, decrement=False):
    # 检查输入密文类型
    check_res = c1.get_cipher_type()
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    if check_res == 1 or check_res == 3:
        raise ValueError("Can only handle vector or array ciphertext, please enter vector or array ciphertext!(Param:c1)")
    # 向量或数组类型的密文
    if c1.ndim == 1: # 1维
        if decrement:
            return __argsort_decrement(c1)
        else:
            return __argsort(c1)
    else: # 2维
        if decrement:
            if axis == 1:
                return __argsort_array_one_decrement(c1, encrypt_type)
            else:
                return __argsort_array_zero_decrement(c1, encrypt_type)
        else:
            if axis == 1:
                return __argsort_array_one(c1, encrypt_type)
            else:
                return __argsort_array_zero(c1, encrypt_type)

def insert(c1, index, c2, axis=0, output_encrypt_type=-1):
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    if c1.ndim != 2:
        raise ValueError("Unable to process one-dimensional vector ciphertext, please enter two-dimensional array ciphertext.(Param:c1)")
    if c2.ndim != 1 :
        raise ValueError("Unable to process two-dimensional array ciphertext, please enter one-dimensional vector ciphertext.(Param:c2)")
    if output_encrypt_type != 0 and output_encrypt_type != 1:
        output_encrypt_type = encrypt_type
    if encrypt_type == 0: # 行加密
        if axis == 0: # 行加密插入一行
            c1 = np.insert(c1, index, c2, axis=0)
            if output_encrypt_type == 0:
                return CipherArray(c1)
            else: # 行列变换
                tmp = CipherArray(c1)
                return tmp.transEncType()
        else: # 行加密追加一列
            return __insert(c1, index, c2, axis, encrypt_type, output_encrypt_type)
    else: # 列加密
        if axis == 0: # 列加密追加一行
            return __insert(c1, index, c2, axis, encrypt_type, output_encrypt_type)
        else: # 列加密追加一列
            c1 = np.insert(c1, index, c2, axis=1)
            if output_encrypt_type == 0:
                tmp = CipherArray(c1)
                return tmp.transEncType()
            else:
                return CipherArray(c1)

