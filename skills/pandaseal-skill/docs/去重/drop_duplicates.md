# drop_duplicates

## 描述

去除重复行（`CipherSeries` 视为单列）；可指定保留首次、末次或删除全部重复。

## 参数（CipherSeries）

| 参数 | 说明 |
|------|------|
| `keep` | `'first'|'last'|False`，默认 `'first'`。 |
| `inplace` | `bool`，默认 `False`。 |
| `ignore_index` | `bool`，默认 `False`。 |

## 参数（CipherDataFrame）

额外 **`subset`**：用于判重的列标签或列表；默认全部列。索引不参与判重。

## 返回值

去重后的密文对象；`inplace=True` 时为 `None`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

s = pd.Series([112, 56, 112, np.nan, 112, 89], name="price")
c = ct.encrypt_df(s)
# ct.decrypt_df(c.drop_duplicates())
# ct.decrypt_df(c.drop_duplicates(keep="last"))
```

```python
df = pd.DataFrame([[1, 2], [1, 2], [3, 4]], columns=["a", "b"])
cipher_df = ct.encrypt_df(df)
# ct.decrypt_df(cipher_df.drop_duplicates(subset=["a"]))
```
