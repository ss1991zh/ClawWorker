# read_csv

## Description

Read a comma-separated values (CSV) file into a labeled ciphertext table.

## Parameters

- **path** (`str`): Path to the CSV file.
- **header** (`int`, default `None`): Row index (0-based) of the header row and start of data. With default `None`, the first line is treated as column names.

## Return value

`CipherDataFrame` built from the file.

## Example

`hp.initDict()` and `ct.initSK()` are assumed to have been called.

```python
import pandaseal as ps

df = ps.read_csv("out.csv")
# Inspect ciphertext structure; decrypt when needed
print(df)
```
