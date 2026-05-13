# max

## 描述

沿指定轴返回最大值；默认跳过 NA。

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
mx = cipher_ser.max()
# ct.decrypt(mx) -> 3.0
```

```python
df = pd.DataFrame({"a": [1, 3], "b": [2, 5]})
cipher_df = ct.encrypt_df(df)
# ct.decrypt_df(cipher_df.max())      # 每列最大
# ct.decrypt_df(cipher_df.max(axis=1)) # 每行最大
```
