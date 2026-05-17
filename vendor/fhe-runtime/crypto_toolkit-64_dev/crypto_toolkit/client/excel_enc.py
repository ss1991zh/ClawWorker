import numpy as np
from .dataframe_enc import encrypt_df, decrypt_df

# 加密excel文件，并将文件保存在output_file中 列加密
def encrypt_excel(input_file, output_file, input_sheet_name=0, input_header=0, input_index_col=0, output_sheet_name='Sheet1', output_header=True, output_index_col=True):

    import pandas as pd

    # 检查sheet_name，仅支持单表
    assert type(input_sheet_name) in {int, str}, "input_sheet_name should be either int or str."
    assert type(output_sheet_name) in {int, str}, "output_sheet_name should be either int or str."

    df = pd.read_excel(input_file, sheet_name=input_sheet_name, header=input_header, index_col=input_index_col, dtype=np.float64)
    cdf = encrypt_df(df)
    cdf.to_excel(output_file, sheet_name=output_sheet_name, header=output_header, index=output_index_col)

    print("Excel encryption is complete, the output file is located at:\n", output_file)
    

# 解密excel文件，并将文件保存在output_file中
def decrypt_excel(input_file, output_file, input_sheet_name=0, input_header=0, input_index_col=0, output_sheet_name='Sheet1', output_header=True, output_index_col=True):

    import pandaseal as ps

    cdf = ps.read_excel(input_file, sheet_name=input_sheet_name, header=input_header, index_col=input_index_col)
    plain = decrypt_df(cdf)
    plain.to_excel(output_file, sheet_name=output_sheet_name, header=output_header, index=output_index_col)

    print("Excel decryption is complete, the output file is located at:\n", output_file)