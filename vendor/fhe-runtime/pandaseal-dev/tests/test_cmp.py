import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()

###################### Test case For CipherDataFrame ######################

df_left = pd.DataFrame({
    'A': [1.0, 2.0, 3.0],
    'B': [4.0, 5.0, 6.0],
    'C': [7.0, 8.0, 9.0]
}, index=['a', 'b', 'c'])

cdf_left = ct.encrypt_df(df_left)

right = [1.0, np.array([1.0, 2.0, 3.0]),
         pd.Series([1.0, 2.0, 3.0], index=['a', 'b', 'c']),
         pd.Series([1.0, 2.0, 3.0], index=['a', 'b', 'c']),
         pd.Series([1.0, 2.0, 3.0], index=['a', 'b', 'd']),
         pd.DataFrame({
        'A': [1.0, 2.0, 3.0],
        'B': [4.0, 5.0, 6.0],
        'D': [7.0, 8.0, 9.0]}, index=['a', 'b', 'd']),
        pd.Series([1.0, 2.0, 3.0], index=['a', 'b', 'c']),
        pd.Series([1.0, 2.0, 3.0], index=['A', 'B', 'C'])]

@pytest.mark.parametrize("right_operand, axis", [
    # 1. 标量与 DataFrame 比较，默认 axis=None
    (right[0], "columns"),
    
    # 2. 列表与 DataFrame 比较，默认 axis=None
    (right[1], "columns"),
    
    # 3. Series 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[2], "columns"),
    
    # 4. Series 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[3], "columns"),
    
    # 5. DataFrame 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[4], "columns"),
    
    # 6. DataFrame 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[5], "columns"),
    
    # 7. 使用 axis=0（按行比较）
    (right[6], 0),
    
    # 8. 使用 axis=1（按列比较）
    (right[7], 1),
])
def test_dataframe_eq_with_axis(right_operand, axis):
    expected = df_left.eq(right_operand, axis=axis)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left.eq(c_right, axis=axis)
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize("right_operand, axis", [
    # 1. 标量与 DataFrame 比较，默认 axis=None
    (right[0], "columns"),
    
    # 2. 列表与 DataFrame 比较，默认 axis=None
    (right[1], "columns"),
    
    # 3. Series 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[2], "columns"),
    
    # 4. Series 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[3], "columns"),
    
    # 5. DataFrame 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[4], "columns"),
    
    # 6. DataFrame 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[5], "columns"),
    
    # 7. 使用 axis=0（按行比较）
    (right[6], 0),
    
    # 8. 使用 axis=1（按列比较）
    (right[7], 1),
])
def test_dataframe_ne_with_axis(right_operand, axis):
    expected = df_left.ne(right_operand, axis=axis)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left.ne(c_right, axis=axis)
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand, axis", [
    # 1. 标量与 DataFrame 比较，默认 axis=None
    (right[0], "columns"),
    
    # 2. 列表与 DataFrame 比较，默认 axis=None
    (right[1], "columns"),
    
    # 3. Series 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[2], "columns"),
    
    # 4. Series 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[3], "columns"),
    
    # 5. DataFrame 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[4], "columns"),
    
    # 6. DataFrame 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[5], "columns"),
    
    # 7. 使用 axis=0（按行比较）
    (right[6], 0),
    
    # 8. 使用 axis=1（按列比较）
    (right[7], 1),
])
def test_dataframe_gt_with_axis(right_operand, axis):
    expected = df_left.gt(right_operand, axis=axis)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left.gt(c_right, axis=axis)
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand, axis", [
    # 1. 标量与 DataFrame 比较，默认 axis=None
    (right[0], "columns"),
    
    # 2. 列表与 DataFrame 比较，默认 axis=None
    (right[1], "columns"),
    
    # 3. Series 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[2], "columns"),
    
    # 4. Series 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[3], "columns"),
    
    # 5. DataFrame 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[4], "columns"),
    
    # 6. DataFrame 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[5], "columns"),
    
    # 7. 使用 axis=0（按行比较）
    (right[6], 0),
    
    # 8. 使用 axis=1（按列比较）
    (right[7], 1),
])
def test_dataframe_ge_with_axis(right_operand, axis):
    expected = df_left.ge(right_operand, axis=axis)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left.ge(c_right, axis=axis)
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand, axis", [
    # 1. 标量与 DataFrame 比较，默认 axis=None
    (right[0], "columns"),
    
    # 2. 列表与 DataFrame 比较，默认 axis=None
    (right[1], "columns"),
    
    # 3. Series 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[2], "columns"),
    
    # 4. Series 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[3], "columns"),
    
    # 5. DataFrame 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[4], "columns"),
    
    # 6. DataFrame 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[5], "columns"),
    
    # 7. 使用 axis=0（按行比较）
    (right[6], 0),
    
    # 8. 使用 axis=1（按列比较）
    (right[7], 1),
])
def test_dataframe_lt_with_axis(right_operand, axis):
    expected = df_left.lt(right_operand, axis=axis)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left.lt(c_right, axis=axis)
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand, axis", [
    # 1. 标量与 DataFrame 比较，默认 axis=None
    (right[0], "columns"),
    
    # 2. 列表与 DataFrame 比较，默认 axis=None
    (right[1], "columns"),
    
    # 3. Series 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[2], "columns"),
    
    # 4. Series 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[3], "columns"),
    
    # 5. DataFrame 与 DataFrame 比较（索引对齐），默认 axis=None
    (right[4], "columns"),
    
    # 6. DataFrame 与 DataFrame 比较（索引不对齐），默认 axis=None
    (right[5], "columns"),
    
    # 7. 使用 axis=0（按行比较）
    (right[6], 0),
    
    # 8. 使用 axis=1（按列比较）
    (right[7], 1),
])
def test_dataframe_le_with_axis(right_operand, axis):
    expected = df_left.le(right_operand, axis=axis)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left.le(c_right, axis=axis)
    pd.testing.assert_frame_equal(result, expected)

###################### Test case For Override operator ######################

right = [
    1.0, np.array([1.0, 2.0, 3.0]),
    pd.DataFrame({
    'A': [1.0, 2.0, 3.0],
    'B': [4.0, 5.0, 6.0],
    'C': [7.0, 8.0, 9.0]}, index=['a', 'b', 'c']),
    pd.Series([1.0, 2.0, 3.0], index=['A', 'B', 'C'])
    ]

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2]), (right[3])])
def test_dataframe_eq_with_override(right_operand):
    expected = df_left == right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left == c_right
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2]), (right[3])])
def test_dataframe_ne_with_override(right_operand):
    expected = df_left != right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left != c_right
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2]), (right[3])])
def test_dataframe_gt_with_override(right_operand):
    expected = df_left > right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left > c_right
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2]), (right[3])])
def test_dataframe_ge_with_override(right_operand):
    expected = df_left >= right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left >= c_right
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2]), (right[3])])
def test_dataframe_lt_with_override(right_operand):
    expected = df_left < right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left < c_right
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2]), (right[3])])
def test_dataframe_le_with_override(right_operand):
    expected = df_left <= right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = cdf_left <= c_right
    pd.testing.assert_frame_equal(result, expected)


###################### Test case For CipherSeries ######################

s_left = pd.Series([1.0, 2.0, 3.0, 4.0], index=['a', 'b', 'c', 'd'])

ca_left = ct.encrypt_df(s_left)

right = [1.0, np.array([0.99, 2.0, 3.11, 9.0]),
         pd.Series([0.99, 2.0, 3.11, 9.0], index=['a', 'b', 'c', 'd']),
         ]

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_eq(right_operand):
    expected = s_left.eq(right_operand)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left.eq(c_right)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_ne(right_operand):
    expected = s_left.ne(right_operand)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left.ne(c_right)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_gt(right_operand):
    expected = s_left.gt(right_operand)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left.gt(c_right)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_ge(right_operand):
    expected = s_left.ge(right_operand)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left.ge(c_right)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_lt(right_operand):
    expected = s_left.lt(right_operand)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left.lt(c_right)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_le(right_operand):
    expected = s_left.le(right_operand)
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left.le(c_right)
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_eq_with_override(right_operand):
    expected = s_left == right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left == c_right
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_ne_with_override(right_operand):
    expected = s_left != right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left != c_right
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_gt_with_override(right_operand):
    expected = s_left > right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left > c_right
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_ge_with_override(right_operand):
    expected = s_left >= right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left >= c_right
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_lt_with_override(right_operand):
    expected = s_left < right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left < c_right
    pd.testing.assert_series_equal(result, expected)

@pytest.mark.parametrize("right_operand", [(right[0]), (right[1]), (right[2])])
def test_series_le_with_override(right_operand):
    expected = s_left <= right_operand
    if isinstance(right_operand, (float, np.ndarray)):
        c_right = ct.encrypt(right_operand)
    else:
        c_right = ct.encrypt_df(right_operand)
    result = ca_left <= c_right
    pd.testing.assert_series_equal(result, expected)

