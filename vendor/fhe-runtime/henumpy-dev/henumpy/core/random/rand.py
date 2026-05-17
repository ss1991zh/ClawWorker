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
    free_double_ptr,
)
from henumpy.base.init_dict import *
from henumpy.base.cipher_array import CipherArray

__all__ = ["rand", "choice"]

def __rand(input):
    c_double_array = (c_double * (len(input)))(*input)
    # 获取函数并设置参数与返回值
    rand_func = get_func_name("plain_to_cipher")
    rand_func.argtypes = [POINTER(c_double), c_int]
    rand_func.restype = POINTER(c_double)
    # 调用函数
    res_ptr = rand_func(c_double_array, c_int(len(input)))
    res = np.ctypeslib.as_array(res_ptr, shape=(int(2+len(input)),))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __rand_array(input, output_encrypt_type):
    input_shape = input.shape
    input = input.reshape(-1,)
    input_double_array = (c_double * len(input))(*input)
    rand_array_func = get_func_name("plain_to_cipher_array")
    rand_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
    rand_array_func.restype = POINTER(c_double)
    res_ptr = rand_array_func(input_double_array, c_int(input_shape[0]), c_int(input_shape[1]), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(input_shape[0], input_shape[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(input_shape[0]+2, input_shape[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 随机生成一个给定长度的数组，其中每一个元素值在 0-1 之间
def rand(n, m=0, output_encrypt_type=0):
    # 随机生成长度为n的一维数组
    if m == 0:
        input = np.random.rand(n)
        return __rand(input)
    else:
        input = np.random.rand(n, m)
        return __rand_array(input, output_encrypt_type)

# 抽样函数choice 随机从密文向量c中抽取 size 个样本
def choice(c1,size_=1):
    # 检查输入
    check_res = c1.get_cipher_type()
    c1 = c1.get_base_array()
    if check_res !=2:
        raise ValueError("Please enter array ciphertext!(Param:c1)!")
    choice_arr = c1[2:]
    temp = np.random.choice(choice_arr, size=size_) # 抽样
    # 数组拼接
    L = len(temp)
    res = c1[:1]
    res = np.append(res, L)
    res = np.append(res, temp)
    return CipherArray(res)