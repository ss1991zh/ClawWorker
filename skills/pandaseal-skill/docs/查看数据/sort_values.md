# `sort_values`

## Description

Sort by **values** (not index labels). On a `CipherSeries`, orders elements by their values. On a `CipherDataFrame`, pass **`by`** with one or more column names (or index levels when `axis=0`). Supports `ascending` as bool or a list matching `by`, `na_position`, `kind`, `inplace`, and `ignore_index`.

## Parameters

**CipherSeries**

- **axis** (`0` / `'index'` or `1` / `'columns'`): axis to sort.
- **ascending** (`bool` or list of bool): default `True`.
- **inplace** (`bool`): default `False`.
- **kind** (`'quicksort'`, `'mergesort'`, `'heapsort'`, `'stable'`).
- **na_position** (`'first'` or `'last'`): placement of missing values.
- **ignore_index** (`bool`): reset to `0..n-1` when `True`.

**CipherDataFrame**

- **by** (`str` or `list[str]`): column(s) or index level name(s) to sort by (with `axis=0`).
- **axis**, **ascending**, **inplace**, **kind**, **na_position**, **ignore_index**: same ideas as above; `ascending` list length must match `by` when using multiple keys.

## Return value

Sorted `CipherSeries` or `CipherDataFrame`, or `None` if `inplace=True`.

## Examples

```python
s = pd.Series([float("nan"), 1, 3, 10, 5])
s_cipher = ct.encrypt_df(s)
res = s_cipher.sort_values(ascending=True)
# Decrypted: 1, 3, 5, 10, then NaN (default na last)
print(ct.decrypt_df(res))
```

```python
df = pd.DataFrame(
    [[1, 2, 11], [4, 5, 6], [7, 8, 13]],
    index=["a", "b", "c"],
    columns=["max_speed", "shield", "age"],
)
cipher_df = ct.encrypt_df(df)
out = cipher_df.sort_values(by=["max_speed", "shield"])
# Decrypted: rows ordered by max_speed then shield
print(ct.decrypt_df(out))
```
