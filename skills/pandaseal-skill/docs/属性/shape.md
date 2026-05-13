# shape

## Description

Tuple describing the length of each dimension: for `CipherSeries`, `(n,)`; for `CipherDataFrame`, `(rows, columns)`.

## Parameters

None (property).

## Return value

`tuple` of `int` — dimensions of the ciphertext object.

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
# (3, 3)
print(cipher_df.shape)
```
