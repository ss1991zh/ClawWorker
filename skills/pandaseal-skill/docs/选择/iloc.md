# `iloc` — integer-based indexing

## Description

Select by **integer position** along rows and/or columns (0-based). Accepts integers, lists of integers, slices, boolean arrays, callables, or a tuple `(row_indexer, col_indexer)`. Raises `IndexError` when a scalar index is out of range; slice indexing follows Python semantics (may truncate without error).

## Parameters

- **Row indexer**: int, list, slice, boolean list, or callable.
- **Column indexer** (optional): same forms for columns when using two-part indexing.

## Return value

- `CipherSeries` or a single ciphertext scalar for a fully scalar selection.
- `CipherDataFrame` for multi-row/multi-column selections.

## Examples

```python
mydict = [
    {"a": 1, "b": 2, "c": 3, "d": 4},
    {"a": 100, "b": 200, "c": 300, "d": 400},
    {"a": 1000, "b": 2000, "c": 3000, "d": 4000},
]
cipher_df = ct.encrypt_df(pd.DataFrame(mydict))
row0 = cipher_df.iloc[0]
# Decrypted: a=1, b=2, c=3, d=4
print(ct.decrypt_df(row0))
```

```python
sub = cipher_df.iloc[[0, 2], [1, 3]]
# Decrypted: rows 0 and 2, columns b and d
print(ct.decrypt_df(sub))
```
