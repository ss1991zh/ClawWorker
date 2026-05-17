import operator
import pandas as pd
import numpy as np
import henumpy as hp
from pandas._libs import lib as  pd_lib
from pandas.core import ops as pd_ops
from pandaseal.core import roperator
from pandaseal.core import ops
from .indexing import _LocIndexer, _ILOCIndexer, _AtIndexer, _IAtIndexer



class CipherSeries:
    """
    
    """
    def __init__(self, data=None, index=None, copy=False, name=None):
        
        if data is None:

            empty = hp.empty_array().get_base_array()[:2]
            PL = pd.Series(empty, index=['_P', '_L'], copy=copy, name=name)
            self.series_A = pd.Series(name=name)
            self.series_PL = PL
            return 

        
        if isinstance(data, dict):
            keys = list(data.keys())
            values = list(data.values())
            # Check whether the values are scalar CipherArray
            for v in values:
                if not isinstance(v, hp.CipherArray) or v.get_cipher_type() != 1:
                    raise ValueError("Values must be scalar CipherArray.")
            carray = hp.empty_array()
            for v in values:
                carray = hp.append(carray, v)
            data = carray
            index = keys
        
        if isinstance(data, hp.CipherArray):
            data = data.get_base_array()
            copy = True  # Ensure that the source data is not modified.
        index_name = None
        if isinstance(index, pd.Index):
            index_name = index.name        
        self.series_PL = pd.Series(data[:2], index=pd.Index(['_P', '_L'], name=index_name), copy=copy, name=name)
        self.series_A  = pd.Series(data[2:], index=index, copy=copy, name=name)
    
    def set_name(self, name):
        self.series_PL.name = name
        self.series_A.name = name

    def copy(self, deep=True):
        """
        Make a copy of this object’s indices and data. default deep copy.

        Parameters
        ----------
        deep : bool, default True
            If True, make a new copy. Otherwise, return a view of the underlying data.

        """

        cs = CipherSeries()
        cs.series_PL = self.series_PL.copy(deep)
        cs.series_A  = self.series_A.copy(deep)

        return cs

    def __str__(self):
        if self.series_A.empty: return self.series_PL.__str__()
        tmp = pd.concat([self.series_PL, self.series_A], axis=0)
        return tmp.__str__()
    
    def __getitem__(self, key):

        """
         Get elements from a series using an index or slice.
        
         Parameters
         ----------
         key : scalar, or list

         Return
         -------
         CipherArray or CipherSeries
         
         Example:
         >>> cs = CipherSeries([-1.2294691318574239e+87, 8., 3., 4., 5., 6., 7., 8., 9., 10.])
         >>> cs[2]
         [-1.2294691318574239e+87, 5.]
         >>> c[[1, 2]]
         _P  -1.2294691318574239e+87
         _L  2.
         1   4.
         2   5.
         dtype: float64

        """
        
        A = self.series_A[key]

        if isinstance(A, pd.Series):
            A_value = A.tolist()
            A_index = A.index
            P = self.series_PL['_P']
            return CipherSeries([P, len(A)] + A_value, index=A_index, name=self.series_A.name)
        # scalar
        else:
            return hp.CipherArray([self.series_PL['_P'], A])
    
    def __setitem__(self, key, value):

        """
         Set elements in a series using an index.
         
         Parameters
         ----------
         key : scalar
         value : CipherArray
         
         Return
         -------
         None
         
         Example:
         >>> cs = CipherSeries([2.3863250134255973e-53, 7.0, 0.45843110386564656, 0.6876466557984698, 0.9168622077312931, 
                                1.1460777596641163, 1.3752933115969397, 1.6045088635297629, 1.8337244154625862])
         >>> cs[2] = CipherArray([5.410267508602945e-246, 0.5027097006680652])
         >>> cs
         _P  1.672790860595632e+188
         _L  7.0
         0   0.41500961909950296
         1   0.6225144286492543
         2   0.4793361100599258
         3   1.0375240477487568
         4   1.2450288572985084
         5   1.4525336668482598
         6   1.6600384763980118
         dtype: float64
         
        """
        
        if not isinstance(value, hp.CipherArray):
            raise TypeError("The value must be a CipherArray.")

        if pd_lib.is_scalar(key):
            ca = self.to_cipherarray()
            # Get the numeric index of the key
            pos = self.series_A.index.get_loc(key)
            ca[pos] = value
            
            self.copy(CipherSeries(ca, name=self.series_A.name, index=self.series_A.index), False)
        else:
            raise TypeError(f"Enter an illegal index type :{type(key)}. Scalar is currently supported.")

    def to_series(self):
        return pd.concat([self.series_PL, self.series_A], axis=0)

    def to_cipherarray(self):
        """
        Convert the CipherSeries to a CipherArray.
        
        Return
        -------
        CipherArray

        Example:
         >>> cs = CipherSeries([-1.2294691318574239e+87, 8., 3., 4., 5., 6., 7., 8., 9., 10.], name='example')
         >>> cs
         _P  -1.2294691318574239e+87
         _L  8.
         0   3.
         1   4.
         2   5.
         3   6.
         4   7.
         5   8.
         6   9.
         7   10.
         name='example', dtype: float64
         >>> c = cs.to_cipherarray()
         >>> c
         [-1.2294691318574239e+87, 8., 3., 4., 5., 6., 7., 8., 9., 10.]
         
        """
        if len(self.series_A) == 0:
            return hp.empty_array()
        return hp.CipherArray(self.series_PL.to_list() + self.series_A.to_list())
    
    def to_cipherdataframe(self):
        """
        Convert the CipherSeries to a CipherDataFrame.
        
        Return
        -------
        CipherDataFrame
        """
        from .cipherframe import CipherDataFrame

        if len(self.series_A) == 0:
            if self.series_A.name is None:
                return CipherDataFrame()
            else:
                if self.series_A.name is not None:
                    return CipherDataFrame(columns=[self.series_A.name])
        if self.series_A.name is None:
            columns = None
        else:
            columns = [self.series_A.name]
        return CipherDataFrame(self.to_cipherarray(), index=self.series_A.index, columns=columns)

    def head(self, n: int = 5):
        """
        Return the first n rows of the CipherSeries.
        
        Parameters
        ----------
        n : int, default 5
            Number of rows to return.

        Return
        -------
        same type as self

        Examples
         >>> cs = CipherSeries([2.3863250134255973e-53, 7.0, 0.45843110386564656, 0.6876466557984698, 0.9168622077312931, 
                                1.1460777596641163, 1.3752933115969397, 1.6045088635297629, 1.8337244154625862])
         >>> cs.head()
            _P    2.386325e-53
            _L    5.000000e+00
            0     4.584311e-01
            1     6.876467e-01
            2     9.168622e-01
            3     1.146078e+00
            4     1.375293e+00
            dtype: float64
        """

        _A = self.series_A.head(n)
        res = CipherSeries()
        if _A.size == 0:
            res.series_A = _A
            return res
        pl = self.modify_L_for_series_PL(self.series_PL, _A.size)
        res.series_A = _A
        res.series_PL = pl
        return res

    def tail(self, n: int = 5):
        """
        Return the last n rows of the CipherSeries.
        
        Parameters
        ----------
        n : int, default 5
            Number of rows to return.

        Return
        -------
        same type as self

        Examples
         >>> cs = CipherSeries([2.3863250134255973e-53, 7.0, 0.45843110386564656, 0.6876466557984698, 0.9168622077312931, 
                                1.1460777596641163, 1.3752933115969397, 1.6045088635297629, 1.8337244154625862])
         >>> cs.tail()
            _P    2.386325e-53
            _L    5.000000e+00
            2     9.168622e-01
            3     1.146078e+00
            4     1.375293e+00
            5     1.604509e+00
            6     1.833724e+00
            dtype: float64
        """

        _A = self.series_A.tail(n)
        res = CipherSeries()
        if _A.size == 0:
            res.series_A = _A
            return res
        pl = self.modify_L_for_series_PL(self.series_PL, _A.size)
        res.series_A = _A
        res.series_PL = pl
        return res        

    @property
    def index(self):
        return self.series_A.index

    def sort_values(
        self, 
        *, 
        axis=0, 
        ascending=True, 
        inplace=False, 
        kind='quicksort', 
        na_position='last', 
        ignore_index=False, 
        key=None
        ):
        """
        Sort the CipherSeries by the values.

        Parameters
        ----------

        axis : {0 or 'index'}, default 0
        ascending : bool, default True
            Whether to sort ascending or descending.

        inplace : bool, default False
            If True, perform operation in-place.

        kind : {'quicksort', 'mergesort', 'heapsort'}, default 'quicksort'
            Choice of sorting algorithm.

        na_position : {'first', 'last'}, default 'last'
            Argument 'first' puts NaNs at the beginning, 'last' puts them at the end.

        ignore_index : bool, default False
            Sort the index after sorting the values.
        """
        if inplace:
            self.series_A.sort_values(
                            axis=axis, 
                            ascending=ascending, 
                            inplace=True, 
                            kind=kind, 
                            na_position=na_position, 
                            ignore_index=ignore_index, 
                            key=key)
            return self
        else:
            sa = self.series_A.sort_values(
                                axis=axis, 
                                ascending=ascending, 
                                inplace=False, 
                                kind=kind, 
                                na_position=na_position, 
                                ignore_index=ignore_index, 
                                key=key)
            res = self.copy()
            res.series_A = sa
            return res

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
        key=None
    ):
        """
        Sort the CipherSeries by the index.
        
        Parameters
        ----------
        axis : {0 or 'index'}, default 0
            Axis to sort by.

        level : int or level name or list of ints or list of level names

        ascending : bool, default True

        inplace : bool, default False

        kind : {'quicksort', 'mergesort', 'heapsort'}, default 'quicksort'

        na_position : {'first', 'last'}, default 'last'

        """
        if inplace:
            self.series_A.sort_index(
                axis=axis, 
                level=level, 
                ascending=ascending, 
                inplace=inplace, 
                kind=kind, 
                na_position=na_position, 
                sort_remaining=sort_remaining, 
                key=key)
            return None
        else: # inplace = False
            res = CipherSeries()
            res.series_A = self.series_A.sort_index(
                axis=axis, 
                level=level, 
                ascending=ascending, 
                inplace=inplace, 
                kind=kind, 
                na_position=na_position, 
                sort_remaining=sort_remaining, 
                key=key)
            res.series_PL = self.series_PL.copy()
            return res


    @property
    def shape(self):
        """'
        Return a tuple representing the dimensionality of the CipherSeries.

        """
        return (self.series_A.size,)
    
    @property
    def ndim(self):
        return 1
    
    @property
    def size(self):
        """
        Return an int representing the number of elements in this object.
        """
        return self.series_A.size
    
    def align(self, other, join='outer', axis=0, fill_value=None):
        """
        Align two objects along their index.
        Only support join='outer' for now.
        1. union index
        2. fill data
        3. sort index
        """

        if join != 'outer':
            raise NotImplementedError("Only support join='outer' for now.")
        
        if isinstance(other, CipherSeries):
            index_new_self = self.series_A.index.union(other.series_A.index, False)
            index_new_other = other.series_A.index.union(self.series_A.index, False)

            if len(index_new_self) > len(self.series_A.index):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    self.series_A = self.series_A.reindex(index_new_self)
                    self.series_PL.iloc[1] = np.float64(len(index_new_self))
                
            if len(index_new_other) > len(other.series_A.index):
                # Prevents incorrect modifications to the original object.
                other = other.copy()
                other.series_A = other.series_A.reindex(index_new_other)
                other.series_PL.iloc[1] = np.float64(len(index_new_other))                                 
            
            if not self.series_A.index.equals(other.series_A.index):
                self = self.sort_index()
                other = other.sort_index()
        
        else:
            from .cipherframe import CipherDataFrame
            if isinstance(other, CipherDataFrame):
                # support axis=0 for now.
                index_new_self = self.series_A.index.union(other.dataframe_A.index, False)
                index_new_other = other.dataframe_A.index.union(self.series_A.index, False)

                if len(index_new_self) > len(self.series_A.index):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    self.series_A = self.series_A.reindex(index_new_self)
                    self.series_PL.iloc[1] = np.float64(len(index_new_self))
                    self = self.sort_index()

                if len(index_new_other) > len(other.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.dataframe_A = other.dataframe_A.reindex(index_new_other)
                    other.dataframe_PL.iloc[1] = np.float64(len(index_new_other))
                    other = other.sort_index()

            else:
                raise TypeError("Only support aligning CipherSeries and CipherDataFrame.")
            
        if fill_value is not None:
            if isinstance(fill_value, hp.CipherArray) and fill_value.get_cipher_type() == 1:
                self = self.fillna(fill_value)
                other = other.fillna(fill_value)
            else:
                raise ValueError(f"Fill_value must be None or a scalar CipherArray, but got {type(fill_value)}.")
            
        return self, other
    
    def _align_for_op(self, other, join='outer', axis=0):
        """
        Align the two operands by index for subsequent evaluation.
        """

        if join != 'outer':
            raise NotImplementedError("Only support join='outer' for now.")
        
        if isinstance(other, CipherSeries):
            index_new_self = self.series_A.index.union(other.series_A.index, False)
            index_new_other = other.series_A.index.union(self.series_A.index, False)

            if len(index_new_self) > len(self.series_A.index):
                # Prevents incorrect modifications to the original object.
                self = self.copy()
                self.series_A = self.series_A.reindex(index_new_self)
                self.series_PL.iloc[1] = np.float64(len(index_new_self))             
            
            if len(index_new_other) > len(other.series_A.index):
                # Prevents incorrect modifications to the original object.
                other = other.copy()
                other.series_A = other.series_A.reindex(index_new_other)
                other.series_PL.iloc[1] = np.float64(len(index_new_other))                                
            
            if not self.series_A.index.equals(other.series_A.index):
                self = self.sort_index()
                other = other.sort_index()
        
        else:
            from .cipherframe import CipherDataFrame
            if isinstance(other, CipherDataFrame):
                # support axis=0 for now.
                index_new_self = self.series_A.index.union(other.dataframe_A.index, False)
                index_new_other = other.dataframe_A.index.union(self.series_A.index, False)

                if len(index_new_self) > len(self.series_A.index):
                    # Prevents incorrect modifications to the original object.
                    self = self.copy()
                    self.series_A = self.series_A.reindex(index_new_self)
                    self.series_PL.iloc[1] = np.float64(len(index_new_self))
                    self = self.sort_index()

                if len(index_new_other) > len(other.dataframe_A.index):
                    # Prevents incorrect modifications to the original object.
                    other = other.copy()
                    other.dataframe_A = other.dataframe_A.reindex(index_new_other)
                    other.dataframe_PL.iloc[1] = np.float64(len(index_new_other))
                    other = other.sort_index()

            else:
                raise TypeError("Only support aligning CipherSeries and CipherDataFrame.")

        return self, other    
    
    def _binop(self, other, op, fill_value=None):
        """
        Perform generic binary operation with optional fill value.

        Parameters
        ----------
        other : Series
        func : binary operator
        fill_value : CipherFloat

        Returns
        -------
        Series
        """

        if not self.index.equals(other.index):
            self, other = self._align_for_op(other)
        
        left, right = ops.fill_binop(self.to_cipherarray(), other.to_cipherarray(), fill_value)
        result = op(left, right)
        result_name = pd_ops.get_op_result_name(self.series_A, other.series_A)
        return CipherSeries(result, name=result_name, index=self.series_A.index)
    
    def _flex_arith_method(self, other, op, fill_value=None):        
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

        if isinstance(other, hp.CipherArray):
            if other.ndim == 1:
                # Convert scalar to 1d CipherArray.
                if other.get_cipher_type() == 1:
                    other = hp.full(self.size, other)

                if other.cipherShape()[0] == self.size:
                    other = CipherSeries(other, index=self.index)
                    return self._binop(other, op, fill_value)
                else:
                    raise ValueError("Lengths must be equal")
            else:
                raise ValueError("Only Support scalar or 1d CipherArray, but 2d CipherArray are given.")
        
        elif isinstance(other, CipherSeries):
            return self._binop(other, op, fill_value)
        elif isinstance(other, (int, float)):
            if fill_value is not None and fill_value.get_cipher_type() == 1:
                if np.isnan(other):
                    c_self = self.to_cipherarray()
                    result = op(c_self, fill_value)
                    return CipherSeries(result, name=self.series_A.name, index=self.series_A.index)
            
            c_self = self.to_cipherarray()
            result = op(c_self, other)
            return CipherSeries(result, name=self.series_A.name, index=self.series_A.index)

    def add(self, other, fill_value=None):
        return self._flex_arith_method(other, operator.add, fill_value)

    def sub(self, other, fill_value=None):
        return self._flex_arith_method(other, operator.sub, fill_value)

    def mul(self, other, fill_value=None):
        return self._flex_arith_method(other, operator.mul, fill_value)
    
    def div(self, other, fill_value=None):
        return self._flex_arith_method(other, operator.truediv, fill_value)

    def radd(self, other, fill_value=None):
        return self._flex_arith_method(other, roperator.radd, fill_value)

    def rsub(self, other, fill_value=None):
        return self._flex_arith_method(other, roperator.rsub, fill_value)
    
    def rmul(self, other, fill_value=None):
        return self._flex_arith_method(other, roperator.rmul, fill_value)
    
    def rdiv(self, other, fill_value=None):
        return self._flex_arith_method(other, roperator.rtruediv, fill_value)
      
    def _cmp_method(self, other, op):
        if isinstance(other, (int, float)) or (isinstance(other, hp.CipherArray) and other.get_cipher_type() == 1):
            c_self = self.to_cipherarray()
            c_res = op(c_self, other)
        elif isinstance(other, hp.CipherArray) and other.ndim == 1:
            if self.size == other.cipherShape()[0]:
                c_self = self.to_cipherarray()
                c_res = op(c_self, other)
            else:
                raise ValueError("Length of CipherArray must be equal to the length of CipherSeries.")
        elif isinstance(other, CipherSeries):
            if not self.index.equals(other.index):
                raise ValueError("Can only compare identically-labeled Series objects")
            c_self = self.to_cipherarray()
            c_other = other.to_cipherarray()
            c_res = op(c_self, c_other)
        return pd.Series(c_res, name=self.series_A.name, index=self.series_A.index)
    
    def eq(self, other):
        return self._cmp_method(other, operator.eq)
    
    def ne(self, other):
        return self._cmp_method(other, operator.ne)
    
    def lt(self, other):
        return self._cmp_method(other, operator.lt)

    def le(self, other):
        return self._cmp_method(other, operator.le)

    def ge(self, other):
        return self._cmp_method(other, operator.ge)

    def gt(self, other):
        return self._cmp_method(other, operator.gt)

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
    
    def __ge__(self, other):
        return self._cmp_method(other, operator.ge)
    
    def __gt__(self, other):
        return self._cmp_method(other, operator.gt)

    # Functions that convert instances to various files. 

    def to_excel(self, path, sheet_name='Sheet1', header=True, index=False):
        s = self.to_series()
        s_str = s.map(lambda x: f'{x:.16e}' if isinstance(x, float) else str(x))
        s_str.to_excel(path, sheet_name=sheet_name, header=header, index=index)

    def to_csv(self, path, header=True):
        s = self.to_series()
        s.to_csv(path, header=header, index=False)

    def to_json(self, path):
        s = self.to_series()
        s = s.map(lambda x: f'{x:.16e}' if isinstance(x, float) else str(x))
        s.to_json(path)
    
    @property
    def loc(self):
        """
        Access a group of rows by label(s) or a boolean array.
        
        Parameters
        ----------
        key : scalar, slice, or list
        
        Return
        -------
        value : CipherArray or CipherSeries

        Example:
         >>> c = CipherSeries([-1.2294691318574239e+87, 8., 3., 4., 5., 6., 7., 8., 9., 10.])
         >>> c.loc[2]
         [-1.2294691318574239e+87, 5.]
         >>> c.loc[[1, 2]]
         _P  -1.2294691318574239e+87
         _L  2.
         1   4.
         2   5.
         dtype: float64
         >>> c.loc[2:4]
         _P  -1.2294691318574239e+87
         _L  3.
         1   4.
         2   5.
         3   6.
         dtype: float64
         
        """
        
        return _LocIndexer(self)
    
    @property
    def iloc(self):
        """
        Get elements from a CipherSeries using integer position.
        
        Parameters
        ----------
        key : scalar, slice, or list
        
        Return
        -------
        value : CipherArray or CipherSeries
        
        Example:
        >>> c = CipherSeries([-1.2294691318574239e+87, 8., 3., 4., 5., 6., 7., 8., 9., 10.])
        >>> c.iloc[2]
        [-1.2294691318574239e+87, 5.]
        >>> c.iloc[[1, 2]]
        _P  -1.2294691318574239e+87
        _L  2.
        1   4.
        2   5.
        dtype: float64
        >>> c.iloc[2:4]
        _P  -1.2294691318574239e+87
        _L   2.
        2    5.
        3    6.
        dtype: float64

        """
        
        return _ILOCIndexer(self)
    
    @property
    def at(self):
        
        """
        Access a single value for a row by label.
        
        Parameters
        ----------
        key : scalar
        
        Return
        -------
        value : CipherArray
        
        Example:
        >>> c = CipherSeries([-1.2294691318574239e+87, 8., 3., 4., 5., 6., 7., 8., 9., 10.])
        >>> c.at[2]
        [-1.2294691318574239e+87, 5.]

        """

        return _AtIndexer(self)

    @property
    def iat(self):
        
        """
        Access a single value for a row by integer position.
        
        Parameters
        ----------
        key : scalar
        
        Return
        -------
        value : CipherArray
        
        Example:
        >>> c = CipherSeries([-1.2294691318574239e+87, 8., 3., 4., 5., 6., 7., 8., 9., 10.])
        >>> c.iat[2]
        [-1.2294691318574239e+87, 5.]
        
        """
        
        return _IAtIndexer(self)

    def dropna(self, **kwargs):
        """
        Return a new CipherSeries with missing values removed.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments for pandas.Series.dropna.

        """
        A_new = self.series_A.dropna(**kwargs)
        res = CipherSeries()
        res.series_A = A_new
        res.series_PL = self.modify_L_for_series_PL(self.series_PL, A_new.size)
        return res

    def modify_L_for_series_PL(self, series_PL, length):
        """
        Change the length of the CipherDataFrame using the specified L.
        """

        pl = series_PL.copy()
        pl.iat[1] = length    
        return pl

    def fillna(self, value, inplace=False):
        """
        Fill NA/NaN values using the specified method.

        Parameters
        ----------
        value : CipherArray, CipherSeries, or dict
            Value to use to fill holes. This value cannot be a list.

        inplace : bool, default False
            If True, fill in-place. Otherwise, return a new object.
        """

        if isinstance(value, hp.CipherArray) and value.get_cipher_type() == 1:
            c_new = hp.append(self.to_cipherarray(), value)
            cs = CipherSeries(c_new[:-1], name=self.series_A.name, index=self.series_A.index)
            cs.series_A = cs.series_A.fillna(c_new.get_base_array()[-1])
            if inplace:
                self.series_A = cs.series_A
                self.series_PL = cs.series_PL
                return self
            else:
                return cs

        if isinstance(value, dict):
            value = CipherSeries(value)

        if isinstance(value, CipherSeries):
            c_new = hp.append(self.to_cipherarray(), value.to_cipherarray())
            cs = CipherSeries(c_new[:self.size], name=self.series_A.name, index=self.series_A.index)
            cs_value = CipherSeries(c_new[self.size:], name=value.series_A.name, index=value.series_A.index)
            cs.series_A = cs.series_A.fillna(cs_value.series_A)
            if inplace:
                self.series_A = cs.series_A
                self.series_PL = cs.series_PL
                return self
            else:
                return cs

    def isna(self):
        """
        Detect missing values.
        """
        return self.series_A.isna()
    
    def sum(self, axis=0, skipna=True):
        """
        Return the sum of the values for the requested axis.

        Parameters
        ----------
        axis : {0, 1, None}, default 0
            Axis along which to operate.

        skipna : bool, default True
            Exclude NA/null values. If the entire Series is NA, the result will be NA.
        """
        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nansum(c_self)
        else:
            res = hp.sums(c_self)
        
        return res        
    
    def mean(self, axis=0, skipna=True):
        """
        Return the mean of the values for the requested axis.

        Parameters
        ----------
        axis : {0, 1, None}, default 0
            Axis along which to operate.

        skipna : bool, default True
            Exclude NA/null values. If the entire Series is NA, the result will be NA.
        """
        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanmean(c_self)
        else:
            res = hp.mean(c_self)
        
        return res
    
    def std(self, axis=0, skipna=True, ddof=1):
        """
        Return the standard deviation of the values for the requested axis.

        Parameters
        ----------
        axis : {0, 1, None}, default 0
            Axis along which to operate.
            
        skipna : bool, default True
            Exclude NA/null values. If the entire Series is NA, the result will be NA.
        
        ddof : int, default 1
            Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of elements.
        """

        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanstd(c_self, ddof=ddof)
        else:
            res = hp.std(c_self, ddof=ddof)
        return res
    
    def var(self, axis=0, skipna=True, ddof=1):
        """
        Return the variance of the values for the requested axis.

        Parameters
        ----------
        axis : {0, 1, None}, default 0
            Axis along which to operate.

        skipna : bool, default True
            Exclude NA/null values. If the entire Series is NA, the result will be NA.

        ddof : int, default 1
            Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of elements.
        """
        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanvar(c_self, ddof=ddof)
        else:
            res = hp.var(c_self, ddof=ddof)
        return res
    
    def max(self, axis=0, skipna=True):
        """
        Return the maximum of the values for the requested axis.

        Parameters
        ----------
        axis : {0, 1, None}, default 0
            Axis along which to operate.

        skipna : bool, default True

        """

        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanmax(c_self)
        else:
            res = hp.max(c_self)
        return res
    
    def min(self, axis=0, skipna=True):
        """
        Return the minimum of the values for the requested axis.

        Parameters
        ----------

        axis : {0, 1, None}, default 0
            Axis along which to operate.
        
        skipna : bool, default True

        """

        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nanmin(c_self)
        else:
            res = hp.min(c_self)
        return res
    
    def quantile(self, q=0.5, axis=0):
        """
        Return value at the given quantile.

        Parameters
        ----------
        q : float or array-like, defaule=0.5
            0 <= q <= 1, the quantile(s) to compute.
        
        axis : {0, 1}, default 0
            The axis along which the quantiles are computed.
        """
        c_self = self.to_cipherarray()
        if isinstance(q, (list, np.ndarray)):
            res = hp.empty_array()
            for i in q:
                res = hp.append(res, hp.quantile(c_self, i))
            return CipherSeries(res, index=q)
        else:
            res = hp.quantile(c_self, q)
            return res
        
    def cov(self, other):
        """
        Return covariance of series with other series.

        Parameters
        ----------
        other : CipherSeries
            Series to use for covariance calculation. If not supplied, defaults to self.
        
        """
        c_self = self.to_cipherarray()
        if isinstance(other, CipherSeries):
            c_other = other.to_cipherarray()
        else:
            raise TypeError("Only support CipherSeries.")
        return hp.cov(c_self, c_other)[0, 1]
    
    def shift(self, periods=1, freq=None, fill_value=None):
        """
        Shift index by desired number of time steps.

        Parameters
        ----------
        periods : int
            Number of periods to move. Can be positive or negative.
        
        freq : DateOffset, timedelta, or offset alias string, optional
            Frequency to use for shifting.
        
        fill_value : CipherArray, default None
        """

        # Create a copy of self to avoid modifying the original object.
        self = self.copy()
        res_shift = self.series_A.shift(periods=periods, freq=freq)
        PL = self.series_PL
        
        if isinstance(res_shift, pd.DataFrame):
            # Series.shift is a DataFrame.
            from .cipherframe import CipherDataFrame

            self = CipherDataFrame()
            self.dataframe_A = res_shift
            self.dataframe_PL = pd.concat([PL]*len(res_shift.columns), axis=1)
            self.dataframe_PL.columns = res_shift.columns
        else:
            self.series_A = res_shift
        
        if fill_value is not None:
            if isinstance(fill_value, hp.CipherArray):
                if fill_value.get_cipher_type() != 1:
                    raise ValueError("fill_value must be a cipher scalar.")
                self = self.fillna(fill_value) 
            else:
                raise ValueError("fill_value must be a cipher scalar.")       
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
        Return cumulative sum of the values for the requested axis.

        Parameters
        ----------
        axis : {0, 1}, default 0
            Axis along which to operate.
        
        skipna : bool, default True
            Exclude NA/null values. If the entire Series is NA, the result will be NA.
        
        Returns
        -------
        CipherSeries
        """       
        isnan = self.isna()

        c_self = self.to_cipherarray()
        if skipna:
            res = hp.nancumsum(c_self)
        else:
            res = hp.cumsum(c_self)
        cs = CipherSeries(res, index=self.index)
        cs.series_A = cs.series_A.where(~isnan, np.nan)
        return cs
    
    def drop_duplicates(
            self,
            *,
            keep: str = "first",
            inplace: bool = False,
            ignore_index: bool = False,
        ):
        """
        Return CipherSeries with duplicate values removed.

        Parameters
        ----------
        keep : {'first', 'last', ``False``}, default 'first'
            Method to handle dropping duplicates:

            - 'first' : Drop duplicates except for the first occurrence.
            - 'last' : Drop duplicates except for the last occurrence.
            - ``False`` : Drop all duplicates.

        inplace : bool, default ``False``
            If ``True``, performs operation inplace and returns None.

        ignore_index : bool, default ``False``
            If ``True``, the resulting axis will be labeled 0, 1, …, n - 1.

            .. versionadded:: 2.0.0

        Returns
        -------
        CipherSeries or None
            CipherSeries with duplicates dropped or None if ``inplace=True``.
        """
        from .reshape import _group_and_replace

        arr = self.series_A.to_numpy()
        arr_new = _group_and_replace(arr)

        if inplace:
            self.series_A = pd.Series(arr_new, index=self.index, name=self.series_A.name)
            self.series_A.drop_duplicates(keep=keep, inplace=inplace, ignore_index=ignore_index)
            self.series_PL = self.modify_L_for_series_PL(self.series_PL, len(self.series_A))
            return 
        else:
            self = self.copy()
            
            self.series_A = pd.Series(arr_new, index=self.index, name=self.series_A.name)
            self.series_A = self.series_A.drop_duplicates(keep=keep, inplace=inplace, ignore_index=ignore_index)
            self.series_PL = self.modify_L_for_series_PL(self.series_PL, len(self.series_A))
            return self            

    def groupby(self, level=0):
        """
        Group CipherSeries by level.

        Parameters
        ----------
        level : int , default 0
            Column level to group by.

        """
        from .groupby import CipherSeriesGroupBy
        return CipherSeriesGroupBy(self, level)