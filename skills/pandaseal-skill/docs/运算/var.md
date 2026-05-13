# var

## 描述

沿指定轴计算无偏方差；除数默认为 `N - ddof`（`ddof=1`）。

## 参数

| 参数 | 说明 |
|------|------|
| `axis` | `CipherSeries` 上通常忽略；`CipherDataFrame` 用 `0`/`1`。 |
| `skipna` | `bool`，默认 `True`。 |
| `ddof` | `int`，默认 `1`。 |

## 返回值

`CipherSeries` 或 `CipherDataFrame`。

**注意：** `CipherDataFrame` 上 `axis=None` 可能在未来改变语义；建议显式 `axis=0`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([1, 2, 3, 7, 10])
cipher_ser = ct.encrypt_df(ser)
v = cipher_ser.var(ddof=1)
# ct.decrypt(v) -> 方差
```

```python
df = pd.DataFrame({"a": [1, 3], "b": [2, 5]})
cipher_df = ct.encrypt_df(df)
# ct.decrypt_df(cipher_df.var())
# ct.decrypt_df(cipher_df.var(axis=1))
# cipher_df.var(ddof=0)
```
