# `to_cipherarray`

## Description

Convert a `CipherSeries` or `CipherDataFrame` into a **`CipherArray`** for array-based homomorphic operations. Values and structure are preserved in encrypted form; decrypt the result with the toolkit’s array helpers as needed.

## Parameters

None (method call). Variants may exist on subclasses; follow the same signature as in your PandaSeal version.

## Return value

A `CipherArray` representing the encrypted numeric data (shape follows the input: 1-D for a series, 2-D for a frame).

## Examples

```python
s = ps.CipherSeries(hp.arange(4, -3))
arr = s.to_cipherarray()
# Decrypted numpy-like values: [-3, -2, -1, 0, 1, 2, 3]
print(ct.decrypt(arr))
```

```python
cipher_df = ct.encrypt_df(
    pd.DataFrame([[1, 2], [4, 5], [7, 8]], columns=["max_speed", "shield"])
)
arr2 = cipher_df.to_cipherarray()
# Decrypted: 3x2 matrix matching plaintext
print(ct.decrypt(arr2))
```
