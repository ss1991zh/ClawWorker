import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()


def test():
    # 空CipherDataFrame的创建以及解密
    empty1 = ps.CipherDataFrame()
    print(ct.decrypt_df(empty1))

    empty2 = ps.CipherDataFrame(index=[1, 2, 3])
    print(ct.decrypt_df(empty2))

    empty3 = ps.CipherDataFrame(columns=['a', 'b', 'c'])
    print(ct.decrypt_df(empty3))

    # 空DataFrame的加密
    empty4 = pd.DataFrame()
    print(ct.encrypt_df(empty4))

    empty5 = pd.DataFrame(index=[1, 2, 3])
    print(ct.encrypt_df(empty5))

    empty6 = pd.DataFrame(columns=['a', 'b', 'c'])
    print(ct.encrypt_df(empty6))

    # 空CipherSeries的创建以及解密
    empty7 = ps.CipherSeries(name='a')
    print(empty7)
    print(ct.decrypt_df(empty7))

    empty8 = pd.Series(name='a') 
    print(ct.encrypt_df(empty8))

