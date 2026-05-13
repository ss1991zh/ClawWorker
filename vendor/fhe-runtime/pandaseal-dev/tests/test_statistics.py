import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()

###################### Test case For CipherDataFrame ######################
# 创建一个 (5, 10) 形状的 DataFrame，包含一些 NaN 值
data = np.random.rand(5, 10) * 10 - 3.
data[2, 3] = np.nan  # 引入一个 NaN 值
data[4, 7] = np.nan  # 引入另一个 NaN 值
df = pd.DataFrame(data)

cdf = ct.encrypt_df(df)

@pytest.mark.parametrize("axis, skipna", [
    (0, True),
    (1, True),
    (0, False),
    (1, False),
    (None, True),
    (None, False),
])
def test_cipher_dataframe_mean(axis, skipna):
    exceptres = df.mean(axis=axis, skipna=skipna)
    result = cdf.mean(axis=axis, skipna=skipna)
    if isinstance(result, ps.CipherSeries):
        result = ct.decrypt_df(result)
    else:
        result = ct.decrypt(result)

    if isinstance(exceptres, pd.Series):
        pd.testing.assert_series_equal(result, exceptres)
    else:
        np.testing.assert_almost_equal(result, exceptres)
    
@pytest.mark.parametrize("axis, skipna", [
    (0, True),
    (1, True),
    (0, False),
    (1, False),
])
def test_cipher_dataframe_std(axis, skipna):
    exceptres = df.std(axis=axis, skipna=skipna)
    result = ct.decrypt_df(cdf.std(axis=axis, skipna=skipna))

    pd.testing.assert_series_equal(result, exceptres)

@pytest.mark.parametrize("axis, skipna", [
    (0, True),
    (1, True),
    (0, False),
    (1, False),
])
def test_cipher_dataframe_var(axis, skipna):
    exceptres = df.var(axis=axis, skipna=skipna)
    result = ct.decrypt_df(cdf.var(axis=axis, skipna=skipna))

    pd.testing.assert_series_equal(result, exceptres)

@pytest.mark.parametrize("axis, skipna", [
    (0, True),
    (1, True),
    (0, False),
    (1, False),
    (None, True),
    (None, False),
])
def test_cipher_dataframe_max(axis, skipna):
    exceptres = df.max(axis=axis, skipna=skipna)
    result = cdf.max(axis=axis, skipna=skipna)
    if isinstance(result, ps.CipherSeries):
        result = ct.decrypt_df(result)
    else:
        result = ct.decrypt(result)
    if isinstance(exceptres, pd.Series):
        pd.testing.assert_series_equal(result, exceptres)
    else:
        np.testing.assert_almost_equal(result, exceptres)

@pytest.mark.parametrize("axis, skipna", [
    (0, True),
    (1, True),
    (0, False),
    (1, False),
    (None, True),
    (None, False),
])
def test_cipher_dataframe_min(axis, skipna):
    exceptres = df.min(axis=axis, skipna=skipna)
    result = cdf.min(axis=axis, skipna=skipna)
    if isinstance(result, ps.CipherSeries):
        result = ct.decrypt_df(result)
    else:
        result = ct.decrypt(result)

    if isinstance(exceptres, pd.Series):
        pd.testing.assert_series_equal(result, exceptres)
    else:
        np.testing.assert_almost_equal(result, exceptres)

data_nonull = np.random.rand(5, 10) * 10 - 3.
df_nonull = pd.DataFrame(data_nonull)
cdf_nonull = ct.encrypt_df(df_nonull)

@pytest.mark.parametrize("q, axis", [
    # q 为标量，axis=0
    (0.5, 0),
    # q 为标量，axis=1
    (0.25, 1),
    # q 为列表，axis=0
    ([0.1, 0.5, 0.9], 0),
    # q 为列表，axis=1
    ([0.2, 0.8], 1),
])
def test_cipher_dataframe_quantile(q, axis):
    expectres = df_nonull.quantile(q, axis=axis)
    result = cdf_nonull.quantile(q, axis=axis)
    result_decrypted = ct.decrypt_df(result)
    # 验证解密后的结果与明文DataFrame的结果是否一致
    if isinstance(expectres, pd.DataFrame):
        pd.testing.assert_frame_equal(result_decrypted, expectres)
    else:
        pd.testing.assert_series_equal(result_decrypted, expectres)

def test_cipher_dataframe_cov():
    expectres = df_nonull.cov()
    result = ct.decrypt_df(cdf_nonull.cov())
    pd.testing.assert_frame_equal(result, expectres)

data_df_ptc = np.random.rand(5, 10) * 10 + 1 # 避免除数为0
df_ptc = pd.DataFrame(data_df_ptc)
cdf_ptc = ct.encrypt_df(df_ptc)

@pytest.mark.parametrize("periods", [
    1,   # 默认周期
    2,   # 两期变化率
    -1,  # 逆向变化率
    3,   # 超出数据长度的周期
])
def test_cipher_dataframe_pct_change(periods):
    # 明文DataFrame计算百分比变化率
    expected = df_ptc.pct_change(periods=periods)
    
    # CipherDataFrame计算百分比变化率
    result_cipher = cdf_ptc.pct_change(periods=periods)
    # 解密后的结果
    result_decrypted = ct.decrypt_df(result_cipher)
    
    # 验证解密后的结果与明文DataFrame的结果是否一致
    pd.testing.assert_frame_equal(result_decrypted, expected, check_dtype=True)

df = pd.DataFrame({"Col1": [10., 20., 15., 30., 45.],
                   "Col2": [13., 23., 18., 33., 48.],
                   "Col3": [17., 27., 22., 37., 52.]},
                  index=pd.date_range("2020-01-01", "2020-01-05"))

cdf = ct.encrypt_df(df)
fill = 1.0

@pytest.mark.parametrize("periods, freq, fill_value", [
    (3, None, None), (3, None, fill), (3, "D", None)])
def test_cipher_dataframe_shift(periods, freq, fill_value):
    if fill_value is not None:
        cfill = ct.encrypt(fill)
    else:
        cfill = None
    
    expectres = df.shift(periods=periods, freq=freq, fill_value=fill_value)
    result = cdf.shift(periods=periods, freq=freq, fill_value=cfill)
    result_decrypted = ct.decrypt_df(result)
    pd.testing.assert_frame_equal(result_decrypted, expectres)

@pytest.mark.parametrize("axis, skipna", [(0, True), (0, False), (1, True), (1, False)])
def test_cipher_dataframe_cumsum(axis, skipna):
    expectres = df.cumsum(axis=axis, skipna=skipna)
    result = ct.decrypt_df(cdf.cumsum(axis=axis, skipna=skipna))
    pd.testing.assert_frame_equal(result, expectres)    

###################### Test case For CipherSeries ######################
# 创建一个包含 NaN 值的 Series
data = np.random.rand(10) * 10 - 3.
data[3] = np.nan  # 引入一个 NaN 值
data[7] = np.nan  # 引入另一个 NaN 值
series = pd.Series(data)

cseries = ct.encrypt_df(series)

@pytest.mark.parametrize("skipna", [True, False])
def test_cipher_series_mean(skipna):
    exceptres = series.mean(skipna=skipna)
    result = ct.decrypt(cseries.mean(skipna=skipna))

    np.testing.assert_almost_equal(result, exceptres)

@pytest.mark.parametrize("skipna", [True, False])
def test_cipher_series_std(skipna):
    exceptres = series.std(skipna=skipna)
    result = ct.decrypt(cseries.std(skipna=skipna))

    np.testing.assert_almost_equal(result, exceptres)

@pytest.mark.parametrize("skipna", [True, False])
def test_cipher_series_var(skipna):
    exceptres = series.var(skipna=skipna)
    result = ct.decrypt(cseries.var(skipna=skipna))

    np.testing.assert_almost_equal(result, exceptres)

data_quantile_series = np.random.rand(10) * 10 - 3.
series_quantile = pd.Series(data_quantile_series)
cseries_quantile = ct.encrypt_df(series_quantile)

@pytest.mark.parametrize("q", [0.5, 0.25, 0.1, 0.9, [0.1, 0.5, 0.9]])
def test_cipher_series_quantile(q):
    expectres = series_quantile.quantile(q)
    result = cseries_quantile.quantile(q)
    if isinstance(result, ps.CipherSeries):
        result_decrypted = ct.decrypt_df(result)
    else:
        result_decrypted = ct.decrypt(result)
    # 验证解密后的结果与明文Series的结果是否一致
    if isinstance(expectres, pd.Series):
        pd.testing.assert_series_equal(result_decrypted, expectres)
    else:
        np.testing.assert_almost_equal(result_decrypted, expectres)

data_nonull_series = np.random.rand(10) * 10 - 3.
series_nonull = pd.Series(data_nonull_series)
cseries_nonull = ct.encrypt_df(series_nonull)
other = np.random.rand(10) * 10 - 3.
other_series = pd.Series(other)
cother_series = ct.encrypt_df(other_series)

def test_cipher_series_cov():
    expectres = series_nonull.cov(other_series)
    print(expectres)
    result = ct.decrypt(cseries_nonull.cov(cother_series))
    print(result)
    np.testing.assert_almost_equal(result, expectres)

data_series_pct = np.random.rand(10) * 10 + 1
series_pct = pd.Series(data_series_pct)
cseries_pct = ct.encrypt_df(series_pct)

@pytest.mark.parametrize("periods", [
    1,   # 默认周期
    2,   # 两期变化率
    -1,  # 逆向变化率
    5,   # 超出数据长度的周期
])
def test_cipher_series_pct_change(periods):
    # 明文Series计算百分比变化率
    expected = series_pct.pct_change(periods=periods)
    
    # CipherSeries计算百分比变化率
    result_cipher = cseries_pct.pct_change(periods=periods)
    
    # 解密后的结果
    result_decrypted = ct.decrypt_df(result_cipher)
    
    # 验证解密后的结果与明文Series的结果是否一致
    pd.testing.assert_series_equal(result_decrypted, expected)


series_shift = pd.Series([10., 20., 15., 30., 45.], index=pd.date_range("2020-01-01", "2020-01-05"))
cseries_shift = ct.encrypt_df(series_shift)


@pytest.mark.parametrize("periods, freq, fill_value", [
    (3, None, None), (3, None, fill), (3, "D", None)])
def test_cipher_series_shift(periods, freq, fill_value):
    if fill_value is not None:
        cfill = ct.encrypt(fill)
    else:
        cfill = None   

    expectres = series_shift.shift(periods=periods, freq=freq, fill_value=fill_value)
    result = cseries_shift.shift(periods=periods, freq=freq, fill_value=cfill)
    result_decrypted = ct.decrypt_df(result)
    pd.testing.assert_series_equal(result_decrypted, expectres)

@pytest.mark.parametrize("skipna", [True, False])
def test_cipher_series_cumsum(skipna):
    expectres = series.cumsum(skipna=skipna)
    result = ct.decrypt_df(cseries.cumsum(skipna=skipna))
    pd.testing.assert_series_equal(result, expectres)