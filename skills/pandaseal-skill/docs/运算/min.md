# min

## 描述

沿指定轴返回最小值；默认跳过 NA。

## 参数

| 参数 | 说明 |
|------|------|
| `axis` | `CipherSeries` 忽略；`CipherDataFrame` 上 `None` 可跨轴聚合，`0`/`1` 为列/行极值。 |
| `skipna` | `bool`，默认 `True`。 |

## 返回值

`CipherFloat` 或 `CipherSeries`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([1, 2, 3])
cipher_ser = ct.encrypt_df(ser)
mn = cipher_ser.min()
# ct.decrypt(mn) -> 1.0
```

```python
df = pd.DataFrame({"a": [1, 3], "b": [2, 5]})
cipher_df = ct.encrypt_df(df)
# ct.decrypt_df(cipher_df.min())
# ct.decrypt_df(cipher_df.min(axis=1))
```
