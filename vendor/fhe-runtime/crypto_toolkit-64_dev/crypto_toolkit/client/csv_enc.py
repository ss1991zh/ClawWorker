import os
import csv
import numpy as np
from .base import _enc_2darray, _dec_2darray
    

def encrypt_csv(input_file, output_file, encrypt_by_column=True, extract_header=True, batch_size=10000):
    input_file = os.path.normpath(input_file)
    output_file = os.path.normpath(output_file)

    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # 读取表头
        header = next(reader) if extract_header else []
        buffered_data = []

        for i, row in enumerate(reader):
            # 将每行转换为浮点数
            row_values = [float(value) for value in row]
            buffered_data.append(row_values)
            if encrypt_by_column == False:
                # 每处理 batch_size 行数据进行加密并写入
                if (i + 1) % batch_size == 0:
                    # 行加密
                    row_values_array = np.array(buffered_data)  # 将当前批次转换为 NumPy 数组
                    cipher = _enc_2darray(row_values_array)
                    write_mode = 'a' if os.path.exists(output_file) else 'w'

                    with open(output_file, write_mode, newline='') as csv_output:
                        writer = csv.writer(csv_output)
                        if extract_header and write_mode == 'w':
                            header = ["_P", "_L"] + header  # 添加新的列名
                            writer.writerow(header)
                        for row_data in cipher:
                            writer.writerow(row_data)

                    buffered_data = []  # 清空缓冲区

                if (i + 1) % 100000 == 0:
                    print(f'Processed {i + 1} lines')

        if encrypt_by_column == False:
            # 处理剩余的数据
            if buffered_data:
                row_values_array = np.array(buffered_data)
                cipher = _enc_2darray(row_values_array)
                write_mode = 'a' if os.path.exists(output_file) else 'w'

                with open(output_file, write_mode, newline='') as csv_output:
                    writer = csv.writer(csv_output)
                    if extract_header and write_mode == 'w':
                        header = ["_P", "_L"] + header
                        writer.writerow(header)
                    for row_data in cipher:
                        writer.writerow(row_data)

        # 列加密逻辑
        if encrypt_by_column:
            col_value = np.array(buffered_data).T  # 转置以按列处理
            cipher = _enc_2darray(col_value)

            write_mode = 'a' if os.path.exists(output_file) else 'w'

            with open(output_file, write_mode, newline='') as csv_output:
                writer = csv.writer(csv_output)
                if extract_header and write_mode == 'w':
                    writer.writerow(header)
                for col_data in zip(*cipher):
                    writer.writerow(col_data)

    print("CSV encryption is complete, the output file is located at:\n", output_file)


def decrypt_csv(input_file, output_file, decrypt_by_column=True, extract_header=True):
    input_file = os.path.normpath(input_file)
    output_file = os.path.normpath(output_file)
    # 从加密的CSV文件读取数据
    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        encrypted_data = list(reader)

    # 分离表头和数据
    header = encrypted_data[0] if extract_header else []
    encrypted_data = encrypted_data[1:] if extract_header else encrypted_data

    # 如果按行解密，则判断输入文件是否是按行加密的，不然报错
    if not decrypt_by_column and extract_header:
        expected_columns = ["_P", "_L"]
        if header[:2] != expected_columns:
            raise ValueError("The first 2 columns are not as expected, and the file is not encrypted by row!")    
    # 转换数据并解密
    if not encrypted_data:
        print("[REMIND] Input_file is empty.")
        decrypted_data = []
    elif decrypt_by_column:
        c_col = []
        for col in range(len(encrypted_data[0])):
            encrypted_column = [float(row[col]) for row in encrypted_data]
            c_col.append(encrypted_column)
        c_col = np.array(c_col)
        decrypted_data = _dec_2darray(c_col)
    else:
        c_row = []
        for row in encrypted_data:
            encrypted_row = [float(value) for value in row]
            c_row.append(encrypted_row)
        c_row = np.array(c_row)
        decrypted_data = _dec_2darray(c_row)

    # 将解密后的数据按列写入新的CSV文件
    with open(output_file, 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)

        if decrypt_by_column:
            # 写入表头
            if extract_header:
                writer.writerow(header)
            # 写入解密后的数据按列
            for col_data in zip(*decrypted_data):
                writer.writerow(col_data)
        else:
            # 删除前5列名并写入表头
            if extract_header:
                writer.writerow(header[5:]) 
            # 写入解密后的数据按行
            for row_data in decrypted_data:
                writer.writerow(row_data)    
                
    print("csv decryption is complete, the output file is located at:\n", output_file)