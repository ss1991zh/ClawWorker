import warnings
import numpy as np
from ctypes import *
from .base import (
    _enc_scalar, 
    _enc_1darray, 
    _enc_1darray_discrete, 
    _dec_scalar, 
    _dec_1darray, 
    _dec_1darray_discrete, 
    _encrypt_ndarray, 
    _decrypt_ndarray, 
    _encrypt_scalar2
)


# 加密方法（入口函数）
def encrypt(input_array, method='hp', encrypt_by_column=False, discrete=False):
    if method == 'hp':  
        import henumpy as hp
        if isinstance(input_array, str):
            raise ValueError("String input is not supported for the time being.")
        if isinstance(input_array, (int, float)):
            return _enc_scalar(input_array)
        input_array = np.array(input_array)
        if input_array.ndim == 1:
            if discrete:
                if encrypt_by_column:
                    return hp.CipherArray(_enc_1darray_discrete(input_array).reshape(-1, 1), discrete=True)
                else:
                    return _enc_1darray_discrete(input_array)
            else:
                if encrypt_by_column:
                    return hp.CipherArray(_enc_1darray(input_array).reshape(-1, 1))
                else:
                    return _enc_1darray(input_array)
        elif input_array.ndim == 2:
            if encrypt_by_column:
                encrypted_data_tmp = []
                for col in range(input_array.shape[1]):
                    column_values = input_array[:, col].astype(float)
                    if discrete:
                        encrypted_data_tmp.append(_enc_1darray_discrete(column_values).get_base_array())
                    else:
                        encrypted_data_tmp.append(_enc_1darray(column_values).get_base_array())
                    encrypted_data = list(map(list, zip(*encrypted_data_tmp))) # 转置
            else:
                encrypted_data = []
                for row in input_array:
                    row_values = row.astype(float)
                    if discrete:
                        encrypted_data.append(_enc_1darray_discrete(row_values).get_base_array())
                    else:
                        encrypted_data.append(_enc_1darray(row_values).get_base_array())
            if discrete:
                return hp.CipherArray(np.array(encrypted_data), discrete=True)
            else:
                return hp.CipherArray(np.array(encrypted_data), discrete=False)
        else:
            raise ValueError("Array parsing above 2 dimensions is not supported for the time being.")
    elif method == 'hp2':
        import henumpy2 as hp2
        # 标量加解密
        if isinstance(input_array, (int, float, np.number)):
            res = _encrypt_scalar2(input_array)
            return hp2.CipherArray(res)
        res = _encrypt_ndarray(input_array)
        return hp2.CipherArray(res.reshape(input_array.shape + (2,)))
    else:
        raise ValueError("Unsupported encryption method")


# 解密方法（入口函数）
def decrypt(input, method='hp', decrypt_by_column=False, discrete=False):
    if method == 'hp':
        if isinstance(input, np.ndarray):
            return _decrypt_cipher_array(input, decrypt_by_column, discrete)
        elif isinstance(input, tuple):
            list_ = []
            for item in input:
                list_.append(_decrypt_cipher_array(item, decrypt_by_column, discrete))
            return tuple(list_)
        else:
            raise TypeError(f"Unable to decrypt data of {type(input)} type")
    elif method == 'hp2':
        shape = input.shape
        data = input.get_base_array()
        res = _decrypt_ndarray(data)
        res = res.reshape(shape)
        return res


def _decrypt_cipher_array(input_array, decrypt_by_column=False, discrete=False):
    if 'hp' not in dir():
        import henumpy as hp
    encryption_type = 1 if decrypt_by_column else 0
    if isinstance(input_array, hp.CipherArray):
        encryption_type = input_array.get_encryption_type() # 如果是CipherArray类型，则获取encryption_type覆盖
        if decrypt_by_column and encryption_type == 0: # 代码检测到行加密但是用户输入列加密的时候给出warning
            warnings.warn("[decode] The detected CipherArray type does not match the one you manually entered. The default is based on the detected type.")
        input_array = input_array.get_base_array()
    # else:
    #     input_array = hp.CipherArray(input_array)
    if input_array.ndim == 1:
        if discrete:
            return _dec_1darray_discrete(input_array)
        else:
            if len(input_array) == 2:
                return _dec_scalar(input_array)
            elif len(input_array) > 2:
                return _dec_1darray(input_array)
            else:
                raise ValueError("len(input_array) error, try to use 'decrypt_by_column=False' please.")
    elif input_array.ndim == 2:
        # 转换数据并解密
        if encryption_type == 1:
            decrypted_data_tmp = []
            for col in range(input_array.shape[1]):
                encrypted_column = input_array[:, col].astype(float)
                decrypted_column = _dec_1darray_discrete(encrypted_column) if discrete else _dec_1darray(encrypted_column)
                decrypted_data_tmp.append(decrypted_column)
                decrypted_data = list(map(list, zip(*decrypted_data_tmp))) # 转置            
        else:
            decrypted_data = []
            for row in input_array:
                encrypted_row = row.astype(float)
                decrypted_row = _dec_1darray_discrete(encrypted_row) if discrete else _dec_1darray(encrypted_row)
                decrypted_data.append(decrypted_row)
        return np.array(decrypted_data)
    else:
        raise ValueError("Array parsing above 2 dimensions is not supported for the time being.")