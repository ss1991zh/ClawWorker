# to_json

## Description

Serialize a `CipherSeries` or `CipherDataFrame` to a JSON file.

## Parameters

- **path** (`str`): Output JSON file path.

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
cipher_df.to_json("example.json")
```
