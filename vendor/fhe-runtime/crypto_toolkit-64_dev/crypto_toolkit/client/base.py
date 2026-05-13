from ctypes import *
import os
import sys
import numpy as np
import platform
import warnings
import weakref
import struct


current_dir = os.path.dirname(os.path.abspath(__file__))
ct_parent_dir = os.path.dirname(current_dir)

# 根据操作系统选择要加载的动态链接库文件
if sys.platform == 'win32':
    # Windows
    dll = CDLL(os.path.join(ct_parent_dir, "./lib/win64_client.dll"))
elif sys.platform == 'linux' or sys.platform == 'linux2':
    # Linux
    dll =  CDLL(os.path.join(ct_parent_dir, "./lib/linux64_client.so"))
elif sys.platform == 'darwin':
    # macOS (Mac OS X)
    s = platform.machine().lower()
    if s == 'amd64' or s == 'x86_64':
        dll =  CDLL(os.path.join(ct_parent_dir, "./lib/macos_amd_client.dylib"))
    else:
        dll =  CDLL(os.path.join(ct_parent_dir, "./lib/macos_arm_client.dylib"))
else:
    print("Unsupported operating system")
    sys.exit(1)


def get_func_name(search_func_name):
    res_func = getattr(dll, search_func_name)
    return res_func


# go切片
class GoString(Structure):
   _fields_ = [("p", c_char_p), ("n", c_longlong)]


# python字符串转go切片
def to_go_string(file: str):
   b_file = file.encode('utf-8')
   return GoString(c_char_p(b_file), c_longlong(len(b_file)))


def initSK(skFilePath=os.path.join(ct_parent_dir, "./file/skf")):
    if not os.path.exists(skFilePath):
        raise ValueError("File does not exist.")
    else:
        init_func = get_func_name("_init_sk")
        init_func.argtypes = [GoString]
        init_func.restype = None
        init_func(to_go_string(skFilePath))


def free_double_ptr(ptr):
    """
    释放double指针指向的内存
    """
    func = get_func_name("FreeDoublePtr")
    func.argtype = POINTER(c_double)
    func.restype = None
    func(ptr)
    return

def free_int_ptr(ptr):
    """
    释放int指针指向的内存
    """ 
    func = get_func_name("FreeIntPtr")
    func.argtype = POINTER(c_int)
    func.restype = None
    func(ptr)
    return

def free_bool_ptr(ptr):
    """
    释放bool指针指向的内存
    """ 
    func = get_func_name("FreeBoolPtr")
    func.argtype = POINTER(c_bool)
    func.restype = None
    func(ptr)
    return

# 单值加密方法
def _enc_scalar(c):
    if 'hp' not in dir():
        import henumpy as hp
    # 类型转换
    c = np.array(c)
    c_double_array = (c_double)(c)

    # 调用go函数
    enc_func = get_func_name("Encode")
    enc_func.argtypes = [c_double]
    enc_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = enc_func(c_double_array)
    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return hp.CipherArray(res)


# 数组加密方法
def _enc_1darray(c):
    if 'hp' not in dir():
        import henumpy as hp    
    # 类型转换
    c_double_array = (c_double * len(c))(*c)

    # 调用go函数
    enc_func = get_func_name("EncodeArray")
    enc_func.argtypes = [POINTER(c_double), c_int]
    enc_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = enc_func(c_double_array, c_int(len(c)))
    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c)+2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return hp.CipherArray(res)


# 离散数组加密方法
def _enc_1darray_discrete(c):
    if 'hp' not in dir():
        import henumpy as hp
    # 类型转换
    c_double_array = (c_double * len(c))(*c)

    # 调用go函数
    enc_func = get_func_name("EncodeDiscreteArray")
    enc_func.argtypes = [POINTER(c_double), c_int]
    enc_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = enc_func(c_double_array, c_int(len(c)))
    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c)*2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return hp.CipherArray(res, discrete=True)


# 单值解密方法
def _dec_scalar(c):

    # 类型转换
    c_double_array = (c_double * len(c))(*c)

    # 调用go函数
    dec_func = get_func_name("Decode")
    dec_func.argtypes = [POINTER(c_double), c_int]
    dec_func.restype = c_double

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = dec_func(c_double_array, c_int(len(c)))

    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(1,))

    return res


# 数组解密方法
def _dec_1darray(c):
    # 检查是否为空数组
    if int(c[1]) == 0 and c[2] == 0.0:
        return np.array([np.NaN])
    # 类型转换
    c1_double_array = (c_double * len(c))(*c)

    # 调用go函数
    dec_func = get_func_name("DecodeArray")
    dec_func.argtypes = [POINTER(c_double), c_int]
    dec_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = dec_func(c1_double_array, c_int(len(c)))

    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c)-2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return res


# 离散数组解密方法
def _dec_1darray_discrete(c):
    # 类型转换
    c_double_array = (c_double * len(c))(*c)

    # 调用go函数
    dec_func = get_func_name("DecodeDiscreteArray")
    dec_func.argtypes = [POINTER(c_double), c_int]
    dec_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = dec_func(c_double_array, c_int(len(c)))

    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c)//2,))

    return res


def _enc_2darray(arr:np.ndarray):
    row = arr.shape[0]
    col = arr.shape[1]

    data = arr.reshape(-1,)
    data_cdouble = (c_double * len(data))(*data)

    func = get_func_name("Encode2DArray")
    func.argtypes = [POINTER(c_double), c_int, c_int]
    func.restype = POINTER(c_double)

    res_ptr = func(data_cdouble, c_int(row), c_int(col))
    res = np.ctypeslib.as_array(res_ptr, shape=(row, col + 2))
    return res


def _dec_2darray(arr:np.ndarray):
    # 空密文解密
    if len(arr) > 1 and np.all(arr[1] == 0.0): # 列加密
        return []
    if len(arr[0]) > 1 and np.all(arr[:, 1] == 0.0): # 行加密
        return []
    row = arr.shape[0]
    col = arr.shape[1]

    data = arr.reshape(-1,)
    data_cdouble = (c_double * len(data))(*data)

    func = get_func_name("DecodeCipherFloat2dArray")
    func.argtypes = [POINTER(c_double), c_int, c_int]
    func.restype = POINTER(c_double)

    res_ptr = func(data_cdouble, c_int(row), c_int(col))
    res = np.ctypeslib.as_array(res_ptr, shape=(row, col - 2))
    return res


def _encrypt_tensor(tensor):
    c = tensor.detach().numpy()
    # 类型转换
    c_float_array = (c_float * len(c))(*c)
    # 调用go函数
    enc_func = get_func_name("EncryptFloat32ArrayToCipherFloat")
    enc_func.argtypes = [POINTER(c_float), c_longlong]
    enc_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = enc_func(c_float_array, c_longlong(len(c)))
    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c) * 2,))

    return res


def _decrypt_tensor(tensor):
    c = tensor
    # 类型转换
    c_float_array = (c_double * len(c))(*c)
    
    # 调用go函数
    dec_func = get_func_name("DecryptCipherFloatToFloat32Array")
    dec_func.argtypes = [POINTER(c_double), c_longlong]
    dec_func.restype = POINTER(c_float)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = dec_func(c_float_array, c_longlong(len(c)))
    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(len(c)//2,))
    return res

##### 针对HENumpy2的加解密方法 #####

def _encrypt_scalar2(scalar):
    # 类型转换
    c = np.array(scalar, dtype=np.float64)
    c_double_array = (c_double)(scalar)

    # 调用go函数
    enc_func = get_func_name("Encode")
    enc_func.argtypes = [c_double]
    enc_func.restype = POINTER(c_double)

    # 将数组传递给C函数，并获取返回的指针
    res_ptr = enc_func(c_double_array)
    # 获取指针指向的数据内容并返回
    res = np.ctypeslib.as_array(res_ptr, shape=(2,))
    return res

def _encrypt_ndarray(input_array : np.ndarray):
    data = input_array.reshape(-1,)
    c_double_array = (c_double * len(data))(*data)
    enc_func = get_func_name("EncodeDiscreteArray")
    enc_func.argtypes = [POINTER(c_double), c_int]
    enc_func.restype = POINTER(c_double)
    res_ptr = enc_func(c_double_array, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data)*2,))
    return res


def _decrypt_ndarray(input_array : np.ndarray):
    data = input_array.reshape(-1,)
    c_double_array = (c_double * len(data))(*data)
    dec_func = get_func_name("DecodeDiscreteArray")
    dec_func.argtypes = [POINTER(c_double), c_int]
    dec_func.restype = POINTER(c_double)
    res_ptr = dec_func(c_double_array, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data)//2,))
    return res



#######################################################################
##############加密函数用于各种数据类型，以编码区分########################
#######################################################################


def _encrypt_float(data):
    """
    将data以float的形式加密
    """ 

    func = get_func_name("EncryptDoubleArrayWithCate")
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = POINTER(c_double)

    data = data.reshape(-1,)
    data_ptr = (c_double * len(data))(*data)

    res_ptr = func(data_ptr, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data) * 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return res

def _encrypt_int(data):
    """
    将data以int的形式加密
    """ 

    func = get_func_name("EncryptIntArrayWithCate")
    func.argtypes = [POINTER(c_int), c_int]
    func.restype = POINTER(c_double)
    data = data.reshape(-1,)
    data_ptr = (c_int * len(data))(*data)
    res_ptr = func(data_ptr, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data) * 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return res

def _encrypt_bool(data):
    """
    将data以bool的形式加密
    """ 

    func = get_func_name("EncryptBoolArrayWithCate")
    func.argtypes = [POINTER(c_bool), c_int]
    func.restype = POINTER(c_double)
    data = data.reshape(-1,)
    data_ptr = (c_bool * len(data))(*data)
    res_ptr = func(data_ptr, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data) * 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return res

def _encrypt_str(data):
    """
    将data以str的形式加密
    """ 

    ints = _string_to_int32_array(data)
    # print(ints)
    ints_ptr = (c_int * len(ints))(*ints)

    func = get_func_name("EncryptStringWithCate")
    func.argtypes = [POINTER(c_int), c_int]
    func.restype = POINTER(c_double)
    res_ptr = func(ints_ptr, c_int(len(ints)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data) * 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return res

def _decrypt_float(data):
    """
    将data以float的形式解密
    """

    func = get_func_name("DecryptCipherFloatWithCateFP64")
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = POINTER(c_double)
    data = data.reshape(-1,)
    data_ptr = (c_double * len(data))(*data)
    res_ptr = func(data_ptr, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data) // 2,))
    weakref.finalize(res, free_double_ptr, res_ptr)
    return res

def _decrypt_int(data):
    """
    将data以int的形式解密
    """

    func = get_func_name("DecryptCipherFloatWithCateInt")
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = POINTER(c_int)
    data = data.reshape(-1,)
    data_ptr = (c_double * len(data))(*data)
    res_ptr = func(data_ptr, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data) // 2,))
    weakref.finalize(res, free_int_ptr, res_ptr)
    return res

def _decrypt_bool(data):
    """
    将data以bool的形式解密
    """

    func = get_func_name("DecryptCipherFloatWithCateBool")  
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = POINTER(c_bool)
    data = data.reshape(-1,)
    data_ptr = (c_double * len(data))(*data)
    res_ptr = func(data_ptr, c_int(len(data)))
    res = np.ctypeslib.as_array(res_ptr, shape=(len(data) // 2,))
    weakref.finalize(res, free_bool_ptr, res_ptr)
    return res

def _decrypt_str(data):
    """
    将data以str的形式解密
    """

    func = get_func_name("DecryptCipherFloatWithCateStr")
    func.argtypes = [POINTER(c_double), c_int]
    func.restype = POINTER(c_int)
    data = data.reshape(-1,)
    data_ptr = (c_double * len(data))(*data)
    res = func(data_ptr, c_int(len(data)))
    # 将结果转换为字符串
    res_ = np.ctypeslib.as_array(res, shape=(len(data) // 2,))
    weakref.finalize(res_, free_int_ptr, res)
    res_str = _int32_array_to_string(res_)
    return res_str


def _string_to_int32_array(s):
    """
    将字符串转换为UTF-8编码的int32数组
    返回：numpy.ndarray - 包含字符串UTF-8编码的int32数组
    """
    int32_values = []
    
    # 遍历字符串中的每个字符
    for char in s:
        # 将字符编码为UTF-8字节数组
        utf8_bytes = char.encode('utf-8')
        n = len(utf8_bytes)
        
        # 创建4字节的数组，在前面补0（右对齐）
        uniform_bytes = bytearray(4)
        uniform_bytes[4-n:] = utf8_bytes
        
        # 将4字节数组转换为int32（大端序）
        int32_value = struct.unpack('>i', uniform_bytes)[0]
        int32_values.append(int32_value)
    
    # 直接返回numpy数组
    return np.array(int32_values, dtype=np.int32)


def _int32_array_to_string(int32_array):
    """
    从int32数组还原为字符串
    """
    result = ""
    
    for int32_value in int32_array:
        # 将int32转换为4字节数组（大端序）
        bytes_data = struct.pack('>I', int32_value)
        
        # 找到第一个非零字节的位置
        start = 0
        for i, b in enumerate(bytes_data):
            if b != 0:
                start = i
                break
        
        # 提取实际的UTF-8字节
        utf8_bytes = bytes_data[start:]
        
        # 解码UTF-8字节为字符
        try:
            char = utf8_bytes.decode('utf-8')
            result += char
        except UnicodeDecodeError:
            # 处理无效的UTF-8序列
            pass
    
    return result
