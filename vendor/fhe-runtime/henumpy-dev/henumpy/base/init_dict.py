import os
from .base_function import get_func_name, GoString, to_go_string

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
default_dir = os.path.join(parent_dir, "file")

__all__ = ["initDict"]

# 返回指定路径下文件名满足前缀的最新文件完整路径
def _find_latest_file_with_prefix(directory, prefix):
    all_files = os.listdir(directory)
    matching_files = [file for file in all_files if file.startswith(prefix)]
    if not matching_files:
        return None
    latest_file = max(matching_files, key=lambda file: os.path.getmtime(os.path.join(directory, file)))
    return os.path.join(directory, latest_file)

dictDefaultPath = _find_latest_file_with_prefix(default_dir, "dictf")

# 初始化计算字典
def initDict(dictFilePath=dictDefaultPath, 
             userFilePath=os.path.join(default_dir, "user_authorization")):
    #print("dictFilePath: ", dictFilePath)
    if os.path.exists(dictFilePath):
        init_func = get_func_name("init_dict")
        init_func.argtypes = [GoString, GoString]
        init_func.restype = None
        init_func(to_go_string(dictFilePath), to_go_string(userFilePath))
    else:
        raise ValueError("File does not exist.")