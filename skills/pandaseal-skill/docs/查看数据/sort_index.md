# `sort_index`

## Description

Sort a `CipherSeries` or `CipherDataFrame` by its **index labels** along an axis. Supports ascending/descending order, `NaN` placement, multi-index `level`, stable `kind` options, `inplace`, optional `key` applied to index values, and `ignore_index` to reset to `0..n-1`.

## Parameters

- **axis** (`0` / `'index'` or `1` / `'columns'`): sort rows (default) or columns.
- **level** (`int`, label, list, or `None`): for `MultiIndex`, which level(s) to sort by.
- **ascending** (`bool` or list of bool): sort direction; per-level when multi-index.
- **inplace** (`bool`): modify in place; returns `None` when `True`.
- **kind** (`'quicksort'`, `'mergesort'`, `'heapsort'`, `'stable'`): algorithm; stable options keep equal-key order.
- **na_position** (`'first'` or `'last'`): where `NaN` labels go (not for all multi-index cases).
- **sort_remaining** (`bool`): with `MultiIndex`, whether to sort other levels after the chosen `level`.
- **ignore_index** (`bool`): if `True`, replace index with `0, 1, …`.
- **key** (`callable` or `None`): optional vectorized transform of the index before ordering.

## Return value

Sorted `CipherSeries` or `CipherDataFrame`, or `None` if `inplace=True`.

## Examples

```python
s = pd.Series([45, 56, 12, 87], index=[3, 2, 1, 4])
s_cipher = ct.encrypt_df(s)
res = s_cipher.sort_index()
# Decrypted: index order 1, 2, 3, 4 → values 12, 56, 45, 87
print(ct.decrypt_df(res))
```

```python
df = pd.DataFrame([1, 2, 3, 4, 5], index=[100, 29, 234, 1, 150], columns=["A"])
cipher_df = ct.encrypt_df(df)
res2 = cipher_df.sort_index(ascending=False)
# Decrypted: rows ordered by index descending
print(ct.decrypt_df(res2))
```
