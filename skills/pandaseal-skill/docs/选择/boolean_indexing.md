# Boolean indexing

## Description

Filter a `CipherSeries` with a **boolean vector** (Python list of `bool`). Combine conditions with `|`, `&`, and `~`; always parenthesize each comparison so precedence matches intent (e.g. `(s > 0) & (s < 3)`). For PandaSeal, condition results are often turned into a plain list with `.to_list()` before indexing.

## Parameters

- **mask**: boolean list aligned to the series index (e.g. `(series > 0).to_list()`).

## Return value

A `CipherSeries` containing only rows where the mask is true.

## Examples

```python
s = ps.CipherSeries(hp.arange(4, -3))
# Keep positive values
res = s[(s > 0).to_list()]
# Decrypted: e.g. 1.0, 2.0, 3.0 at preserved positions
print(ct.decrypt_df(res))
```

```python
res2 = s[(((s < -1) | (s > 0.5))).to_list()]
# Decrypted: combined OR condition
print(ct.decrypt_df(res2))
```
