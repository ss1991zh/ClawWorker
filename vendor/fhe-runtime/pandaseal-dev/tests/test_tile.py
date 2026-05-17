import pytest
import crypto_toolkit as ct
import numpy as np
import henumpy as hp
import pandas as pd
import pandaseal as ps

ct.initSK()
hp.initDict()

data = np.random.rand(10) * 20. - 5.
s = pd.Series(data)
cs = ct.encrypt_df(s)
bins = np.array([-5., 0., 5., 10., 15., 20.])

@pytest.mark.parametrize("bins, labels, right, ordered",
                         [(4, ["A", "B", "C", "D"], True, True),
                          (bins, ["A", "B", "C", "D", "E"], False, False),
                          (3, ["B", "A", "B"], True, False)])
def test_cut(bins, labels, right, ordered):
    s_cut = pd.cut(s, bins, right=right, labels=labels, ordered=ordered)

    if isinstance(bins, int):
        cs_cut = ps.cut(cs, bins, labels, right, ordered)
    else:
        cbins = ct.encrypt(bins)
        cs_cut = ps.cut(cs, cbins, labels, right, ordered)

    pd.testing.assert_series_equal(s_cut, cs_cut)

