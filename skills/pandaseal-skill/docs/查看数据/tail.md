# `tail`

## Description

Return the last `n` rows by **position**. If `n` is negative, return all but the first `|n|` rows (like `df[|n|:]`). If `n` exceeds the row count, return all rows.

## Parameters

- **n** (`int`, default `5`): number of rows from the end.

## Return value

Same type as the caller (`CipherSeries` or `CipherDataFrame`), sliced to the last `n` rows.

## Examples

```python
cipher_df = ct.encrypt_df(
    pd.DataFrame([[1, 2], [4, 5], [7, 8], [3, 7], [5, 9], [6, 4]], columns=["max_speed", "shield"])
)
res = cipher_df.tail()
# Decrypted: last 5 rows
print(ct.decrypt_df(res))
```

```python
res2 = cipher_df.tail(3)
# Decrypted: last 3 rows
print(ct.decrypt_df(res2))
```
