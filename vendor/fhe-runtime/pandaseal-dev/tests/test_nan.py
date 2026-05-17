import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()

###################### Test case For CipherDataFrame ######################

df = pd.DataFrame({
        "A": [1., 2., np.nan],
        "B": [4., np.nan, 6.],
        "C": [7., 8., 9.]
    })

cdf = ct.encrypt_df(df)


# 测试用例
@pytest.mark.parametrize("dropna_kwargs", [
    {},  # 默认参数
    {"axis": 0},  # 删除包含 NaN 的行
    {"axis": 1},  # 删除包含 NaN 的列
    {"how": "all"},  # 删除所有元素为 NaN 的行或列
    {"thresh": 2},  # 保留至少有两个非 NaN 值的行或列
    {"subset": ["A", "B"]},  # 仅考虑子集列 ["A", "B"]
])
def test_cipher_dataframe_dropna(dropna_kwargs):

    # 原始 DataFrame 的 dropna 结果
    expected = df.dropna(**dropna_kwargs)

    # CipherDataFrame 的 dropna 结果
    result = ct.decrypt_df(cdf.dropna(**dropna_kwargs))

    # 验证结果是否一致
    pd.testing.assert_frame_equal(result, expected)

df2 = pd.DataFrame({
        "A": [1, np.nan, 3],
        "B": [4, np.nan, 6],
        "C": [7, 8, np.nan]
    })

cdf2 = ct.encrypt_df(df2)

fillna_value = [0.1, {"A": 0.1, "B": 99.}, 
                pd.Series({"A": 0.1, "C": 42}),
                pd.DataFrame({
                "A": [0., 1., 2.],
                "B": [3., 4., 5.],
                "C": [6., 7., 8.]})]

cfillna_value = [ct.encrypt(0.1), {"A": ct.encrypt(0.1), "B": ct.encrypt(99.)},
                 ct.encrypt_df(fillna_value[2]), ct.encrypt_df(fillna_value[3])]

# 测试用例
@pytest.mark.parametrize("index", [
    # 1. 标量填充
    (0),

    # 2. 字典填充（指定列填充）
    (1),

    # 3. Series 填充（按列名对齐）
    (2),

    # 4. DataFrame 填充
    (3),
])
def test_cipher_dataframe_fillna(index):


    # 原始 DataFrame 的 fillna 结果
    expected_result = df2.copy().fillna(fillna_value[index])

    # CipherDataFrame 的 fillna 结果
    result = ct.decrypt_df(cdf2.copy().fillna(cfillna_value[index]))

    # 验证结果是否一致
    pd.testing.assert_frame_equal(result, expected_result)


###################### Test case For CipherSeries ######################

s = pd.Series([1, np.nan, 3], index=["a", "b", "c"])
cs = ct.encrypt_df(s)

fillna_value2 = [0.1, {"a": 0.1, "b": 99.},
                    pd.Series({"a": 0.1, "c": 42})]

cfillna_value2 = [ct.encrypt(0.1), {"a": ct.encrypt(0.1), "b": ct.encrypt(99.)},
                    ct.encrypt_df(fillna_value2[2])]

# 测试用例
@pytest.mark.parametrize("dropna_kwargs", [
    {},  # 默认参数
])
def test_cipher_series_dropna(dropna_kwargs):

    # 原始 Series 的 dropna 结果
    expected = s.dropna(**dropna_kwargs)

    # CipherSeries 的 dropna 结果
    result = ct.decrypt_df(cs.dropna(**dropna_kwargs))

    # 验证结果是否一致
    pd.testing.assert_series_equal(result, expected)


@pytest.mark.parametrize("index", [
    # 1. 标量填充
    (0),

    # 2. 字典填充（指定列填充）
    (1),

    # 3. Series 填充（按列名对齐）
    (2),
])
def test_cipher_series_fillna(index):
    # 原始 Series 的 dropna 结果
    expected = s.copy().fillna(fillna_value2[index])

    # CipherSeries 的 dropna 结果
    result = ct.decrypt_df(cs.copy().fillna(cfillna_value2[index]))

    print(result)
    # 验证结果是否一致
    pd.testing.assert_series_equal(result, expected)