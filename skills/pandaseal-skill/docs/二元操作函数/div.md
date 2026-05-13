# div

## Description

Element-wise floating-point division of a `CipherSeries` or `CipherDataFrame` by another object. Same idea as `CipherSeries / other` / `CipherDataFrame / other`, with optional `fill_value` for missing values before alignment.

Unmatched indices are aligned by union (outer join).

## Parameters

### CipherSeries

- **other** — `CipherSeries`, `CipherArray`, or scalar: divisor.
- **fill_value** — `Cipherfloat` or `None` (default `None`, treated as `NaN`): fills existing `NaN` and new positions needed for alignment; if both operands are still missing, the result stays missing.

### CipherDataFrame

- **other** — scalar, sequence, `CipherSeries`, `dict`, or `CipherDataFrame`.
- **axis** — `0` / `'index'` or `1` / `'columns'`: axis when aligning with `CipherSeries` (or similar).
- **fill_value** — `Cipherfloat` or `None` (default `None`): same semantics as for `CipherSeries`.

## Return value

`CipherSeries` or `CipherDataFrame`: element-wise quotient.

## Example

Assumes `hp.initDict()` and `ct.initSK()` are already called.

```python
import pandas as pd

df = pd.DataFrame(
    {"angles": [0, 3, 4], "degrees": [360, 180, 360]},
    index=["circle", "triangle", "rectangle"],
)
cipher_df = ct.encrypt_df(df)
out = cipher_df.div(2)
# ct.decrypt_df(out): angles 0,1.5,2; degrees 180,90,180
```
