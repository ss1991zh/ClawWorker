#放一些密文csv的IO程序

import numpy as np
from ctypes import *
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path = list(set(sys.path))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from base.base_function import *

# 读取csv文件
def readcsv(path):
    # 读取数据
    data = np.loadtxt(open(path,"rb"),delimiter=",",skiprows=1)
    # 转置数据
    #data = data.T
    return data

# 获取cipherarray中第i个密文
def getCipher(arr, i):
    if i >= arr[4]:
        raise ValueError("The index is out of bounds")
    return np.array([arr[0], arr[1], arr[2], arr[3], arr[i+5]])

