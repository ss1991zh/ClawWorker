import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()

#################################################################
#########################dataframe###############################

# 测试数据
data = {
    "A": [1.1, 2.2, 1.1, 4.4, 2.2],
    "B": [5.5, 6.6, 5.5, 7.7, 6.6],
    "C": [9.9, 10.1, 9.9, 11.2, 10.1],
}

df = pd.DataFrame(data)

# 加密数据
c_df = ct.encrypt_df(df)

@pytest.mark.parametrize("subset, keep, ignore_index", [
    # 1. 默认所有列，保留首次出现，保持原索引
    (None, "first", False),

    # 2. 默认所有列，保留最后一次出现，保持原索引
    (None, "last", False),

    # 3. 使用 subset 指定部分列，保留首次出现
    (["A", "B"], "first", False),

    # 4. 使用 subset 指定部分列，保留最后一次出现
    (["A", "B"], "last", False),

    # 5. 使用 ignore_index 重置索引
    (None, "first", True),
])
def test_drop_duplicates(subset, keep, ignore_index):
    # 明文结果
    result = df.drop_duplicates(subset=subset, keep=keep, ignore_index=ignore_index)

    # 加密结果
    c_result = c_df.drop_duplicates(subset=subset, keep=keep, ignore_index=ignore_index)
    decrypted_result = ct.decrypt_df(c_result)

    # 验证明文与加密结果一致
    pd.testing.assert_frame_equal(result, decrypted_result, check_dtype=False)


#################################################################
############################series###############################

# 测试数据
data1 = [1.1, 2.2, 1.1, 4.4, 2.2]
s = pd.Series(data1)

# 加密数据
c_s = ct.encrypt_df(s)

@pytest.mark.parametrize("keep, ignore_index", [
    # 1. 保留首次出现，保持原索引
    ("first", False),

    # 2. 保留最后一次出现，保持原索引
    ("last", False),

    # 3. 删除所有重复项
    (False, False),

    # 4. 保留首次出现，重置索引
    ("first", True),

    # 5. 保留最后一次出现，重置索引
    ("last", True),
])
def test_series_drop_duplicates(keep, ignore_index):
    # 明文结果
    result = s.drop_duplicates(keep=keep, ignore_index=ignore_index)

    # 加密结果
    c_result = c_s.drop_duplicates(keep=keep, ignore_index=ignore_index)
    decrypted_result = ct.decrypt_df(c_result)

    # 验证明文与加密结果一致
    pd.testing.assert_series_equal(decrypted_result, result, check_dtype=False)