from .dataframe_enc import encrypt_df, decrypt_df


def encrypt_json(input_file, output_file, typ='frame'):
    """
    加密json文件，并将文件保存在output_file中，列加密
    支持加密将pandas对象以默认形式保存的json文件

    参数:
    -----------
    input_file: str
        待加密的json文件路径
    output_file: str
        加密后保存的文件路径
    typ: str
        用于表示输入文件中保存的对象类型，默认为'frame'，即DataFrame，支持'series'，即Series

    """
    
    import pandas as pd

    if typ == 'frame' or typ == 'series':
        df = pd.read_json(input_file, typ=typ)
        cdf = encrypt_df(df)
        cdf.to_json(output_file)
        print("JSON encryption is complete, the output file is located at:\n", output_file)
    else:
        raise ValueError("typ should be either 'frame' or 'series'.")
    

def decrypt_json(input_file, output_file, typ='frame'):
    """
    解密json文件，并将文件保存在output_file中，列解密

    参数:
    -----------
    input_file: str
        待解密的json文件路径
    output_file: str
        解密后保存的文件路径
    typ: str
        用于表示输入文件中保存的对象类型，默认为'frame'，即DataFrame，支持'series'，即Series
    
    """
    import pandaseal as ps

    if typ == 'frame' or typ == 'series':
        cdf = ps.read_json(input_file, typ=typ)
        df = decrypt_df(cdf)
        df.to_json(output_file)
        print("CSV decryption is complete, the output file is located at:\n", output_file)        
    else:
        raise ValueError("typ should be either 'frame' or 'series'.")
