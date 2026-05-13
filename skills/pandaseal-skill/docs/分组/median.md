# median（GroupBy）

## 描述

计算各组中位数，忽略缺失值。多键分组时结果索引可为 `MultiIndex`。

## 参数

无。

## 返回值

`CipherSeries` 或 `CipherDataFrame`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([7, 2, 8, 4, 3, 3], index=["a", "a", "a", "b", "b", "b"])
cipher = ct.encrypt_df(ser)
res = cipher.groupby(level=0).median()
# ct.decrypt_df(res)
```

```python
df = pd.DataFrame({"a": [1, 3, 5], "b": [1, 4, 8]}, index=["dog", "dog", "dog"])
res = ct.encrypt_df(df).groupby(level=0).median()
# ct.decrypt_df(res)
```
