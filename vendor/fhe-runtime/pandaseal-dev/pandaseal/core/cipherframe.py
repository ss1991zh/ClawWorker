import operator
import pandas as pd
import numpy as np
from collections.abc import (
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)

import henumpy as hp
from .cipherseries import CipherSeries
from pandaseal.core import roperator
from .indexing import _ILOCIndexer, _LocIndexer, _AtIndexer, _IAtIndexer
from pandaseal.core import ops

class CipherDataFrame:

    def __init__(self, data=None, index=None, columns=None, copy=False):
        """
        Init CipherDataFrame from CipherArray or Numpy Array which encrypted by column.
        TODO: The 'data' variable supports CipherSeries and Dictionary types.
        Parameters
        data : CipherArray or Numpy Array
        index : Index or array-like
        columns : Index or array-like
        copy : bool, default False
        """

        if data is None:
            if columns is None:
                PL = pd.DataFrame(index=['_P', '_L'])
            else:
                empty = hp.empty_array().get_base_array()[:2]
                PL = pd.DataFrame(index=['_P', '_L'], columns=columns)
                PL.iloc[0] = empty[0]
                PL.iloc[1] = empty[1]

            self.dataframe_PL = PL
            self.dataframe_A  = pd.DataFrame(index=index, columns=columns)
            return 

        if isinstance(data, hp.CipherArray):
            # encrypted by column
            if data.get_encryption_type() != 1:

                data = data.transEncType()
                print('data is not encrypted by column, executing transEncType')
            data = data.get_base_array()
            copy = True

        index_name = None
        if isinstance(index, pd.Index):
            index_name = index.name
        self.dataframe_PL = pd.DataFrame(data[:2], index=pd.Index(['_P', '_L'], name=index_name), columns=columns, copy=copy)
        self.dataframe_A  = pd.DataFrame(data[2:], index=index, columns=columns, copy=copy)

    def copy(self, deep=True):
        """
        Make a copy of this object’s indices and data. default deep Copy.
        """

        cdf = CipherDataFrame()
        cdf.dataframe_PL = self.dataframe_PL.copy(deep)
        cdf.dataframe_A  = self.dataframe_A.copy(deep)

        return cdf

    def __str__(self):
        tmp = pd.concat([self.dataframe_PL, self.dataframe_A], axis=0)
        return tmp.__str__()
    
    def __getitem__(self, key):
        
        """
        Get elements from dataframe using columns or slice.
        
        
        Parameters
        ----------
        key : str, list or slice
        
        Return
        -------
        CipherSeries or CipherDataFrame
        
        Example:
        >>> cdf = CipherDataFrame(data=np.array([[-6.863455134783327e-222, 1.1443994549670154e-72, -1.6081617951495907e+29, 1.0781824876420455e+87], 
                                                [3.0,                   3.0,                3.0,                3.0], 
                                                [0.23178933351905856, 0.09438296616649205, 0.1612789927674723, 0.07284000130254832], 
                                                [0.1137413270981526, 0.007959673521443002, 0.1401111356282174, 0.0024372481791582836], 
                                                [0.12187587941377741, 0.21759976516752358, 0.0033326023266366037, 0.12500503519950357]]), 
                                                index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])
        >>> cdf['A']
        _P   -6.863455e-222
        _L    3.000000e+00
        a     2.317893e-01
        b     1.137413e-01
        c     1.218759e-01
        Name: A, dtype: float64
        >>> cdf[['A', 'B']]
                    A             B
        _P -6.863455e-222  1.144399e-72
        _L  3.000000e+00  3.000000e+00
        a   2.317893e-01  9.438297e-02
        b   1.137413e-01  7.959674e-03
        c   1.218759e-01  2.175998e-01
        >>> cdf[:2]
                    A             B             C             D
        _P -6.863455e-222  1.144399e-72 -1.608162e+29  1.078182e+87
        _L  2.000000e+00  2.000000e+00  2.000000e+00  2.000000e+00
        a   2.317893e-01  9.438297e-02  1.612790e-01  7.284000e-02
        b   1.137413e-01  7.959674e-03  1.401111e-01  2.437248e-03        
        
        """ 
        
        A = self.dataframe_A[key]

        A_shape     = A.shape
        self_shape  = self.dataframe_A.shape

        if len(A_shape) == 1:
            PL = self.dataframe_PL[key]
            tmp = CipherSeries()
            tmp.series_PL = PL
            tmp.series_A  = A
            return tmp
        
        elif len(A_shape) == 2:  # 行
            if A_shape[0] < self_shape[0]:
                # PL = _modify_L_for_dataframe_PL(self.dataframe_PL, A_shape[0])
                PL = self.modify_L_for_PL(self.dataframe_PL, A_shape[0])
            else:
                PL = self.dataframe_PL[key]
            cdf = CipherDataFrame()
            cdf.dataframe_PL = PL
            cdf.dataframe_A  = A
            return cdf
    
    def __setitem__(self, key, value):
        
        """
        Set elements of dataframe using columns or slice.
        
        
        Parameters
        ----------
        key : str, list or slice
        value : CipherSeries or CipherDataFrame
        
        Return
        -------
        None
        
        Example:
        >>> cdf = CipherDataFrame(data=np.array())
        """
        if isinstance(value, CipherSeries):
            self.dataframe_PL[key] = value.series_PL
            self.dataframe_A[key]  = value.series_A
        elif isinstance(value, CipherDataFrame):
            self.dataframe_PL[key] = value.dataframe_PL
            self.dataframe_A[key]  = value.dataframe_A
        elif isinstance(value, hp.CipherArray):
            if value.ndim == 1 and value.get_cipher_type() == 2:
                # fix len(self.index)!= hp.cipherLen(value)
                # TODO: need to test
                if len(self.index) != hp.cipherLen(value):
                    idx = None
                else:
                    idx = self.index
                cs = CipherSeries(value, index=idx)
                self.dataframe_A[key] = cs.series_A
                self.dataframe_PL[key] = cs.series_PL
            elif value.ndim == 2 and value.get_cipher_type() == 2:
                cdf = CipherDataFrame(value, index=self.dataframe_A.index)
                self.dataframe_A[key] = cdf.dataframe_A
                self.dataframe_PL[key] = cdf.dataframe_PL
        else:
            pass

    def to_dataframe(self):
        """
        Convert the CipherDataFrame to a DataFrame.

        """
        return pd.concat([self.dataframe_PL, self.dataframe_A], axis=0)

    def to_cipherarray(self):
        """
        Convert the CipherDataFrame to a CipherArray.

        Return
        -------
        CipherArray

        Example:
        >>> cdf = CipherDataFrame(data=np.array([[-6.863455134783327e-222, 1.1443994549670154e-72, -1.6081617951495907e+29, 1.0781824876420455e+87], 
                                                [3.0,                   3.0,                3.0,                3.0], 
                                                [0.23178933351905856, 0.09438296616649205, 0.1612789927674723, 0.07284000130254832], 
                                                [0.1137413270981526, 0.007959673521443002, 0.1401111356282174, 0.0024372481791582836], 
                                                [0.12187587941377741, 0.21759976516752358, 0.0033326023266366037, 0.12500503519950357]]), 
                                                index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])
        >>> cdf
                        A             B             C             D
        _P -6.863455e-222  1.144399e-72 -1.608162e+29  1.078182e+87
        _L  3.000000e+00  3.000000e+00  3.000000e+00  3.000000e+00
        a   2.317893e-01  9.438297e-02  1.612790e-01  7.284000e-02
        b   1.137413e-01  7.959674e-03  1.401111e-01  2.437248e-03
        c   1.218759e-01  2.175998e-01  3.332602e-03  1.250050e-01
        >>> cdf.to_cipherarray()
        [[-6.863455134783327e-222, 1.1443994549670154e-72, -1.6081617951495907e+29, 1.0781824876420455e+87],
        [              3.0,               3.0,               3.0,               3.0],
        [0.23178933351905856, 0.09438296616649205, 0.1612789927674723, 0.07284000130254832],
        [0.1137413270981526, 0.007959673521443002, 0.1401111356282174, 0.0024372481791582836],
        [0.12187587941377741, 0.21759976516752358, 0.0033326023266366037, 0.12500503519950357]]
               
        """
        # handle empty dataframe
        if self.dataframe_A.size == 0:
            shape = self.dataframe_A.shape
            if shape[0] != 0:
                # return 2d-empty cipherarray
                """
                [[-2.393278e-236, 0.000000e+00, 0.000000e+00],
                [ 3.027406e-265, 0.000000e+00, 0.000000e+00],
                .               .             .           
                .               .             .           
                .               .             .           
                [-1.283117e+34, 0.000000e+00, 0.000000e+00]]
                """ 
                empty = [hp.empty_array().get_base_array().tolist()] * shape[0]
                return hp.CipherArray(np.array(empty))

            elif shape[1] != 0:
                """
                [[-2.393278e-236  3.027406e-265  ... -1.283117e+34],
                [  0.000000e+00   0.000000e+00  ...  0.000000e+00],
                [  0.000000e+00   0.000000e+00  ...  0.000000e+00]]                
                """
                empty = [hp.empty_array().get_base_array().tolist()] * shape[1]
                return hp.CipherArray(np.array(empty).T)
            
            else: # shape = (0, 0)
                empty = [hp.empty_array().get_base_array().tolist()]
                return hp.CipherArray(np.array(empty))

        return hp.CipherArray(np.concatenate([self.dataframe_PL.values, self.dataframe_A.values], axis=0))

    def head(self, n: int = 5):
        """
        Return the first n rows of the CipherDataFrame.

        Parameters
        ----------
        n : int, default 5
            Number of rows to return.
            
        Return
        -------
        same type as caller

        Examples
        ---------
        >>>cdf = CipherDataFrame(data=np.array([[-1.045643791556698e+87, -1.0587661011588215e-202, -5.741362103692961e-116, 2.4385751319152947e-289],
                                                [              6.0,               6.0,               6.0,               6.0],
                                                [0.2740765794401703, 0.5004966647600307, 0.24798336838583565, 0.7276119755283638],
                                                [0.525313443926993, 0.709036941743377, 0.4734227941911408, 0.9355011113936105],
                                                [0.7765503084138158, 0.9384312464250578, 0.6988622199964459, 1.1433902472588573],
                                                [0.5024737289736455, -0.02085402769833462, -2.0514987748282767, 1.3512793831241041],
                                                [0.7080311635537733, 1.0218473572183964, 0.4734227941911408, 1.559168518989351],
                                                [0.022839714953347523, 0.04170805539666924, 0.06763182774159153, 0.08315565434609871]]), columns=['A', 'B', 'C', 'D'])
        >>>cdf.head()
                        A              B              C              D
            _P -1.045644e+87 -1.058766e-202 -5.741362e-116  2.438575e-289
            _L  5.000000e+00   5.000000e+00   5.000000e+00   5.000000e+00
            0   2.740766e-01   5.004967e-01   2.479834e-01   7.276120e-01
            1   5.253134e-01   7.090369e-01   4.734228e-01   9.355011e-01
            2   7.765503e-01   9.384312e-01   6.988622e-01   1.143390e+00
            3   5.024737e-01  -2.085403e-02  -2.051499e+00   1.351279e+00
            4   7.080312e-01   1.021847e+00   4.734228e-01   1.559169e+00

        """
        _A = self.dataframe_A.head(n)
        res = CipherDataFrame()
        if _A.shape[0] == 0: 
            res.dataframe_A = _A
            return res
        # L = _modify_L_for_dataframe_PL(self.dataframe_PL, _A.shape[0])
        L = self.modify_L_for_PL(self.dataframe_PL, _A.shape[0])
        res = CipherDataFrame()
        res.dataframe_PL = L
        res.dataframe_A = _A
        return res

    def tail(self, n: int = 5):
        """
        Return the last n rows of the CipherDataFrame.

        Parameters
        ----------
        n : int, default 5
            Number of rows to return.
            
        Return
        -------
        same type as caller

        Examples
        ---------
        >>>cdf = CipherDataFrame(data=np.array([[-1.045643791556698e+87, -1.0587661011588215e-202, -5.741362103692961e-116, 2.4385751319152947e-289],
                                                [              6.0,               6.0,               6.0,               6.0],
                                                [0.2740765794401703, 0.5004966647600307, 0.24798336838583565, 0.7276119755283638],
                                                [0.525313443926993, 0.709036941743377, 0.4734227941911408, 0.9355011113936105],
                                                [0.7765503084138158, 0.9384312464250578, 0.6988622199964459, 1.1433902472588573],
                                                [0.5024737289736455, -0.02085402769833462, -2.0514987748282767, 1.3512793831241041],
                                                [0.7080311635537733, 1.0218473572183964, 0.4734227941911408, 1.559168518989351],
                                                [0.022839714953347523, 0.04170805539666924, 0.06763182774159153, 0.08315565434609871]]), columns=['A', 'B', 'C', 'D'])
        >>>cdf.tail()
                        A              B              C              D
            _P -1.045644e+87 -1.058766e-202 -5.741362e-116  2.438575e-289
            _L  5.000000e+00   5.000000e+00   5.000000e+00   5.000000e+00
            1   5.253134e-01   7.090369e-01   4.734228e-01   9.355011e-01
            2   7.765503e-01   9.384312e-01   6.988622e-01   1.143390e+00
            3   5.024737e-01  -2.085403e-02  -2.051499e+00   1.351279e+00
            4   7.080312e-01   1.021847e+00   4.734228e-01   1.559169e+00
            5   2.283971e-02   4.170806e-02   6.763183e-02   8.315565e-02
        """
        _A = self.dataframe_A.tail(n)
        res = CipherDataFrame()
        if _A.shape[0] == 0: 
            res.dataframe_A = _A
            return res
        L = self.modify_L_for_PL(self.dataframe_PL, _A.shape[0])
        res = CipherDataFrame()
        res.dataframe_PL = L
        res.dataframe_A = _A
        return res        

    @property
    def index(self):
        return self.dataframe_A.index

    @property
    def columns(self):
        return self.dataframe_A.columns

    def sort_index(
        self,
        *, 
        axis=0, 
        level=None, 
        ascending=True, 
        inplace=False, 
        kind='quicksort', 
        na_position='last', 
        sort_remaining=True, 
        ignore_index=False, 
        key=None, 
        ):
        """
        Sort CipherDataFrame by the index labels. 
        Fully reusing pandas' interface, 
        only need to sort PL at the same time as the column direction sort.

        """
        if inplace:
            self.dataframe_A.sort_index(
                axis=axis, 
                level=level, 
                ascending=ascending, 
                inplace=inplace, 
                kind=kind, 
                na_position=na_position, 
                sort_remaining=sort_remaining, 
                ignore_index=ignore_index, 
                key=key)
            if axis == 1:
                self.dataframe_PL.sort_index(
                    axis=axis, 
                    level=level, 
                    ascending=ascending, 
                    inplace=inplace, 
                    kind=kind, 
                    na_position=na_position, 
                    sort_remaining=sort_remaining, 
                    ignore_index=ignore_index, 
                    key=key)
            return None
        
        else: # inplace = False
            res = CipherDataFrame()
            res.dataframe_A = self.dataframe_A.sort_index(
                axis=axis, 
                level=level, 
                ascending=ascending, 
                inplace=inplace, 
                kind=kind, 
                na_position=na_position, 
                sort_remaining=sort_remaining, 
                ignore_index=ignore_index, 
                key=key)
            
            if axis == 1:
                res.dataframe_PL = self.dataframe_PL.sort_index(
                    axis=axis, 
                    level=level, 
                    ascending=ascending, 
                    inplace=inplace, 
                    kind=kind, 
                    na_position=na_position, 
                    sort_remaining=sort_remaining, 
                    ignore_index=ignore_index, 
                )
            else:
                res.dataframe_PL = self.dataframe_PL.copy()

        # if axis != 0:
        #     self.dataframe_PL = self.dataframe_PL.sort_index(axis=axis, level=level, ascending=ascending, inplace=inplace, kind=kind, na_position=na_position, sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
        
            return res

    def sort_values(
        self,
        by,
        *, 
        ascending=True, 
        inplace=False, 
        kind='quicksort', 
        na_position='last', 
        ignore_index=False, 
        key=None, 
        ):
        """
        Sort CipherDataFrame by the values along either axis.
        reusing pandas' interface.
        ```Currently only axis=0 is supported.```
        
        """
        if inplace:
            self.dataframe_A.sort_values(
                        by, 
                        axis=0, 
                        ascending=ascending, 
                        inplace=True, 
                        kind=kind, 
                        na_position=na_position, 
                        ignore_index=ignore_index, 
                        key=key)
            return self
        else:
            d = self.dataframe_A.sort_values(
                by, 
                axis=0, 
                ascending=ascending, 
                inplace=False, 
                kind=kind, 
                na_position=na_position, 
                ignore_index=ignore_index, 
                key=key)
            res = self.copy()
            res.dataframe_A = d
            return res

    @property
    def shape(self):
        return self.dataframe_A.shape
    
    @property
    def ndim(self):
        return 2

    @property
    def size(self):
        """
        Return an int representing the number of elements in this object.

        """
        return self.dataframe_A.size

    def align(self, other, join='outer', axis=None, fill_value=None):
        """
        Align two objects along their index.
        Only support join='outer' for now.
        """
        
        if join != 'outer':
            raise NotImplementedError("Only support join='outer' for now")
        
        if isinstance(other, CipherSeries):
            if axis == 0:
                # Merge indexes, not sort
                index_new = self.dataframe_A.index.union(other.series_A.index, False)
                index_new_series = other.series_A.index.union(self.dataframe_A.index, False)
               
                # dataframe need fill
                if len(index_new) > len(self.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    self.dataframe_A = self.dataframe_A.reindex(index=index_new)
                    self.dataframe_PL.iloc[1] = np.float64(len(index_new))

                # series need fill    
                if len(index_new_series) > len(other.series_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.series_A = other.series_A.reindex(index=index_new_series)
                    other.series_PL.iloc[1] = np.float64(len(index_new_series))
                
                if not self.index.equals(other.index):
                    self = self.sort_index()
                    other = other.sort_index()

            elif axis == 1:
                self_shape = self.shape
                other_shape = other.shape
                # Merge columns, not sort
                columns_new = self.dataframe_A.columns.union(other.series_A.index, False)
                index_new_series = other.series_A.index.union(self.dataframe_A.columns, False)

                # dataframe need fill
                if len(columns_new) > len(self.dataframe_A.columns):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    # fill missing column
                    self.dataframe_A = self.dataframe_A.reindex(columns=columns_new)
                    self.dataframe_PL = self.dataframe_PL.reindex(columns=columns_new)
                    self.dataframe_PL.iloc[0, self_shape[1]:] = self.dataframe_PL.iloc[0, 0]
                    self.dataframe_PL.iloc[1, self_shape[1]:] = np.float64(self_shape[0])

                if len(index_new_series) > len(other.series_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.series_A = other.series_A.reindex(index=index_new_series)
                    other.series_PL.iloc[1] = np.float64(len(index_new_series))

                # sort index
                if not self.columns.equals(other.index):
                    self = self.sort_index(axis=1)
                    other = other.sort_index()
            
            else:
                raise ValueError("Must specify axis=0 or 1.") 

        elif isinstance(other, CipherDataFrame):
            self_shape = self.shape
            other_shape = other.shape
            # union index and columns, do not sort
            self_index_new = self.dataframe_A.index.union(other.dataframe_A.index, False)
            self_columns_new = self.dataframe_A.columns.union(other.dataframe_A.columns, False)
            other_index_new = other.dataframe_A.index.union(self.dataframe_A.index, False)
            other_columns_new = other.dataframe_A.columns.union(self.dataframe_A.columns, False)

            if axis == 0 or axis is None:
                # need fill data
                if len(self_index_new) > len(self.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    self.dataframe_A = self.dataframe_A.reindex(index=self_index_new)
                    self.dataframe_PL.iloc[1] = np.float64(len(self_index_new))

                if len(other_index_new) > len(other.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.dataframe_A = other.dataframe_A.reindex(index=other_index_new)
                    other.dataframe_PL.iloc[1] = np.float64(len(other_index_new))

                if not self.index.equals(other.index):
                    self = self.sort_index()
                    other = other.sort_index()

            if axis == 1 or axis is None:
                if len(self_columns_new) > len(self.dataframe_A.columns):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    # fill missing column
                    self.dataframe_A = self.dataframe_A.reindex(columns=self_columns_new)
                    self.dataframe_PL = self.dataframe_PL.reindex(columns=self_columns_new)
                    self.dataframe_PL.iloc[0, self_shape[1]:] = self.dataframe_PL.iloc[0, 0]
                    self.dataframe_PL.iloc[1] = np.float64(self.dataframe_A.shape[0])

                if len(other_columns_new) > len(other.dataframe_A.columns):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    # fill missing column
                    other.dataframe_A = other.dataframe_A.reindex(columns=other_columns_new)
                    other.dataframe_PL = other.dataframe_PL.reindex(columns=other_columns_new)
                    other.dataframe_PL.iloc[0, other_shape[1]:] = other.dataframe_PL.iloc[0, 0]
                    other.dataframe_PL.iloc[1] = np.float64(other.dataframe_A.shape[0])

                if not self.columns.equals(other.columns):
                    self = self.sort_index(axis=1)
                    other = other.sort_index(axis=1)

 
        else:
            raise TypeError("Only support aligning CipherSeries and CipherDataFrame.")
        
        if fill_value is not None:
            if isinstance(fill_value, hp.CipherArray) and fill_value.get_cipher_type() == 1:
                self = self.fillna(fill_value)
                other = other.fillna(fill_value)
            else:
                raise ValueError(f"Fill_value must be None or a scalar CipherArray, but got {type(fill_value)}.")
            
        return self, other
    
    def _align_for_op(self, other, join='outer', axis=None):
        """
        Align the two operands by index for subsequent evaluation.
        """
        
        if join != 'outer':
            raise NotImplementedError("Only support join='outer' for now")
        
        if isinstance(other, CipherSeries):
            if axis == 0:
                # Merge indexes, not sort
                index_new = self.dataframe_A.index.union(other.series_A.index, False)
                index_new_series = other.series_A.index.union(self.dataframe_A.index, False)
               
                need_sort_col = False
                # dataframe need fill
                if len(index_new) > len(self.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    self.dataframe_A = self.dataframe_A.reindex(index=index_new)
                    self.dataframe_PL.iloc[1] = np.float64(len(index_new))
                    # need_sort_col = True

                # series need fill    
                if len(index_new_series) > len(other.series_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.series_A = other.series_A.reindex(index=index_new_series)
                    other.series_PL.iloc[1] = np.float64(len(index_new_series))
                    need_sort_col = True
                
                if need_sort_col:
                    self = self.sort_index()
                    other = other.sort_index()                    

            elif axis == 1:
                self_shape = self.shape
                other_shape = other.shape
                # Merge columns, not sort
                columns_new = self.dataframe_A.columns.union(other.series_A.index, False)
                index_new_series = other.series_A.index.union(self.dataframe_A.columns, False)

                need_sort_index = False

                # dataframe need fill
                if len(columns_new) > len(self.dataframe_A.columns):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    # fill missing column
                    self.dataframe_A = self.dataframe_A.reindex(columns=columns_new)
                    self.dataframe_PL = self.dataframe_PL.reindex(columns=columns_new)
                    self.dataframe_PL.iloc[0, self_shape[1]:] = self.dataframe_PL.iloc[0, 0]
                    self.dataframe_PL.iloc[1, self_shape[1]:] = np.float64(self_shape[0])
                    need_sort_index = True

                if len(index_new_series) > len(other.series_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.series_A = other.series_A.reindex(index=index_new_series)
                    other.series_PL.iloc[1] = np.float64(len(index_new_series))
                    need_sort_index = True
                
                # sort index
                if need_sort_index:
                    self = self.sort_index(axis=1)
                    other = other.sort_index()                    
            
            else:
                raise ValueError("Must specify axis=0 or 1.") 

        elif isinstance(other, CipherDataFrame):
            self_shape = self.shape
            other_shape = other.shape
            # union index and columns, do not sort
            self_index_new = self.dataframe_A.index.union(other.dataframe_A.index, False)
            self_columns_new = self.dataframe_A.columns.union(other.dataframe_A.columns, False)
            other_index_new = other.dataframe_A.index.union(self.dataframe_A.index, False)
            other_columns_new = other.dataframe_A.columns.union(self.dataframe_A.columns, False)

            need_sort_index = False
            need_sort_col = False
            if axis == 0 or axis is None:
                # need fill data
                if len(self_index_new) > len(self.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    self.dataframe_A = self.dataframe_A.reindex(index=self_index_new)
                    self.dataframe_PL.iloc[1] = np.float64(len(self_index_new))
                    need_sort_index = True

                if len(other_index_new) > len(other.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.dataframe_A = other.dataframe_A.reindex(index=other_index_new)
                    other.dataframe_PL.iloc[1] = np.float64(len(other_index_new))
                    need_sort_inedx = True

            if axis == 1 or axis is None:
                if len(self_columns_new) > len(self.dataframe_A.columns):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    # fill missing column
                    self.dataframe_A = self.dataframe_A.reindex(columns=self_columns_new)
                    self.dataframe_PL = self.dataframe_PL.reindex(columns=self_columns_new)
                    self.dataframe_PL.iloc[0, self_shape[1]:] = self.dataframe_PL.iloc[0, 0]
                    self.dataframe_PL.iloc[1] = np.float64(self.dataframe_A.shape[0])
                    need_sort_col = True

                if len(other_columns_new) > len(other.dataframe_A.columns):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    # fill missing column
                    other.dataframe_A = other.dataframe_A.reindex(columns=other_columns_new)
                    other.dataframe_PL = other.dataframe_PL.reindex(columns=other_columns_new)
                    other.dataframe_PL.iloc[0, other_shape[1]:] = other.dataframe_PL.iloc[0, 0]
                    other.dataframe_PL.iloc[1] = np.float64(other.dataframe_A.shape[0])
                    need_sort_col = True
            
            if need_sort_index:
                self = self.sort_index()
                other = other.sort_index()
            if need_sort_col:
                self = self.sort_index(axis=1)
                other = other.sort_index(axis=1)
 
        else:
            raise TypeError("Only support aligning CipherSeries and CipherDataFrame.")
        
        return self, other
        
    def _flex_arith_method(self, other, op, axis = "columns", fill_value=None):
        """
        Flexible arithmetic operations with operand alignment.

        Parameters
        ----------
        other : CipherSeries, CipherDataFrame, or scalar

        op : operator
            The operator to apply.

        axis : {0, 1, 'index', 'columns'}, default 'columns'
            The axis to align with.

        fill_value : None or scalar, default None
        """
        axis = self._get_axis_number(axis)       
        # other is CipherArray 
        # try convert CipherArray to CipherDataFrame or CipherSeries
        if isinstance(other, hp.CipherArray) and other.get_cipher_type() != 1:            
            if other.ndim == 1:
                shape = other.cipherShape()
                if axis == 0:
                    if shape[0] == self.shape[0]:
                        other = CipherSeries(other, index=self.index)
                    else:
                        raise ValueError(f"The lenght of right operand is {shape[0]}, but the length of left operand with axis=0 is {self.shape[0]}."
                                         " Can not align.")
                elif axis == 1:
                    if shape[0] == self.shape[1]:
                        other = CipherSeries(other, index=self.columns)
                    else:
                        raise ValueError(f"The lenght of right operand is {shape[0]}, but the length of left operand with axis=1 is {self.shape[1]}."
                                         " Can not align.")
            elif other.ndim == 2: 
                shape = other.cipherShape()
                if shape == self.shape:
                    other = CipherDataFrame(other, index=self.index, columns=self.columns)
                elif shape[0] == self.shape[0] and shape[1] == 1:
                    other = hp.broadcast_to(other, self.shape, output_encrypt_type=1)
                    other = CipherDataFrame(other, index=self.index, columns=self.columns)
                elif shape[0] == 1 and shape[1] == self.shape[1]:
                    other = hp.broadcast_to(other, self.shape, output_encrypt_type=1)
                else:
                    raise ValueError(
                        "Unable to coerce to DataFrame, shape "
                        f"must be {self.shape}: given {other.shape}"
                    )

        # 1. Index align
        # 2. Missing value filling
        # 3. Execute arith
        if isinstance(other, CipherSeries):
            # pandas not support fill_value
            if isinstance(fill_value, hp.CipherArray):
                raise NotImplementedError(f"fill_value {fill_value} not supported.") 

            self, other = self._align_for_op(other, axis=axis)

            c_self = self.to_cipherarray()
            c_other = other.to_cipherarray()
            if axis == 0:
                c_other = c_other.transpose(1)
            c_res = op(c_self, c_other)
            return CipherDataFrame(c_res, index=self.index, columns=self.columns)

        elif isinstance(other, CipherDataFrame):
            self, other = self._align_for_op(other)      

            """
            DataFrame 1:
                  A  B
            row1  1  3
            row2  2  4
            DataFrame 2:
                  B  C
            row2  5  7
            row3  6  8
            DataFrame1.add(DataFrame2, fill_value=0)
                    A    B    C
            row1  1.0  3.0  NaN
            row2  2.0  9.0  7.0
            row3  NaN  6.0  8.0
            """
            # The location where both dataframes are missing is set to nan.
            left, right = ops.fill_binop(self.to_cipherarray(), other.to_cipherarray(), fill_value)
            self = CipherDataFrame(left, index=self.index, columns=self.columns)
            other = CipherDataFrame(right, index=other.index, columns=other.columns)

            c_self = self.to_cipherarray()
            c_other = other.to_cipherarray()
            c_res = op(c_self, c_other)
            return CipherDataFrame(c_res, index=self.index, columns=self.columns)
        
        # other is scalar
        elif isinstance(other, (int, float)) or (isinstance(other, hp.CipherArray) and other.get_cipher_type()==1):
            if isinstance(fill_value, hp.CipherArray) and fill_value.get_cipher_type() == 1:
                self = self.fillna(fill_value)
            c = self.to_cipherarray()
            c = op(c, other)
            return CipherDataFrame(c, columns=self.columns, index=self.index)
    
    def _get_axis_number(self, axis):
        """
        Converts the strings' columns' and 'index' to an axis of numeric type        
        """

        if axis == 'columns':
            axis = 1
        elif axis == 'index':
            axis = 0

        return axis        

    def add(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, operator.add, axis, fill_value)

    def sub(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, operator.sub, axis, fill_value)

    def mul(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, operator.mul, axis, fill_value)
    
    def div(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, operator.truediv, axis, fill_value)

    def radd(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, roperator.radd, axis, fill_value)
    
    def rsub(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, roperator.rsub, axis, fill_value)
    
    def rmul(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, roperator.rmul, axis, fill_value)

    def rdiv(self, other, axis='columns', fill_value=None):
        return self._flex_arith_method(other, roperator.rtruediv, axis, fill_value)     

    def _cmp_method(self, other, op, axis='columns', flex=False):
        """
        A flexible comparison method that either aligns the DataFrame and performs the operation
        or directly performs the operation without alignment, depending on the `flex` parameter.

        Parameters:
        - other: The right-hand side operand (can be scalar, CipherArray, CipherSeries, CipherDataFrame).
        - op: The comparison operator to apply.
        - axis: The axis along which to operate ('columns' or 'index').
        - flex: If True, align the DataFrame before performing the operation; otherwise, do not align.
        
        Returns:
        - DataFrame: Result of the comparison.
        """
        axis = self._get_axis_number(axis)
        
        # 1. Handle scalar or CipherArray operation (same logic for both methods)
        if isinstance(other, (int, float)) or (isinstance(other, hp.CipherArray) and other.get_cipher_type() == 1):
            c = self.to_cipherarray()
            c = op(c, other)
            return pd.DataFrame(c, columns=self.columns, index=self.index)

        # 2. Handle CipherArray (1D)
        elif isinstance(other, hp.CipherArray) and other.ndim == 1:
            l_self = self.dataframe_A.shape[axis]
            l_other = other.cipherShape()[0]
            if l_self == l_other:
                c = self.to_cipherarray()
                if axis == 0:
                    other = other.transpose(1)
                c = op(c, other)
                return pd.DataFrame(c, columns=self.columns, index=self.index)
            else:
                raise ValueError('The length of the two CipherDataFrame must be the same.')

        # 3. Handle CipherArray (2D)
        elif isinstance(other, hp.CipherArray) and other.ndim == 2:
            c = self.to_cipherarray()
            c = op(c, other)
            return pd.DataFrame(c, columns=self.columns, index=self.index)
        
        # 4. Handle CipherSeries (align if flex is True)
        elif isinstance(other, CipherSeries):
            if flex:
                self, other = self._align_for_op(other, axis=axis)
            else:
                # If flex is False, ensure alignment (check if indexes match)
                if not other.index.equals(self.columns):
                    raise ValueError("Operands are not aligned. Do `left, right = left.align(right, axis=1)` before operating.")
            c_self = self.to_cipherarray()
            c_other = other.to_cipherarray()
            if axis == 0:
                c_other = c_other.transpose(1)
            c_res = op(c_self, c_other)
            return pd.DataFrame(c_res, index=self.index, columns=self.columns)

        # 5. Handle CipherDataFrame (align if flex is True)
        elif isinstance(other, CipherDataFrame):
            if flex:
                self, other = self._align_for_op(other, axis=None)
            else:
                if not (self.index.equals(other.index) and self.columns.equals(other.columns)):
                    raise ValueError(
                        "Can only compare identically-labeled (both index and columns) DataFrame objects"
                    )
            
            c_self = self.to_cipherarray()
            c_other = other.to_cipherarray()
            c_res = op(c_self, c_other)
            return pd.DataFrame(c_res, index=self.index, columns=self.columns)
        
        # 6. Raise error if `other` is an unsupported type
        else:
            raise TypeError(f"Unsupported type for comparison: {type(other)}")

    def eq(self, other, axis='columns'):
        return self._cmp_method(other, operator.eq, axis, True)
    
    def ne(self, other, axis='columns'):
        return self._cmp_method(other, operator.ne, axis, True)
    
    def lt(self, other, axis='columns'):
        return self._cmp_method(other, operator.lt, axis, True)
    
    def le(self, other, axis='columns'):
        return self._cmp_method(other, operator.le, axis, True)
    
    def gt(self, other, axis='columns'):
        return self._cmp_method(other, operator.gt, axis, True)
    
    def ge(self, other, axis='columns'):
        return self._cmp_method(other, operator.ge, axis, True)

    # Override binary operators
    
    def __add__(self, other):
        return self._flex_arith_method(other, operator.add)
    
    def __sub__(self, other):
        return self._flex_arith_method(other, operator.sub)
    
    def __mul__(self, other):
        return self._flex_arith_method(other, operator.mul)
    
    def __truediv__(self, other):
        return self._flex_arith_method(other, operator.truediv)
    
    def __radd__(self, other):
        return self._flex_arith_method(other, roperator.radd)
    
    def __rsub__(self, other):
        return self._flex_arith_method(other, roperator.rsub)
    
    def __rmul__(self, other):
        return self._flex_arith_method(other, roperator.rmul)
    
    def __rtruediv__(self, other):
        return self._flex_arith_method(other, roperator.rtruediv)

    def __eq__(self, other):
        return self._cmp_method(other, operator.eq)
    
    def __ne__(self, other):
        return self._cmp_method(other, operator.ne)
    
    def __lt__(self, other):
        return self._cmp_method(other, operator.lt)
    
    def __le__(self, other):
        return self._cmp_method(other, operator.le)
    
    def __gt__(self, other):
        return self._cmp_method(other, operator.gt)
    
    def __ge__(self, other):
        return self._cmp_method(other, operator.ge)

    # Functions that convert instances to various files. 

    def to_excel(self, path, sheet_name='Sheet1', header=True, index=False):
        df = self.to_dataframe()
        df_str = df.map(lambda x: f'{x:.16e}' if isinstance(x, float) else str(x))
        df_str.to_excel(path, sheet_name=sheet_name, header=header, index=index)

    def to_csv(self, path, header=True):
        df = self.to_dataframe()
        df.to_csv(path, header=header, index=False)

    def to_json(self, path):
        df = self.to_dataframe()
        df_str = df.map(lambda x: f'{x:.16e}' if isinstance(x, float) else str(x))
        df_str.to_json(path)

    @property
    def loc(self):
        """
        Access a group of rows and columns by label(s) or a boolean array.
        
        Parameters
        ----------
        key : scalar, slice, list or tuple of labels
        
        Returns
        -------
        CipherArray, CipherSeries or CipherDataFrame
        

        Example:
         >>>cdf = CipherDataFrame(data=np.array([[-6.863455134783327e-222, 1.1443994549670154e-72, -1.6081617951495907e+29, 1.0781824876420455e+87], 
                                                [3.0,                   3.0,                3.0,                3.0], 
                                                [0.23178933351905856, 0.09438296616649205, 0.1612789927674723, 0.07284000130254832], 
                                                [0.1137413270981526, 0.007959673521443002, 0.1401111356282174, 0.0024372481791582836], 
                                                [0.12187587941377741, 0.21759976516752358, 0.0033326023266366037, 0.12500503519950357]]), 
                                                index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])
                                                
         >>>cdf.loc['a']
            _P   -2.427987e+183
            _L    4.000000e+00
            A     2.142645e-01
            B     8.868727e-02
            C     1.609159e-01
            D     6.936588e-02
            Name: a, dtype: float64
         >>>cdf.loc[:, 'A']
            _P   -6.863455e-222
            _L    3.000000e+00
            a     2.317893e-01
            b     1.137413e-01
            c     1.218759e-01
            Name: A, dtype: float64        
         >>>cdf.loc[['a', 'b']]
                            A             B             C             D
            _P -6.863455e-222  1.144399e-72 -1.608162e+29  1.078182e+87
            _L  2.000000e+00  2.000000e+00  2.000000e+00  2.000000e+00
            a   2.317893e-01  9.438297e-02  1.612790e-01  7.284000e-02
            b   1.137413e-01  7.959674e-03  1.401111e-01  2.437248e-03 
         >>>cdf.loc['a', 'A']
          [-6.863455134783327e-222, 0.23178933351905856]         

        """
        
        return _LocIndexer(self)      
    
    @property
    def iloc(self):
        """
        Access a group of rows and columns by Integer(s) or a boolean array.
        
        Parameters
        ----------
        key : scalar, slice, list or tuple of Integer
        
        Returns
        -------
        CipherArray, CipherSeries or CipherDataFrame
        
        Example:
         >>>cdf = CipherDataFrame(data=np.array([[-6.863455134783327e-222, 1.1443994549670154e-72, -1.6081617951495907e+29, 1.0781824876420455e+87], 
                                                [3.0,                   3.0,                3.0,                3.0], 
                                                [0.23178933351905856, 0.09438296616649205, 0.1612789927674723, 0.07284000130254832], 
                                                [0.1137413270981526, 0.007959673521443002, 0.1401111356282174, 0.0024372481791582836], 
                                                [0.12187587941377741, 0.21759976516752358, 0.0033326023266366037, 0.12500503519950357]]), 
                                                index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])
         >>>cdf.iloc[0]
            _P    7.728536e+168
            _L    4.000000e+00
            A     1.970178e-01
            B     8.154858e-02
            C     1.479633e-01
            D     6.378242e-02
            Name: a, dtype: float64
         >>>cdf.iloc[:, 0]
            _P   -6.863455e-222
            _L    3.000000e+00
            a     2.317893e-01
            b     1.137413e-01
            c     1.218759e-01
            Name: A, dtype: float64
         >>>cdf.iloc[[0, 1]]
                            A             B             C             D
            _P -6.863455e-222  1.144399e-72 -1.608162e+29  1.078182e+87
            _L  2.000000e+00  2.000000e+00  2.000000e+00  2.000000e+00
            a   2.317893e-01  9.438297e-02  1.612790e-01  7.284000e-02
            b   1.137413e-01  7.959674e-03  1.401111e-01  2.437248e-03
         >>>cdf.iloc[0, 0]
            [-6.863455134783327e-222, 0.23178933351905856]                                             

        """        

        return _ILOCIndexer(self)

    @property
    def at(self):
        """
        Access a single value for a row/column label pair.
        
        Parameters
        ----------
        row : row label
        col : column label
        
        Returns
        -------
        CipherArray

        Example:
         >>>cdf = CipherDataFrame(data=np.array([[-6.863455134783327e-222, 1.1443994549670154e-72, -1.6081617951495907e+29, 1.0781824876420455e+87], 
                                                [3.0,                   3.0,                3.0,                3.0], 
                                                [0.23178933351905856, 0.09438296616649205, 0.1612789927674723, 0.07284000130254832], 
                                                [0.1137413270981526, 0.007959673521443002, 0.1401111356282174, 0.0024372481791582836], 
                                                [0.12187587941377741, 0.21759976516752358, 0.0033326023266366037, 0.12500503519950357]]), 
                                                index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])
         >>>cdf.at['a', 'A']
         [-6.863455134783327e-222, 0.23178933351905856]
         
        """
        
        return _AtIndexer(self)
    
    @property
    def iat(self):
        """
        Access a single value for a row/column integer pair.
        
        Parameters
        ----------
        row : integer
        col : integer
        
        Returns
        -------
        CipherArray

        Example:
         >>>cdf = CipherDataFrame(data=np.array([[-6.863455134783327e-222, 1.1443994549670154e-72, -1.6081617951495907e+29, 1.0781824876420455e+87], 
                                                [3.0,                   3.0,                3.0,                3.0], 
                                                [0.23178933351905856, 0.09438296616649205, 0.1612789927674723, 0.07284000130254832], 
                                                [0.1137413270981526, 0.007959673521443002, 0.1401111356282174, 0.0024372481791582836], 
                                                [0.12187587941377741, 0.21759976516752358, 0.0033326023266366037, 0.12500503519950357]]), 
                                                index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])
         >>>cdf.at[0, 0]
         [-6.863455134783327e-222, 0.23178933351905856]
         
        """        
        
        return _IAtIndexer(self)
    
    def dropna(self, **kwargs):
        """
        Remove missing values.
        Parameters:
        ----------
        axis : {0 or ‘index’, 1 or ‘columns’}, default 0
        Determine if rows or columns which contain missing values are removed.

        0, or ‘index’ : Drop rows which contain missing values.

        1, or ‘columns’ : Drop columns which contain missing value.

        Only a single axis is allowed.

        how : {‘any’, ‘all’}, default ‘any’
        Determine if row or column is removed from DataFrame, when we have at least one NA or all NA.

        ‘any’ : If any NA values are present, drop that row or column.

        ‘all’ : If all values are NA, drop that row or column.

        thresh : int, optional
        Require that many non-NA values. Cannot be combined with how.

        subset : column label or sequence of labels, optional
        Labels along other axis to consider, e.g. if you are dropping rows these would be a list of columns to include.

        inplace : bool, default False
        Whether to modify the DataFrame rather than creating a new one.

        ignore_index : bool, default False
        If True, the resulting axis will be labeled 0, 1, …, n - 1.

        """

        # default inplace is False.
        A_new = self.dataframe_A.dropna(**kwargs)
        shape = A_new.shape
        # if A_new.columns is empty PL_new will be an empty dataframe
        PL_new = self.dataframe_PL[A_new.columns]

        """
        Because modifying the value of an empty Dataframe row 
        using the loc or iloc method does not change the value of the Dataframe, 
        no special processing is required.        
        """
        PL_new = self.modify_L_for_PL(PL_new, shape[0])                
        res = CipherDataFrame()
        res.dataframe_PL = PL_new
        res.dataframe_A = A_new
        return res

    def modify_L_for_PL(self, PL, L):
        """
        Change the length of the CipherDataFrame using the specified L.
        """

        PL_new = PL.copy()
        PL_new.iloc[1] = np.float64(L)
        return PL_new

    def fillna(self, value, inplace=False):
        """
        Fill NA/NaN values using the specified method.

        Parameters
        ----------
        value : CipherArray, CipherDataFrame, CipherSeries, or dict
            Value to use to fill holes. This value cannot be a list.
        """

        if isinstance(value, CipherDataFrame):
            intersection = self.columns.intersection(value.columns)
            if len(intersection) == 0:
                return self
            elif len(intersection) == 1:
                cs_self = self[intersection]
                cs_value = value[intersection]
                carray = hp.append(cs_self.to_cipherarray(), cs_value.to_cipherarray())
                cs_self = CipherSeries(carray[:len(cs_self)], index=cs_self.index)
                fill = carray.get_base_array()[-len(cs_value):]
                s = pd.Series(fill, index=cs_value.index)
                cs_self.series_A = cs_self.series_A.fillna(s)
                if inplace:
                    self[intersection] = cs_self
                    return self
                else:
                    self_copy = self.copy()
                    self_copy[intersection] = cs_self
                    return self_copy
                
            else:
                self_intersection = self[intersection]
                value_intersection = value[intersection]
                carray = self_intersection.to_cipherarray()
                carray = hp.append(carray, value_intersection.to_cipherarray(), axis=0)
                cdf = CipherDataFrame(carray[:len(self_intersection.index)], columns=intersection, index=self_intersection.index)
                fill = carray.get_base_array()[-len(value_intersection.index):]
                df = pd.DataFrame(fill, index=value_intersection.index, columns=intersection)
                cdf.dataframe_A = cdf.dataframe_A.fillna(df)
                if inplace:
                    self[intersection] = cdf
                    return self
                else:
                    self_copy = self.copy()
                    self_copy[intersection] = cdf
                    return self_copy

        else:
            # When the type of value is dictionary or CipherSeries, the intersection of columns is required.

            if isinstance(value, hp.CipherArray) and value.get_cipher_type() == 1:
                carray = hp.broadcast_to(value, (self.dataframe_A.shape[1],)).cipherReshape(1, -1, output_encrypt_type=1)
                c_self = self.to_cipherarray()
                tmp = hp.append(c_self, carray, axis=0)
                c_self = tmp[0:-1]
                self_new = CipherDataFrame(c_self, columns=self.columns, index=self.index)
                fill = pd.Series(tmp.get_base_array()[-1], index=self_new.columns)
                self_new.dataframe_A = self_new.dataframe_A.fillna(fill)
                if inplace:
                    self.dataframe_PL = self_new.dataframe_PL
                    self.dataframe_A = self_new.dataframe_A
                    return self
                else:
                    return self_new
                
            # Converts the value of the dictionary type to CipherSeries.
            if isinstance(value, dict):
                value = CipherSeries(value)
            
            if isinstance(value, CipherSeries):
                intersection = self.columns.intersection(value.index)
                value_intersection = value[intersection]
                self_intersection = self[intersection]
                # the intersection is empty, then do not fill
                if len(intersection) == 0:
                    return self

                # The intersection has only one element.    
                # self_intersection is CipherSeries, and value_intersection is CipherSeries.
                elif len(intersection) == 1:
                    carray = self_intersection.to_cipherarray()
                    carray = hp.append(carray, value_intersection)
                    cs = CipherSeries(carray[0:-1], index=self.index)
                    fill = carray.get_base_array()[-1]
                    cs.series_A = cs.series_A.fillna(fill)
                    if inplace:
                        self[intersection] = cs
                        return self
                    else:
                        self_copy = self.copy()
                        self_copy[intersection] = cs
                        return self_copy
                else:
                    carray = self_intersection.to_cipherarray()
                    carray = hp.append(carray, value_intersection.to_cipherarray().cipherReshape(1, -1, output_encrypt_type=1), axis=0)
                    cdf = CipherDataFrame(carray[0:-1], columns=intersection, index=self.index)
                    fill = pd.Series(carray.get_base_array()[-1], index=intersection)
                    cdf.dataframe_A = cdf.dataframe_A.fillna(fill)
                    if inplace:
                        self[intersection] = cdf
                        return self
                    else:
                        self_copy = self.copy()
                        self_copy[intersection] = cdf
                        return self_copy

    def isna(self):
        """
        Detect missing values.
        """
        return self.dataframe_A.isna()

    def mean(self, axis=0, skipna=True):
        """
        Return the mean of the values for the requested axis.

        Parameters
        ----------
        axis : {index (0), columns (1), or None}, default 0

        skipna : bool, default True
        Exclude NA/null values. If the entire row/column is NA, the result will be NA.

        """
        c_self = self.to_cipherarray()
        if skipna:
            mean_res = hp.nanmean(c_self, axis=axis)
        else:
            mean_res = hp.mean(c_self, axis=axis)

        if axis == 0:
            index = self.columns
        elif axis == 1:
            index = self.index
        elif axis is None:
            return mean_res

        return CipherSeries(mean_res, index=index)

    def std(self, axis=0, skipna=True, ddof=1):
        """
        Return the standard deviation of the values for the requested axis.

        Parameters
        ----------
        axis : {index (0), columns (1), or None}, default 0

        ddof : int, default 1
        Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of elements.

        skipna : bool, default True
        Exclude NA/null values. If the entire row/column is NA, the result will be NA.

        """
        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanstd(c_self, axis=axis, ddof=ddof)
        else:
            res = hp.std(c_self, axis=axis, ddof=ddof)
        
        if axis==0:
            index = self.columns
        elif axis==1:
            index = self.index
        return CipherSeries(res, index=index)

    def var(self, axis=0, skipna=True, ddof=1):
        """
        Return the variance of the values for the requested axis.

        Parameters
        ----------
        axis : {index (0), columns (1), or None}, default 0

        ddof : int, default 1
        Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of elements.

        skipna : bool, default True
        Exclude NA/null values. If the entire row/column is NA, the result will be NA.
        """
        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanvar(c_self, axis=axis, ddof=ddof)
        else:
            res = hp.var(c_self, axis=axis, ddof=ddof)
        
        if axis==0:
            index = self.columns
        elif axis==1:
            index = self.index
        return CipherSeries(res, index=index)

    def max(self, axis=0, skipna=True):
        """
        Return the maximum of the values over the requested axis.

        Parameters
        ----------
        axis : {index (0), columns (1), or None}, default 0

        skipna : bool, default True
        Exclude NA/null values. If the entire row/column is NA, the result will be NA.
        """
        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanmax(c_self, axis=axis)
        else:
            res = hp.max(c_self, axis=axis)
        
        if axis==0:
            index = self.columns
        elif axis==1:
            index = self.index
        elif axis is None:
            return res
        return CipherSeries(res, index=index)
    
    def min(self, axis=0, skipna=True):
        """
        Return the minimum of the values over the requested axis.
        
        Parameters
        ----------
        axis : {index (0), columns (1), or None}, default 0

        skipna : bool, default True
        Exclude NA/null values. If the entire row/column is NA, the result will be NA.

        """
        if skipna:
            res = hp.nanmin(self.to_cipherarray(), axis=axis)
        else:
            res = hp.min(self.to_cipherarray(), axis=axis)
        
        if axis==0:
            index = self.columns
        elif axis==1:
            index = self.index
        elif axis is None:
            return res
        return CipherSeries(res, index=index)

    def quantile(self, q=0.5, axis=0):
        """
        Return values at the given quantile over requested axis.

        Parameters
        ----------
        q : float or array-like, default 0.5 (50% quantile)

        axis : {0 or ‘index’, 1 or ‘columns’}, default 0

        """
        c_self = self.to_cipherarray()

        if isinstance(q, (list, np.ndarray)):
            for i in range(len(q)):
                if q[i] < 0 or q[i] > 1:
                    raise ValueError("q must be in the interval [0, 1]")
                resi = hp.quantile(c_self, q[i], axis=axis)
                if i == 0:
                    res = resi.cipherReshape(1, -1, output_encrypt_type=1)
                else:
                    res = hp.append(res, resi.cipherReshape(1, -1, output_encrypt_type=1), axis=0)
            
            if axis==0:
                columns = self.columns
            elif axis==1:
                columns = self.index
            return CipherDataFrame(res, index=q, columns=columns)
        else:
            if q < 0. or q > 1.:
                raise ValueError("q must be in the interval [0, 1]")            
            res = hp.quantile(c_self, q, axis=axis)
            if axis==0:
                index = self.columns
            elif axis==1:
                index = self.index
            return CipherSeries(res, index=index, name=q)
        
    def cov(self):
        """
        Compute pairwise covariance of columns, excluding NA/null values.
        """
        c_self = self.to_cipherarray()
        res = hp.cov(c_self.transpose(1))
        return CipherDataFrame(res, columns=self.columns, index=self.columns)

    def shift(self, periods=1, freq=None, fill_value=None):
        """
        Shift index by desired number of periods.

        Parameters
        ----------
        periods : int
        Number of periods to shift. Can be positive or negative.

        freq : DateOffset, timedelta, or offset alias string, optional

        fill_value : CipherArray, optional

        """
        self = self.copy()
        self.dataframe_A = self.dataframe_A.shift(periods=periods, freq=freq)

        if fill_value is not None:
            if isinstance(fill_value, hp.CipherArray):
                if fill_value.get_cipher_type() == 1:
                    self = self.fillna(fill_value)
                else:
                    raise ValueError("fill_value must be a cipherarray scalar.")
            else:
                raise ValueError("fill_value must be a cipherarray scalar.")
        return self


    def pct_change(self, periods=1):
        """
        Fractional change between the current and a prior element.

        Parameters
        ----------
        periods : int, default 1
        Periods to shift for forming percent change.

        """
        # Create a copy of self to avoid modifying the original object.
        self_shifted = self.shift(periods=periods)
        return self / self_shifted - 1

    def cumsum(self, axis=0, skipna=True):
        """
        Return cumulative sum over a DataFrame or Series axis.

        Parameters
        ---------------
        axis: {0 or ‘index’, 1 or ‘columns’}, default 0
        The index or the name of the axis. 0 is equivalent to None or ‘index’. For Series this parameter is unused and defaults to 0.

        skipna: bool, default True
        Exclude NA/null values. If an entire row/column is NA, the result will be NA.
        skipnan 

        Returns:
        ---------------
        DataFrame
        Return cumulative sum of DataFrame.        
        """

        isnan = self.isna()

        axis = self._get_axis_number(axis)
        c_self = self.to_cipherarray()

        if skipna:
            res = hp.nancumsum(c_self, axis=axis)
        else:
            res = hp.cumsum(c_self, axis=axis)
        cs = CipherDataFrame(res, columns=self.columns, index=self.index)
        cs.dataframe_A = cs.dataframe_A.where(~isnan, np.nan)
        return cs
    
    def join(self, other, how='left', lsuffix='', rsuffix='', sort=False):
        """
        Join columns of another DataFrame.

        Parameters
        -------------
        other: CipherDataFrame or CipherSeries

        how: {'left', 'right', 'outer', 'inner'}, default 'left'

        lsuffix: str, default ''
        Suffix to use from left frame’s overlapping columns.

        rsuffix: str, default ''
        Suffix to use from right frame’s overlapping columns.

        sort: bool, default False
        Order result DataFrame lexicographically by the join key. 
        If False, the order of the join key depends on the join type (how keyword).

        """

        if isinstance(other, CipherSeries):

            if other.series_A.name is None:
                raise ValueError("Other CipherSeries must have a name.")

            else:

                A_new = self.dataframe_A.join(other.series_A, how=how, lsuffix=lsuffix, rsuffix=rsuffix, sort=sort)  
                PL_new = self.dataframe_PL.join(other.series_PL, lsuffix=lsuffix, rsuffix=rsuffix)
                PL_new = self.modify_L_for_PL(PL_new, len(A_new))
                res = CipherDataFrame()
                res.dataframe_A = A_new
                res.dataframe_PL = PL_new
                return res
            
        if isinstance(other, CipherDataFrame):
            A_new = self.dataframe_A.join(other.dataframe_A, how=how, lsuffix=lsuffix, rsuffix=rsuffix, sort=sort)
            PL_new = self.dataframe_PL.join(other.dataframe_PL, lsuffix=lsuffix, rsuffix=rsuffix)
            PL_new = self.modify_L_for_PL(PL_new, len(A_new))
            res = CipherDataFrame()
            res.dataframe_A = A_new
            res.dataframe_PL = PL_new
            return res

    def drop_duplicates(
            self,
            subset: Hashable | Sequence[Hashable] | None = None,
            keep: str = 'first',
            inplace: bool = False,
            ignore_index: bool = False,
        ):
        """

        Return CipherDataFrame with duplicate rows removed.

        Considering certain columns is optional. Indexes, including time indexes
        are ignored.

        Parameters
        ----------
        subset : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns.
        keep : {'first', 'last', ``False``}, default 'first'
            Determines which duplicates (if any) to keep.

            - 'first' : Drop duplicates except for the first occurrence.
            - 'last' : Drop duplicates except for the last occurrence.
            - ``False`` : Drop all duplicates.

        inplace : bool, default ``False``
            Whether to modify the CipherDataFrame rather than creating a new one.
        ignore_index : bool, default ``False``
            If ``True``, the resulting axis will be labeled 0, 1, …, n - 1.

        Returns
        -------
        CipherDataFrame or None
            CipherDataFrame with duplicates removed or None if ``inplace=True``.

        """

        from .reshape import _group_and_replace

        arr = self.dataframe_A.to_numpy()
        arr_new = _group_and_replace(arr)
        # modify inplace
        if inplace:
            self.dataframe_A = pd.DataFrame(arr_new, index=self.dataframe_A.index, columns=self.dataframe_A.columns)
            self.dataframe_A.drop_duplicates(subset=subset, keep=keep, inplace=True, ignore_index=ignore_index)
            self.dataframe_PL = self.modify_L_for_PL(self.dataframe_PL, len(self.dataframe_A))
            return 
        self = self.copy()
        self.dataframe_A = pd.DataFrame(arr_new, index=self.dataframe_A.index, columns=self.dataframe_A.columns)
        self.dataframe_A = self.dataframe_A.drop_duplicates(subset=subset, keep=keep, inplace=inplace, ignore_index=ignore_index)
        self.dataframe_PL = self.modify_L_for_PL(self.dataframe_PL, len(self.dataframe_A))
        return self

    def groupby(self, level=0):
        """
        Group CipherDataFrame by level.

        Parameters
        ----------
        level : int
        """
        from .groupby import CipherDataFrameGroupBy
        return CipherDataFrameGroupBy(self, level)