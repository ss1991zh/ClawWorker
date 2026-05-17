import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()


#################################CipherDataFrameGroupBy######################################

df = pd.DataFrame(np.random.rand(10, 5), index=list("AABBCCABCD"))
df.iat[0, 0] = np.nan

cdf = ct.encrypt_df(df)

def test_CipherDataFrameGroupBy_sum():
    res_exception = df.groupby(level=0).sum()
    res_c = cdf.groupby(level=0).sum()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_frame_equal(res_exception, res_plain)

def test_CipherDataFrameGroupBy_std():
    res_exception = df.groupby(level=0).std()
    res_c = cdf.groupby(level=0).std()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_frame_equal(res_exception, res_plain)

def test_CipherDataFrameGroupBy_var():
    res_exception = df.groupby(level=0).var()
    res_c = cdf.groupby(level=0).var()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_frame_equal(res_exception, res_plain)

def test_CipherDataFrameGroupBy_median():
    res_exception = df.groupby(level=0).median()
    res_c = cdf.groupby(level=0).median()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_frame_equal(res_exception, res_plain)

def test_CipherDataFrameGroupBy_mean():
    res_exception = df.groupby(level=0).mean()
    res_c = cdf.groupby(level=0).mean()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_frame_equal(res_exception, res_plain)

def test_CipherDataFrameGroupBy_quantile():
    res_exception = df.groupby(level=0).quantile(0.5)
    res_c = cdf.groupby(level=0).quantile(0.5)
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_frame_equal(res_exception, res_plain)


####################################CipherSeriesGroupBy######################################


s = pd.Series(np.random.rand(10), index=list("AABCCABCDD"), name='salary')

cs = ct.encrypt_df(s)

def test_CipherSeriesGroupBy_sum():
    res_exception = s.groupby(level=0).sum()
    res_c = cs.groupby(level=0).sum()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_series_equal(res_exception, res_plain)

def test_CipherSeriesGroupBy_std():
    res_exception = s.groupby(level=0).std()
    res_c = cs.groupby(level=0).std()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_series_equal(res_exception, res_plain)

def test_CipherSeriesGroupBy_var():
    res_exception = s.groupby(level=0).var()
    res_c = cs.groupby(level=0).var()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_series_equal(res_exception, res_plain)

def test_CipherSeriesGroupBy_median():
    res_exception = s.groupby(level=0).median()
    res_c = cs.groupby(level=0).median()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_series_equal(res_exception, res_plain)

def test_CipherSeriesGroupBy_mean():
    res_exception = s.groupby(level=0).mean()
    res_c = cs.groupby(level=0).mean()
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_series_equal(res_exception, res_plain)

def test_CipherSeriesGroupBy_quantile():
    res_exception = s.groupby(level=0).quantile(0.5)
    res_c = cs.groupby(level=0).quantile(0.5)
    print(res_c)
    res_plain = ct.decrypt_df(res_c)
    pd.testing.assert_series_equal(res_exception, res_plain)