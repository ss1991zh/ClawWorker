# mean（GroupBy）

## 描述

计算各组均值，忽略缺失值。

## 参数

无。

## 返回值

`CipherSeries` 或 `CipherDataFrame`；多键分组时索引可能为 `MultiIndex`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([7, 2, 8, 4, 3, 3], index=["a", "a", "a", "b", "b", "b"])
cipher = ct.encrypt_df(ser)
res = cipher.groupby(level=0).mean()
# ct.decrypt_df(res)
```

```python
df = pd.DataFrame({"a": [1, 3, 5], "b": [1, 4, 8]}, index=["dog", "dog", "dog"])
res = ct.encrypt_df(df).groupby(level=0).mean()
# ct.decrypt_df(res)
```
