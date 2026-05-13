# `.columns` — column labels

## Description

Access the **column labels** of a `CipherDataFrame`. Same role as in pandas: names for `loc`, `[]`, and `sort_values(by=...)`.

## Parameters

None (attribute access).

## Return value

Column index (e.g. `Index(['col1', 'col2'], ...)`).

## Examples

```python
cipher_df = ct.encrypt_df(
    pd.DataFrame([[1, 2], [4, 5]], index=["cobra", "viper"], columns=["max_speed", "shield"])
)
print(cipher_df.columns)
# Index(['max_speed', 'shield'], dtype='object')
```

```python
by_first = cipher_df.sort_values(by=cipher_df.columns[0])
print(ct.decrypt_df(by_first))
```
