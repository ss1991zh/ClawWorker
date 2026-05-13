# quantile（GroupBy）

## 描述

返回各组在指定分位数 `q` 上的值（`0 <= q <= 1`）。

## 参数

| 参数 | 说明 |
|------|------|
| `q` | `float`，默认 `0.5`（中位数）。 |

## 返回值

`CipherSeries` 或 `CipherDataFrame`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([7, 2, 8, 4, 3, 3], index=["a", "a", "a", "b", "b", "b"])
cipher = ct.encrypt_df(ser)
res = cipher.groupby(level=0).quantile(0.3)
# ct.decrypt_df(res)
```

```python
df = pd.DataFrame({"a": [1, 3, 5, 7], "b": [1, 4, 8, 4]}, index=["dog", "dog", "mouse", "mouse"])
res = ct.encrypt_df(df).groupby(level=0).quantile(0.3)
# ct.decrypt_df(res)
```
