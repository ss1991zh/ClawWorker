# std

## 描述

沿指定轴计算样本标准差；默认除数为 `N - ddof`（默认 `ddof=1`）。与 `numpy.std` 一致时可设 `ddof=0`。

## 参数

| 参数 | 说明 |
|------|------|
| `axis` | `CipherSeries` 上通常忽略；`CipherDataFrame` 用 `0`/`1` 表示列/行。 |
| `skipna` | `bool`，默认 `True`；若整行/列全为 NA，结果为 NA。 |
| `ddof` | `int`，默认 `1`。除数为 `N - ddof`。 |

## 返回值

`CipherSeries` 或 `CipherDataFrame`（按轴聚合时）。

**注意：** `CipherDataFrame` 上 `axis=None` 的行为可能在未来版本变更；建议显式使用 `axis=0`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([1, 2, 3, 7, 10])
cipher_ser = ct.encrypt_df(ser)
s = cipher_ser.std(ddof=1)
# ct.decrypt(s) -> 样本标准差
```

```python
df = pd.DataFrame({"age": [21, 25, 62, 43], "height": [1.61, 1.87, 1.49, 2.01]})
cipher_df = ct.encrypt_df(df)
# ct.decrypt_df(cipher_df.std())
# ct.decrypt_df(cipher_df.std(axis=1))
```
