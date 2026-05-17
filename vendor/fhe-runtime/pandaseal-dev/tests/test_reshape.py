import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()

#########################索引已对齐#################################

# 创建测试用的 DataFrame
def generate_dataframe(rows, cols, start=0):
    data = np.arange(start, start + rows * cols).reshape(rows, cols)
    return pd.DataFrame(data, columns=[f"col{i}" for i in range(cols)], dtype=float)

# 生成测试数据
df1_1 = generate_dataframe(3, 3)  # DataFrame 1
df2_1 = generate_dataframe(3, 3, start=9)  # DataFrame 2 with different values

# 加密测试数据
cdf1_1 = ct.encrypt_df(df1_1)
cdf2_1 = ct.encrypt_df(df2_1)

@pytest.mark.parametrize("axis", [0, 1])  # 按行或按列拼接
@pytest.mark.parametrize("join", ["outer", "inner"])  # 外连接或内连接
@pytest.mark.parametrize("ignore_index", [True, False])  # 是否忽略索引
def test_concat_1(axis, join, ignore_index):
    # 明文 DataFrame 拼接
    expected = pd.concat([df1_1, df2_1], axis=axis, join=join, ignore_index=ignore_index)
    
    # 加密 DataFrame 拼接
    result_cipher = ps.concat([cdf1_1, cdf2_1], axis=axis, join=join, ignore_index=ignore_index)

    # 解密加密结果
    result_decrypted = ct.decrypt_df(result_cipher)

    # 验证解密结果与明文结果是否一致
    pd.testing.assert_frame_equal(result_decrypted, expected)


###########################索引不对齐###################################

# 创建测试数据
series1 = pd.Series([1, 2, 3], index=["a", "b", "c"], dtype=float)
series2 = pd.Series([4, 5, 6], index=["b", "c", "d"], dtype=float)
df1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=["a", "b", "c"], dtype=float)
df2 = pd.DataFrame({"C": [7, 8, 9], "D": [10, 11, 12]}, index=["b", "c", "d"], dtype=float)

# 加密测试数据
c_series1 = ct.encrypt_df(series1)
c_series2 = ct.encrypt_df(series2)
c_df1 = ct.encrypt_df(df1)
c_df2 = ct.encrypt_df(df2)

@pytest.mark.parametrize("data1, data2, axis, join, ignore_index", [
    # Series 和 Series
    (series1, series2, 0, "outer", False),
    (series1, series2, 1, "inner", False),
    
    # Series 和 DataFrame
    (series1, df1, 0, "outer", True),
    (series1, df2, 1, "inner", False),
    
    # DataFrame 和 DataFrame
    (df1, df2, 0, "outer", False),
    (df1, df2, 1, "inner", True),
    
    # DataFrame 和 Series
    (df1, series2, 0, "outer", True),
    (df2, series1, 1, "inner", False),
])
def test_concat_2(data1, data2, axis, join, ignore_index):
    # 明文拼接
    expected = pd.concat([data1, data2], axis=axis, join=join, ignore_index=ignore_index)
    
    # 加密数据
    c_data1 = ct.encrypt_df(data1) if isinstance(data1, (pd.DataFrame, pd.Series)) else ct.encrypt(data1)
    c_data2 = ct.encrypt_df(data2) if isinstance(data2, (pd.DataFrame, pd.Series)) else ct.encrypt(data2)
    
    # 加密拼接
    result_cipher = ps.concat([c_data1, c_data2], axis=axis, join=join, ignore_index=ignore_index)

    # 解密结果
    result_decrypted = ct.decrypt_df(result_cipher)
    
    # 验证
    if isinstance(result_decrypted, pd.Series):
        pd.testing.assert_series_equal(result_decrypted, expected, check_dtype=True)
    else:
        pd.testing.assert_frame_equal(result_decrypted, expected, check_dtype=True)


###############################join###################################
# 创建测试数据
df1_join = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
}, index=["a", "b", "c"], dtype=float)

df2_join = pd.DataFrame({
    "C": [7, 8, 9],
    "D": [10, 11, 12]
}, index=["b", "c", "d"], dtype=float)

series1_join = pd.Series([13, 14, 15], index=["b", "c", "d"], name="E", dtype=float)

# 加密测试数据
c_df1_join = ct.encrypt_df(df1_join)
c_df2_join = ct.encrypt_df(df2_join)
c_series1_join = ct.encrypt_df(series1_join)

@pytest.mark.parametrize("right, how, sort", [
    # DataFrame.join(DataFrame) 情况
    (df2_join, "left", False),
    (df2_join, "right", True),
    (df2_join, "outer", False),
    (df2_join, "inner", True),
    
    # DataFrame.join(Series) 情况
    (series1_join, "left", False),
    (series1_join, "right", True),
    (series1_join, "outer", False),
    (series1_join, "inner", True),
])
def test_join(right, how, sort):
    # 明文 join
    expected = df1_join.join(right, how=how, sort=sort)
    
    # 加密数据准备
    c_right = ct.encrypt_df(right)

    # 加密 join
    result_cipher = c_df1_join.join(c_right, how=how, sort=sort)
    
    # 解密结果
    result_decrypted = ct.decrypt_df(result_cipher)
    
    # 验证加密计算结果与明文计算结果是否一致
    pd.testing.assert_frame_equal(result_decrypted, expected)

############################### merge #################################
#######################################################################

# 创建测试数据
left = pd.DataFrame({
    "key1": [1, 2, 3, 4],
    "key2": [5, 6, 7, 8],
    "value1": [9, 10, 11, 12]
}, dtype=float)

right = pd.DataFrame({
    "key1": [3, 4, 5, 6],
    "key2": [7, 8, 9, 10],
    "value2": [13, 14, 15, 16]
}, dtype=float)

# 加密测试数据
c_left = ct.encrypt_df(left)
c_right = ct.encrypt_df(right)

@pytest.mark.parametrize("on, how", [
    # 使用单列作为连接键
    ("key1", "inner"),
    ("key1", "left"),
    ("key1", "right"),
    ("key1", "outer"),
    
    # 使用多列作为连接键
    # (["key1", "key2"], "inner"),
    (["key1", "key2"], "left"),
    (["key1", "key2"], "right"),
    (["key1", "key2"], "outer"),
])
def test_merge(on, how):
    # 明文 merge
    expected = pd.merge(left, right, on=on, how=how)
    
    # 加密 merge
    result_cipher = ps.merge(c_left, c_right, on=on, how=how)
    
    # 解密结果
    result_decrypted = ct.decrypt_df(result_cipher)
    
    # 验证加密计算结果与明文结果是否一致
    pd.testing.assert_frame_equal(result_decrypted, expected, check_dtype=True)
    
    # 打印成功信息
    # print(f"Test with on={on}, how='{how}' passed!\nDecrypted result:\n{result_decrypted}\n")