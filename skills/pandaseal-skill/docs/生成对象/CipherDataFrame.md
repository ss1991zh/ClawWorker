# CipherDataFrame

## Description

Two-dimensional, size-mutable table that may hold heterogeneous ciphertext data. Row and column labels align arithmetic operations. It behaves like a dict of `CipherSeries` columns.

## Parameters

- **data** (`CipherArray`): Ciphertext matrix backing the frame.
- **index** (`Index` or array-like): Row labels. Defaults to `RangeIndex` if omitted and not implied by data.
- **columns** (`Index` or array-like): Column labels. If data already has column names, selection may apply; default is `RangeIndex(0..n-1)`.
- **copy** (`bool` or `None`, default `None`): Whether to copy input data.

## Return value

A `CipherDataFrame` instance.

## Example

`hp.initDict()` and `ct.initSK()` are assumed to have been called.

```python
import numpy as np
import pandaseal as ps
import crypto_toolkit as ct

A = np.array([[1.0, 2.0, 3.0], [2.0, -3.0, 4.0], [3.0, 1.0, 4.0]])
cipher_A = ct.encrypt(A, encrypt_by_column=True)
df = ps.CipherDataFrame(data=cipher_A, columns=["A", "B", "C"])
# After decrypt: rows match A; columns A, B, C
print(ct.decrypt_df(df))
```
