# helearn/__init__.py

# 使用相对导入方式来导入子模块
from .base import *
from .linear_model import *
from .metrics import *
from .preprocessing import *
from .tree import *
from .utils import *
from .datasets import *

if __name__ == "__main__":
    print("Info: import success.")
