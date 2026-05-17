import numpy as np
import crypto_toolkit as ct

import os
import pkg_resources
package_location = pkg_resources.get_distribution('crypto_toolkit').location

if __name__ == "__main__":
    # 初始化
    ct.initSK()

    a = 5
    A = ct.encrypt(a)
    print("单值加密: \n", A)
    print("单值解密: \n", ct.decrypt(A))

    x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

    X = ct.encrypt(x)
    print("数组行加密: \n", X)
    print("数组行解密: \n", ct.decrypt(X))

    X = ct.encrypt(x, encrypt_by_column=True)
    print("数组列加密: \n", X)
    print("数组列解密: \n", ct.decrypt(X, decrypt_by_column=True))
    
    X = ct.encrypt(x, discrete=True)
    print("离散数组行加密: \n", X)
    print("离散数组行解密: \n", ct.decrypt(X, discrete=True))

    #x = np.array([[1.0], [2.0], [3.0]])
    X = ct.encrypt(x, encrypt_by_column=True, discrete=True)
    print("离散数组列加密: \n", X)
    print("离散数组列解密: \n", ct.decrypt(X, decrypt_by_column=True, discrete=True))

    input_file = os.path.join(package_location, "./crypto_toolkit/file/input.csv")    # 输入CSV文件名
    output_file = os.path.join(package_location, "./crypto_toolkit/file/output.csv")   # 输出加密后的CSV文件名
    ct.encrypt_csv(input_file, output_file, encrypt_by_column=True)

    input_file = os.path.join(package_location, "./crypto_toolkit/file/output.csv")   # 加密的输入CSV文件名
    output_file = os.path.join(package_location, "./crypto_toolkit/file/deinput.csv")   # 解密后的输出CSV文件名
    ct.decrypt_csv(input_file, output_file, decrypt_by_column=True)

    