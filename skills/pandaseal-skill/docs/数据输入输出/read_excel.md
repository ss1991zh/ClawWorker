# read_excel

## Description

Load an Excel workbook sheet into a `CipherDataFrame`.

## Parameters

- **path** (`str`): Path to the `.xlsx` (or supported Excel) file.
- **sheet_name** (`str` or `int`, default `0`): Sheet name, or zero-based sheet index (chart sheets are not counted in the index).
- **header** (`int`, default `0`): Row index (0-based) used as column labels.
- **index_col** (`int`, default `None`): Column index (0-based) to use as row labels, or `None` if there is no index column.

**`sheet_name` examples:** `0` — first sheet; `1` — second sheet; `"Sheet1"` — sheet by name.

## Return value

`CipherDataFrame` parsed from the selected sheet.

## Example

`hp.initDict()` and `ct.initSK()` are assumed to have been called.

```python
import pandaseal as ps

res = ps.read_excel("output.xlsx", index_col=0)
print(res)
```

Optional: `ps.read_excel("tmp.xlsx", index_col=None, header=None)` for no header/index column.
