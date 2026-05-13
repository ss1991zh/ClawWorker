from setuptools import setup, find_packages

VERSION = '0.2'

# 读取 build_requirements.txt 文件并提取依赖项
with open('build_requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='crypto_toolkit',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True ,
    install_requires=requirements,
    extras_require={
        "base": [
        ],
        "all": [
            "torch==2.0.1",
            "Pillow",
        ],
        "tensor": [
            "torch==2.0.1",
            "Pillow",
        ],
    },
    python_requires='>=3.11',
    author='TongTaiTech',
    author_email='wuxiteam@tongtaitech.com',
    description='Encryption and decryption tools for HE-Numpy, HE-Learn, and HE-Torch.',
    url='http://10.11.0.105:3000/XGT3/crypto_toolkit',
)
