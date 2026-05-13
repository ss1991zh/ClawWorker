# `[]` — bracket indexing

## Description

Select columns from a `CipherDataFrame` using `df[column]` or `df[[col1, col2]]`. A single column returns a `CipherSeries`; a list of column names returns a new `CipherDataFrame` with columns in the given order. Assignment with `df[['B', 'A']] = df[['A', 'B']]` swaps or reorders encrypted columns in place.

## Parameters

- **key**: column label (`str`) or list of column labels (`list[str]`).

## Return value

- `CipherSeries` when selecting one column.
- `CipherDataFrame` when selecting multiple columns via a list.

## Examples

```python
df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=["A", "B", "C"])
cipher_df = ct.encrypt_df(df)
s = cipher_df["A"]
# Decrypted: one column as a series, e.g. [1.0, 4.0, 7.0]
print(ct.decrypt_df(s))
```

```python
sub = cipher_df[["B", "A"]]
# Decrypted: columns B then A
print(ct.decrypt_df(sub))
```
