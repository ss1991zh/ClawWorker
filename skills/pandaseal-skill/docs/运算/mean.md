# mean

## 描述

沿指定轴计算算术平均值；可跳过缺失值。

## 参数

| 参数 | 说明 |
|------|------|
| `axis` | `CipherSeries` 上通常忽略；`CipherDataFrame` 上 `None` 可跨两轴聚合，`0`/`1` 为列/行方向。 |
| `skipna` | `bool`，默认 `True`，计算时排除 NA。 |

## 返回值

`CipherFloat` 或 `CipherSeries`（按列或行聚合时）。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([1, 2, 3])
cipher_ser = ct.encrypt_df(ser)
m = cipher_ser.mean()
# ct.decrypt(m) -> 约 2.0
```

```python
df = pd.DataFrame({"a": [1, 3], "b": [2, 5]}, index=["tiger", "zebra"])
cipher_df = ct.encrypt_df(df)
col_means = cipher_df.mean()
row_means = cipher_df.mean(axis=1)
# ct.decrypt_df(col_means) / ct.decrypt_df(row_means)
```
