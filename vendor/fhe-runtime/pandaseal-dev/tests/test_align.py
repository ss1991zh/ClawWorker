import unittest
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
import crypto_toolkit as ct
import pandaseal as ps
import henumpy as hp


ct.initSK()
hp.initDict()


class TestCipherDataFrameAlign(unittest.TestCase):

    def setUp(self):
        # 初始化明文 DataFrame 和对齐的目标 DataFrame
        self.df1 = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        }, index=[0, 1, 2], dtype='float64')

        self.df2 = pd.DataFrame({
            'B': [7, 8, 9],
            'C': [10, 11, 12]
        }, index=[1, 2, 3], dtype='float64')

        # 将明文 DataFrame 加密为 CipherDataFrame
        self.cipher_df1 = ct.encrypt_df(self.df1)
        self.cipher_df2 = ct.encrypt_df(self.df2)

        self.series1 = pd.Series([1, 2, 3], index=[0, 1, 2], dtype='float64')
        self.series2 = pd.Series([4, 5, 6], index=[1, 2, 3], dtype='float64')

        self.cipher_series1 = ct.encrypt_df(self.series1)
        self.cipher_series2 = ct.encrypt_df(self.series2)


    def test_align_dataframewithdataframe_axis_0(self):
        # 明文 DataFrame 的对齐操作，axis=0
        expected_left, expected_right = self.df1.align(self.df2, join='outer', axis=0, fill_value=None)

        # 对应的 CipherDataFrame 的对齐操作，axis=0
        result_left, result_right = self.cipher_df1.align(self.cipher_df2, join='outer', axis=0)

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_frame_equal(result_left_plain, expected_left)
        assert_frame_equal(result_right_plain, expected_right)

    def test_align_dataframewithdataframe_axis_1(self):
        # 明文 DataFrame 的对齐操作，axis=1
        expected_left, expected_right = self.df1.align(self.df2, join='outer', axis=1, fill_value=10.0)

        # 对应的 CipherDataFrame 的对齐操作，axis=1
        encrypted_fill_value = ct.encrypt(10.0)  # 加密填充值为0
        result_left, result_right = self.cipher_df1.align(self.cipher_df2, join='outer', axis=1, fill_value=encrypted_fill_value)

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_frame_equal(result_left_plain, expected_left)
        assert_frame_equal(result_right_plain, expected_right)

    def test_align_dataframewithdataframe_axis_none(self):
        # 明文 DataFrame 的对齐操作，axis=None
        expected_left, expected_right = self.df1.align(self.df2, join='outer', axis=None, fill_value=None)

        # 对应的 CipherDataFrame 的对齐操作，axis=None
        result_left, result_right = self.cipher_df1.align(self.cipher_df2, join='outer', axis=None, fill_value=None)

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_frame_equal(result_left_plain, expected_left)
        assert_frame_equal(result_right_plain, expected_right)

    def test_align_dataframewithseries_axis_0(self):
        # 明文 DataFrame 的对齐操作，axis=None
        expected_left, expected_right = self.df1.align(self.series1, join='outer', axis=0, fill_value=None)

        # 对应的 CipherDataFrame 的对齐操作，axis=None
        result_left, result_right = self.cipher_df1.align(self.cipher_series1, join='outer', axis=0, fill_value=None)

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_frame_equal(result_left_plain, expected_left)
        assert_series_equal(result_right_plain, expected_right)

        # 明文 DataFrame 的对齐操作，axis=None
        expected_left, expected_right = self.df1.align(self.series1, join='outer', axis=0, fill_value=1.0)

        # 对应的 CipherDataFrame 的对齐操作，axis=None
        result_left, result_right = self.cipher_df1.align(self.cipher_series1, join='outer', axis=0, fill_value=hp.ones())

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_frame_equal(result_left_plain, expected_left)
        assert_series_equal(result_right_plain, expected_right) 

    def test_align_serieswithseries_axis_0(self):
        # 明文 DataFrame 的对齐操作，axis=None
        expected_left, expected_right = self.series1.align(self.series2, join='outer', axis=0, fill_value=None)

        # 对应的 CipherDataFrame 的对齐操作，axis=None
        result_left, result_right = self.cipher_series1.align(self.cipher_series2, join='outer', axis=0, fill_value=None)

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_series_equal(result_left_plain, expected_left)
        assert_series_equal(result_right_plain, expected_right)

        # 明文 DataFrame 的对齐操作，axis=None
        expected_left, expected_right = self.series1.align(self.series2, join='outer', axis=0, fill_value=1.0)

        # 对应的 CipherDataFrame 的对齐操作，axis=None
        result_left, result_right = self.cipher_series1.align(self.cipher_series2, join='outer', axis=0, fill_value=hp.ones())

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_series_equal(result_left_plain, expected_left)
        assert_series_equal(result_right_plain, expected_right)   

    def test_align_serieswithdataframe_axis_0(self):
        # 明文 DataFrame 的对齐操作，axis=None
        expected_left, expected_right = self.series1.align(self.df2, join='outer', axis=0, fill_value=None)

        # 对应的 CipherDataFrame 的对齐操作，axis=None
        result_left, result_right = self.cipher_series1.align(self.cipher_df2, join='outer', axis=0, fill_value=None)

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_series_equal(result_left_plain, expected_left)
        assert_frame_equal(result_right_plain, expected_right)

        # 明文 DataFrame 的对齐操作，axis=None
        expected_left, expected_right = self.series1.align(self.df2, join='outer', axis=0, fill_value=1.0)

        # 对应的 CipherDataFrame 的对齐操作，axis=None
        result_left, result_right = self.cipher_series1.align(self.cipher_df2, join='outer', axis=0, fill_value=hp.ones())

        # 解密结果以便比较
        result_left_plain = ct.decrypt_df(result_left)
        result_right_plain = ct.decrypt_df(result_right)

        # 验证解密后的结果与明文对齐结果一致
        assert_series_equal(result_left_plain, expected_left)
        assert_frame_equal(result_right_plain, expected_right)         

if __name__ == '__main__':
    unittest.main()
