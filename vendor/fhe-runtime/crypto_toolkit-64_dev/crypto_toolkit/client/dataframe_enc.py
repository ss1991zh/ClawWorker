from .base import _enc_1darray, _enc_2darray, _dec_1darray, _dec_2darray


def _encrypt_series(series):
    
    if 'ps' not in dir():
        import pandaseal as ps

    array = series.to_numpy()
    if len(array) == 0:
        return ps.CipherSeries(name=series.name)
    c = _enc_1darray(array)
    return ps.CipherSeries(c, series.index, name=series.name)


def _encrypt_dataframe(df):
    
    if 'ps' not in dir():
        import pandaseal as ps
    
    if df.empty:
        if len(df.index) == 0:
            idx = None
        else:
            idx = df.index
        if len(df.columns) == 0:
            cols = None
        else:
            cols = df.columns
        return ps.CipherDataFrame(index=idx, columns=cols)

    columns = df.columns
    index = df.index
    data = df.to_numpy().T
    c = _enc_2darray(data).T
    return ps.CipherDataFrame(c, index, columns)


def encrypt_df(df):
    if 'pd' not in dir():
        import pandas as pd

    if isinstance(df, pd.Series):
        return _encrypt_series(df)
    elif isinstance(df, pd.DataFrame):
        return _encrypt_dataframe(df)
    else:
        raise TypeError(f"Invalid input type. Expected pandas.Series or pandas.DataFrame. but got {type(df)}.")


def decrypt_df(cdf):

    import pandaseal as ps
    import pandas as pd
    import numpy as np

    if isinstance(cdf, ps.CipherSeries):
        if len(cdf.series_A) == 0:
            return pd.Series(name=cdf.series_A.name)
        plain = _dec_1darray(cdf.to_cipherarray().get_base_array())
        return pd.Series(plain, index=cdf.series_A.index, name=cdf.series_A.name)
    elif isinstance(cdf, ps.CipherDataFrame):
        plain = _dec_2darray(cdf.to_cipherarray().get_base_array().T)
        if isinstance(plain, np.ndarray):
            plain = plain.T

        return pd.DataFrame(plain, index=cdf.dataframe_A.index, columns=cdf.dataframe_A.columns)
    else:
        raise TypeError(f"Invalid input type. Expected CipherSeries or CipherDataFrame. but got {type(cdf)}.")