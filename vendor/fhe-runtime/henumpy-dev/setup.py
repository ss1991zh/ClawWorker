from setuptools import setup, find_packages

VERSION = '2.1.1'

# 读取 build_requirements.txt 文件并提取依赖项
with open('build_requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='henumpy',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True ,
    options={'install': {'force': True}},
    install_requires=requirements,
    python_requires='>=3.11',
    author='TongTaiTech',
    author_email='wuxiteam@tongtaitech.com',
    description='A custom NumPy-like package for fully homomorphic encrypted computation.',
    url='http://10.11.0.105:3000/XGT3/henumpy',
)
