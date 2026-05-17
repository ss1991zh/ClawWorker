import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()


###################### Test case For CipherDataFrame ######################

# 创建左操作数 DataFrame，数据类型改为 float64
df_left = pd.DataFrame({
    'A': [1.0, 2.0, 3.0],
    'B': [4.0, 5.0, 6.0],
    'C': [7.0, 8.0, 9.0]
}, index=['a', 'b', 'c'])

cdf_left = ct.encrypt_df(df_left)


right = [pd.Series([1.0, 2.0, 3.0], index=['A', 'B', 'C']),
         pd.Series([1.0, 2.0, 3.0], index=['a', 'b', 'c']),
         np.array([1.0, 2.0, 3.0]),
         np.array([1.0, 2.0, 3.0]),
         pd.DataFrame({
        'A': [1.0, 2.0, 3.0],
        'D': [1.0, 2.0, 3.0]
    }, index=['a', 'b', 'c']),
    pd.DataFrame({
        'D': [1.0, 2.0, 3.0],
        'E': [1.0, 2.0, 3.0]
    }, index=['d', 'e', 'f'])]

# add
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 0.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 0.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 0.0)
])
def test_dataframe_addition_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.add(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.add(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)

# sub
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 0.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 0.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 0.0)
])
def test_dataframe_substract_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.sub(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.sub(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)

# mul
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 0.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 0.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 0.0)
])
def test_dataframe_multiply_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.mul(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.mul(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)

# div
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 1.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 1.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 1.0)
])
def test_dataframe_div_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.div(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.div(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)


# radd
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 0.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 0.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 0.0)
])
def test_dataframe_raddition_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.radd(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.radd(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)

# rsub
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 0.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 0.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 0.0)
])
def test_dataframe_rsubstract_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.rsub(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.rsub(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)

# rmul
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 0.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 0.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 0.0)
])
def test_dataframe_rmultiply_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.rmul(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.rmul(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)

# rdiv
@pytest.mark.parametrize("right_operand, axis, fill_value", [
    # 1. 沿着列轴(axis=1)进行加法
    (right[0], 1, None),
    
    # 2. 沿着行轴(axis=0)进行加法
    (right[1], 0, None),
    
    # # 3. 沿着列轴(axis=1)进行加法，使用fill_value
    # (right[2], 1, 1.0),
    
    # # 4. 沿着行轴(axis=0)进行加法，使用fill_value
    # (right[3], 0, 1.0),
    
    # 5. DataFrame加法（索引不对齐，列对齐），没有fill_value
    (right[4], None, None),
    
    # 6. DataFrame加法（索引和列都不对齐），使用fill_value
    (right[5], None, 1.0)
])
def test_dataframe_rdiv_with_axis_and_fill_value(right_operand, axis, fill_value):
    expected = df_left.rdiv(right_operand, axis=axis, fill_value=fill_value)
    if isinstance(right_operand, (pd.DataFrame, pd.Series)):
        cright_operand = ct.encrypt_df(right_operand)
    else:
        cright_operand = ct.encrypt(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cdf_left.rdiv(cright_operand, axis=axis, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_frame_equal(result, expected)


###################### Test case For CipherSeries ######################

series_left = pd.Series([1.0, 2.0, 3.0], index=['a', 'b', 'c'])
cs_left = ct.encrypt_df(series_left)

right = [1.0, np.array([1.0, 1.0, 1.0]),
         pd.Series([1.0, 1.0, 1.0], index=['a', 'b', 'c']),
         pd.Series([1.0, 1.0, 1.0], index=['a', 'b', 'd']),
         pd.Series([1.0, 1.0, 1.0], index=['a', 'b', 'd']),
         pd.Series([1.0, 1.0, 1.0], index=['a', 'b', 'd'])]


# add
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_addition(right_operand, fill_value):
    expected = series_left.add(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.add(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)

# sub
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_substract(right_operand, fill_value):
    expected = series_left.sub(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.sub(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)

# mul
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_multiply(right_operand, fill_value):
    expected = series_left.mul(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.mul(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)

# div
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_multiply(right_operand, fill_value):
    expected = series_left.div(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.div(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)

# radd
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_raddition(right_operand, fill_value):
    expected = series_left.radd(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.radd(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)

# rsub
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_rsubstract(right_operand, fill_value):
    expected = series_left.rsub(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.rsub(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)

# rmul
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_rmultiply(right_operand, fill_value):
    expected = series_left.rmul(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.rmul(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)

# rdiv
@pytest.mark.parametrize("right_operand, fill_value", [
    # 1. 标量加法
    (right[0], None),
    
    # 2. np.array加法
    (right[1], None),
    
    # 3. pd.Series加法（索引对齐）
    (right[2], None),
    
    # 4. pd.Series加法（索引不对齐）
    (right[3], None),
    
    # 5. pd.Series加法（索引不对齐，使用fill_value=1.0）
    (right[4], 1.0),
    
    # 6. pd.Series加法（索引不对齐，使用fill_value=None）
    (right[5], None),
])
def test_series_rdiv(right_operand, fill_value):
    expected = series_left.rdiv(right_operand, fill_value=fill_value)
    if isinstance(right_operand, (float, np.ndarray)):
        cright_operand = ct.encrypt(right_operand)
    else:
        cright_operand = ct.encrypt_df(right_operand)
    if fill_value is not None:
        fill_value = ct.encrypt(fill_value)
    cresult = cs_left.rdiv(cright_operand, fill_value=fill_value)
    result = ct.decrypt_df(cresult)
    pd.testing.assert_series_equal(result, expected)