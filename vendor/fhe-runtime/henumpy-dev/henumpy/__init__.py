# henumpy/henumpy/__init__.py

# 使用相对导入方式来导入子模块
from .base import *
from .core import *
import difflib

attributes = dir()

def __getattr__(attr):
    if attr == "random":
        from .core import random
        return random 

    advicename = difflib.get_close_matches(attr, attributes)
    raise NameError(f"Module 'henumpy' has no attribute '{attr}'. Do you mean '{advicename}'?")
