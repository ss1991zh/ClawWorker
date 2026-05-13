# `iat` — fast scalar access by position

## Description

Get or set a **single value** by **integer position** (0-based). Use for one cell at `(row_i, col_i)` on a `CipherDataFrame` or one position on a `CipherSeries`. Raises `IndexError` if the position is out of range.

## Parameters

- **DataFrame**: `df.iat[row_i, col_i]`.
- **Series**: `s.iat[i]` (often `df.iloc[row].iat[col]`).

## Return value

A ciphertext scalar (decrypt with `ct.decrypt`).

## Examples

```python
df = pd.DataFrame([[0, 2, 3], [0, 4, 1]], index=[4, 5], columns=["A", "B", "C"])
cipher_df = ct.encrypt_df(df)
v = cipher_df.iat[1, 2]
# Decrypted: 1.0 (second row, third column)
print(ct.decrypt(v))
```

```python
v2 = cipher_df.iloc[0].iat[1]
# Decrypted: 2.0
print(ct.decrypt(v2))
```
