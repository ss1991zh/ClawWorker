# dropna

## 描述

删除 `CipherSeries` 或 `CipherDataFrame` 中的缺失值（NA/NaN），行为与 pandas 类似。

## 参数（CipherSeries）

| 参数 | 说明 |
|------|------|
| `axis` | `0` 或 `'index'`。未使用，仅为与 DataFrame API 兼容。 |
| `inplace` | `bool`，默认 `False`。为 `True` 时原地修改并返回 `None`。 |
| `how` | `str`，可选。未使用，保留兼容。 |
| `ignore_index` | `bool`，默认 `False`。为 `True` 时结果索引为 `0..n-1`。 |

## 参数（CipherDataFrame）

| 参数 | 说明 |
|------|------|
| `axis` | `0`/`'index'` 删含 NA 的行；`1`/`'columns'` 删含 NA 的列。 |
| `how` | `'any'`（任一为 NA 即删）或 `'all'`（全为 NA 才删）。 |
| `thresh` | `int`，可选。至少非 NA 个数；不可与 `how` 同用。 |
| `subset` | 列标签或列表，仅在这些列上判断 NA。 |
| `inplace` / `ignore_index` | 同上。 |

## 返回值

`CipherSeries` 或 `CipherDataFrame`；`inplace=True` 时为 `None`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

ser = pd.Series([1.0, 2.0, np.nan])
cipher_ser = ct.encrypt_df(ser)
res = cipher_ser.dropna()
# ct.decrypt_df(res) -> 保留 1.0, 2.0 两行
```

```python
df = pd.DataFrame([[1, 2, 11], [np.nan, np.nan, 6]], columns=["a", "b", "c"])
cipher_df = ct.encrypt_df(df)
res = cipher_df.dropna()  # 默认 axis=0, how='any'
# ct.decrypt_df(res) -> 仅保留第一行
```
