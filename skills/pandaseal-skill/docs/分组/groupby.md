# groupby

## 描述

按索引层级分组，得到 `CipherSeriesGroupBy` 或 `CipherDataFrameGroupBy`，再调用 `sum`、`mean` 等聚合。

## 参数

| 参数 | 说明 |
|------|------|
| `level` | `int`、层级名或列表；多级索引时按指定层分组。 |

## 返回值

`CipherSeriesGroupBy` 或 `CipherDataFrameGroupBy`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

ser = pd.Series([1, 2, 3, 3], index=["a", "a", "b", np.nan])
cipher = ct.encrypt_df(ser)
g = cipher.groupby(level=0)
# for name, part in g: ...
```

```python
df = pd.DataFrame([[6, 2]], index=["cobra"], columns=list("abc"))
cipher_df = ct.encrypt_df(df)
# cipher_df.groupby(level=0)
```
