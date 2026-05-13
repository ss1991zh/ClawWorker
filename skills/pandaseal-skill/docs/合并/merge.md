# merge

## 描述

合并两个 `CipherDataFrame` 或带 `name` 的 `CipherSeries`（视为单列表）。列连接时通常忽略两侧行索引；索引/列连接规则与 pandas 一致。`cross` 合并时不要求 `on` 列。

## 参数

| 参数 | 说明 |
|------|------|
| `left`, `right` | 左、右对象。 |
| `how` | `'left'|'right'|'outer'|'inner'|'cross'`，默认 `'inner'`。 |
| `on` | 连接键（列名或列表）；未指定且非索引连接时为列名交集。 |

## 返回值

`CipherDataFrame`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd
import pandaseal as ps

df1 = pd.DataFrame({"k": [1, 2], "v": [3, 4]})
df2 = pd.DataFrame({"k": [1, 2], "w": [5, 6]})
a, b = ct.encrypt_df(df1), ct.encrypt_df(df2)
res = ps.merge(a, b, on="k")
# ct.decrypt_df(res)
```

```python
# ps.merge(cipher_left, cipher_right, how="left", on="shield")
```
