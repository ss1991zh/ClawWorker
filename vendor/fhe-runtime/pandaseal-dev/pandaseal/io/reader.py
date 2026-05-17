import pandas as pd
import numpy as np
from pandaseal.core.cipherframe import CipherDataFrame
from pandaseal.core.cipherseries import CipherSeries


__all__ = ['read_excel', 'read_csv', 'read_json']

def read_excel(path, sheet_name=0, header=0, index_col=None):
    """
    Read an excel file and return a CipherDataFrame object.

    Parameters
    -----------
    path : str
        Path to the excel file.
    sheet_name : str
        Name of the sheet to read.
    header : int, default None
        Row number for the header. If None, the first row will be used as header.
    index_col : int, default None
        Column number for the index. If None, the first column will be used as index.

    """

    if header is None or header == 0:
        pass
    else:
        raise NotImplementedError("Currently, you can only specify a table header as None or 0.")
    
    if index_col is None or index_col == 0:
        pass
    else:
        raise NotImplementedError("Currently, you can only specify an index column as None or 0.")

    # 1. read as string
    # 2. convert to float
    df = pd.read_excel(path, sheet_name=sheet_name, header=header, index_col=index_col, dtype=str)
    df = df.astype(np.float64)

    # index is None, so do not need to split index
    if index_col is None:
        data = df.to_numpy()
        return CipherDataFrame(data=data, columns=df.columns)
    # split index, preserve original index
    else:
        index_list = df.index[2:]
        return CipherDataFrame(data=df.to_numpy(), index=index_list, columns=df.columns)
        

def read_csv(path, header=0):
    """
    Read a csv file and return a CipherDataFrame or CipherSeries object.

    Parameters
    ----------
    path : str
        Path to the csv file.
    header : int, default None
        Row number for the header. If None, the first row will be used as header.

    """

    if header is None or header == 0:
        pass
    else:
        raise NotImplementedError("Currently, you can only specify a table header as None or 0.")

    df = pd.read_csv(path, header=header, dtype=str)
    df = df.astype(np.float64)
    return CipherDataFrame(data=df.to_numpy(), columns=df.columns)

def read_json(path, typ='frame'):
    """
    Read a json file and return a CipherDataFrame or CipherSeries object.

    Parameters
    -----------
    path : str
        Path to the json file.
    typ : str, {'frame', 'series'}, default 'frame'
        The type of object to recover.

    """

    if typ == 'frame':
        df = pd.read_json(path, dtype=str)
        df = df.astype(np.float64)
        return CipherDataFrame(data=df.to_numpy(), index=df.index[2:], columns=df.columns)
    elif typ == 'series':
        series = pd.read_json(path, typ=typ, dtype=str)
        series = series.astype(np.float64)
        return CipherSeries(data=series.to_numpy(), index=series.index[2:])
    else:
        raise ValueError("typ must be 'frame' or 'series'.")




