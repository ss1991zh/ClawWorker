import pandas as pd
import numpy as np
import henumpy as hp
from .cipherframe import CipherDataFrame
from .cipherseries import CipherSeries
from .base import _group_and_replace
from .reshape import concat


class CipherDataFrameGroupBy:
    """
    Class for grouping and aggregating relational data.

    See aggregate, transform, and apply functions on this object.

    It's easiest to use obj.groupby(...) to use GroupBy.

    Parameters
    ----------
    obj : CipherDataFrame object
    level : int, default None
    groupings : list of Grouping objects
        Most users should ignore this
    exclusions : array-like, optional
        List of columns to exclude
    name : str
        Most users should ignore this

    Returns
    -------
    **Attributes**
    groups : dict
        {group name -> group labels}
    len(grouped) : int
        Number of groups
    """

    def __init__(
            self,
            obj : CipherDataFrame, 
            level=0,
    ):
        obj = obj.copy()
        self.obj = obj
        self.groupby = obj.dataframe_A.groupby(level=level)
        self.P = obj.dataframe_PL.iloc[0]
        
    def __iter__(self):
        """
        Iterate over groups as (name, group) pairs.

        """
        for group_name, group_df in self.groupby:
            cipher_group_df = CipherDataFrame()
            cipher_group_df.dataframe_A = group_df
            # no dtype will raise setvalue error
            cipher_group_df.dataframe_PL = pd.DataFrame(index=['_P', '_L'], columns=self.P.index, dtype=float)
            cipher_group_df.dataframe_PL.iloc[0] = self.P
            cipher_group_df.dataframe_PL.iloc[1] = len(group_df)

            yield (group_name, cipher_group_df)

    def sum(self):
        FIRST_ELEMENT = True
        
        for group_name, group_df in self:
            c_group_df = group_df.to_cipherarray()
            sum_c = hp.nansum(c_group_df, axis=0).cipherReshape(1, -1).transEncType()
            cdf = CipherDataFrame(sum_c, index=[group_name], columns=group_df.columns)
            if FIRST_ELEMENT:
                res = cdf
                FIRST_ELEMENT = False
            else:
                res = concat([res, cdf], axis=0)
        
        return res
    
    def std(self, ddof=1):
        FIRST_ELEMENT = True

        for group_name, group_df in self:
            c_group_df = group_df.to_cipherarray()
            std_c = hp.nanstd(c_group_df, axis=0, ddof=ddof).cipherReshape(1, -1).transEncType()
            cdf = CipherDataFrame(std_c, index=[group_name], columns=group_df.columns)
            if FIRST_ELEMENT:
                res = cdf
                FIRST_ELEMENT = False
            else:
                res = concat([res, cdf], axis=0)
        return res

    def var(self, ddof=1):
        FIRST_ELEMENT = True

        for group_name, group_df in self:
            c_group_df = group_df.to_cipherarray()
            std_c = hp.nanvar(c_group_df, axis=0, ddof=ddof)
            std_c = std_c.cipherReshape(1, -1)
            std_c = std_c.transEncType()
            cdf = CipherDataFrame(std_c, index=[group_name], columns=group_df.columns)
            if FIRST_ELEMENT:
                res = cdf
                FIRST_ELEMENT = False
            else:
                res = concat([res, cdf], axis=0)
        return res

    def mean(self):
        FIRST_ELEMENT = True

        for group_name, group_df in self:
            c_group_df = group_df.to_cipherarray()
            mean_c = hp.nanmean(c_group_df, axis=0).cipherReshape(1, -1).transEncType()
            cdf = CipherDataFrame(mean_c, index=[group_name], columns=group_df.columns)
            if FIRST_ELEMENT:
                res = cdf
                FIRST_ELEMENT = False
            else:
                res = concat([res, cdf], axis=0)
        return res

    def median(self):
        FIRST_ELEMENT = True

        for group_name, group_df in self:
            c_group_df = group_df.to_cipherarray()
            median_c = hp.nanmedian(c_group_df, axis=0).cipherReshape(1, -1).transEncType()
            cdf = CipherDataFrame(median_c, index=[group_name], columns=group_df.columns)
            if FIRST_ELEMENT:
                res = cdf
                FIRST_ELEMENT = False
            else:
                res = concat([res, cdf], axis=0)
        return res
        
    def quantile(self, q=0.5):
        FIRST_ELEMENT = True

        for group_name, group_df in self:
            c_group_df = group_df.to_cipherarray()
            quantile_c = hp.nanquantile(c_group_df, q, axis=0).cipherReshape(1, -1).transEncType()
            cdf = CipherDataFrame(quantile_c, index=[group_name], columns=group_df.columns)
            if FIRST_ELEMENT:
                res = cdf
                FIRST_ELEMENT = False
            else:
                res = concat([res, cdf], axis=0)        
        return res



class CipherSeriesGroupBy:
    def __init__(
            self,
            obj : CipherSeries,
            level,
    ):
        obj = obj.copy()
        self.obj = obj
        self.groupby = obj.series_A.groupby(level=level)
        self.P = obj.series_PL.iloc[0]

    def __iter__(self):
        """
        Iterate over groups as (name, group) pairs.

        """
        for group_name, group_df in self.groupby:
            cipher_group_s = CipherSeries()
            cipher_group_s.series_A = group_df
            # no dtype will raise setvalue error
            cipher_group_s.series_PL = pd.Series(index=['_P', '_L'], dtype=float)
            cipher_group_s.series_PL.iloc[0] = self.P
            cipher_group_s.series_PL.iloc[1] = len(group_df)

            yield (group_name, cipher_group_s)

    def sum(self):
        c_res = hp.empty_array()
        idx = []
        for group_name, group_s in self:
            c_group_s = group_s.to_cipherarray()
            sum_c = hp.nansum(c_group_s)
            c_res = hp.append(c_res, sum_c)
            idx.append(group_name)
        return CipherSeries(c_res, index=idx, name=self.obj.series_A.name)
    
    def std(self, ddof=1):
        c_res = hp.empty_array()
        idx = []
        for group_name, group_s in self:
            c_group_s = group_s.to_cipherarray()
            std_c = hp.nanstd(c_group_s, ddof=ddof)
            c_res = hp.append(c_res, std_c)
            idx.append(group_name)
        return CipherSeries(c_res, index=idx, name=self.obj.series_A.name)

    def var(self, ddof=1):
        c_res = hp.empty_array()
        idx = []
        for group_name, group_s in self:
            c_group_s = group_s.to_cipherarray()
            var_c = hp.nanvar(c_group_s, ddof=ddof)
            c_res = hp.append(c_res, var_c)
            idx.append(group_name)
        return CipherSeries(c_res, index=idx, name=self.obj.series_A.name)
    
    def mean(self):
        c_res = hp.empty_array()
        idx = []
        for group_name, group_s in self:
            c_group_s = group_s.to_cipherarray()
            mean_c = hp.nanmean(c_group_s)
            c_res = hp.append(c_res, mean_c)
            idx.append(group_name)
        return CipherSeries(c_res, index=idx, name=self.obj.series_A.name)
    
    def median(self):
        c_res = hp.empty_array()
        idx = []
        for group_name, group_s in self:
            c_group_s = group_s.to_cipherarray()
            median_c = hp.nanmedian(c_group_s)
            c_res = hp.append(c_res, median_c)
            idx.append(group_name)
        return CipherSeries(c_res, index=idx, name=self.obj.series_A.name)    
    
    def quantile(self, q=0.5):
        c_res = hp.empty_array()
        idx = []
        for group_name, group_s in self:
            c_group_s = group_s.to_cipherarray()
            quantile_c = hp.nanquantile(c_group_s, q)
            c_res = hp.append(c_res, quantile_c)
            idx.append(group_name)
        return CipherSeries(c_res, index=idx, name=self.obj.series_A.name) 