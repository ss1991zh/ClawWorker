# ndim

## Description

Number of axes: `1` for `CipherSeries`, `2` for `CipherDataFrame`.

## Parameters

None (property).

## Return value

`int` — 1 or 2 for supported PandaSeal types.

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
# 2
print(cipher_df.ndim)
```
