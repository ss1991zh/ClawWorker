#放一些密文随机函数

import numpy as np
from ctypes import *
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path = list(set(sys.path))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from helearn.base.base_function import *