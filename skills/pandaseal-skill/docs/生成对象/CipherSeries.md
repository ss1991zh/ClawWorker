# CipherSeries

## Description

One-dimensional `CipherArray` with an axis index (including time-like indexes). Labels need not be unique but must be hashable. Operations between series align on index; lengths may differ. Stats methods mirror `CipherArray` and skip missing values (currently `NaN`).

## Parameters

- **data** (`CipherArray`): Values stored in the series.
- **index** (array-like or `Index`, 1d): Hashable labels, same length as data. Default `RangeIndex`. If data is dict-like without index, keys become the index; if index is given, data is reindexed.
- **name** (hashable, optional): Series name.
- **copy** (`bool`, default `False`): Whether to copy input data.

## Return value

A `CipherSeries` instance.

## Example

`hp.initDict()` and `ct.initSK()` are assumed to have been called.

```python
import numpy as np
import pandaseal as ps
import crypto_toolkit as ct

d = np.array([0.5, 0.3, 4.3, 0.1])
cipher_d = ct.encrypt(d)
ser = ps.CipherSeries(
    data=cipher_d, index=["a", "b", "c", "d"], name="demo", copy=False
)
# After decrypt: a=0.5, b=0.3, c=4.3, d=0.1
print(ct.decrypt_df(ser))
```
