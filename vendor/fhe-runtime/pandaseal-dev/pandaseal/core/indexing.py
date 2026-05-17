import henumpy as hp
import numpy as np
import pandas as pd
from pandas._libs import lib


class _LocationIndexer:
    
    def __init__(self, obj):
        self.obj = obj

class _LocIndexer(_LocationIndexer):

    def __getitem__(self, key):

        # Use lazy importing of CipherSeries to avoid circular import issues.
        from .cipherseries import CipherSeries
        from .cipherframe  import CipherDataFrame

        if isinstance(self.obj, CipherSeries):     
        
            A = self.obj.series_A.loc[key]

            if lib.is_list_like(key):
                A_value = A.tolist()
                A_index = A.index
                P = self.obj.series_PL['_P']
                return CipherSeries([P, len(A_value)] + A_value, index=A_index, name=self.obj.series_A.name)
            
            # The is_scalar function of pandas is used to determine whether a key is a scalar.
            if lib.is_scalar(key):
                p = self.obj.series_PL['_P']
                return hp.CipherArray([p, A])
            
            raise TypeError(f"Enter an illegal index type :{type(key)}. Scalar and list_like are currently supported.")
        
        elif isinstance(self.obj, CipherDataFrame):
            
            A = self.obj.dataframe_A.loc[key]

            # Check the type of A. Scalar, Series or DataFrame.
            # 1.Scalar
            #   The result is a CipherArray.
            # 2.Series
            #   The result is a CipherSeries. 
            #   The corresponding column needs to be picked out from dataframe_PL.
            #   Depending on whether you are accessing the column or row of the dataframe. 
            #   Column access only needs to fetch the corresponding column in dataframe_PL. 
            #   Row access requires fetching the _P of all columns to perform vectorization operations.
            # 3.DataFrame
            #   The result is a CipherDataFrame.
            #   The corresponding column needs to be picked out from dataframe_PL.
            #   The _L of the result needs to be modified.
            if isinstance(A, pd.Series):
                # Row access
                if len(A.index) == len(self.obj.dataframe_A.columns) and (A.index == self.obj.dataframe_PL.columns).all():
                    P_array = self.obj.dataframe_PL.iloc[0].to_numpy()
                    A_array = A.to_numpy()
                    c = hp.empty_array()
                    for i in range(len(A)):
                        c = hp.append(c, hp.CipherArray([P_array[i], A_array[i]]))
                    return CipherSeries(c, index=A.index, name=A.name)
                
                # Column access
                else:
                    PL_series = self.obj.dataframe_PL.loc[:, key[1]]
                    PL_series['_L'] = A.size
                    res = CipherSeries()
                    res.series_A = A
                    res.series_PL = PL_series
                    return res
                
            elif isinstance(A, pd.DataFrame):
                A_shape = A.shape
                if isinstance(key, tuple):
                    # Has share memory problem.
                    PL_new = pd.DataFrame(self.obj.dataframe_PL[key[1]], copy=True)
                else:
                    PL_new = pd.DataFrame(self.obj.dataframe_PL, copy=True)
                PL_new.iloc[1] = A_shape[0]
                res = CipherDataFrame()
                res.dataframe_A = A
                res.dataframe_PL = PL_new
                return res
                
            else:
                P = self.obj.dataframe_PL.loc['_P', key[1]]
                return hp.CipherArray([P, A])
                
    def __setitem__(self, key, value):
        
        # Use lazy importing of CipherSeries to avoid circular import issues.
        from .cipherseries import CipherSeries
        from .cipherframe import CipherDataFrame

        if isinstance(self.obj, CipherDataFrame):
            raise TypeError("Do not support CipherDataFrame for now.")
        
        if not isinstance(value, hp.CipherArray):
            raise TypeError("The value must be a CipherArray.")

        # Here you need to check for statements of type key, 
        # because pandas will not do these things without calling the 'loc' function directly.        
        if lib.is_scalar(key):
            ca = self.obj.to_cipherarray()
            # Get the numeric index of the key.
            pos = self.obj.series_A.index.get_loc(key)
            ca[pos] = value
            s_new = CipherSeries(ca, index=self.obj.series_A.index, name=self.obj.series_A.name)
            self.obj.series_A = s_new.series_A
            self.obj.series_PL = s_new.series_PL
        else:
            raise TypeError(f"Enter an illegal index type :{type(key)}. Scalar is currently supported.")

class _ILOCIndexer(_LocationIndexer):

    def __getitem__(self, key):
        
        # Use lazy importing of CipherSeries to avoid circular import issues.
        from .cipherseries import CipherSeries
        from .cipherframe import CipherDataFrame

        if isinstance(self.obj, CipherSeries):

            A = self.obj.series_A.iloc[key]
            
            if lib.is_list_like(key):
                A_value = A.tolist()
                A_index = A.index
                P = self.obj.series_PL['_P']
                return CipherSeries([P, len(A_value)] + A_value, index=A_index, name=self.obj.series_A.name)

            # The is_scalar function of pandas is used to determine whether a key is a scalar.
            if lib.is_integer(key):
                p = self.obj.series_PL['_P']
                return hp.CipherArray([p, A])
            
            # Scalar and list_like are not all types
            raise TypeError(f"Enter an illegal index type :{type(key)}. Integer and list_like are currently supported.")
        
        elif isinstance(self.obj, CipherDataFrame):
            
            A = self.obj.dataframe_A.iloc[key]
            
            if isinstance(A, pd.Series):
                # Row access
                if len(A.index) == len(self.obj.dataframe_A.columns) and (A.index == self.obj.dataframe_PL.columns).all():
                    P_array = self.obj.dataframe_PL.iloc[0].to_numpy()
                    A_array = A.to_numpy()
                    c = hp.empty_array()
                    for i in range(len(A)):
                        c = hp.append(c, hp.CipherArray([P_array[i], A_array[i]]))
                    return CipherSeries(c, index=A.index, name=A.name)
                
                # Column access
                else:
                    PL_series = self.obj.dataframe_PL.iloc[:, key[1]]
                    res = CipherSeries()
                    res.series_A = A
                    res.series_PL = PL_series
                    return res
                
            elif isinstance(A, pd.DataFrame):
                A_shape = A.shape
                if isinstance(key, tuple):
                    # Has share memory problem.
                    PL_new = pd.DataFrame(self.obj.dataframe_PL.iloc[:, key[1]], copy=True)
                else:
                    PL_new = pd.DataFrame(self.obj.dataframe_PL, copy=True)
                PL_new.iloc[1] = A_shape[0]
                res = CipherDataFrame()
                res.dataframe_A = A
                res.dataframe_PL = PL_new
                return res
                
            else:
                P = self.obj.dataframe_PL.iloc[0, key[1]]
                return hp.CipherArray([P, A])
                            
    def __setitem__(self, key, value):
        
        # Use lazy importing of CipherSeries to avoid circular import issues.
        from .cipherseries import CipherSeries
        from .cipherframe import CipherDataFrame

        if isinstance(self.obj, CipherDataFrame):
            raise TypeError("Do not support CipherDataFrame for now.")        
        
        if not isinstance(value, hp.CipherArray):
            raise  TypeError("The value must be a CipherArray.")
        
        if lib.is_integer(key):
            ca = self.obj.to_cipherarray()
            ca[key] = value
            s_new = CipherSeries(ca, index=self.obj.series_A.index, name=self.obj.series_A.name)
            self.obj.series_A = s_new.series_A
            self.obj.series_PL = s_new.series_PL
        else:
            raise TypeError(f"Enter an illegal index type :{type(key)}. Integer is currently supported.")

                
class _AtIndexer(_LocationIndexer):
    
    def __getitem__(self, key):
        
        from .cipherseries import CipherSeries
        from .cipherframe import CipherDataFrame
        
        if isinstance(self.obj, CipherSeries):

            # There is no need to check the type of key because pandas will do that.
            A = self.obj.series_A.at[key]
            P = self.obj.series_PL['_P']
            return hp.CipherArray([P, A])

        elif isinstance(self.obj, CipherDataFrame):
            
            A = self.obj.dataframe_A.at[key]
            P = self.obj.dataframe_PL.at['_P', key[1]]
            return hp.CipherArray([P, A])
            
    def __setitem__(self, key, value):
        
        # Use lazy importing of CipherSeries to avoid circular import issues.
        from .cipherseries import CipherSeries
        from .cipherframe import CipherDataFrame

        if isinstance(self.obj, CipherDataFrame):
            raise TypeError("Do not support CipherDataFrame for now.")
        
        if not isinstance(value, hp.CipherArray):
            raise TypeError("The value must be a CipherArray.")
        
        # Here you need to check for statements of type key, 
        # because pandas will not do these things without calling the 'at' function directly.        
        if lib.is_scalar(key):
            pos = self.obj.series_A.index.get_loc(key)
            ca = self.obj.to_cipherarray()
            ca[pos] = value
            s_new = CipherSeries(ca, index=self.obj.series_A.index, name=self.obj.series_A.name)
            self.obj.series_A = s_new.series_A
            self.obj.series_PL = s_new.series_PL
        else:
            raise TypeError(f"Enter an illegal index type :{type(key)}. Scalar is currently supported.")

class _IAtIndexer(_LocationIndexer):
    
    def __getitem__(self, key):
        
        from .cipherseries import CipherSeries
        from .cipherframe import CipherDataFrame
        
        if isinstance(self.obj, CipherSeries):
            # There is no need to check the type of key because pandas will do that.        
            A = self.obj.series_A.iat[key]
            P = self.obj.series_PL['_P']
            return hp.CipherArray([P, A])
        elif isinstance(self.obj, CipherDataFrame):
            A = self.obj.dataframe_A.iat[key]
            P = self.obj.dataframe_PL.iat[0, key[1]]
            return hp.CipherArray([P, A])

    def __setitem__(self, key, value):
        
        # Use lazy importing of CipherSeries to avoid circular import issues.
        from .cipherseries import CipherSeries
        from .cipherframe import CipherDataFrame

        if isinstance(self.obj, CipherDataFrame):
            raise TypeError("Do not support CipherDataFrame for now.")        
        
        if not isinstance(value, hp.CipherArray):
            raise TypeError("The value must be a CipherArray.")
        
        # Here you need to check for statements of type key, 
        # because pandas will not do these things without calling the 'iat' function directly.  
        if lib.is_integer(key):
            ca = self.obj.to_cipherarray()
            ca[key] = value
            s_new = CipherSeries(ca, index=self.obj.series_A.index, name=self.obj.series_A.name)
            self.obj.series_A = s_new.series_A
            self.obj.series_PL = s_new.series_PL
        else:
            raise TypeError(f"Enter an illegal index type :{type(key)}. Integer is currently supported.")