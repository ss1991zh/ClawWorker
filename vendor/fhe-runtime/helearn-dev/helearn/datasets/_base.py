import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
helearn_parent_dir = os.path.dirname(current_dir)
sys.path = list(set(sys.path))
if helearn_parent_dir not in sys.path:
    sys.path.append(helearn_parent_dir)

from base.base_function import *
from ._block import Block
from helearn.utils.csv_parsers import *
import henumpy as hp

def load_boston(data_type="cipher"):

    if data_type == "cipher":
        train_file_name = "Boston_Train_Cipher.csv"
        test_file_name = "Boston_Test_Cipher.csv"
        path_train_data = os.path.join(helearn_parent_dir, "./datasets/cipher_data/Boston_Train_Cipher.csv")
        path_test_data = os.path.join(helearn_parent_dir, "./datasets/cipher_data/Boston_Test_Cipher.csv")
        data_train = hp.CipherArray(readcsv(path_train_data))
        data_test = hp.CipherArray(readcsv(path_test_data))

        # 如果输入数据为行加密则转为列加密
        if data_train.get_encryption_type == 0:
            data_train = data_train.transEncType()
        if data_test.get_encryption_type() == 0:
            data_test = data_test.transEncType()

        train_data = data_train[:,:data_train.cipherShape()[1]-1]
        train_target = data_train[:,data_train.cipherShape()[1]-1]
        test_data = data_test[:,:data_test.cipherShape()[1]-1]
        test_target = data_test[:,data_test.cipherShape()[1]-1] 

    elif data_type == "plain":
        train_file_name = "Boston_Train.csv"
        test_file_name = "Boston_Test.csv"
        path_train_data = os.path.join(helearn_parent_dir, "./datasets/plain_data/Boston_Train.csv")
        path_test_data = os.path.join(helearn_parent_dir, "./datasets/plain_data/Boston_Test.csv")

        train = np.loadtxt(path_train_data, dtype=float, delimiter=',', skiprows=1)
        test = np.loadtxt(path_test_data, dtype=float, delimiter=',', skiprows=1)

        train_data = train[:,:len(train[0])-1]
        train_target = train[:,len(train[0])-1:]
        test_data = test[:,:len(test[0])-1]
        test_target =test[:,len(test[0])-1:]

    else:
        raise ValueError("data type must be 'cipher' or 'plain'.")
    
    # 描述文件路径
    descr_path = os.path.join(helearn_parent_dir, "./datasets/descr/boston.rst")
    with open(descr_path, 'r') as file:
        fdescr = file.read()
    
    feature_names = [
        "CRIM",
        "ZN",
        "INDUS",
        "CHAS",
        "NOX",
        "RM",
        "AGE",
        "DIS",
        "RAD",
        "TAX",
        "PTRATIO",
        "B",
        "LSTAT",
    ]

    target_names = [
        "MEDV",
    ]

    return Block(
        train_data=train_data,
        train_target=train_target,
        test_data=test_data,
        test_target=test_target,
        DESCR=fdescr,
        feature_names=feature_names,
        target_names=target_names,
        train_file_name=train_file_name,
        test_file_name=test_file_name,
    )


def load_diabetes(data_type="cipher"):

    if data_type == "cipher":
        train_file_name = "Diabetes_Train_Cipher.csv"
        test_file_name = "Diabetes_Test_Cipher.csv"
        path_train_data = os.path.join(helearn_parent_dir, "./datasets/cipher_data/Diabetes_Train_Cipher.csv")
        path_test_data = os.path.join(helearn_parent_dir, "./datasets/cipher_data/Diabetes_Test_Cipher.csv")        
        data_train = hp.CipherArray(readcsv(path_train_data))
        data_test = hp.CipherArray(readcsv(path_test_data))

        # 如果输入数据为行加密则转为列加密
        if data_train.get_encryption_type == 0:
            data_train = data_train.transEncType()
        if data_test.get_encryption_type() == 0:
            data_test = data_test.transEncType()

        train_data = data_train[:,:data_train.cipherShape()[1]-1]
        train_target = data_train[:,data_train.cipherShape()[1]-1]
        test_data = data_test[:,:data_test.cipherShape()[1]-1]
        test_target = data_test[:,data_test.cipherShape()[1]-1] 

    elif data_type == "plain":
        train_file_name = "Diabetes_Train.csv"
        test_file_name = "Diabetes_Test.csv"
        path_train_data = os.path.join(helearn_parent_dir, "./datasets/plain_data/Diabetes_Train.csv")
        path_test_data = os.path.join(helearn_parent_dir, "./datasets/plain_data/Diabetes_Test.csv")

        train = np.loadtxt(path_train_data, dtype=float, delimiter=',', skiprows=1)
        test = np.loadtxt(path_test_data, dtype=float, delimiter=',', skiprows=1)

        train_data = train[:,:len(train[0])-1]
        train_target = train[:,len(train[0])-1:]
        test_data = test[:,:len(test[0])-1]
        test_target =test[:,len(test[0])-1:]

    else:
        raise ValueError("data type must be 'cipher' or 'plain'.")
    
    # 描述文件路径
    descr_path = os.path.join(helearn_parent_dir, "./datasets/descr/diabetes.rst")
    with open(descr_path, 'r') as file:
        fdescr = file.read()

    feature_names = [
        "Age",
        "Sex",
        "Body mass index",
        "Average blood pressure",
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",

    ]

    target_names = [
        "target",
    ]
    

    return Block(
        train_data=train_data,
        train_target=train_target,
        test_data=test_data,
        test_target=test_target,
        DESCR=fdescr,
        feature_names=feature_names,
        target_names=target_names,
        train_file_name=train_file_name,
        test_file_name=test_file_name,
    )

def load_breast_cancer(data_type="cipher"):

    if data_type == "cipher":
        train_file_name = "Breast_cancer_Train_Cipher.csv"
        test_file_name = "Breast_cancer_Test_Cipher.csv"
        path_train_data = os.path.join(helearn_parent_dir, "./datasets/cipher_data/Breast_cancer_Train_Cipher.csv")
        path_test_data = os.path.join(helearn_parent_dir, "./datasets/cipher_data/Breast_cancer_Test_Cipher.csv")
        data_train = hp.CipherArray(readcsv(path_train_data))
        data_test = hp.CipherArray(readcsv(path_test_data))

        # 如果输入数据为行加密则转为列加密
        if data_train.get_encryption_type == 0:
            data_train = data_train.transEncType()
        if data_test.get_encryption_type() == 0:
            data_test = data_test.transEncType()

        train_data = data_train[:,:data_train.cipherShape()[1]-1]
        train_target = data_train[:,data_train.cipherShape()[1]-1]
        test_data = data_test[:,:data_test.cipherShape()[1]-1]
        test_target = data_test[:,data_test.cipherShape()[1]-1] 
    
    elif data_type == "plain":
        train_file_name = "Breast_cancer_Train.csv"
        test_file_name = "Breast_cancer_Test.csv"
        path_train_data = os.path.join(helearn_parent_dir, "./datasets/plain_data/Breast_cancer_Train.csv")
        path_test_data = os.path.join(helearn_parent_dir, "./datasets/plain_data/Breast_cancer_Test.csv")

        train = np.loadtxt(path_train_data, dtype=float, delimiter=',', skiprows=1)
        test = np.loadtxt(path_test_data, dtype=float, delimiter=',', skiprows=1)

        train_data = train[:,:len(train[0])-1]
        train_target = train[:,len(train[0])-1:]
        test_data = test[:,:len(test[0])-1]
        test_target =test[:,len(test[0])-1:]

    else:
        raise ValueError("data type must be 'cipher' or 'plain'.")

    # 描述文件路径
    descr_path = os.path.join(helearn_parent_dir, "./datasets/descr/breast_cancer.rst")
    with open(descr_path, 'r') as file:
        fdescr = file.read()
    
    feature_names = [
        'mean radius', 'mean texture',
        'mean perimeter', 'mean area',
        'mean smoothness', 'mean compactness',
        'mean concavity', 'mean concave points',
        'mean symmetry', 'mean fractal dimension',
        'radius error', 'texture error',
        'perimeter error', 'area error',
        'smoothness error', 'compactness error',
        'concavity error', 'concave points error',
        'symmetry error', 'fractal dimension error',
        'worst radius', 'worst texture',
        'worst perimeter', 'worst area',
        'worst smoothness', 'worst compactness',
        'worst concavity', 'worst concave points',
        'worst symmetry', 'worst fractal dimension'

    ]

    target_names = [
        "target",
    ]
    

    return Block(
        train_data=train_data,
        train_target=train_target,
        test_data=test_data,
        test_target=test_target,
        DESCR=fdescr,
        feature_names=feature_names,
        target_names=target_names,
        train_file_name=train_file_name,
        test_file_name=test_file_name,
    )

if __name__ == "__main__":
    boston = load_boston()
    # print(boston.train_data[0])
    print(boston.test_data[0])

    diabetes = load_diabetes()
    print(diabetes.test_data[0])