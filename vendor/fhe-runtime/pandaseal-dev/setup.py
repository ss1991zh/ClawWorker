from setuptools import setup, find_packages

VERSION = '1.0.0'

# 读取 build_requirements.txt 文件并提取依赖项
with open('build_requirements.txt') as f:
    requirements = f.read().splitlines()

description = 'A custom Pandas-Like package to support the processing of full homomorphic ciphertext data.'

setup(
    name='pandaseal',
    version=VERSION,
    options={'install': {'force': True}}, 
    description=description,
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.11',
    include_package_data=True, 
    url='https://gitlab.com/phantaverse-tech/ai-product/pandaseal',
    author='TongTaiTech',
    author_email='wuxiteam@tongtaitech.com',
)