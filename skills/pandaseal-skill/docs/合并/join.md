# join

## 描述

在 `CipherDataFrame` 上按索引（或等价键）并入另一个 `CipherDataFrame` / `CipherSeries` 的列；重叠列名用 `lsuffix`/`rsuffix` 区分。

## 参数

| 参数 | 说明 |
|------|------|
| `other` | `CipherDataFrame`、`CipherSeries` 或列表；Series 需有 `name` 作为列名。 |
| `how` | `'left'|'right'|'outer'|'inner'|'cross'`，默认 `'left'`。 |
| `lsuffix`, `rsuffix` | 左右重名列后缀。 |
| `sort` | `bool`，默认 `False`；为 `True` 时按键字典序排序。 |

## 返回值

`CipherDataFrame`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

df1 = pd.DataFrame({"a": [1, 2]}, index=["x", "y"])
df2 = pd.DataFrame({"b": [3, 4]}, index=["x", "y"])
left, right = ct.encrypt_df(df1), ct.encrypt_df(df2)
res = left.join(right)
# ct.decrypt_df(res)
```

```python
# left.join(right, how="inner", lsuffix="_L", rsuffix="_R")
```
