import numpy as np
import copy
from ctypes import *
from .base_function import (
    get_func_name, 
    get_func_parallelization_config, 
    CHECK_ARRAY, 
    CHECK_DISCRETE, 
    free_bool_ptr, 
    free_double_ptr, 
    free_int_ptr
)

import struct
import weakref

__all__ = ["CipherArray"]

class CipherArray(np.ndarray):
    # 定义全局变量
    tolerance = 1e-10
    length = -1
    num_floats = -1
    encryption_type = -1 # 标识加密类型：行加密0、列加密1
    cipher_type = -1     # 标识密文类型：标量密文1、向量密文2、离散密文数组3
    discrete = False     # 是否为离散密文，目前只支持一维数组

    # 新建对象操作
    def __new__(cls, input_array, discrete=False):
        #print("--new--")
        obj = np.asarray(input_array).view(cls)
        obj.discrete = discrete
        obj._check_cipher()
        return obj
    
    # 返回适当的字符串表示形式
    def __str__(self):
        return str(self.tolist())
    
    # 实例化操作
    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.discrete = getattr(obj, 'discrete', False)
        self._base_array = obj  # 存储底层的np.ndarray

    def __reduce__(self):
        pickled_state = super().__reduce__()
        new_state = pickled_state[2] + (self.__dict__, )
        return (*pickled_state[0:2], new_state)

    def __setstate__(self, state):
        self.__dict__.update(state[-1])
        super().__setstate__(state[0:-1])

    # 获取底层np.ndarray格式数据
    def get_base_array(self):
        return self._base_array
    
    # 获取加密类型
    def get_encryption_type(self):
        """
        行加密0、列加密1
        """
        return self.encryption_type
    
    # 获取密文类型
    def get_cipher_type(self):
        """
        标量密文1、向量密文2、离散密文数组3
        """
        return self.cipher_type

    # 返回密文数组的形状
    def cipherShape(self):
        ndarray = self.get_base_array()
        #print("ndarray.shape: ", ndarray.shape)
        if ndarray.shape[0] is not None:
            if not self.discrete:
                max_row = ndarray.shape[0] if self.encryption_type == 0 else ndarray.shape[0] - 2
            else:
                max_row = ndarray.shape[0] if self.encryption_type == 0 else ndarray.shape[0] // 2
        else:
            max_row = None
        if self.ndim == 1:
            if self.cipher_type == 1:
                return ()
            elif self.cipher_type == 2:
                return (int(ndarray[1]),)
            elif self.cipher_type == 3:
                return (max_row // 2,)
            else:
                raise ValueError(f"Cipher type error")
        if not self.discrete:
            max_col = ndarray.shape[1] if self.encryption_type == 1 else ndarray.shape[1] - 2
        else:
            max_col = ndarray.shape[1] if self.encryption_type == 1 else ndarray.shape[1] // 2
        return (max_row, max_col)
    
    # 判断数组是否符合浮点密文格式
    def _check_cipher(self, s=""):
        if self.ndim > 2:
            raise ValueError("Array parsing above 2 dimensions is not supported for the time being.")
        elif self.ndim == 2: # 二维密文没有做严格的验证
            self._check_encryption_type()  # 有赋值语句
            if not self.discrete:        
                self.cipher_type = 2
                return 2
            else:
                self.cipher_type = 3
                return 3
        
        elif self.ndim == 1:
            self.encryption_type = 0  # 一维密文是行加密
            self.length = len(self)
            #print("length: ", self.length)
            if self.length < 2:
                raise ValueError("Input array length must be at least 2" + s)
            
            if self.length == 2:  # 标量密文
                check_result, error_msg = _check_prefix_approx_int(self.get_base_array(), 0, 1)
                if check_result:
                    self.cipher_type = 1
                    return 1
                else:
                    raise ValueError(error_msg)
            else:
                ndarry = self.get_base_array()
                if not self.discrete: # 数组密文
                    self.num_floats = int(ndarry[1])
                    # if self.length == 4 + self.num_floats + 1:
                    if (self.length == 1 + self.num_floats + 1) or (int(ndarry[1]) == 0 and ndarry[2] == 0.0): # 增加空数组的情况
                        check_result, error_msg = _check_prefix_approx_int(ndarry, 0, 1)
                        if check_result:
                            self.cipher_type = 2
                            return 2
                        else:
                            raise ValueError(error_msg)
                    else:
                        if self.length % 2 == 0:
                            for i in range(0, self.length // 2):
                                check_result, error_msg = _check_prefix_approx_int(ndarry, i * 2, i * 2 + 1)
                                if not check_result:
                                    raise ValueError(error_msg)
                            raise ValueError("Input array may be of discrete type, which can be indicated by adding \"discrete = True\"")
                        else:
                            raise ValueError("Input array length is inconsistent with specified number of integers and floats" + s)
            
                else:  # 离散数组密文
                    if self.length % 2 != 0:
                        raise ValueError("[length error] Input array is not discrete")
                    for i in range(0, self.length // 2):
                        check_result, error_msg = _check_prefix_approx_int(ndarry, i * 2, i * 2 + 1)
                        if not check_result:
                            raise ValueError(error_msg)
                    self.cipher_type = 3
                    return 3
        else:
            raise ValueError("Array dimensions parsing error.")                

    # 判断二维数组的加密类型  行加密或列加密
    def _check_encryption_type(self):
        if self.ndim == 1:
            self.encryption_type = 0
            return 0
        elif self.ndim == 2:
            ndarray = self.get_base_array()

            # 离散数组密文
            if self.discrete: # 只检查某一行或某一列
                if self.shape[0]>=2 and self.shape[0] % 2 == 0:
                    check_result, _ = _check_prefix_approx_int(ndarray[0], 0, len(ndarray[0]))
                    if check_result:
                        self.encryption_type = 1
                        return 1 # 列加密
                if self.shape[1]>=2 and self.shape[1] % 2 == 0:
                    check_result, _ = _check_prefix_approx_int(ndarray[:,0], 0, len(ndarray[:,0]))
                    if check_result:
                        self.encryption_type = 0
                        return 0 # 行加密
                else:
                    raise ValueError("Encryption type error: encrypt_type must be row or column")

            # 增加对空2维数组的支持
            if len(ndarray[0]) > 1:
                is_all_zero_axis0 = np.all(ndarray[:, 1] == 0.0)
                if is_all_zero_axis0:
                    self.encryption_type = 0
                    return 0
            if len(ndarray) > 1:
                is_all_zero_axis1 = np.all(ndarray[1, :] == 0.0)
                if is_all_zero_axis1:
                    
                    self.encryption_type = 1
                    return 1


            # 数组密文
            if self.shape[0] > 2 and int(ndarray[1, 0]) + 2 == len(ndarray):
                # 特殊情况处理
                if self.shape[1]>2 and int(ndarray[0, 1]) + 2 == len(ndarray[0]):
                    check_result, error_msg = _check_prefix_approx_int(ndarray[0], 0, len(ndarray[0]))
                    if not check_result:
                        self.encryption_type = 0
                        return 0 # 行加密
                # 正常情况
                self.encryption_type = 1
                return 1 # 列加密
            elif self.shape[1]>2 and int(ndarray[0, 1]) + 2 == len(ndarray[0]):
                self.encryption_type = 0
                return 0 # 行加密
            else:
                print(self.shape, int(ndarray[1, 0]) + 2 )
                raise ValueError("Encryption type error: encrypt_type must be row or column")
        else:
            raise ValueError("Array parsing above 2 dimensions is not supported for the time being.")
    
    # 重写__getitem__方法以自定义访问下标
    def __getitem__(self, key):
        ndarray = self.get_base_array()
        if isinstance(key, int) and self.ndim == 1:
            col = key
            if self.cipher_type == 3: 
                max_col = self.shape[0] // 2
                if col < 0:
                    col = max_col + col  # 处理负数索引
                if col >= max_col:
                    raise IndexError(f"index {col} is out of bounds with size {max_col}")
                return CipherArray(ndarray[key*2 : key*2+2], discrete=True)
            else: 
                max_col = self.shape[0] - 2
                if col < 0:
                    col = max_col + col  # 处理负数索引
                if col >= max_col:
                    raise IndexError(f"index {col} is out of bounds with size {max_col}")
                result = list(ndarray[:1])
                result.append(ndarray[2+col])
                return CipherArray(np.array(result))
            
        elif isinstance(key, slice) and self.ndim == 1:
            col = key
            if self.cipher_type == 3: 
                max_col = self.shape[0] // 2
                # 处理列负数切片
                if col.start is None:
                    col_start = 0
                elif col.start < 0:
                    col_start = max_col + col.start
                else:
                    col_start = col.start
                
                if col.stop is None:
                    col_stop = max_col
                elif col.stop < 0:
                    col_stop = max_col + col.stop
                else:
                    col_stop = min(col.stop, max_col)
                return CipherArray(ndarray[col_start*2 : (col_stop-1)*2+2], discrete=True)
            else: # 
                max_col = self.shape[0] - 2
                
                # 处理列负数切片
                if col.start is None:
                    col_start = 0
                elif col.start < 0:
                    col_start = max_col + col.start
                else:
                    col_start = col.start
                
                if col.stop is None:
                    col_stop = max_col
                elif col.stop < 0:
                    col_stop = max_col + col.stop
                else:
                    col_stop = min(col.stop, max_col)
                
                col = slice(col_start, col_stop, col.step)

                result = list(ndarray[:1])
                result.append(col_stop-col_start)
                for i in range(col_start, col_stop):
                    result.append(ndarray[2+i])
                return CipherArray(np.array(result))

        elif isinstance(key, int) and self.ndim == 2:
            if self.encryption_type == 0: # 对于行加密的情况
                max_row = self.shape[0]
                row = key
                if row < 0:
                    row = max_row + row  # 处理负数索引
                if row >= max_row:
                    raise IndexError(f"index {row} is out of bounds with size {max_row}")
                if self.cipher_type == 3:
                    return CipherArray(ndarray[row], discrete=True) # 返回该行
                else:
                    return CipherArray(ndarray[row]) # 返回该行
            elif self.encryption_type == 1 and self.shape[1] == 1: # 对于列加密且只有一列的情况
                max_row = self.shape[0] - 2 if self.cipher_type == 3 else self.shape[0] // 2
                row = key
                if row < 0:
                    row = max_row + row  # 处理负数索引
                if row >= max_row:
                    raise IndexError(f"index {row} is out of bounds with size {max_row}")
                if self.cipher_type == 3:
                    return CipherArray(ndarray[row*2 : row*2+2, 0], discrete=True)
                else:
                    result = list(ndarray[:1, 0])
                    result.append(ndarray[2+row, 0])
                    return CipherArray(np.array(result))
            else:  # 对于列加密且有多列的情况
                max_row = self.shape[0] - 2 if self.cipher_type == 3 else self.shape[0] // 2
                row = key
                if row < 0:
                    row = max_row + row  # 处理负数索引
                if row >= max_row:
                    raise IndexError(f"index {row} is out of bounds with size {max_row}")
                if self.cipher_type == 3:
                    return CipherArray(ndarray[row*2 : row*2+2, :], discrete=True)
                else:
                    result_array = empty_cipher_array()
                    for i in range(0, self.shape[1]):
                        result = list(ndarray[:1, i])
                        result.append(ndarray[2+row, i])
                        result_array = cipher_array_append(result_array, CipherArray(np.array(result)))
                    return CipherArray(np.array(result_array))

        elif isinstance(key, tuple) and self.ndim == 2:
            if len(key) != 2 :
                raise IndexError("Array parsing above 2 dimensions is not supported for the time being.")
            if self.cipher_type == 3:
                max_row = self.shape[0] if self.encryption_type == 0 else self.shape[0] // 2
                max_col = self.shape[1] if self.encryption_type == 1 else self.shape[1] // 2
            else:
                max_row = self.shape[0] if self.encryption_type == 0 else self.shape[0] - 2
                max_col = self.shape[1] if self.encryption_type == 1 else self.shape[1] - 2
            row, col = key

            # 当行列都是整数
            if isinstance(row, int) and isinstance(col, int):
                if row < 0:
                    row = max_row + row  # 处理负数索引
                if col < 0:
                    col = max_col + col  # 处理负数索引
                if row < 0 or row >= max_row or col < 0 or col >= max_col:
                    raise IndexError(f"index ({row},{col}) is out of bounds with size ({max_row},{max_col})")
                if self.cipher_type == 3:
                    if self.encryption_type == 0: # 对于行加密的情况
                        return CipherArray(ndarray[row, col*2 : col*2+2], discrete=True)
                    else: # 对于列加密的情况
                        return CipherArray(ndarray[row*2 : row*2+2, col], discrete=True)
                else:
                    if self.encryption_type == 0: # 对于行加密的情况
                        result = list(ndarray[row, :1])
                        result.append(ndarray[row, 2+col])
                        return CipherArray(np.array(result))
                    else: # 对于列加密的情况
                        result = list(ndarray[:1, col])
                        result.append(ndarray[2+row, col])
                        return CipherArray(np.array(result))
            
            # 当行是整数，列是切片
            elif isinstance(row, int) and isinstance(col, slice) and self.ndim == 2:
                if row < 0:
                    row = max_row + row  # 处理负数索引
                if row < 0 or row >= max_row:
                    raise IndexError(f"index {row} is out of bounds for axis 0 with size {max_row}")

                # 处理列负数切片
                if col.start is None:
                    col_start = 0
                elif col.start < 0:
                    col_start = max_col + col.start
                else:
                    col_start = col.start
                
                if col.stop is None:
                    col_stop = max_col
                elif col.stop < 0:
                    col_stop = max_col + col.stop
                else:
                    col_stop = min(col.stop, max_col)
                
                col = slice(col_start, col_stop, col.step)
                
                if self.cipher_type == 3:
                    if self.encryption_type == 0: # 对于行加密的情况
                        return CipherArray(ndarray[row, col_start*2 : col_stop*2], discrete=True)
                    else: # 对于列加密的情况
                        return CipherArray(ndarray[row:row+2, col], discrete=True)
                else:
                    if self.encryption_type == 0: # 对于行加密的情况
                        result_array = list(ndarray[row, :1])
                        result_array.append(col_stop-col_start)
                        if col_start == col_stop:
                            result_array.append(np.nan)
                        else:
                            for i in range(col_start, col_stop):
                                result_array.append(ndarray[row, 2+i])
                        return CipherArray(np.array(result_array))
                    else: # 对于列加密的情况
                        result_array = empty_cipher_array()
                        for i in range(col_start, col_stop):
                            result = list(ndarray[:1, i])
                            result.append(ndarray[2+row, i])
                            result_array = cipher_array_append(result_array, CipherArray(np.array(result)))
                        return CipherArray(np.array(result_array))
            
            # 当行是切片，列是整数
            elif isinstance(row, slice) and isinstance(col, int) and self.ndim == 2:
                if col < 0:
                    col = max_col + col  # 处理负数索引
                if col < 0 or col >= max_col:
                    raise IndexError(f"index {col} is out of bounds for axis 1 with size {max_col}")
                
                # 处理行负数切片
                if row.start is None:
                    row_start = 0
                elif row.start < 0:
                    row_start = max_row + row.start
                else:
                    row_start = row.start
                
                if row.stop is None:
                    row_stop = max_row
                elif row.stop < 0:
                    row_stop = max_row + row.stop
                else:
                    row_stop = min(row.stop, max_row)
                
                row = slice(row_start, row_stop, row.step)

                if self.cipher_type == 3:
                    if self.encryption_type == 0: # 对于行加密的情况
                        #print("xxx: ", ndarray[row, col*5 : col*5+2])
                        return CipherArray(ndarray[row, col*2 : col*2+2], discrete=True)
                    else: # 对于列加密的情况
                        return CipherArray(ndarray[row_start*2 : row_stop*2, col], discrete=True)
                else:
                    if self.encryption_type == 0: # 对于行加密的情况
                        result_array = empty_cipher_array()
                        for i in range(row_start, row_stop):
                            result = list(ndarray[i, :1])
                            result.append(ndarray[i, 2+col])
                            result_array = cipher_array_append(result_array, CipherArray(np.array(result)))
                        return CipherArray(np.array(result_array))
                    else: # 对于列加密的情况
                        result_array = list(ndarray[:1, col])
                        result_array.append(row_stop-row_start)
                        if row_start == row_stop:
                            result_array.append(np.nan)
                        else:
                            for i in range(row_start, row_stop):
                                result_array.append(ndarray[2+i, col])
                        return CipherArray(np.array(result_array))
            
            elif isinstance(row, slice) and isinstance(col, slice) and self.ndim == 2:
                
                # 处理行负数切片
                if row.start is None:
                    row_start = 0
                elif row.start < 0:
                    row_start = max_row + row.start
                else:
                    row_start = row.start
                
                if row.stop is None:
                    row_stop = max_row
                elif row.stop < 0:
                    row_stop = max_row + row.stop
                else:
                    row_stop = min(row.stop, max_row)
                
                row = slice(row_start, row_stop, row.step)

                # 处理列负数切片
                if col.start is None:
                    col_start = 0
                elif col.start < 0:
                    col_start = max_col + col.start
                else:
                    col_start = col.start
                
                if col.stop is None:
                    col_stop = max_col
                elif col.stop < 0:
                    col_stop = max_col + col.stop
                else:
                    col_stop = min(col.stop, max_col)
                
                col = slice(col_start, col_stop, col.step)

                # 无效索引返回空
                if row_start == row_stop or col_start == col_stop:
                    return empty_cipher_array()
                
                if self.cipher_type == 3:
                    if self.encryption_type == 0: # 对于行加密的情况
                        return CipherArray(ndarray[row, col_start*2 : col_stop*2], discrete=True)
                    else: # 对于列加密的情况
                        return CipherArray(ndarray[row_start*2 : row_stop*2, col], discrete=True)
                else:
                    result_array = []
                    if self.encryption_type == 0: # 对于行加密的情况
                        for i in range(row_start, row_stop):
                            result = list(ndarray[i, :1])
                            result.append(col_stop-col_start)
                            for j in range(col_start, col_stop):
                                result.append(ndarray[i, 2+j])
                            result_array.append(result)
                        return CipherArray(np.array(result_array))
                    else: # 对于列加密的情况
                        for j in range(col_start, col_stop):
                            result = list(ndarray[:1, j])
                            result.append(row_stop-row_start)
                            for i in range(row_start, row_stop):
                                result.append(ndarray[2+i, j])
                            result_array.append(result)
                        return CipherArray(np.array(result_array).T)
        
        elif isinstance(key, slice) and self.ndim == 2:
            # 行加密
            if self.get_encryption_type() == 0:
                # # 离散密文
                # if self.get_cipher_type() == 3:
                #     if key.start is None:
                #         start = 0
                #     elif key.start < 0:
                #         if key.start < -self.cipherShape()[0]:
                #             raise IndexError(f"index {key.start} is out of bounds with size {self.cipherShape()[0]}")
                #         start = self.cipherShape()[0] + key.start
                        
                #     else:
                #         if key.start >= self.cipherShape()[0]:
                #             raise IndexError(f"index {key.start} is out of bounds with size {self.cipherShape()[0]}")
                #         start = key.start
                # 行加密访问行切片只需要复用原ndarray的行切片方法即可
                return CipherArray(self.get_base_array()[key])
            # 列加密    
            elif self.get_encryption_type() == 1:
                # 离散密文
                if key.start is None:
                    start = 0
                elif key.start < 0:
                    if key.start < -self.cipherShape()[0]:
                        raise IndexError(f"index {key.start} is out of bounds with size {self.cipherShape()[0]}")
                    start = self.cipherShape()[1] + key.start
                    
                else:
                    if key.start >= self.cipherShape()[0]:
                        raise IndexError(f"index {key.start} is out of bounds with size {self.cipherShape()[0]}")
                    start = key.start
                
                if key.stop is None:
                    stop = self.cipherShape()[0]
                elif key.stop < 0:
                    if key.stop < -self.cipherShape()[0]:
                        raise IndexError(f"index {key.stop} is out of bounds with size {self.cipherShape()[0]}")
                    stop = self.cipherShape()[0] + key.stop
                else:
                    if key.stop > self.cipherShape()[0]:
                        raise IndexError(f"index {key.stop} is out of bounds with size {self.cipherShape()[0]}")
                    stop = key.stop
                if key.step is None:
                    step = 1
                
                slice_len = (stop - start + step - 1) // step
                res_list = []
                for i in range(start, stop, step):
                    # 离散密文
                    if self.get_cipher_type() == 3:
                        res_list.append(self.get_base_array()[i*2:i*2+2])
                    # 向量密文    
                    else:
                        if i == start:
                            res_list.append(self.get_base_array()[0])
                            res_list.append([slice_len] * self.cipherShape()[1])
                        res_list.append(self.get_base_array()[2+i])
                if self.get_cipher_type() == 3: # 离散密文
                    array = np.concatenate(res_list, axis=0)
                else:
                    array = np.array(res_list)
                return CipherArray(array)
        else: 
            raise ValueError("Unsupported indexing operation")
    
    # 重写__setitem__方法以自定义修改指定下标位置内容
    def __setitem__(self, key, value):
        if self.cipher_type == 3: # 离散密文数组
            if not isinstance(value, CipherArray):
                raise ValueError("Value type error")
            value = value.get_base_array()
            if isinstance(key, int) and self.ndim == 1: 
                for i in range(len(value)):
                    self.get_base_array()[2 * key + i] = value[i]
            elif isinstance(key, tuple) and self.ndim == 2:
                row, col = key
                # 当行列都是整数
                if isinstance(row, int) and isinstance(col, int):
                    if self.encryption_type == 0: # 对于行加密的情况
                        for i in range(len(value)):
                            self.get_base_array()[row, 2 * col + i] = value[i]
                    else: # 对于列加密的情况
                        for i in range(len(value)):
                            self.get_base_array()[2 * row + i, col] = value[i]
                else: 
                    raise ValueError("Unsupported indexing operation")
            else: 
                raise ValueError("Unsupported indexing operation")
        elif self.cipher_type == 2: # 连续密文数组
            if isinstance(key, int) and self.ndim == 1:
                if key < 0:
                    key = int(self.get_base_array()[1]) + key
                if not isinstance(value, CipherArray):
                    raise ValueError("Value type error")
                tmp_result = cipher_array_append(self, value)
                l = tmp_result.get_base_array().tolist()
                l[1] -= 1
                if key == self.get_base_array()[1] - 1:
                    l = l[:-2] + l[-1:]
                else:
                    l = l[:2+key] + [l[-1]] + l[2+key+1:-1]
                self.get_base_array()[:] = l
            else: 
                raise ValueError("Unsupported indexing operation")
        else: 
            raise ValueError("Unsupported indexing operation")

    # 行列加密转换
    def transEncType(self):
        if self.size == 0:
            return empty_cipher_array()
        elif self.ndim == 1:
            arr = self.get_base_array()
            arr = arr.reshape(-1,1)
            return CipherArray(arr)
        elif self.ndim == 2:
            if self.cipher_type == 3:
                raise ValueError("Unsupported discrete cipher array transpose operation")
            else:
                # if self.shape[0] == 1 or self.shape[1] == 1:
                #     arr = self.get_base_array()
                #     arr = arr.T
                #     return CipherArray(arr)
                return self._trans_enctype()
        else:
            raise ValueError("Arrays with dimensions greater than 2 are not supported")                    
   
    def _broadcast_arrays(self, other):
        """
        最高支持二维密文的通用广播
        """
        self_shape = self.cipherShape()
        other_shape = other.cipherShape()

        if self_shape == other_shape:
            return self, other

        # 1. 补齐形状的长度
        # 2. 判断是否满足广播条件
        # 3. 满足广播条件，则进行广播
        if len(self_shape) == 0:
            self_shape = (1,)
        if len(other_shape) == 0:
            other_shape = (1,)
        if len(self_shape) != len(other_shape):
            if len(self_shape) > len(other_shape):
                other_shape = (1, other_shape[0])
            else:
                self_shape = (1, self_shape[0])
        
        common_shape = []
        for i in range(len(self_shape)):
            if self_shape[i] == other_shape[i] or self_shape[i] == 1 or other_shape[i] == 1:
                if self_shape[i] >= other_shape[i]:
                    common_shape += [self_shape[i]]
                else:
                    common_shape += [other_shape[i]]
                continue
            raise ValueError(f"The two shapes {self.cipherShape()} and {other.cipherShape()} cannot be broadcast to a common shape")
        common_shape = tuple(common_shape)    
        
        if len(common_shape) == 1:
            if self_shape[0] != common_shape[0] or len(self.cipherShape()) == 0:
                self = self._broadcast_to(common_shape)
            if other_shape[0] != common_shape[0] or len(other.cipherShape()) == 0:
                other = other._broadcast_to(common_shape)
            return self, other
        else: # len(common_shape) == 2
            if self.get_cipher_type() == 1: # 标量
                self = self._broadcast_to(common_shape, other.get_encryption_type())
                return self, other
            if other.get_cipher_type() == 1: # 标量
                other = other._broadcast_to(common_shape, self.get_encryption_type())
                return self, other
            
            if self.get_cipher_type() == 2 and self.ndim == 1:
                self = self._broadcast_to(common_shape, other.get_encryption_type())
                return self, other
            if other.get_cipher_type() == 2 and other.ndim == 1:
                other = other._broadcast_to(common_shape, self.get_encryption_type())
                return self, other
            
            # 将矩阵广播至指定维度
            if self_shape[0] != common_shape[0] or self_shape[1] != common_shape[1]:
                # 公共密文形状对应的底层数组形状
                # common_shape = (3, 4)
                # 1. 行加密  base_common_shape = (3, 6) 2. 列加密 base_common_shape = (5, 4)
                self = self._broadcast_to(common_shape)
            if other_shape[0] != common_shape[0] or other_shape[1] != common_shape[1]:
                other = other._broadcast_to(common_shape)
                
            return self, other

    def _broadcast_to(self, shape, output_encrypt_type=-1):
        """
        通用广播函数，类似 numpy.broadcast_to
        参数：
        self: CipherArray类型，需要广播的数组
        shape: tuple类型，广播到的目标形状
        encrypt_type: int类型，加密类型，0为行加密，1为列加密
        """

        encrypt_type = self.get_encryption_type()
        cipher_type = self.get_cipher_type()
        array = self.get_base_array()
        cipher_shape = self.cipherShape()
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

    # 标量密文添加到向量密文
    def _append(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)

        append_func = get_func_name("append")
        append_func.argtypes = [POINTER(c_double), c_int, POINTER(c_double), c_int]
        append_func.restype = POINTER(c_double)

        res_ptr = append_func(self_double_array, c_int(len(self)), other_double_array, c_int(len(other)))
        if int(self[1]) == 0 and self[2] == 0.0:
            res = np.ctypeslib.as_array(res_ptr, shape=(int(len(self)),))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(int(len(self)+1),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 向量密文添加到向量密文
    def _append_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)

        append_array_func = get_func_name("append_array")
        append_array_func.argtypes = [POINTER(c_double), c_int, POINTER(c_double), c_int]
        append_array_func.restype = POINTER(c_double)

        res_ptr = append_array_func(self_double_array, c_int(len(self)), other_double_array, c_int(len(other)))
        if int(self[1]) == 0 and self[2] == 0.0:
            res = np.ctypeslib.as_array(res_ptr, shape=(len(other),))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(int(len(self)+other[1]),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _append_1d_2d(self, other):
        encrypt_type = other.get_encryption_type()
        cipher_shape_other = other.cipherShape()
        self = self.get_base_array()
        other = other.get_base_array()
        other_shape = other.shape
        self_double_array = (c_double * len(self))(*self)
        other = other.reshape(-1,)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("append")
        func = get_func_name("append_1d_2d")
        func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        func.restype = POINTER(c_double)
        res_ptr = func(self_double_array, other_double_array, c_int(len(self)), c_int(other_shape[0]), c_int(other_shape[1]), c_int(encrypt_type), c_bool(parallel))
        # 检查向量是否为空向量
        if int(self[1]) == 0 and self[2] == 0.0: # 空向量
            length = cipher_shape_other[0] * cipher_shape_other[1]
        else:
            length = int(self[1]) + cipher_shape_other[0] * cipher_shape_other[1]
        res = np.ctypeslib.as_array(res_ptr, shape=(length+2,))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _append_2d_scalar(self, other):
        encrypt_type = self.get_encryption_type()
        cipher_shape_self = self.cipherShape()
        self = self.get_base_array()
        other = other.get_base_array()
        self_shape = self.shape
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("append")
        func = get_func_name("append_2d_scalar")
        func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        func.restype = POINTER(c_double)
        res_ptr = func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(len(other)), c_int(encrypt_type), c_bool(parallel))
        length = cipher_shape_self[0] * cipher_shape_self[1] + 1
        res = np.ctypeslib.as_array(res_ptr, shape=(length+2,))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _append_2d_1d(self, other):
        encrypt_type = self.get_encryption_type()
        cipher_shape_self = self.cipherShape()
        self = self.get_base_array()
        other = other.get_base_array()
        self_shape = self.shape
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("append")
        func = get_func_name("append_2d_1d")
        func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        func.restype = POINTER(c_double)
        res_ptr = func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(len(other)), c_int(encrypt_type), c_bool(parallel))
        length = cipher_shape_self[0] * cipher_shape_self[1] + int(other[1])
        res = np.ctypeslib.as_array(res_ptr, shape=(length+2,))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _append_2d_2d(self, other, axis, output_encrypt_type):
        encrypt_type = self.encryption_type
        cipher_shape_self = self.cipherShape()
        cipher_shape_other = other.cipherShape()
        self = self.get_base_array()
        other = other.get_base_array()
        self_shape = self.shape
        other_shape = other.shape
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        if axis is None:
            parallel = get_func_parallelization_config("append")
            func = get_func_name("append_2d_2d_axisnone")
            func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
            func.restype = POINTER(c_double)
            res_shape = (cipher_shape_self[0] * cipher_shape_self[1] + cipher_shape_other[0] * cipher_shape_other[1] + 2,)
            res_ptr = func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(other_shape[0]), c_int(other_shape[1]), c_int(encrypt_type), c_bool(parallel))
            res = np.ctypeslib.as_array(res_ptr, shape=res_shape)
            weakref.finalize(res, free_double_ptr, res_ptr)
            return CipherArray(res)
        elif axis == 0:
            func = get_func_name("append_2d_2d_axis0")
            res_shape = (cipher_shape_self[0] + cipher_shape_other[0], cipher_shape_self[1])
        else:
            func = get_func_name("append_2d_2d_axis1")
            res_shape = (cipher_shape_self[0], cipher_shape_self[1] + cipher_shape_other[1]) 
        if output_encrypt_type == 0:
            res_shape = (res_shape[0], res_shape[1] +2)
        else:
            res_shape = (res_shape[0]+2, res_shape[1])
        func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool] 
        func.restype = POINTER(c_double)
        res_ptr =func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(other_shape[0]), c_int(other_shape[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=res_shape)
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 标量密文添加到向量密文中    
    def append(self, other, axis=None, output_encrypt_type=-1):
        check_res1 = self.get_cipher_type()
        check_res2 = other.get_cipher_type()
        if check_res1 == 2: # 向量或数组
            if self.ndim == 1:
                if check_res2 == 1:
                    return self._append(other)
                elif check_res2 == 2:
                    if other.ndim == 1:
                        return self._append_array(other)
                    else:
                        return self._append_1d_2d(other)
                else:
                    raise ValueError("Unable to handle discrete ciphertext array type, please enter scalar or array ciphertext.(Param:other)")
            else: # self.ndim = 2
                if check_res2 == 1:
                    return self._append_2d_scalar(other)
                elif check_res2 == 2:
                    if other.ndim == 1:
                        return self._append_2d_1d(other)
                    else:
                        if self.encryption_type != other.encryption_type:
                            other = other.transEncType()
                        if output_encrypt_type == -1:
                            output_encrypt_type = self.encryption_type
                        if axis == 0 and (self.cipherShape()[1] != other.cipherShape()[1]):
                            raise ValueError(f"Axis 1 has different lengths.[self.shape={self.cipherShape()}, other.shape={other.cipherShape()}]")
                        if axis == 1 and (self.cipherShape()[0] != other.cipherShape()[0]):
                            raise ValueError(f"Axis 0 has different lengths.[self.shape={self.cipherShape()}, other.shape={other.cipherShape()}]")
                        return self._append_2d_2d(other, axis, output_encrypt_type)

    def _reshape(self, shape, output_encrypt_type):
        self = self.get_base_array()
        self_double_array = (c_double * len(self))(*self)
        func = get_func_name("reshape")
        func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
        func.restype = POINTER(c_double)

        res_ptr = func(self_double_array, c_int(len(self)), shape[0], shape[1], c_int(output_encrypt_type))
        if output_encrypt_type == 0:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape[0], shape[1] + 2))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(2+shape[0], shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _reshape_array(self, shape, output_encrypt_type):
        encrypt_type = self.get_encryption_type()
        self_cshape = self.cipherShape()
        self = self.get_base_array()
        self_shape = self.shape
        self = self.reshape(-1,)
        s = np.array(shape)
        self_double_array = (c_double * len(self))(*self)
        s_int_array = (c_int * len(s))(*s)

        parallel = get_func_parallelization_config("reshape")
        func = get_func_name("reshape_array")
        func.argtypes = [POINTER(c_double), POINTER(c_int), c_int, c_int, c_int, c_int, c_int, c_bool]
        func.restype = POINTER(c_double)
        res_ptr = func(self_double_array, s_int_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(len(s)), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        if len(s) == 1:
            res = np.ctypeslib.as_array(res_ptr, shape=(2+self_cshape[0]*self_cshape[1],))
        else:
            if output_encrypt_type == 0 :
                res = np.ctypeslib.as_array(res_ptr, shape=(shape[0], shape[1] + 2))
            else:
                res = np.ctypeslib.as_array(res_ptr, shape=(shape[0]+2, shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def cipherReshape(self, *shape, output_encrypt_type=-1):
        if len(shape) > 2:
            raise ValueError("The length of shape must smaller than 2.")
        else:pass
        CHECK_ARRAY(self, "self")
        encrypt_type = self.get_encryption_type()
        if output_encrypt_type == -1:
            output_encrypt_type = encrypt_type
        cs = self.cipherShape()
        if self.ndim == 1:
            if len(shape) == 1:
                if shape[0] != -1 and shape[0] != cs[0]:
                    raise ValueError(f"Error input shape {shape},the shape of self is {cs}.")
                else:pass
                return self
            else:
                if (shape[0] * shape[1] != cs[0] and shape[0] != -1 and shape[1] != -1) or (shape[0] == -1 and cs[0] % shape[1] != 0) or (shape[1] == -1 and cs[0] % shape[0] != 0):
                    raise ValueError(f"Error input shape {shape},the shape of self is {cs}.")
                if shape[0] == -1:
                    shape = (cs[0] // shape[1], shape[1])
                if shape[1] == -1:
                    shape = (shape[0], cs[0] // shape[0])
                return self._reshape(shape, output_encrypt_type)
        else:        
            if len(shape) == 1:
                if shape[0] != -1 and shape[0] != cs[0] * cs[1]:
                    raise ValueError(f"Error input shape {shape},the shape of self is {cs}.")
            else:
                if (shape[0] * shape[1] != cs[0] * cs[1] and shape[0] != -1 and shape[1] != -1) or (shape[0] == -1 and (cs[0] * cs[1]) % shape[1] != 0) or (shape[1] == -1 and (cs[0] * cs[1]) % shape[0] != 0):
                    raise ValueError(f"Error input shape {shape},the shape of self is {cs}.")
                else:pass
                if shape[0] == -1:
                    shape = ((cs[0] * cs[1]) // shape[1], shape[1])
                else:pass
                if shape[1] == -1:
                    shape = (shape[0], (cs[0] * cs[1]) // shape[0])
                else:pass
            return self._reshape_array(shape, output_encrypt_type)

    # 标量密文加法
    def _add(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)

        # 调用go函数
        add_func = get_func_name("add")
        add_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        add_func.restype = POINTER(c_double)

        # 将数组传递给C函数，并获取返回的指针
        res_ptr = add_func(self_double_array, other_double_array, c_int(len(self)))

        # 获取指针指向的数据内容并返回
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        # print("python back res: \n %d, %d, %d, %d, %.16f"% (res[0], res[1], res[2], res[3], res[4]))

        # 使用ctypes库创建C数组指针无须手动释放C数组的内存， 使用Cython或其他扩展库需要手动释放
        # freeMemory(self_double_array)
        # freeMemory(other_double_array)
        # freeMemory(res_ptr)
        # print(res)
        weakref.finalize(res, free_double_ptr, res_ptr)
        return  CipherArray(res)
    
    def _add_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * len(self))(*self)
        # 调用go函数
        add_double_func = get_func_name("add_double")
        add_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        add_double_func.restype = POINTER(c_double)

        # 将数组传递给C函数，并获取返回的指针
        res_ptr = add_double_func(self_double_array, c_int(len(self)), c_double(other))

        # 获取指针指向的数据内容并返回
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return  CipherArray(res)
    
    # 数组密文加法
    def _add_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        add_array_func =  get_func_name("add_array")
        add_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        add_array_func.restype = POINTER(c_double)
        # 获取返回值指针
        res_ptr = add_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return  CipherArray(res)
    
    # 向量密文加明文
    def _add_array_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        add_array_double_func =  get_func_name("add_array_double")
        add_array_double_func.argtypes = [POINTER(c_double),  c_int, c_double]
        add_array_double_func.restype = POINTER(c_double)
        # 获取返回值指针
        res_ptr = add_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return  CipherArray(res)
    
    def _add_array_array(self, other):
        # 调用时具有相同的加密类型
        encrypt_type = self.encryption_type
        self = self.get_base_array()
        other = other.get_base_array()
        self_shape = self.shape
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        parallel = get_func_parallelization_config("add")
        add_array_array_func = get_func_name("add_array_array")
        add_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        add_array_array_func.restype = POINTER(c_double)
        res_ptr = add_array_array_func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _add_array_array_double(self, m):
        encrypt_type = self.encryption_type
        self = self.get_base_array()        
        self_shape = self.shape
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("add")
        add_array_array_double_func = get_func_name("add_array_array_double")
        add_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
        add_array_array_double_func.restype = POINTER(c_double)
        res_ptr = add_array_array_double_func(self_double_array, c_double(m), c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 标量密文减法
    def _sub(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        # 调用go函数
        sub_func = get_func_name("sub")
        sub_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        sub_func.restype = POINTER(c_double)
        # sub_func.restypes = POINTER(c_double)  加s出问题
        # 将数组传递给C函数，并获取返回指针
        res_ptr = sub_func(self_double_array, other_double_array, c_int(len(self)))
        # 获取指针指向的数据内容并返回
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    # 标量密文减明文
    def _sub_double(self,other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * len(self))(*self)

        # 调用go函数
        sub_double_func = get_func_name("sub_double")
        sub_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        sub_double_func.restype = POINTER(c_double)

        res_ptr = sub_double_func(self_double_array, c_int(len(self)), c_double(other))
        # 获取指针指向的数据内容并返回
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _sub_double_right(self, m):
        # 类型转换        
        self = self.get_base_array()
        self_double_array = (c_double * len(self))(*self)
        # 调用go函数
        sub_double_right_func = get_func_name("sub_double_right")
        sub_double_right_func.argtypes = [POINTER(c_double), c_int, c_double]
        sub_double_right_func.restype = POINTER(c_double)
        
        res_ptr = sub_double_right_func(self_double_array, c_int(len(self)), c_double(m))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 数组密文减法
    def _sub_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        sub_array_func = get_func_name("sub_array")
        sub_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        sub_array_func.restype = POINTER(c_double)

        res_ptr = sub_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _sub_array_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        # 调用go函数
        sub_array_double_func = get_func_name("sub_array_double")
        sub_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        sub_array_double_func.restype = POINTER(c_double)

        res_ptr = sub_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    # 明文减数组密文
    def _sub_array_double_right(self, m):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        sub_array_double_right_func = get_func_name("sub_array_double_right")
        sub_array_double_right_func.argtypes = [POINTER(c_double), c_int, c_double]
        sub_array_double_right_func.restype = POINTER(c_double)

        res_ptr = sub_array_double_right_func(self_double_array, c_int(len(self)), c_double(m))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _sub_array_array(self, other):
        encrypt_type = self.encryption_type
        self = self.get_base_array()
        other = other.get_base_array()
        self_shape = self.shape
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        parallel = get_func_parallelization_config("sub")
        sub_array_array_func = get_func_name("sub_array_array")
        sub_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        sub_array_array_func.restype = POINTER(c_double)
        res_ptr = sub_array_array_func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _sub_array_array_double(self, m):
        encrypt_type = self.encryption_type
        self = self.get_base_array()
        self_shape = self.shape
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("sub")
        sub_array_array_double_func = get_func_name("sub_array_array_double")
        sub_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
        sub_array_array_double_func.restype = POINTER(c_double)
        res_ptr = sub_array_array_double_func(self_double_array, c_double(m), c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _sub_array_array_double_right(self, m):
        encrypt_type = self.encryption_type
        self = self.get_base_array()
        self_shape = self.shape
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("sub")
        sub_array_array_double_right_func = get_func_name("sub_array_array_double_right")
        sub_array_array_double_right_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
        sub_array_array_double_right_func.restype = POINTER(c_double)
        res_ptr = sub_array_array_double_right_func(self_double_array, c_double(m), c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 标量密文乘法
    def _mul(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)

        # 调用go函数
        mul_func = get_func_name("mul")
        mul_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        mul_func.restype = POINTER(c_double)

        # 将数组指针传递给函数，并接收返回指针
        res_ptr = mul_func(self_double_array, other_double_array, c_int(len(self)))

        # 获取指针指向数据内容并返回
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 标量密文乘明文
    def _mul_double(self, other):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        mul_double_func = get_func_name("mul_double")
        mul_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        mul_double_func.restype = POINTER(c_double)

        res_ptr = mul_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    # 数组密文乘法
    def _mul_array(self, other):
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)

        mul_array_func = get_func_name("mul_array")
        mul_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        mul_array_func.restype = POINTER(c_double)

        res_ptr = mul_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 数组密文乘明文
    def _mul_array_double(self, other):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        mul_array_double_func = get_func_name("mul_array_double")
        mul_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        mul_array_double_func.restype = POINTER(c_double)

        res_ptr = mul_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 数组密文乘明文数组
    def _mul_array_double_array(self, other):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)

        mul_array_double_array_func = get_func_name("mul_array_double_array")
        mul_array_double_array_func.argtypes = [POINTER(c_double), c_int, POINTER(c_double), c_int]
        mul_array_double_array_func.restype = POINTER(c_double)

        res_ptr = mul_array_double_array_func(self_double_array, c_int(len(self)), other_double_array, c_int(len(other)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _mul_array_array(self, other):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        other = other.get_base_array()
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        parallel = get_func_parallelization_config("mul")
        mul_array_array_func = get_func_name("mul_array_array")
        mul_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        mul_array_array_func.restype = POINTER(c_double)
        res_ptr = mul_array_array_func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _mul_array_array_double(self, m):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("mul")
        mul_array_array_double_func = get_func_name("mul_array_array_double")
        mul_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
        mul_array_array_double_func.restype = POINTER(c_double)
        res_ptr = mul_array_array_double_func(self_double_array, c_double(m), c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)    

    # 标量密文除法
    def _div(self, other):

        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)

        # 调用go函数
        div_func = get_func_name("div")
        div_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        div_func.restype = POINTER(c_double)

        res_ptr = div_func(self_double_array, other_double_array, c_int(len(self)))

        # 获取指针指向数据内容并将其转换为ndarray数组
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 标量密文除明文
    def _div_double(self, other):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        div_double_func = get_func_name("div_double")
        div_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        div_double_func.restype = POINTER(c_double)

        res_ptr = div_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _div_double_right(self, m):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        div_double_right_func = get_func_name("div_double_right")
        div_double_right_func.argtypes = [POINTER(c_double), c_int, c_double]
        div_double_right_func.restype = POINTER(c_double)

        res_ptr = div_double_right_func(self_double_array, c_int(len(self)), c_double(m))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 数组密文除法
    def _div_array(self, other):
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)

        div_array_func = get_func_name("div_array")
        div_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        div_array_func.restype = POINTER(c_double)

        res_ptr = div_array_func(self_double_array, other_double_array, c_int(len(self)))

        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 数组密文乘明文
    def _div_array_double(self, other):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        div_array_double_func = get_func_name("div_array_double")
        div_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        div_array_double_func.restype = POINTER(c_double)

        res_ptr = div_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _div_array_double_right(self, m):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        div_array_double_func = get_func_name("div_array_double_right")
        div_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        div_array_double_func.restype = POINTER(c_double)

        res_ptr = div_array_double_func(self_double_array, c_int(len(self)), c_double(m))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _div_array_array(self, other):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        other = other.get_base_array()
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        parallel = get_func_parallelization_config("div")
        div_array_array_func = get_func_name("div_array_array")
        div_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        div_array_array_func.restype = POINTER(c_double)
        res_ptr = div_array_array_func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res) 
    
    def _div_array_array_double(self, m):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("div")
        div_array_array_double_func = get_func_name("div_array_array_double")
        div_array_array_double_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
        div_array_array_double_func.restype = POINTER(c_double)
        res_ptr = div_array_array_double_func(self_double_array, c_double(m), c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _div_array_array_double_right(self, m):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("div")
        div_array_array_double_right_func = get_func_name("div_array_array_double_right")
        div_array_array_double_right_func.argtypes = [POINTER(c_double), c_double, c_int, c_int, c_int, c_int, c_bool]
        div_array_array_double_right_func.restype = POINTER(c_double)
        res_ptr = div_array_array_double_right_func(self_double_array, c_double(m), c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res) 

    # 逐元素负数计算
    def _negative(self):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        negative_func = get_func_name("negative")
        negative_func.argtypes = [POINTER(c_double), c_int]
        negative_func.restype = POINTER(c_double)

        res_ptr = negative_func(self_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    # 逐元素负数计算
    def _negative_array(self):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        negative_array_func = get_func_name("negative_array")
        negative_array_func.argtypes = [POINTER(c_double), c_int]
        negative_array_func.restype = POINTER(c_double)

        res_ptr = negative_array_func(self_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _negative_array_array(self):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("negative")
        negative_array_array_func = get_func_name("negative_array_array")
        negative_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        negative_array_array_func.restype = POINTER(c_double)

        res_ptr = negative_array_array_func(self_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    # 标量密文整数次幂
    def _pow(self,other):
        # 数据类型转换python->C
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        pow_func = get_func_name("pow")
        pow_func.argtypes = [POINTER(c_double), c_int, c_int]
        pow_func.restype = POINTER(c_double)

        res_ptr = pow_func(self_double_array, c_int(len(self)), c_int(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    # 向量密文整数次幂
    def _pow_array(self,other):
        # 数据类型转换python->C
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        pow_array_func = get_func_name("pow_array")
        pow_array_func.argtypes = [POINTER(c_double), c_int, c_int]
        pow_array_func.restype = POINTER(c_double)

        res_ptr = pow_array_func(self_double_array, c_int(len(self)), c_int(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _pow_array_array(self, other):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("pow")
        pow_array_array_func = get_func_name("pow_array_array")
        pow_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
        pow_array_array_func.restype = POINTER(c_double)

        res_ptr = pow_array_array_func(self_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(other), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)        

    # 标量密文小数次幂
    def _power_float(self, other):
        # 数据类型转换python->C
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        power_float_func = get_func_name("float_power")
        power_float_func.argtypes = [POINTER(c_double), c_int, c_double]
        power_float_func.restype = POINTER(c_double)

        res_ptr = power_float_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    # 向量密文小数次幂
    def _power_float_array(self, other):
        # 数据类型转换python->C
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)

        power_float_array_func = get_func_name("float_power_array")
        power_float_array_func.argtypes = [POINTER(c_double), c_int, c_double]
        power_float_array_func.restype = POINTER(c_double)

        res_ptr = power_float_array_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _power_float_array_array(self, other):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("float_power")
        pow_array_array_func = get_func_name("float_power_array_array")
        pow_array_array_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_bool]
        pow_array_array_func.restype = POINTER(c_double)

        res_ptr = pow_array_array_func(self_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_double(other), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res) 
    
    # 返回除法元素的余数
    def _mod(self,other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 获取函数
        mod_func = get_func_name("mod")
        mod_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        mod_func.restype = POINTER(c_double)
        res_ptr = mod_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _mod_double(self, other):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        mod_double_func = get_func_name("mod_double")
        mod_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        mod_double_func.restype = POINTER(c_double)
        res_ptr = mod_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _mod_array(self, other):
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        mod_array_func = get_func_name("mod_array")
        mod_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        mod_array_func.restype = POINTER(c_double)
        res_ptr = mod_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _mod_array_double(self, other):
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        mod_array_double_func = get_func_name("mod_array_double")
        mod_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        mod_array_double_func.restype = POINTER(c_double)
        res_ptr = mod_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(len(self),))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    def _mod_array_array(self, other):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        other = other.get_base_array()
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        parallel = get_func_parallelization_config("mod")
        mod_array_array_func = get_func_name("mod_array_array")
        mod_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        mod_array_array_func.restype = POINTER(c_double)
        res_ptr = mod_array_array_func(self_double_array, other_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _mod_array_array_double(self, m):
        encrypt_type = self.encryption_type
        self_shape = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("mod")
        mod_array_array_double_func = get_func_name("mod_array_array_double")
        mod_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_double, c_bool]
        mod_array_array_double_func.restype = POINTER(c_double)
        res_ptr = mod_array_array_double_func(self_double_array, c_int(self_shape[0]), c_int(self_shape[1]), c_int(encrypt_type), c_int(encrypt_type), c_double(m), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(self_shape[0], self_shape[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)         

    # 标量密文相等==
    def _equal(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        equal_func = get_func_name("equal")
        equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        equal_func.restype = c_bool
        res = equal_func(self_double_array, other_double_array, c_int(len(self)))
        return res
    
    # 标量与明文比较相等==
    def _equal_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        equal_double_func = get_func_name("equal_double")
        equal_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        equal_double_func.restype = c_bool
        res = equal_double_func(self_double_array, c_int(len(self)), c_double(other))
        return res

    # 向量密文相等
    def _equal_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        equal_array_func = get_func_name("equal_array")
        equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        equal_array_func.restype = POINTER(c_bool)

        res_ptr = equal_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _equal_array_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        equal_array_double = get_func_name("equal_array_double")
        equal_array_double.argtypes = [POINTER(c_double), c_int, c_double]
        equal_array_double.restype = POINTER(c_bool)
        res_ptr = equal_array_double(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _equal_array_array(self, other):
        # 默认self与other具有相同的加密类型以及形状
        encrypt_type = self.get_encryption_type()
        if encrypt_type != other.get_encryption_type():
            other = other.transEncType()
        self = self.get_base_array()
        other = other.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("equal")
        # 调用go函数
        equal_array_array_func = get_func_name("equal_array_array")
        equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
        equal_array_array_func.restype = POINTER(c_bool)
        res_ptr = equal_array_array_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _equal_array_array_double(self, other):
        encrypt_type = self.get_encryption_type()
        self = self.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        parallel = get_func_parallelization_config("equal")
        # 调用go函数
        equal_array_array_double_func = get_func_name("equal_array_array_double")
        equal_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
        equal_array_array_double_func.restype = POINTER(c_bool)
        res_ptr = equal_array_array_double_func(self_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_double(other), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res

    # 标量密文不等 ！=
    def _not_equal(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        not_equal_func = get_func_name("not_equal")
        not_equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        not_equal_func.restype = c_bool
        res = not_equal_func(self_double_array, other_double_array, c_int(len(self)))
        return res
    
    def _not_equal_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        not_equal_double_func = get_func_name("not_equal_double")
        not_equal_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        not_equal_double_func.restype = c_bool
        res = not_equal_double_func(self_double_array, c_int(len(self)), c_double(other))
        return res

    # 向量密文不等 ！=
    def _not_equal_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        not_equal_array_func = get_func_name("not_equal_array")
        not_equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        not_equal_array_func.restype = POINTER(c_bool)

        res_ptr = not_equal_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _not_equal_array_double(self,other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        not_equal_array_double_func = get_func_name("not_equal_array_double")
        not_equal_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        not_equal_array_double_func.restype = POINTER(c_bool)
        res_ptr = not_equal_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _not_equal_array_array(self, other):
        # 默认self与other具有相同的加密类型以及形状
        encrypt_type = self.get_encryption_type()
        if encrypt_type != other.get_encryption_type():
            other = other.transEncType()        
        self = self.get_base_array()
        other = other.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("not_equal")
        # 调用go函数
        not_equal_array_array_func = get_func_name("not_equal_array_array")
        not_equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
        not_equal_array_array_func.restype = POINTER(c_bool)
        res_ptr = not_equal_array_array_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _not_equal_array_array_double(self, other):
        encrypt_type = self.get_encryption_type()
        self = self.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        parallel = get_func_parallelization_config("not_equal")
        # 调用go函数
        not_equal_array_array_double_func = get_func_name("not_equal_array_array_double")
        not_equal_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
        not_equal_array_array_double_func.restype = POINTER(c_bool)
        res_ptr = not_equal_array_array_double_func(self_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_double(other), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    # 标量密文大于等于 >=
    def _greater_equal(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        greater_equal_func = get_func_name("greater_equal")
        greater_equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        greater_equal_func.restype = c_bool
        res = greater_equal_func(self_double_array, other_double_array, c_int(len(self)))
        return res
    
    def _greater_equal_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        greater_equal_double_func = get_func_name("greater_equal_double")
        greater_equal_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        greater_equal_double_func.restype = c_bool
        res = greater_equal_double_func(self_double_array, c_int(len(self)), c_double(other))
        return res
    
    # 向量密文大于等于 >=
    def _greater_equal_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        greater_equal_array_func = get_func_name("greater_equal_array")
        greater_equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        greater_equal_array_func.restype = POINTER(c_bool)

        res_ptr = greater_equal_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _greater_equal_array_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        greater_equal_array_double_func = get_func_name("greater_equal_array_double")
        greater_equal_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        greater_equal_array_double_func.restype = POINTER(c_bool)
        res_ptr = greater_equal_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _greater_equal_array_array(self, other):
        # 默认self与other具有相同的加密类型以及形状
        encrypt_type = self.get_encryption_type()
        if encrypt_type != other.get_encryption_type():
            other = other.transEncType()        
        self = self.get_base_array()
        other = other.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("greater_equal")
        # 调用go函数
        greater_equal_array_array_func = get_func_name("greater_equal_array_array")
        greater_equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
        greater_equal_array_array_func.restype = POINTER(c_bool)
        res_ptr = greater_equal_array_array_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _greater_equal_array_array_double(self, other):
        encrypt_type = self.get_encryption_type()
        self = self.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        parallel = get_func_parallelization_config("greater_equal")
        # 调用go函数
        greater_equal_array_array_double_func = get_func_name("greater_equal_array_array_double")
        greater_equal_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
        greater_equal_array_array_double_func.restype = POINTER(c_bool)
        res_ptr = greater_equal_array_array_double_func(self_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_double(other), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    # 标量密文小于等于 <=
    def _less_equal(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        less_equal_func = get_func_name("less_equal")
        less_equal_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        less_equal_func.restype = c_bool
        res = less_equal_func(self_double_array, other_double_array, c_int(len(self)))
        return res
    
    def _less_equal_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        less_equal_double_func = get_func_name("less_equal_double")
        less_equal_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        less_equal_double_func.restype = c_bool
        res = less_equal_double_func(self_double_array, c_int(len(self)), c_double(other))
        return res

    # 向量密文小于等于 <=
    def _less_equal_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        less_equal_array_func = get_func_name("less_equal_array")
        less_equal_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        less_equal_array_func.restype = POINTER(c_bool)

        res_ptr = less_equal_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _less_equal_array_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        less_equal_array_double_func = get_func_name("less_equal_array_double")
        less_equal_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        less_equal_array_double_func.restype = POINTER(c_bool)
        res_ptr = less_equal_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _less_equal_array_array(self, other):
        # 默认self与other具有相同的加密类型以及形状
        encrypt_type = self.get_encryption_type()
        if encrypt_type != other.get_encryption_type():
            other = other.transEncType()
        self = self.get_base_array()
        other = other.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("less_equal")
        # 调用go函数
        less_equal_array_array_func = get_func_name("less_equal_array_array")
        less_equal_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
        less_equal_array_array_func.restype = POINTER(c_bool)
        res_ptr = less_equal_array_array_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _less_equal_array_array_double(self, other):
        encrypt_type = self.get_encryption_type()
        self = self.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        parallel = get_func_parallelization_config("less_equal")
        # 调用go函数
        less_equal_array_array_double_func = get_func_name("less_equal_array_array_double")
        less_equal_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
        less_equal_array_array_double_func.restype = POINTER(c_bool)
        res_ptr = less_equal_array_array_double_func(self_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_double(other), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    # 标量密文大于>
    def _greater(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        greater_func = get_func_name("greater")
        greater_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        greater_func.restype = c_bool
        res = greater_func(self_double_array, other_double_array, c_int(len(self)))
        return res
    
    def _greater_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        greater_double_func = get_func_name("greater_double")
        greater_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        greater_double_func.restype = c_bool
        res = greater_double_func(self_double_array, c_int(len(self)), c_double(other))
        return res
    
    # 向量密文大于
    def _greater_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        greater_array_func = get_func_name("greater_array")
        greater_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        greater_array_func.restype = POINTER(c_bool)

        res_ptr = greater_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _greater_array_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        greater_array_double_func = get_func_name("greater_array_double")
        greater_array_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        greater_array_double_func.restype = POINTER(c_bool)
        res_ptr = greater_array_double_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _greater_array_array(self, other):
        # 默认self与other具有相同的加密类型以及形状
        encrypt_type = self.get_encryption_type()
        if encrypt_type != other.get_encryption_type():
            other = other.transEncType()
        self = self.get_base_array()
        other = other.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("greater")
        # 调用go函数
        greater_array_array_func = get_func_name("greater_array_array")
        greater_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
        greater_array_array_func.restype = POINTER(c_bool)
        res_ptr = greater_array_array_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _greater_array_array_double(self, other):
        encrypt_type = self.get_encryption_type()
        self = self.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        parallel = get_func_parallelization_config("greater")
        # 调用go函数
        greater_array_array_double_func = get_func_name("greater_array_array_double")
        greater_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
        greater_array_array_double_func.restype = POINTER(c_bool)
        res_ptr = greater_array_array_double_func(self_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_double(other), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res

    # 标量密文小于
    def _less(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        less_func = get_func_name("less")
        less_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        less_func.restype = c_bool
        res = less_func(self_double_array, other_double_array, c_int(len(self)))
        return res
    
    def _less_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        less_double_func = get_func_name("less_double")
        less_double_func.argtypes = [POINTER(c_double), c_int, c_double]
        less_double_func.restype = c_bool
        res = less_double_func(self_double_array, c_int(len(self)), c_double(other))
        return res
    
    # 向量密文小于
    def _less_array(self, other):
        # 类型转换
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        other_double_array = (c_double * (len(other)))(*other)
        # 调用go函数
        less_array_func = get_func_name("less_array")
        less_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        less_array_func.restype = POINTER(c_bool)

        res_ptr = less_array_func(self_double_array, other_double_array, c_int(len(self)))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _less_array_double(self, other):
        # 类型转换
        self = self.get_base_array()
        self_double_array = (c_double * (len(self)))(*self)
        # 调用go函数
        less_array_func = get_func_name("less_array_double")
        less_array_func.argtypes = [POINTER(c_double), c_int, c_double]
        less_array_func.restype = POINTER(c_bool)
        res_ptr = less_array_func(self_double_array, c_int(len(self)), c_double(other))
        res = np.ctypeslib.as_array(res_ptr, shape=(int(self[1]),))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _less_array_array(self, other):
        # 默认self与other具有相同的加密类型以及形状
        encrypt_type = self.get_encryption_type()
        if encrypt_type != other.get_encryption_type():
            other = other.transEncType()
        self = self.get_base_array()
        other = other.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("less")
        # 调用go函数
        less_array_array_func = get_func_name("less_array_array")
        less_array_array_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_bool]
        less_array_array_func.restype = POINTER(c_bool)
        res_ptr = less_array_array_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res
    
    def _less_array_array_double(self, other):
        encrypt_type = self.get_encryption_type()
        self = self.get_base_array()
        # 密文数组的形状
        shape_self = self.shape
        if encrypt_type == 0:
            shape_new = (shape_self[0], shape_self[1]-2)
        else:
            shape_new = (shape_self[0]-2, shape_self[1])
        # ndarray转c数组
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        parallel = get_func_parallelization_config("less")
        # 调用go函数
        less_array_array_double_func = get_func_name("less_array_array_double")
        less_array_array_double_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_double, c_bool]
        less_array_array_double_func.restype = POINTER(c_bool)
        res_ptr = less_array_array_double_func(self_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(encrypt_type), c_double(other), c_bool(parallel))
        res = np.ctypeslib.as_array(res_ptr, shape=(shape_new[0], shape_new[1]))
        weakref.finalize(res, free_bool_ptr, res_ptr)
        return res

    def _inner(self, other):
        self = self.get_base_array()
        other = other.get_base_array()
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        inner_func = get_func_name("inner")
        inner_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
        inner_func.restype = POINTER(c_double)
        # 调用函数并接收返回值
        res_ptr = inner_func(self_double_array, other_double_array, len(self))
        res = np.ctypeslib.as_array(res_ptr, shape=(2,))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _trans_enctype(self):
        encryt_type = self.get_encryption_type()
        shape_self = self.cipherShape()
        arr = self.get_base_array()
        shape_self_origion = arr.shape
        arr = arr.reshape(-1,)
        arr_double_array = (c_double * (len(arr)))(*arr)
        parallel = get_func_parallelization_config("trans_enctype")
        trans_enctype_func = get_func_name("trans_enctype")
        trans_enctype_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_bool]
        trans_enctype_func.restype = POINTER(c_double)
        res_ptr = trans_enctype_func(arr_double_array, c_int(shape_self_origion[0]), c_int(shape_self_origion[1]), c_int(encryt_type), c_bool(parallel))
        if encryt_type == 0: # 原本为行加密，输出为列加密
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_self[0]+2, shape_self[1]))
        else: # 原本为列加密，输出为行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_self[0], shape_self[1]+2))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)  

    def _matmul(self, other):
        encrypt_type = self.encryption_type # 默认self与other具有相同的加密类型
        shape_self_new = self.cipherShape() # 获取密文的维度
        shape_other_new = self.cipherShape()
        self = self.get_base_array()
        other = other.get_base_array()
        shape_self = self.shape
        shape_other = other.shape
        self = self.reshape(-1,)
        other = other.reshape(-1,)
        # 一维ndarray转c数组
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        parallel = get_func_parallelization_config("matmul")
        # 调用go函数
        if encrypt_type == 0:
            matmul_func = get_func_name("matmul")
        else:
            matmul_func = get_func_name("matmul_col")
        matmul_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_int, c_bool]
        matmul_func.restype = POINTER(c_double)
        output_encrypt_type = encrypt_type
        res_ptr = matmul_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(shape_other[0]), c_int(shape_other[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        if output_encrypt_type == 0:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_self_new[0], shape_other_new[1]+2))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_self_new[0]+2, shape_other_new[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _matmul_1Dwith2D(self, other): 
        encrypt_type = other.encryption_type # 默认self与other具有相同的加密类型
        self = self.get_base_array()
        other = other.get_base_array()
        shape_other = other.shape
        # 计算结果向量的长度
        m = shape_other[1] if encrypt_type == 1 else shape_other[1]-2
        other = other.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)
        matmul_1Dwith2D_func = get_func_name("matmul_1dwith2d") 
        matmul_1Dwith2D_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int]
        matmul_1Dwith2D_func.restype = POINTER(c_double)

        res_ptr = matmul_1Dwith2D_func(self_double_array, other_double_array, c_int(len(self)), c_int(shape_other[0]), c_int(shape_other[1]), c_int(encrypt_type))
        res = np.ctypeslib.as_array(res_ptr, shape=(m+2,))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)

    def _matmul_2DWith1D(self, other):
        encrypt_type = self.encryption_type
        self = self.get_base_array()
        other = other.get_base_array()
        shape_self = self.shape
        # 计算结果矩阵的形状
        n = shape_self[0] if encrypt_type == 0 else shape_self[0]-2
        m = len(other)-2
        shape_res = (n, m)
        self = self.reshape(-1,)
        self_double_array = (c_double * len(self))(*self)
        other_double_array = (c_double * len(other))(*other)

        parallel = get_func_parallelization_config("matmul")
        matmul_2DWith1D_func = get_func_name("matmul_2dwith1d")
        matmul_2DWith1D_func.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int, c_int, c_bool]
        matmul_2DWith1D_func.restype = POINTER(c_double)

        res_ptr = matmul_2DWith1D_func(self_double_array, other_double_array, c_int(shape_self[0]), c_int(shape_self[1]), c_int(len(other)), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        if encrypt_type == 0:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_res[0], shape_res[1]+2))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_res[0]+2, shape_res[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)                                     

    # 密文加法包含 标量加标量、标量加向量、向量加标量、向量加向量
    def __add__(self, other):
        # 检查输入
        CHECK_DISCRETE(self, "Left operand")
        check_self = self.cipher_type
        type_other = type(other) 
        if type_other == float or type_other == int or isinstance(other, np.number):
            if check_self == 1:
                return self._add_double(other)
            elif check_self == 2:
                if self.ndim == 1:
                    return self._add_array_double(other)
                else:
                    return self._add_array_array_double(other)
        elif type_other == CipherArray:
            check_other = other.get_cipher_type()
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            
            if check_self == 1 and check_other == 1:
                return self._add(other)
            
            if self.ndim == 1 and other.ndim == 1:
                return self._add_array(other)
            
            if self.encryption_type != other.encryption_type:
                other = other.transEncType()
            return self._add_array_array(other)      
            
    # 重载右向加法
    def __radd__(self, other):
        # 进入此重载方法说明左操作数类型不是CipherArray类型
        CHECK_DISCRETE(self, "Right operand")         
        check_self = self.cipher_type
        type_other = type(other)
        if type_other == float or type_other == int or isinstance(other, np.number):
            if check_self == 1: # 标量密文
                return self._add_double(other)
            elif check_self == 2: # 向量密文
                if self.ndim == 1:
                    return self._add_array_double(other)
                elif self.ndim == 2:
                    return self._add_array_array_double(other)
        else:
            raise ValueError("Please check the parameter type!(Left operand)")

    # # 重载减法运算符 "-"
    def __sub__(self, other):
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._sub(other)
            if self.ndim == 1:
                return self._sub_array(other)
            return self._sub_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._sub_double(other)
            elif self.ndim == 1:
                return self._sub_array_double(other)
            return self._sub_array_array_double(other)
        raise ValueError("Please check the parameter type!(Right operand)")

    # 重载右向减法
    def __rsub__(self, other):
        # 进入此重载方法说明左操作数类型不是CipherArray类型
        CHECK_DISCRETE(self, "Right operand") 
        type_other = type(other)
        check_self = self.cipher_type
        if type_other == float or type_other == int or isinstance(other, np.number):
            if check_self == 1: # 标量密文
                return self._sub_double_right(other)
            elif check_self == 2: # 向量密文
                if self.ndim == 1:
                    return self._sub_array_double_right(other)
                elif self.ndim == 2:
                    return self._sub_array_array_double_right(other)
        else:
            raise ValueError("Please check the parameter type!(Left operand)")

    # 重载乘法运算符 "*"
    def __mul__(self, other):
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._mul(other)
            if self.ndim == 1:
                return self._mul_array(other)
            if self.ndim == 2:
                return self._mul_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._mul_double(other)
            if self.ndim == 1:
                return self._mul_array_double(other)
            if self.ndim == 2:
                return self._mul_array_array_double(other)
        elif isinstance(other, (list, np.ndarray)):
            if self.get_cipher_type() == 1:
                self = self._broadcast_to((len(other),))
                return self._mul_array_double_array(other)
            if self.get_cipher_type() == 2:
                if self.ndim == 1:
                    if self.shape[0]-2 < len(other):
                        self = self._broadcast_to((len(other),), broadcast_type=2)
                    elif self.shape[0]-2 > len(other):
                        raise ValueError(f"Can not broadcast![self.shape={self.shape},other.shape={other.shape}]")  
                    return self._mul_array_double_array(other)
                else:
                    raise ValueError(f"Can not broadcast![self.shape={self.shape},other.shape={other.shape}]")             
   
    # 重载右向乘法
    def __rmul__(self, other):
        # 检查self是否是合法的密文
        CHECK_DISCRETE(self, "Right operand")
        check_self = self.get_cipher_type()
        # 如果other是浮点型或整型，则调用明文与密文的运算函数
        if type(other) == float or type(other) == int or isinstance(other, np.number):
            if check_self == 1:
                return self._mul_double(other)
            elif check_self == 2:
                if self.ndim == 1:
                    return self._mul_array_double(other)
                elif self.ndim == 2:
                    return self._mul_array_array_double(other)
        elif type(other) == list or type(other) == np.ndarray:
            if check_self == 1:
                self = self._broadcast_to((len(other),))
            if check_self == 2:
                if self.ndim == 1 and len(self) < len(other):
                    self = self._broadcast_to((len(other)))
                else:
                    raise ValueError(f"Can not broadcast![self.shape={self.shape},other.shape={other.shape}]")  
            return self._mul_array_double_array(other)     
        else:
            raise ValueError("Please check the parameter type!(Left operand)")   

    # 重载除法运算符 "/"
    def __truediv__(self, other):
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._div(other)
            if self.ndim == 1 and other.ndim == 1:
                return self._div_array(other)
            if self.ndim == 2 and other.ndim == 2:
                return self._div_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._div_double(other)
            if self.ndim == 1:
                return self._div_array_double(other)
            if self.ndim == 2:
                return self._div_array_array_double(other)

    # 重载右向除法运算符
    def __rtruediv__(self, other):
        # 右向除法，左操作数是一个非密文类型
        # 检查self是否是合法的密文
        CHECK_DISCRETE(self, "Right operand")         
        check_self = self.get_cipher_type()
        # 如果other是浮点型或整型，则调用明文与密文的运算函数
        if type(other) == float or type(other) == int or isinstance(other, np.number):
            if check_self == 1:
                return self._div_double_right(other)
            elif check_self == 2:
                if self.ndim == 1:
                    return self._div_array_double_right(other)
                elif self.ndim == 2:
                    return self._div_array_array_double_right(other)
        else:
            raise ValueError("Please check the parameter type!(Left operand)")

    # 重载取负运算符 "-"
    def __neg__(self):
        # 检查输入
        CHECK_DISCRETE(self, "self")         
        check_res = self.get_cipher_type() 
        if check_res == 1:
            return self._negative()
        elif check_res == 2:
            if self.ndim == 1:
                return self._negative_array()
            else:
                return self._negative_array_array()

    # 重载幂运算符 "**" 或 np.power
    def __pow__(self, exponent):
        CHECK_DISCRETE(self, "Left operand")         
        check_res = self.get_cipher_type()
        if check_res == 1:
            if type(exponent) == int :
                return self._pow(exponent)
            elif type(exponent) == float or isinstance(exponent, np.number):
                return self._power_float(exponent)
            else:
                raise ValueError("Please enter integer or float!(Right operand)")
        elif check_res == 2:
            if self.ndim == 1:
                if type(exponent) == int :
                    return self._pow_array(exponent)
                elif type(exponent) == float or isinstance(exponent, np.number):
                    return self._power_float_array(exponent)
                else:
                    raise ValueError("Please enter integer or float!(Right operand)")
            else:
                if type(exponent) == int :
                    return self._pow_array_array(exponent)
                elif type(exponent) == float or isinstance(exponent, np.number):
                    return self._power_float_array_array(exponent)
                else:
                    raise ValueError("Please enter integer or float!(Right operand)")

    # 重载取余数运算符 "%" 或 np.mod
    def __mod__(self, other):
        CHECK_DISCRETE(self, "Left operand")         
        if isinstance(other, CipherArray):
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1:
                return self._mod(other)
            if self.get_cipher_type() == 2:
                if self.ndim == 1 and other.ndim == 1:
                    return self._mod_array(other)
                if self.ndim == 2 and other.ndim == 2:
                    return self._mod_array_array(other)                          
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._mod_double(other)
            if self.get_cipher_type() == 2:
                if self.ndim == 1:
                    return self._mod_array_double(other)
                if self.ndim == 2:
                    return self._mod_array_array_double(other)

    # 重载等于运算符 "=="
    def __eq__(self, other):
        # 检查输入
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._equal(other)
            if self.ndim == 1:
                return self._equal_array(other)
            if self.ndim == 2:
                return self._equal_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._equal_double(other)
            if self.ndim == 1:
                return self._equal_array_double(other)
            if self.ndim == 2:
                return self._equal_array_array_double(other)

    # 重载不等于运算符 "!="
    def __ne__(self, other):
        # 检查输入
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._not_equal(other)
            if self.ndim == 1:
                return self._not_equal_array(other)
            if self.ndim == 2:
                return self._not_equal_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._not_equal_double(other)
            if self.ndim == 1:
                return self._not_equal_array_double(other)
            if self.ndim == 2:
                return self._not_equal_array_array_double(other)

    # 重载大于运算符 ">"
    def __gt__(self, other):
        # 检查输入
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._greater(other)
            if self.ndim == 1:
                return self._greater_array(other)
            if self.ndim == 2:
                return self._greater_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._greater_double(other)
            if self.ndim == 1:
                return self._greater_array_double(other)
            if self.ndim == 2:
                return self._greater_array_array_double(other)

    # 重载小于运算符 "<"
    def __lt__(self, other):
        # 检查输入
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._less(other)
            if self.ndim == 1:
                return self._less_array(other)
            if self.ndim == 2:
                return self._less_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._less_double(other)
            if self.ndim == 1:
                return self._less_array_double(other)
            if self.ndim == 2:
                return self._less_array_array_double(other)

    # 重载大于等于运算符 ">="
    def __ge__(self, other):
        # 检查输入
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._greater_equal(other)
            if self.ndim == 1:
                return self._greater_equal_array(other)
            if self.ndim == 2:
                return self._greater_equal_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._greater_equal_double(other)
            if self.ndim == 1:
                return self._greater_equal_array_double(other)
            if self.ndim == 2:
                return self._greater_equal_array_array_double(other)

    # 重载小于等于运算符 "<="
    def __le__(self, other):
        # 检查输入
        CHECK_DISCRETE(self, "Left operand")
        if isinstance(other, CipherArray):
            CHECK_DISCRETE(other, "Right operand")
            self, other = self._broadcast_arrays(other)
            if self.get_cipher_type() == 1 and other.get_cipher_type() == 1:
                return self._less_equal(other)
            if self.ndim == 1:
                return self._less_equal_array(other)
            if self.ndim == 2:
                return self._less_equal_array_array(other)
        elif isinstance(other, (int, float, np.number)):
            if self.get_cipher_type() == 1:
                return self._less_equal_double(other)
            if self.ndim == 1:
                return self._less_equal_array_double(other)
            if self.ndim == 2:
                return self._less_equal_array_array_double(other)

    # 重载矩阵乘法运算符@
    def __matmul__(self, other):
        CHECK_DISCRETE(self, "Left operand") 
        CHECK_DISCRETE(other, "Right operand")                 
        check_res1 = self.get_cipher_type()
        check_res2 = other.get_cipher_type()
        # 如果是向量密文则调用内积
        if len(self.cipherShape()) == 1 and len(other.cipherShape()) == 1:
            if check_res1 == 1 or check_res2 == 1:
                return self.__mul__(other)
            if check_res1 == 2 and check_res2 == 2:
                if len(self) == len(other) :
                    return self._inner(other)
                else:
                    raise ValueError("The two ciphertext lengths do not match!")
        elif len(self.cipherShape()) == 1 and len(other.cipherShape()) == 2:
            return self._matmul_1Dwith2D(other)
        elif len(self.cipherShape()) == 2 and len(other.cipherShape()) == 1:
            return self._matmul_2DWith1D(other)
        else:
            return self._matmul(other)

    # 重载转置函数
    @property
    def T(self):
        # # 标量密文报错
        # if self.get_cipher_type() == 1:
        #     raise ValueError("Unable to handle scalar cipherarray.")
        # if self.ndim == 1:
        #     base_array = self.get_base_array()
        #     base_array = base_array.reshape(1, -1)
        #     self = CipherArray(base_array)
        # encrypt_type = self.get_encryption_type()
        # shape_c1 = self.cipherShape()
        # shape_c1_new = self.shape
        # self = self.get_base_array()
        # self = self.reshape(-1,)
        # self_double_array = (c_double * (len(self)))(*self)
        # parallel = get_func_parallelization_config("transpose")
        # transpose_func = get_func_name("transpose")
        # transpose_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        # transpose_func.restype = POINTER(c_double)
        # res_ptr = transpose_func(self_double_array, c_int(shape_c1_new[0]), c_int(shape_c1_new[1]), c_int(encrypt_type), c_int(encrypt_type), c_bool(parallel))
        # if encrypt_type == 0:
        #     res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[1], shape_c1[0]+2))
        # else:
        #     res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[1]+2, shape_c1[0]))
        # return CipherArray(res)
        return self.transpose()
    
    def transpose(self, output_encrypt_type=-1):
        # 标量密文报错
        if self.get_cipher_type() == 1:
            raise ValueError("Unable to handle scalar cipherarray.")
        if self.ndim == 1:
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
            base_array = self.get_base_array()
            base_array = base_array.reshape(1, -1)
            # 向量密文转置为列加密的数组密文，不需要进行计算，直接调用矩阵转置函数
            if output_encrypt_type == 1:
                return CipherArray(base_array.T)
            self = CipherArray(base_array)
        encrypt_type = self.get_encryption_type()
        if output_encrypt_type != 0 and output_encrypt_type != 1:
            output_encrypt_type = encrypt_type
        shape_c1 = self.cipherShape()
        shape_c1_new = self.shape
        self = self.get_base_array()
        self = self.reshape(-1,)
        self_double_array = (c_double * (len(self)))(*self)
        parallel = get_func_parallelization_config("transpose")
        transpose_func = get_func_name("transpose")
        transpose_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int, c_bool]
        transpose_func.restype = POINTER(c_double)
        res_ptr = transpose_func(self_double_array, c_int(shape_c1_new[0]), c_int(shape_c1_new[1]), c_int(encrypt_type), c_int(output_encrypt_type), c_bool(parallel))
        if output_encrypt_type == 0:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[1], shape_c1[0]+2))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_c1[1]+2, shape_c1[0]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
    
    # 矩阵求逆
    @property
    def I(self):
        shape_self = self.cipherShape()
        if len(shape_self) == 1:
            raise ValueError("Unable to handle one-dimensional vector ciphertext, please enter two-dimensional array ciphertext.(Param:self)")
        if shape_self[0] != shape_self[1]:
            raise ValueError("The input parameter is not a square matrix, please check the input.(Param:self)")
        encrypt_type = self.get_encryption_type()
        self = self.get_base_array()
        shape_self_new = self.shape
        self = self.reshape(-1,) # 转为一维数组
        self_double_array = (c_double * len(self))(*self)
        # 调用go函数
        inv_func = get_func_name("inv")
        inv_func.argtypes = [POINTER(c_double), c_int, c_int, c_int, c_int]
        inv_func.restype = POINTER(c_double)
        # 输出与输入的加密类型一致
        res_ptr = inv_func(self_double_array, c_int(shape_self_new[0]), c_int(shape_self_new[1]), c_int(encrypt_type), c_int(encrypt_type))
        if encrypt_type == 0: # 行加密
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_self[0], shape_self[1] + 2))
        else:
            res = np.ctypeslib.as_array(res_ptr, shape=(shape_self[0] + 2, shape_self[1]))
        weakref.finalize(res, free_double_ptr, res_ptr)
        return CipherArray(res)
        
# 判断浮点数组前几位是否是接近整数的数
def _check_prefix_approx_int(ndarray, start_index=0, end_index=0):
    for i in range(start_index, end_index):
        uint16_list = _float64_to_uint16(ndarray[i]) # uint16_list是一个列表，内部存放整数
        for data in uint16_list:
            if data >= 1000 or data < 0:
                error_msg = f"The element at index {i} is not encoded from the first four digits of the ciphertext."
                return False, error_msg
    error_msg = ""
    return True, error_msg

def _float64_to_uint16(f64):
    # 将64位浮点数转换为字节串（8个字节）
    byte_data = struct.pack('>d', f64)  # '>d' 表示大端序的64位浮点数

    # 将每两个字节（16位）组合成无符号整数
    uint16_list = []
    for i in range(0, len(byte_data), 2):
        # 将两个字节组合为一个16位无符号整数 (高8位 + 低8位)
        uint16 = (byte_data[i+1] << 8) | byte_data[i]
        uint16_list.append(uint16)

    return uint16_list

# 获取空数组
def empty_cipher_array():
    # 调用go函数
    empty_array_func = get_func_name("empty_array")
    empty_array_func.argtype = None
    empty_array_func.restype = POINTER(c_double)
    res_ptr = empty_array_func()
    res = np.ctypeslib.as_array(res_ptr, shape=(3,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

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
    weakref.finalize(res, free_double_ptr, res_ptr)
    return CipherArray(res)

# 向数组添加元素
def cipher_array_append(c1,c2):
    check_res1 = c1.get_cipher_type()
    check_res2 = c2.get_cipher_type()
    c1 = c1.get_base_array()
    c2 = c2.get_base_array()
    if check_res1 == 2:
        if check_res2 == 1:
            return __append(c1, c2)
        elif check_res2 == 2:
            return __append_array(c1, c2)
        else:
            raise ValueError("Unable to handle discrete ciphertext array type, please enter scalar or vector ciphertext.(Param:c2)")
    else:
        raise ValueError("Can only handle vector ciphertext, please enter vector ciphertext!(Param:c1)")