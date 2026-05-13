# `head`

## Description

Return the first `n` rows by **position**. Useful for inspecting encrypted frames. If `n` is negative, return all but the last `|n|` rows (like `df[:n]`). If `n` exceeds the row count, return all rows.

## Parameters

- **n** (`int`, default `5`): number of rows from the start.

## Return value

Same type as the caller (`CipherSeries` or `CipherDataFrame`), sliced to the first `n` rows.

## Examples

```python
cipher_df = ct.encrypt_df(
    pd.DataFrame([[1, 2], [4, 5], [7, 8]], columns=["max_speed", "shield"])
)
res = cipher_df.head()
# Decrypted: first 5 (or all) rows
print(ct.decrypt_df(res))
```

```python
res3 = cipher_df.head(3)
# Decrypted: first 3 rows only
print(ct.decrypt_df(res3))
```
