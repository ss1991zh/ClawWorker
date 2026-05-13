# `at` — fast scalar access by label

## Description

Get or set a **single value** by row and column **labels** on a `CipherDataFrame`, or by label on a `CipherSeries`. Prefer `at` over `loc` when only one scalar is needed. Raises `KeyError` if the label is missing; `ValueError` if the indexer is not a scalar pair (for frames) or if a list-like label is used where a scalar is required (for series).

## Parameters

- **DataFrame**: `df.at[row_label, col_label]`.
- **Series**: `s.at[label]` (often chained: `df.loc[row].at[col]`).

## Return value

A ciphertext scalar (decrypt with `ct.decrypt`).

## Examples

```python
df = pd.DataFrame([[0, 2, 3], [0, 4, 1]], index=[4, 5], columns=["A", "B", "C"])
cipher_df = ct.encrypt_df(df)
v = cipher_df.at[4, "B"]
# Decrypted: 2.0
print(ct.decrypt(v))
```

```python
v2 = cipher_df.loc[5].at["B"]
# Decrypted: 4.0
print(ct.decrypt(v2))
```
