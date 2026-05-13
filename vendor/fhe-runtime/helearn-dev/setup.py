import os
import subprocess
from setuptools import setup, find_packages

VERSION = '0.2'

# 判断操作系统平台
if os.name == 'posix':  # 针对类 Unix 系统（Linux、macOS）
    script_path = './env_check.sh'  
    try:
        subprocess.run(['bash', script_path], check=True)  # 使用bash执行.sh脚本
        print("Successfully executed sh script")
    except subprocess.CalledProcessError as e:
        print(f"Error executing sh script: {e}")

elif os.name == 'nt':  # 针对 Windows 系统
    script_path = '.\env_check.bat'  
    try:
        subprocess.run(['cmd.exe', '/c', script_path], check=True)  # 使用cmd执行.bat脚本
        print("Successfully executed bat script")
    except subprocess.CalledProcessError as e:
        print(f"Error executing bat script: {e}")

else:
    print("Unsupported platform")

# 读取 build_requirements.txt 文件并提取依赖项
with open('build_requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='helearn',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True ,
    install_requires=requirements,
    python_requires='>=3.11',
    author='TongTaiTech',
    author_email='wuxiteam@tongtaitech.com',
    description='A custom Sklearn-like package for fully homomorphic encrypted computation.',
    url='http://10.11.0.105:3000/XGT3/helearn',
)
