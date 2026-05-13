# to_excel

## Description

Write a `CipherSeries` or `CipherDataFrame` to an Excel workbook.

## Parameters

- **path** (`str`): Output file path.
- **sheet_name** (`str`, default `'Sheet1'`): Worksheet name for the ciphertext data.
- **header** (`bool` or list of `str`, default `True`): Whether to write column headers; a list is treated as aliases for column names.
- **index** (`bool`, default `True`): Whether to write row labels (index).

## Return value

None (writes to disk).

## Example

`hp.initDict()` and `ct.initSK()` are assumed to have been called.

```python
import numpy as np
import pandas as pd
import crypto_toolkit as ct

df = pd.DataFrame(
    np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=["A", "B", "C"]
)
cipher_df = ct.encrypt_df(df)
cipher_df.to_excel("output.xlsx", sheet_name="Sheet_name_1")
```
