# rsub

## Description

Reverse element-wise subtraction: `other - CipherSeries` or `other - CipherDataFrame`. Supports `fill_value` when either side has missing data.

Unmatched indices are aligned by union (outer join).

## Parameters

### CipherSeries

- **other** — `CipherSeries`, `CipherArray`, or scalar: minuend (left of `-`).
- **fill_value** — `Cipherfloat` or `None` (default `None`, treated as `NaN`): fills existing `NaN` and new positions needed for alignment; if both operands are still missing, the result stays missing.

### CipherDataFrame

- **other** — scalar, sequence, `CipherSeries`, `dict`, or `CipherDataFrame`.
- **axis** — `0` / `'index'` or `1` / `'columns'`: axis when aligning with `CipherSeries` (or similar).
- **fill_value** — `Cipherfloat` or `None` (default `None`): same semantics as for `CipherSeries`.

## Return value

`CipherSeries` or `CipherDataFrame`: element-wise `other - self`.

## Example

Assumes `hp.initDict()` and `ct.initSK()` are already called.

```python
import pandas as pd

df = pd.DataFrame(
    {"angles": [0, 3, 4], "degrees": [360, 180, 360]},
    index=["circle", "triangle", "rectangle"],
)
cipher_df = ct.encrypt_df(df)
out = cipher_df.rsub(10)
# ct.decrypt_df(out): 10 - angles, 10 - degrees per cell
```
