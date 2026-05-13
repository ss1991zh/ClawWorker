# fillna

## 描述

用标量或对齐后的密文对象填充 `CipherSeries` / `CipherDataFrame` 中的 NA/NaN。

## 参数

| 参数 | 说明 |
|------|------|
| `value` | `CipherFloat`、`CipherSeries` 或 `CipherDataFrame`。按位置/列对齐填充；不能是 Python 列表。 |
| `inplace` | `bool`，默认 `False`。为 `True` 时原地修改，返回 `None`。 |

## 返回值

填充后的 `CipherSeries` 或 `CipherDataFrame`；`inplace=True` 时为 `None`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

ser = pd.Series([1.0, 2.0, np.nan])
cipher_ser = ct.encrypt_df(ser)
zero = ct.encrypt(0)
res = cipher_ser.fillna(zero)
# ct.decrypt_df(res) -> 第三项为 0（或近零浮点）
```

```python
df = pd.DataFrame([[np.nan, 2], [3, 4]], columns=list("AB"))
cipher_df = ct.encrypt_df(df)
fill_df = ct.encrypt_df(pd.DataFrame(np.zeros((2, 2)), columns=list("AB")))
res = cipher_df.fillna(fill_df)
# 按列名与索引对齐填充缺失处
```
