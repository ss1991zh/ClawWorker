# `.index` — row index

## Description

Read the **row labels** of a `CipherSeries` or `CipherDataFrame`. The index is an ordered label sequence used for alignment and label-based selection (`loc`, `at`). You can inspect it like a pandas `Index`; assignment may change labels when supported.

## Parameters

None (attribute access).

## Return value

The index object for the series or frame (row axis), e.g. `Index([...], dtype=...)`.

## Examples

```python
s = ps.CipherSeries(hp.arange(1, -2), index=["a", "b", "c"])
# Decrypted values: -2, -1, 0
print(ct.decrypt_df(s))
print(s.index)
# Index(['a', 'b', 'c'], dtype='object')
```

```python
cipher_df = ct.encrypt_df(
    pd.DataFrame([[1, 2], [4, 5]], index=["cobra", "viper"], columns=["max_speed", "shield"])
)
print(cipher_df.index)
# Index(['cobra', 'viper'], dtype='object')
```
