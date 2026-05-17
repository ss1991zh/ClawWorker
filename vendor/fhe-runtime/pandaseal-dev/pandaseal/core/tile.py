import pandas as pd
import numpy as np
import henumpy as hp
from .cipherseries import CipherSeries


def cut(x: CipherSeries, bins: int | hp.CipherArray, labels, right: bool = True, ordered: bool = True):
    """
    Cut the values in x into discrete intervals.

    Parameters
    x : CipherSeries
        The values to be cut.
    bins : CipherArray or integer
        CipherArray - It must be a sorted 1-dimensional array of unique values.
    labels : array
        The labels to use for the returned categories.
    right : bool, default True
        Indicator of whether the binsinclude the rightmost edge or not.
    ordered : bool, default True
        Indicator of whether the categories are ordered.

    Returns
    -------
    Series
        The bins that each value in x belongs to.
    """

    # 1. check the x
    # 2. if bins is an integer, create a list of bins
    # 3. call hp.digitize return the index of bins that each value in x belongs to
    # 4. construct category from bins and labels
    # 5. return the category

    if not isinstance(x, CipherSeries):
        raise TypeError("x must be a CipherSeries.")
    
    na = x.isna()
    if na.all(): # all values are NaN
        return pd.Series(np.full(x.size(), 'NaN'), name=x.series_A.name)
    if na.any():
        x = x.copy()
        for i in range(x.size):
            if not na[i]:
                fill_value = x.series_A.iloc[i]
                break
        x.series_A.fillna(fill_value, inplace=True)

    c_x = x.to_cipherarray()

    # how to convert bins with integer type to hp.CipherArray
    if isinstance(bins, int):
        min = hp.min(c_x)
        max = hp.max(c_x)

        if min == max:
            if min == 0:
                min = min - 0.001
            else:
                min = min - hp.absolute(min) * 0.001
            
            if max == 0:
                max  = max + 0.001
            else:
                max  = max + hp.absolute(max) * 0.001

        bins = hp.linspace(min, max, bins + 1, endpoint=True)

        adj = (max - min) * 0.001  # 0.1% of the range
        if right:
            bins[0] = bins[0] - adj
        else:
            bins[-1] = bins[-1] + adj

    if not isinstance(bins, hp.CipherArray):
        raise TypeError("bins must be an integer or a hp.CipherArray.")
    
    if ordered and len(set(labels)) != len(labels):
        raise ValueError(
            "labels must be unique if ordered=True; pass ordered=False "
            "for duplicate labels")
    else:
        if len(labels) != hp.cipherLen(bins)-1:
                raise ValueError(
                    "Bin labels must be one fewer than the number of bin edges")        

    bins_indices = hp.digitize(c_x, bins, right=right)
    bins_indices -= 1
    # if dtype is not object, the dtype is '<U1'. Can not present nan.
    lab = np.array(labels, dtype=object)[bins_indices]
    for i in range(len(lab)):
        if bins_indices[i] == -1 or na.iloc[i]:
            lab[i] = np.nan
    if len(set(labels)) != len(labels):
        labels = None
    return pd.Series(pd.Categorical(lab, categories=labels, ordered=ordered), index=x.series_A.index, name=x.series_A.name)