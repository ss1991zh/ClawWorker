# `loc` — label-based indexing

## Description

Access rows and columns by **label** (not integer position unless labels are integers). Supports single labels, label lists, label slices (endpoints **inclusive**), boolean arrays aligned to the axis, aligned boolean `Series`, and callables. Raises `KeyError` for missing labels and `IndexingError` when keys cannot align with the frame index.

## Parameters

- **First indexer**: row label(s), slice, boolean mask, or callable.
- **Second indexer** (optional): column label(s) when using comma form, e.g. `df.loc[row, col]`.

## Return value

- `CipherSeries` for a single row or single scalar cell (depending on selection shape).
- `CipherDataFrame` for multiple rows/columns.

## Examples

```python
df = pd.DataFrame(
    [[1, 2], [4, 5], [7, 8]],
    index=["cobra", "viper", "sidewinder"],
    columns=["max_speed", "shield"],
)
cipher_df = ct.encrypt_df(df)
row = cipher_df.loc["viper"]
# Decrypted: max_speed 4.0, shield 5.0
print(ct.decrypt_df(row))
```

```python
cell = cipher_df.loc["cobra", "shield"]
# Decrypted scalar, e.g. 2.0
print(ct.decrypt(cell))
```
