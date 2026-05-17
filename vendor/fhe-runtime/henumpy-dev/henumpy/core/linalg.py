import numpy as np
import math
from ctypes import *
import os
import sys
import itertools
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
from .arithmetic import mul, add

__all__ = ["dot", "inner", "outer", "matmul", "matrix_power", "kron", "norm", "trace", "det", 
           "eye", "inv",  "transpose", "vander", "polyfit"]

# n范数
def __normn(c1,n):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置函数参数以及返回值
    normn_func = get_func_name("normn")
    normn_func.argtypes = [POINTER(c_double), c_int, c_int]
    normn_func.restype = POINTER(c_double)
    
    res_ptr = normn_func(c1_double_array, c_int(len(c1)), c_int(n))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 0范数
def __norm_zero(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置函数参数以及返回值
    norm_zero_func = get_func_name("norm_zero")
    norm_zero_func.argtypes = [POINTER(c_double), c_int]
    norm_zero_func.restype = c_int

    res = norm_zero_func(c1_double_array, c_int(len(c1)))
    return int(res)

# 正无穷范数
def __norm_posinf(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置函数参数以及返回值
    norm_posinf_func = get_func_name("norm_posinf")
    norm_posinf_func.argtypes = [POINTER(c_double), c_int]
    norm_posinf_func.restype = POINTER(c_double)

    res_ptr = norm_posinf_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 负无穷范数
def __norm_neginf(c1):
    # 类型转换
    c1_double_array = (c_double * (len(c1)))(*c1)
    # 获取函数并设置参数以及返回值
    norm_neginf_func = get_func_name("norm_neginf")
    norm_neginf_func.argtypes = [POINTER(c_double), c_int]
    norm_neginf_func.restype = POINTER(c_double)

    res_ptr = norm_neginf_func(c1_double_array, c_int(len(c1)))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# n*m dot m
def __dot(c1, c2, encrypt_type):
    shape_c1 = c1.shape
    n = shape_c1[0]+2 if encrypt_type == 0 else shape_c1[0]
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("dot")
    dot_func = get_func_name("dot")
    dot_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    dot_func.restype = POINTER(c_double)
    res_ptr = dot_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(len(c2)), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(n,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向量内积inner
def __inner(c1, c2):
    # 类型转化
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    # 获取函数并设置参数以及返回值
    inner_func = get_func_name("inner")
    inner_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
    inner_func.restype = POINTER(c_double)
    # 调用函数并接收返回值
    res_ptr = inner_func(c1_double_array, c2_double_array, len(c1))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# n*m inner (m,)
def __inner_2d_1d(c1, c2, encrypt_type):
    shape_c1 = c1.shape
    n = shape_c1[0]+2 if encrypt_type == 0 else shape_c1[0]
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("inner")
    inner_2d_1d_func = get_func_name("inner_2d_1d")
    inner_2d_1d_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    inner_2d_1d_func.restype = POINTER(c_double)

    res_ptr = inner_2d_1d_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(len(c2)), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(n,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# n*m inner k*m
def __inner_2d_2d(c1, c2, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    shape_c2 = c2.shape
    n = shape_c1[0] if encrypt_type == 0 else shape_c1[0]-2    
    k = shape_c2[0] if encrypt_type == 0 else shape_c2[0]-2
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    c2_double_array = (c_double * (len(c2)))(*c2)
    parallel = get_func_parallelization_config("inner")
    inner_2d_2d_func = get_func_name("inner_2d_2d")
    inner_2d_2d_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    inner_2d_2d_func.restype = POINTER(c_double)

    res_ptr = inner_2d_2d_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(shape_c2[0]), c_int(shape_c2[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(n, k+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(n+2, k))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 矩阵乘法
def __matmul(c1, c2, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    shape_c2 = c2.shape
    if encrypt_type == 0:
        shape_new = (shape_c1[0], shape_c2[1] - 2)
    else:
        shape_new = (shape_c1[0] - 2, shape_c2[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    # 一维ndarray转c数组
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("matmul")
    # 调用go函数
    matmul_func = get_func_name("matmul")
    matmul_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    matmul_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = encrypt_type
    res_ptr = matmul_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(shape_c2[0]), c_int(shape_c2[1]), 
                          c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0]+2, shape_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)    

def __matmul_col(c1, c2, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    shape_c2 = c2.shape
    shape_new = (c1.shape[0]-2, c2.shape[1])
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    # 一维ndarray转c数组
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("matmul")
    # 调用go函数
    matmul_array_func = get_func_name("matmul_col")
    matmul_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    matmul_array_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = encrypt_type
    res_ptr = matmul_array_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(shape_c2[0]), c_int(shape_c2[1]), 
                          c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0]+2, shape_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 1*n @ n * m
def __matmul_1Dwith2D(c1, c2, encrypt_type):
    shape_c2 = c2.shape
    # 计算结果向量的长度
    m = shape_c2[1] if encrypt_type == 1 else shape_c2[1]-2
    c2 = c2.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    matmul_1Dwith2D_func = get_func_name("matmul_1dwith2d") 
    matmul_1Dwith2D_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int]
    matmul_1Dwith2D_func.restype = POINTER(c_double)

    res_ptr = matmul_1Dwith2D_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(shape_c2[0]), c_int(shape_c2[1]), c_int(encrypt_type))
    res = np.ctypeslib.as_array(res_ptr, shape=(m+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# n*1 @ 1 * m
def __matmul_2DWith1D(c1, c2, encrypt_type, output_encrypt_type):
    shape_c1 = c1.shape
    # 计算结果矩阵的形状
    n = shape_c1[0] if encrypt_type == 0 else shape_c1[0]-2
    m = len(c2)-2
    shape_res = (n, m)
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)

    parallel = get_func_parallelization_config("matmul")
    matmul_2DWith1D_func = get_func_name("matmul_2dwith1d")
    matmul_2DWith1D_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
    matmul_2DWith1D_func.restype = POINTER(c_double)

    res_ptr = matmul_2DWith1D_func(c1_double_array, c2_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(len(c2)), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_res[0], shape_res[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_res[0]+2, shape_res[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __vander(c1, degree, output_encrypt_type):
    c1_double_array = (c_double * len(c1))(*c1)

    vander_func = get_func_name("vander")
    vander_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
    vander_func.restype = POINTER(c_double)

    res_ptr = vander_func(c1_double_array, c_int(len(c1)), c_int(degree), c_int(output_encrypt_type))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]), degree+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1])+2, degree))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def __polyfit(c1, c2, degree):
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)

    polyfit_func = get_func_name("polyfit")
    polyfit_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int]
    polyfit_func.restype = POINTER(c_double)

    res_ptr = polyfit_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(degree))
    res = np.ctypeslib.as_array(res_ptr, shape=(degree + 3,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 点积dot函数
def dot(c1, c2, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    if check_res1 == 1 or check_res2 == 1:
        return mul(c1, c2, output_encrypt_type)
    else:
        if c1.ndim == 1 and c2.ndim == 1:
            return inner(c1, c2)
        elif c1.ndim == 1 and c2.ndim == 2:
            return matmul(c1, c2)
        elif c1.ndim == 2 and c2.ndim == 1:
            encrypt_type = c1.get_encryption_type()
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            return __dot(c1, c2 ,encrypt_type)
        elif c1.ndim == 2 and c2.ndim == 2:
            return matmul(c1, c2, output_encrypt_type)

# # 内积函数inner       
def inner(c1, c2, output_encrypt_type=-1):
    # 检查输入
    CHECK_DISCRETE(c1, "c1")
    CHECK_DISCRETE(c2, "c2")    
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    # 如果c1或c2是标量密文
    if check_res1 == 1 or check_res2 == 1:
        return mul(c1, c2)
    elif check_res1 == 2 and check_res2 == 2:
        encrypt1 = c1.get_encryption_type()
        encrypt2 = c2.get_encryption_type()
        cipherShape1 = c1.cipherShape()
        cipherShape2 = c2.cipherShape()
        if c1.ndim == 1 and c2.ndim == 1:
            if len(c1) == len(c2) :
                c1 = c1.get_base_array()
                c2 = c2.get_base_array()
                return __inner(c1, c2)
            else:
                raise ValueError(f"The lengths of two vectors are different.[len(c1)={len(c1)-2}, len(c2)={len(c2)-2}]")
        elif c1.ndim == 1:
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            if cipherShape1[0] == cipherShape2[1]:
                return __inner_2d_1d(c2, c1, encrypt2)
            else:
                raise ValueError(f"The last dimension of input data is not equal.[c1.shape={cipherShape1}, c2.shape={cipherShape2}]")
        elif c2.ndim == 1:
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            if cipherShape1[1] == cipherShape2[0]:
                return __inner_2d_1d(c1, c2, encrypt1)
            else:
                raise ValueError(f"The last dimension of input data is not equal.[c1.shape={cipherShape1}, c2.shape={cipherShape2}]")       
        else:
            if encrypt1 != encrypt2:
                c2 = c2.transEncType()
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()                     
            if cipherShape1[1] == cipherShape2[1]:
                if output_encrypt_type == -1:
                    output_encrypt_type = encrypt1
                return __inner_2d_2d(c1, c2, encrypt1, output_encrypt_type)
            else:
                raise ValueError(f"The last dimension of input data is not equal.[c1.shape={cipherShape1}, c2.shape={cipherShape2}]")

# 计算两个向量的外积
def outer(c1, c2, output_encrypt_type=-1):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    CHECK_ARRAY(c2, "c2")
    if c1.ndim != 1:
        raise("The input must be ventor.(Param:c1)")
    if c2.ndim != 1:
        raise("The input must be ventor.(Param:c2)")
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("outer")
    # 调用go函数
    outer_func = get_func_name("outer")
    outer_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
    outer_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = 0
    res_ptr = outer_func(c1_double_array, c2_double_array, c_int(len(c1)), c_int(len(c2)), c_int(output_encrypt_type), c_bool(parallel))
    # 转为二维数组
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1]),len(c2)))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(int(c1[1])+2,len(c2)-2))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)  
    
def matmul(c1, c2, output_encrypt_type=-1):
    CHECK_ARRAY(c1, "c1")
    CHECK_ARRAY(c2, "c2")
    c1_shape = c1.cipherShape()
    c2_shape = c2.cipherShape()
    encrypt_type1 = c1.get_encryption_type()
    encrypt_type2 = c2.get_encryption_type()

    # 如果是向量密文则调用内积
    if len(c1_shape) == 1 and len(c2_shape) == 1:
        if c1_shape[0] == c2_shape[0] :
            return inner(c1, c2)
        else:
            raise ValueError(f"The lengths of two vectors are different.[len(c1)={len(c1)-2}, len(c2)={len(c2)-2}]")
    # 如果c1或c2是一维的则增加一个维度
    elif len(c1_shape) == 1:
        # 1*n @ n * m, 检查输入维度是否符合矩阵乘法要求
        if c1_shape[0] == c2_shape[0]:
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            return __matmul_1Dwith2D(c1, c2, encrypt_type2)
        else:
            raise ValueError(f"The input cipher shape does not meet matrix multiplication rules.[c1.shape={c1_shape}, c2.shape={c2_shape}]")
    elif len(c2_shape) == 1:
        # n*1 @ 1*m 检查输入维度是否符合矩阵乘法要求
        if c1_shape[1] == c2_shape[0]:
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type1
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            return __matmul_2DWith1D(c1, c2, encrypt_type1, output_encrypt_type)
        else:
            raise ValueError(f"The input cipher shape does not meet matrix multiplication rules.[c1.shape={c1_shape}, c2.shape={c2_shape}]")
    else:
        # 检查是否满足矩阵乘法规则
        if c1_shape[1] != c2_shape[0]:
            raise ValueError(f"The input cipher shape does not meet matrix multiplication rules.[c1.shape={c1_shape}, c2.shape={c2_shape}]")
        else:
            if encrypt_type1 != encrypt_type2:
                c2 = c2.transEncType()
            else: 
                pass
            if output_encrypt_type == -1:
                output_encrypt_type = encrypt_type1
            else:
                pass
            c1 = c1.get_base_array()
            c2 = c2.get_base_array()
            if encrypt_type1 == 0:
                return __matmul(c1, c2, encrypt_type1, output_encrypt_type) 
            else:
                return __matmul_col(c1, c2, encrypt_type1, output_encrypt_type)

# 将方阵提高到（整数）幂 n
def matrix_power(c1, n, output_encrypt_type=-1): # output_encrypt_type 输出密文的加密类型，默认输出与输入保持一致
    # 如果n为0则返回与c1形状相同的单位矩阵
    if n == 0:
        if output_encrypt_type != 0 and output_encrypt_type != 1:
            raise ValueError("output_encrypt_type must be '1' or '0'")
        return eye(c1.cipherShape()[0], output_encrypt_type)
    CHECK_ARRAY(c1, "c1")
    encrypt_type = c1.encryption_type 
    shape_c1_new = c1.cipherShape() # 获取密文的维度
    c1 = c1.get_base_array()
    shape_c1 = c1.shape
    x_c1 = shape_c1[0] # 数组c1的行数
    y_c1 = shape_c1[1] # 数组c1的列数
    # 将二维密文数组转换为一维ndarray
    c1 = c1.reshape(-1,)
    # 将一维ndarray转换为c数组
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("matrix_power")
    # 调用go函数
    matrix_power_func = get_func_name("matrix_power")
    matrix_power_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
    matrix_power_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = encrypt_type

    res_ptr = matrix_power_func(c1_double_array, c_int(x_c1), c_int(y_c1), c_int(n), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0], shape_c1_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]+2, shape_c1_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 两个阵列的Kronecker乘积（调用go实现）行加密
def kron(c1, c2, output_encrypt_type=-1):
    CHECK_ARRAY(c1, "c1")
    CHECK_ARRAY(c2, "c2")
    encrypt_type = c1.encryption_type # 默认c1与c2具有相同的加密类型
    shape_c1_new = c1.cipherShape() # 获取密文的维度
    shape_c2_new = c2.cipherShape()
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    shape_c1 = c1.shape
    shape_c2 = c2.shape
    x_c1 = shape_c1[0] # 数组c1的行数
    y_c1 = shape_c1[1] # 数组c1的列数
    x_c2 = shape_c2[0] # 数组c2的行数
    y_c2 = shape_c2[1] # 数组c2的列数
    # 将二维密文数组转换为一维ndarray
    c1 = c1.reshape(-1,)
    c2 = c2.reshape(-1,)
    # 将一维ndarray转换为c数组
    c1_double_array = (c_double * len(c1))(*c1)
    c2_double_array = (c_double * len(c2))(*c2)
    parallel = get_func_parallelization_config("kron")
    # 调用go函数
    kron_func = get_func_name("kron")
    kron_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
    kron_func.restype = POINTER(c_double)

    if output_encrypt_type != 0 and output_encrypt_type != 1: # 如果输出密文的加密类型不是0或1，则将其置为与输入加密类型一致的数
        output_encrypt_type = encrypt_type
    res_ptr = kron_func(c1_double_array, c2_double_array, c_int(x_c1), c_int(y_c1), c_int(x_c2), c_int(y_c2), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]*shape_c2_new[0], shape_c1_new[1]*shape_c2_new[1]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1_new[0]*shape_c2_new[0]+2, shape_c1_new[1]*shape_c2_new[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 求范数
def norm(c1,n=2):
    # 检查输入
    CHECK_ARRAY(c1, "c1")
    c1 = c1.get_base_array()
    # 根据输入值n判断处理函数
    if np.isposinf(n):# n为正无穷
        return __norm_posinf(c1)
    elif np.isneginf(n):# n为负无穷
        return __norm_neginf(c1)
    elif n > 0:
        return __normn(c1,n)
    elif n == 0:
        return __norm_zero(c1)
    raise ValueError("Please enter a positive integer!(Param:c1)")

# 返回对角线元素的和（调用go）行加密
def trace(c1):
    # 检查输入是否为方阵
    shape_c1 = c1.cipherShape()
    if len(shape_c1) != 2:
        raise ValueError("Can only handle two-dimensional array cipher, please enter two-dimensional array cipher!(Param:c1)")
    if shape_c1[0] != shape_c1[1]:
        raise ValueError("The input parameter is not a square matrix, please check the input.(Param:c1)")
    encrypt_type = c1.encryption_type
    # 将二维密文数组转换为一维ndarray
    c1 = c1.get_base_array()
    shape_c1 = c1.shape
    c1 = c1.reshape(-1,)
    # 将一维ndarray转换为c数组
    c1_double_array = (c_double * len(c1))(*c1)
    parallel = get_func_parallelization_config("trace")
    # 调用go函数
    trace_func = get_func_name("trace")
    trace_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
    trace_func.restype = POINTER(c_double)
    res_ptr = trace_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type), c_bool(parallel))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 计算行列式（go）
def det(c1):
    # 检查输入是否为方阵
    shape_c1 = c1.cipherShape()
    if len(shape_c1) != 2:
        raise ValueError("Can only handle two-dimensional array cipher, please enter two-dimensional array cipher!(Param:c1)")
    if shape_c1[0] != shape_c1[1]:
        raise ValueError("The input parameter is not a square matrix, please check the input.(Param:c1)")
    # 将二维密文数组转换为一维ndarray
    encrypt_type = c1.encryption_type
    c1 = c1.get_base_array()
    shape_c1 = c1.shape
    c1 = c1.reshape(-1,)
    # 将一维ndarray转换为c数组
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    det_func = get_func_name("det")
    det_func.argtypes = [POINTER(c_double), c_int, c_int, c_int]
    det_func.restype = POINTER(c_double)
    res_ptr = det_func(c1_double_array, c_int(shape_c1[0]), c_int(shape_c1[1]), c_int(encrypt_type))
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 获取单位矩阵
def eye(n, output_encrypt_type=0):
    eye_func = get_func_name("eye")
    eye_func.argtype = [c_int, c_int]
    eye_func.restype = POINTER(c_double)

    res_ptr = eye_func(c_int(n), c_int(output_encrypt_type))
    if output_encrypt_type != 0 and output_encrypt_type != 1:
        raise ValueError("output_encrypt_type must be '1'or '0'")
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(n, n+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(n+2, n))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 矩阵求逆
def inv(c1, output_encrypt_type=-1):
    shape_c1 = c1.cipherShape()
    if len(shape_c1) == 1:
        raise ValueError("Can only handle two-dimensional array cipher, please enter two-dimensional array cipher!(Param:c1)")
    if shape_c1[0] != shape_c1[1]:
        raise ValueError("The input parameter is not a square matrix, please check the input.(Param:c1)")
    encrypt_type = c1.get_encryption_type()
    c1 = c1.get_base_array()
    shape_c1_new = c1.shape
    c1 = c1.reshape(-1,) # 转为一维数组
    c1_double_array = (c_double * len(c1))(*c1)
    # 调用go函数
    inv_func = get_func_name("inv")
    inv_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
    inv_func.restype = POINTER(c_double)
    if output_encrypt_type != 0 and output_encrypt_type != 1:
        output_encrypt_type = encrypt_type
    res_ptr = inv_func(c1_double_array, c_int(shape_c1_new[0]), c_int(shape_c1_new[1]), c_int(encrypt_type), c_int(output_encrypt_type))
    if output_encrypt_type == 0: # 行加密
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[0], shape_c1[1] + 2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[0] + 2, shape_c1[1]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 矩阵求转置
def transpose(c1, output_encrypt_type=-1):
    CHECK_DISCRETE(c1, "c1")
    # 标量密文报错
    if c1.get_cipher_type() == 1:
        raise ValueError("Unable to handle scalar cipherarray.")
    if c1.ndim == 1:
        """
        一维密文转置
        示例：
        >>> c1 = [P, 3, A1, A2, A3]
        >>> c1.transpose() # 转置为具有相同加密方式的密文
        [[P1, 1, A1'],
        [P2, 1, A2'],
        [P3, 1, A3']]
        >>> c1.transpose(output_encrypt_type=1) # 转置为列加密的数组密文
        [[P],
        [3],
        [A1],
        [A2],
        [A3]]
        """
        base_array = c1.get_base_array()
        base_array = base_array.reshape(1, -1)
        # 向量密文转置为列加密的数组密文，不需要进行计算，直接调用矩阵转置函数
        if output_encrypt_type == 1:
            return CipherArray(base_array.T)
        c1 = CipherArray(base_array)
    encrypt_type = c1.get_encryption_type()
    shape_c1 = c1.cipherShape()
    shape_c1_new = c1.shape
    c1 = c1.get_base_array()
    c1 = c1.reshape(-1,)
    c1_double_array = (c_double * (len(c1)))(*c1)
    parallel = get_func_parallelization_config("transpose")
    transpose_func = get_func_name("transpose")
    transpose_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
    transpose_func.restype = POINTER(c_double)
    if output_encrypt_type != 0 and output_encrypt_type != 1:
        output_encrypt_type = encrypt_type
    res_ptr = transpose_func(c1_double_array, c_int(shape_c1_new[0]), c_int(shape_c1_new[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
    if output_encrypt_type == 0:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[1], shape_c1[0]+2))
    else:
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[1]+2, shape_c1[0]))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

def vander(c1, degree=0, output_encrypt_type=-1):
    check_res = c1.get_cipher_type()
    if check_res != 2 or c1.ndim != 1:
        raise ValueError("Can only handle vector cipher, please enter vector cipher!(Param:c1)")
    else:
        c1 = c1.get_base_array()
        if degree == 0: # degree默认和密文长度相同
            degree = int(c1[1])
        if output_encrypt_type == -1:
                output_encrypt_type = 0
        return __vander(c1, degree, output_encrypt_type)
    
def polyfit(c1, c2, degree):
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    if check_res1 != 2 or c1.ndim != 1:
        raise ValueError("Can only handle vector cipher, please enter vector cipher!(Param:c1)")
    if check_res2 != 2 or c2.ndim != 1:
        raise ValueError("Can only handle vector cipher, please enter vector cipher!(Param:c2)")
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    return __polyfit(c1, c2, degree)
