# lt

## Description

Element-wise **less-than** comparison between a `CipherSeries` or `CipherDataFrame` and `other`. Equivalent to operators `<` where supported.

## Parameters

- **other** — scalar, `CipherFloat`, `CipherArray`, `CipherSeries`, or `CipherDataFrame`: right-hand side of the comparison.
- **axis** — `0` / `'index'` or `1` / `'columns'` (default `'columns'`): broadcast axis when comparing with `CipherSeries` or aligning frames.

## Return value

`CipherSeries` or `CipherDataFrame` of **boolean** values: element-wise `self < other`.

## Example

Assumes `hp.initDict()` and `ct.initSK()` are already called.

```python
import pandas as pd

df = pd.DataFrame(
    {"cost": [250, 150, 100], "revenue": [100, 250, 300]},
    index=["A", "B", "C"],
)
cipher_df = ct.encrypt_df(df)
mask = cipher_df.lt(150)
# Decrypted truth table: cost F,F,T; revenue T,F,F
```
