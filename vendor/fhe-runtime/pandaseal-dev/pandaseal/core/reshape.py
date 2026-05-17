import pandas as pd
import numpy as np
import henumpy as hp
from .cipherframe import CipherDataFrame
from .cipherseries import CipherSeries
from .base import _group_and_replace

def concat(
        objs,
        *,
        axis=0,
        join='outer',
        ignore_index=False,
):
    """
    Concatenate pandas objects along a particular axis.

    Parameters
    -------------
    objs : a sequence of pandaseal objs. The length of sequence must be 2.
    axis : {0, 1, 'index', 'columns'}
        The axis to concatenate along. The value 0 axis is the row axis. The
        value 1 is the column axis.
    join : {'outer', 'inner'}, default 'outer'
        How to handle indexes on other axis (i.e. columns). If join is 'outer'
        (union) then combine indexes. If join is 'inner' (intersection) then
       intersect indexes.
    
    Return
    -------
    concat_objs : CipherDataFrame or CipherSeries
    When concatenating all CipherSeries along the index (axis=0), a CipherSeries is returned. 
    When objs contains at least one CipherDataFrame, a CipherDataFrame is returned. 
    When concatenating along the columns (axis=1), a CipherDataFrame is returned.
    """
    if not isinstance(objs, (tuple, list)):
        raise TypeError("The type of objs must be list or tuple.")
    
    if len(objs) != 2:
        raise ValueError("The length of objs must be 2.")
    
    if not isinstance(objs[0], (CipherSeries, CipherDataFrame)):
        raise TypeError("The type of objs[0] must be CipherSeries or CipherDataFrame.")
    
    if not isinstance(objs[1], (CipherSeries, CipherDataFrame)):
        raise TypeError("The type of objs[1] must be CipherSeries or CipherDataFrame.")

    if join not in ["outer", "inner"]:
        raise ValueError(f"The value of join must be 'outer' or 'inner', but got {join}.")
    
    if axis == 'columns': axis = 1
    elif axis == 'index': axis = 0

    # axis=0 
    # 1. Find the intersection of the two object columns, and then execute hp.append().
    # 2. Call pandas.concat().
    # axis=1
    # 1. Call pandas.concat().

    if axis == 0:
        # [CipherSeries, CipherSeries]
        if isinstance(objs[0], CipherSeries) and isinstance(objs[1], CipherSeries):
            left = objs[0].to_cipherarray()
            right = objs[1].to_cipherarray()
            append = hp.append(left, right)

            # ignore_index=True
            if ignore_index:
                index = None
            # ignore_index=False
            else:
                index=objs[0].index.append(objs[1].index)

            return CipherSeries(append, index=index)
                
        # Convert CipherSeries to CipherDataFrame
        elif isinstance(objs[0], CipherSeries):
            objs[0] = objs[0].to_cipherdataframe()
        elif isinstance(objs[1], CipherSeries):
            objs[1] = objs[1].to_cipherdataframe()
        
        # [CipherDataFrame, CipherDataFrame]
        intersect = objs[0].columns.intersection(objs[1].columns)
        # has intersection
        if len(intersect) > 0:
            left = objs[0][intersect].to_cipherarray()
            right = objs[1][intersect].to_cipherarray()
            append = hp.append(left, right, axis=0)
            left_new = append[:hp.cipherLen(left)]
            right_new = append[hp.cipherLen(left):hp.cipherLen(append)]
            left_new = CipherDataFrame(left_new, columns=intersect, index=objs[0].index)
            right_new = CipherDataFrame(right_new, columns=intersect, index=objs[1].index)
            objs[0][intersect] = left_new
            objs[1][intersect] = right_new

        if join == "outer":
            A_new = pd.concat([objs[0].dataframe_A, objs[1].dataframe_A], axis=0, ignore_index=ignore_index, join='outer')
            PL_new = pd.concat([objs[0].dataframe_PL, objs[1].dataframe_PL[objs[1].columns.difference(objs[0].columns)]], axis=1)
            PL_new = objs[0].modify_L_for_PL(PL_new, len(A_new))

        elif join == "inner":
            A_new = pd.concat([objs[0].dataframe_A, objs[1].dataframe_A], axis=0, ignore_index=ignore_index, join='inner')
            PL_new = objs[0].dataframe_PL[intersect]
            PL_new = objs[0].modify_L_for_PL(PL_new, len(A_new))

        res = CipherDataFrame()
        res.dataframe_A = A_new
        res.dataframe_PL = PL_new
        return res        
    
    else:
        # [CipherSeries, CipherSeries]
        if isinstance(objs[0], CipherSeries) and isinstance(objs[1], CipherSeries):
            A_new = pd.concat([objs[0].series_A, objs[1].series_A], axis=axis, ignore_index=ignore_index, join=join)
            PL_new = pd.concat([objs[0].series_PL, objs[1].series_PL], axis=axis, ignore_index=ignore_index, join=join)
            PL_new = CipherDataFrame().modify_L_for_PL(PL_new, len(A_new))
            res = CipherDataFrame()
            res.dataframe_A = A_new
            res.dataframe_PL = PL_new
            return res

        if isinstance(objs[0], CipherSeries):
            objs[0] = objs[0].to_cipherdataframe()
        if isinstance(objs[1], CipherSeries):
            objs[1] = objs[1].to_cipherdataframe()
        
        res = CipherDataFrame()
        res.dataframe_A = pd.concat([objs[0].dataframe_A, objs[1].dataframe_A], axis=1, ignore_index=ignore_index, join=join)
        res.dataframe_PL = pd.concat([objs[0].dataframe_PL, objs[1].dataframe_PL], axis=1, ignore_index=ignore_index, join=join)
        res.dataframe_PL = res.modify_L_for_PL(res.dataframe_PL, len(res.dataframe_A))
        return res
    

def merge(
        left : CipherDataFrame | CipherSeries, 
        right : CipherDataFrame | CipherSeries, 
        how='inner', 
        on=None, 
        # left_on=None, 
        # right_on=None, 
        # left_index=False, 
        # right_index=False, 
        # sort=False, 
        # suffixes=('_x', '_y'), 
        # copy=None, 
        # indicator=False, 
        # validate=None
):
    """
    Merge CipherDataFrame objects by performing a database-style join operation by columns or indexes.

    Parameters
    ----------------
    left : CipherDataFrame or CipherSeries

    right : CipherDataFrame or CipherSeries

    how : {'left', 'right', 'outer', 'inner', 'cross'}, default 'inner'
        Type of merge to be performed.

    on : label or list of labels, optional
        Column or index level names to join on. These must be found in both
        DataFrames. If on is None and not merging on indexes then this defaults
        to the intersection of the columns in both left and right.

    left_on : label or list, optional
        Column or index level names to join on in the left obj. Can also
        be a vector or list of vectors of the length of the left obj.
        These must match the length of the obj and the index of the
        right obj when on is None.

    right_on : label or list, optional
        Column or index level names to join on in the right obj. Can also
        be a vector or list of vectors of the length of the right obj.
        These must match the length of the obj and the index of the
        left obj when on is None.

    sort : bool, default False
        Sort the join keys lexicographically in the result obj.
        If False, the order of the join keys depends on the order of the
        appearance of the keys in the two DataFrames.

    suffixes : list-like, default is (“_x”, “_y”)
        A length-2 sequence where each element is optionally a string indicating the suffix 
        to add to overlapping column names in left and right respectively. 
        Pass a value of None instead of a string to indicate that the column name from left or right should be left as-is, 
        with no suffix. At least one of the values must not be None.

    copy : bool, default True
        Always copy (even if not necessary) to ensure that no state is left behind in the original objects.

    indicator : bool or str, default False
        If True, adds a column to the output obj called “_merge” with information on the source of each row. 
        The column can be given a different name by providing a string argument. 
        The column will have a Categorical type with the value of “left_only” for observations whose merge key only appears in the left obj, 
        “right_only” for observations whose merge key only appears in the right obj, 
        and “both” if the observation’s merge key is found in both DataFrames.

    validate : str, default None
        If specified, checks if merge is of specified type.
        “one_to_one” or “1:1”: check if merge keys are unique in both left and right datasets.
        “one_to_many” or “1:m”: check if merge keys are unique in left dataset.
        “many_to_one” or “m:1”: check if merge keys are unique in right dataset.
        “many_to_many” or “m:m”: allowed, but does not result in checks.
    
    Return
    -----------
        CipherDataFrame

    """
    
    # convert series to frame
    # 1. find the columns or indexes to compare
    # 2. append
    # 3. pd.merge
    # 4. modify the PL
    # 5. return the CipherDataFrame

    left = _validate_operand(left)
    right = _validate_operand(right)

    # check if the parameters (on left_on right_on ) are valid use pd.merge
    """
    df1 = pd.DataFrame([], columns=left.columns, index=left.index)
    df2 = pd.DataFrame([], columns=right.columns, index=right.index)
    pd.merge(df1, 
             df2, 
             how=how, 
             on=on, 
             left_on=left_on, 
             right_on=right_on, 
             left_index=left_index, 
             right_index=right_index, 
             sort=sort, 
             suffixes=suffixes, 
             copy=copy, 
             indicator=indicator, 
             validate=validate)
    # check if the parameters are valid
    ON_NOT_NONE = on is not None
    LEFT_ON_NOT_NONE = (left_on is not None) or (right_on is not None)
    LEFT_INDEX_TRUE = (not left_index) or (not right_index)
    if (ON_NOT_NONE + LEFT_ON_NOT_NONE + LEFT_INDEX_TRUE) > 1:
        s = ''
        if ON_NOT_NONE:
            s += 'on'
        if LEFT_ON_NOT_NONE:
            s += 'left_on and right_on'
        if LEFT_INDEX_TRUE:
            s += 'left_index and right_index'
        raise ValueError(f'Only one of {s} can be specified')
    
    if ON_NOT_NONE:

    elif LEFT_ON_NOT_NONE:
    elif LEFT_INDEX_TRUE:
    
    # no columns or indexes specifyed to be compared, 
    # so get the intersection of the columns in both left and right  
    else:
    """
    
    # get the columns to compare
    if on is None:
        intersection = left.columns.intersection(right.columns)
        if len(intersection) == 0:
            raise ValueError("No common columns to perform merge on.")
        if len(intersection) == 1:
            cols = intersection[0]
        else:
            cols = intersection
    else:
        cols = on
        
    left_cols = left[cols]
    right_cols = right[cols]
    c_left = left_cols.to_cipherarray()
    c_right = right_cols.to_cipherarray()
    # cols has only one element
    if isinstance(left_cols, CipherSeries):
        append = hp.append(c_left, c_right).get_base_array()
        A = append[2:]
        A_new = _group_and_replace(A)
        append_new = hp.CipherArray(np.append(append[:2], A_new))        
    # cols has more than one element    
    elif isinstance(left_cols, CipherDataFrame):
        append = hp.append(c_left, c_right, axis=0, output_encrypt_type=1).get_base_array()
        A = append[2:]
        A_new = _group_and_replace(A)
        append_new = hp.CipherArray(np.append(append[:2], A_new, axis=0))

    if len(cols) == 1:
        cols = cols[0]
    left[cols] = append_new[:hp.cipherLen(c_left)]
    right[cols] = append_new[hp.cipherLen(c_left):]

    if not isinstance(cols, list):
        cols = [cols]
    right_cols = right.columns.difference(cols)

    A_merge = pd.merge(left.dataframe_A, right.dataframe_A, how=how, on=cols)
    PL_merge = pd.merge(left.dataframe_PL, right.dataframe_PL[right_cols], left_index=True, right_index=True)
    PL_merge = PL_merge[A_merge.columns]
    PL_merge = left.modify_L_for_PL(PL_merge, len(A_merge))

    # merge operator can not cause the case where columns are empty
    res = CipherDataFrame()
    res.dataframe_PL = PL_merge
    res.dataframe_A = A_merge
    return res


def _validate_operand(obj: CipherDataFrame | CipherSeries) -> CipherDataFrame:
    if isinstance(obj, CipherDataFrame):
        return obj
    elif isinstance(obj, CipherSeries):
        if obj.series_A.name is None:
            raise ValueError("Cannot merge a Series without a name")
        return obj.to_cipherdataframe()
    else:
        raise TypeError(
            f"Can only merge CipherSeries or CipherDataFrame objects, a {type(obj)} was passed"
        )

