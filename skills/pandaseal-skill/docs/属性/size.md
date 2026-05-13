# size

## Description

Number of elements in the object. For `CipherSeries`, this is the row count. For `CipherDataFrame`, it is rows × columns.

## Parameters

None (property).

## Return value

`int` — total element count.

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
# 3 rows × 3 columns → 9
assert cipher_df.size == 9
```
