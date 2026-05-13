# concat

## 描述

沿轴拼接多个 `CipherSeries` 或 `CipherDataFrame`。序列中**仅支持两个对象**。

## 参数

| 参数 | 说明 |
|------|------|
| `objs` | 含两个密文对象的序列。 |
| `axis` | `0`/`'index'` 或 `1`/`'columns'`，默认 `0`。 |
| `join` | `'inner'` 或 `'outer'`，默认 `'outer'`（非连接轴）。 |
| `ignore_index` | `bool`，默认 `False`；为 `True` 时连接轴重置为 `0..n-1`。 |

## 返回值

全为 Series 且 `axis=0` 时为 `CipherSeries`；否则为 `CipherDataFrame`。`axis=1` 时为 `CipherDataFrame`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd
import pandaseal as ps

s1, s2 = ct.encrypt_df(pd.Series([1, 2])), ct.encrypt_df(pd.Series([3, 4]))
res = ps.concat([s1, s2])
# ct.decrypt_df(res)
# ps.concat([s1, s2], ignore_index=True)
```

```python
d1, d2 = ct.encrypt_df(pd.DataFrame({"a": [1]})), ct.encrypt_df(pd.DataFrame({"b": [2]}))
# ps.concat([d1, d2], axis=1)
# ps.concat([d1, d2], join="inner")
```
