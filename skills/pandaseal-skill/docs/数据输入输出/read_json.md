# read_json

## Description

Deserialize a JSON file into a PandaSeal ciphertext object.

## Parameters

- **path** (`str`): Path to the JSON file.
- **typ** (`str`, default `'frame'`): Object type to restore: `'frame'` for a table or `'series'` for a series.

## Return value

`CipherDataFrame` or `CipherSeries`, depending on `typ`.

## Example

`hp.initDict()` and `ct.initSK()` are assumed to have been called.

```python
import pandaseal as ps

df = ps.read_json("example.json")
print(df)
```
