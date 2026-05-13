# sum（GroupBy）

## 描述

对 `CipherSeriesGroupBy` / `CipherDataFrameGroupBy` 各组求和。

## 参数

无。

## 返回值

`CipherSeries` 或 `CipherDataFrame`，索引为分组键。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

ser = pd.Series([1, 4, 3, 3], index=["a", "a", "b", np.nan])
cipher = ct.encrypt_df(ser)
res = cipher.groupby(level=0).sum()
# ct.decrypt_df(res) -> a: 5, b: 3（NaN 索引是否参与以实际行为为准）
```

```python
df = pd.DataFrame([[1, 2], [3, 4]], index=["x", "x"])
res = ct.encrypt_df(df).groupby(level=0).sum()
# ct.decrypt_df(res)
```
