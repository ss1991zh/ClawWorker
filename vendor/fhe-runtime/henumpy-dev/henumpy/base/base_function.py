from ctypes import *
import configparser
import numpy as np
import difflib
import platform

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
henumpy_parent_dir = os.path.dirname(current_dir)

import sys

__all__ = ["get_func_parallelization_config", "cipherLen", "printCipher", "set_parallelization"]

# 根据操作系统选择要加载的动态链接库文件
if sys.platform == 'win32':
    # Windows
    dll = CDLL(os.path.join(henumpy_parent_dir, "./lib/win64_core.dll"))
elif sys.platform == 'linux' or sys.platform == 'linux2':
    # Linux
    dll =  CDLL(os.path.join(henumpy_parent_dir, "./lib/linux64_core.so"))
elif sys.platform == 'darwin':
    # macOS (Mac OS X)
    if platform.machine().lower() == 'x86_64':
        dll =  CDLL(os.path.join(henumpy_parent_dir, "./lib/macos_amd_core.dylib"))
    else:
        dll =  CDLL(os.path.join(henumpy_parent_dir, "./lib/macos_arm_core.dylib"))
else:
    print("Unsupported operating system")
    sys.exit(1)

# 读取函数映射配置文件
config = configparser.ConfigParser()
config.read(os.path.join(henumpy_parent_dir, "./lib/float_mapping.ini"))

# 获取函数映射关系
function_mapping = dict(config.items("FUNCTION_MAPPING"))

# 获取函数名
def get_func_name(search_func_name):
    res_func = getattr(dll, function_mapping[search_func_name])
    return res_func

# 获取函数默认并行配置
parallel_config = dict(config.items("PARALLEL_CONFIG"))

# 获取函数的并行配置
def get_func_parallelization_config(func_name=None):
    if func_name is None:
        return parallel_config
    else:
        s = parallel_config[func_name].lower()
        if s == "true":
            return True
        else:
            return False

def set_parallelization(parallel_strategy=2):
    """
    函数并行策略配置：四种配置模式————全部配置为非并行、全部配置为并行、恢复函数默认并行配置、指定函数配置为并行或非并行.

    参数
    ----------
    parallel_strategy : 整型以及字典类型, 默认值为2.
        值为0全部函数配置为非并行;
        值为1全部函数配置为并行;
        值为2全部函数配置为默认配置;
        值为字典则将字典中指定函数配置为并行或非并行.
    """    
    global parallel_config # 使用全局的parallel_config变量
    if type(parallel_strategy) == int:
        if parallel_strategy == 0:
            for key in parallel_config.keys():
                parallel_config[key] = "False"
        elif parallel_strategy == 1:
            for key in parallel_config.keys():
                parallel_config[key] = "True"
        elif parallel_strategy == 2:
            parallel_config = dict(config.items("PARALLEL_CONFIG"))
        else:
            raise ValueError("When the parameter is an 'int', the value range is [0,1,2].")
    elif type(parallel_strategy) == dict:
        for key in parallel_strategy.keys():
            if type(key) != str:       # 检查键是否为字符类型
                raise ValueError(f"The type of key must be 'str', but '{type(v)}' is given.")
            
            if key in parallel_config: # 配置策略中指定的键存在于配置选项中
                v = parallel_strategy[key]
                if type(v) == bool:    # 检查值是否为合法的字符类型或布尔类型
                    v = "True" if v else "False"
                elif type(v) == str:
                    if v.lower() != "true" and v.lower() == "false":
                        raise ValueError(f"The value range of a character string is ['True', 'False'], but '{v}' is given.")
                    else:pass
                else:
                    raise ValueError(f"The type of the key's value needs to be an 'bool' or 'str', but '{type(v)}' is given.")     
                parallel_config[key] = v
            else: # 配置策略中指定的key不存在于配置选项中
               l = list(parallel_config.keys())
               advicestr = difflib.get_close_matches(key, l) # 找出与输入相近的函数名
               raise ValueError(f"Function parallel configuration options are not included '{key}'.Do you mean : '{advicestr}'?") 
    else:
        raise ValueError(f"The input parameter must be an integer, but '{type(parallel_strategy)}' is given.")     

def free_double_ptr(ptr):

    func = get_func_name("free_memory")
    func.argtype = POINTER(c_double)
    func.restype = None
    func(ptr)

def free_int_ptr(ptr):

    func = get_func_name("free_int_ptr")
    func.argtype = POINTER(c_int)
    func.restype = None
    func(ptr)

def free_bool_ptr(ptr):

    func = get_func_name("free_bool_ptr")
    func.argtype = POINTER(c_bool)
    func.restype = None
    func(ptr)

# go切片
class GoString(Structure):
   _fields_ = [("p", c_char_p), ("n", c_longlong)]

# python字符串转go切片
def to_go_string(file: str):
   b_file = file.encode('utf-8')
   return GoString(c_char_p(b_file), c_longlong(len(b_file)))

# 返回密文数组长度
def cipherLen(cipher_array):
    ndarray = cipher_array.get_base_array()
    if ndarray.shape[0] is not None:
        if cipher_array.ndim == 2:
            if cipher_array.cipher_type == 3:
                max_row = ndarray.shape[0] if cipher_array.encryption_type == 0 else ndarray.shape[0] // 2
            else:
                max_row = ndarray.shape[0] if cipher_array.encryption_type == 0 else ndarray.shape[0] - 2
        elif cipher_array.ndim == 1:
            if cipher_array.cipher_type == 1:
                max_row = ndarray.shape[0] - 1
            elif cipher_array.cipher_type == 2:
                max_row = int(ndarray[1])
            elif cipher_array.cipher_type == 3:
                max_row = ndarray.shape[0] // 2
            else:
                raise ValueError(f"Cipher type error")
        else:
            raise ValueError("Array parsing above 2 dimensions is not supported for the time being.")
    else:
        max_row = 0
    return max_row

# 二维数组密文字符拼接
def _format_2d_array2(array_2d, cipher_type=2, encryption_type=0):
    
    max_int_len = 3
    max_float_len = 17
    # 设置每列的最大字符长度存到max_lengths
    if cipher_type == 2:
        if encryption_type == 0:
            max_lengths = [max_float_len]+[1]+[max_float_len]*(array_2d.shape[1]-2)
        elif encryption_type == 1:
            max_lengths = [max_float_len]*array_2d.shape[1]
        else:
            raise ValueError(f"Encryption type error")
    elif cipher_type == 3:
        max_lengths = []
        if encryption_type == 0:
            max_lengths += [max_float_len, max_float_len] * (array_2d.shape[1] // 2)
        elif encryption_type == 1:
            max_lengths += [max_float_len]*array_2d.shape[1]
        else:
            raise ValueError(f"Encryption type error")
    else:
        raise ValueError(f"Cipher type error")

    result_string = "["
    is_first_row = True
    for row in array_2d:
        result_string += "[" if is_first_row else " ["
        is_first_row =  False
        for val, length in zip(row, max_lengths):
            # 根据每列的最大字符长度对齐并拼接
            if length <= max_int_len:
                formatted_val = str(int(val)).rjust(length)
            else:
                formatted_val = str(val).rjust(length)
            result_string += f"{formatted_val}, "
        # 移除最后一个逗号和空格
        result_string = result_string[:-2]
        result_string += "], \n"

    # 移除最后一个逗号和空格
    result_string = result_string[:-3]
    result_string += "]"

    return result_string

# # 打印numpy密文数组
def printCipher(obj):
    # 元组密文打印
    if type(obj) == tuple:
        res_str = "("
        for item in obj:
            res_str += "CipherArray(" + _cipher_to_str(item) + "), \n"
        res_str = res_str[:-3] + ")"
    else:
        res_str = _cipher_to_str(obj)

    print(res_str)

def _cipher_to_str(cipher_array):
    cipher_type = cipher_array.get_cipher_type()
    encryption_type = cipher_array.get_encryption_type()
    cipher_base_array = cipher_array.get_base_array()
    
    if cipher_type == 1 : # 标量密文
        res_str = "[" + str(cipher_base_array[0]) + ", " + str(cipher_base_array[1]) + "]"

    elif cipher_type == 2: # 数组密文
        if cipher_base_array.ndim == 1: # 一维数组
            num_floats = cipher_base_array[1] 
            # float_values = cipher_base_array[5:int(5+num_floats)]
            if int(cipher_base_array[1]) == 0 and cipher_base_array[2] == 0.0: # 空数组
                float_values = cipher_base_array[2:]
            else:
                float_values = cipher_base_array[2:int(2+num_floats)]
            res_str = "[" + str(cipher_base_array[0]) + ", " + str(int(num_floats)) + ", "
            res_str += ", ".join(map(str, float_values))
            res_str += "]"
        else: # 多维数组
            #np.set_printoptions(linewidth=np.inf, suppress=True, precision=16) # 取消受数组长度限制而进行换行, 取消科学计数法
            #res_str = np.array2string(cipher_base_array, separator=',')
            res_str = _format_2d_array2(cipher_base_array, cipher_type, encryption_type)
        
    elif cipher_type == 3: # 离散数组密文
        if cipher_base_array.ndim == 1: # 一维数组
            res_str = "["
            for i in range (len(cipher_base_array)//2):
                if i > 0:
                    res_str += ", " 
                res_str += str(cipher_base_array[i*2]) + ", " + str(cipher_base_array[i*2+1])
            res_str += "]"
        else: # 多维数组
            #np.set_printoptions(linewidth=np.inf, suppress=True, precision=16) # 取消受数组长度限制而进行换行, 取消科学计数法
            #res_str = np.array2string(cipher_base_array, separator=',')
            res_str = _format_2d_array2(cipher_base_array, cipher_type, encryption_type)

    else:
        raise ValueError("Error: cipher_type is not correct") 

    return res_str   

def CHECK_DISCRETE(c, param_name):
    """
    检查是否是离散密文数组
    """
    if c.get_cipher_type() == 3:
        raise ValueError(f"Unable to handle discrete array-type cipher , please enter array-type cipher.(Param:{param_name})")
    else:
        pass

def CHECK_ARRAY(c, param_name):
    """
    检查是否为1D或2D数组类型
    """
    if c.get_cipher_type() != 2:
        raise ValueError(f"Can only handle 1D or 2D array-type cipher, please enter 1D or 2D array-type cipher.(Param:{param_name})")
    else:
        pass

