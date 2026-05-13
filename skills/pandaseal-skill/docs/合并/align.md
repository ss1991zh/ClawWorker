# align

## 描述

按 `join` 与 `axis` 将两个密文对象在索引/列上对齐；缺失处可用 `fill_value` 填充。

## 参数

| 参数 | 说明 |
|------|------|
| `other` | 另一个 `CipherSeries` 或 `CipherDataFrame`。 |
| `join` | 默认 `'outer'`；键为两对象并集（`outer` 时常排序）。 |
| `axis` | `0`、`1` 或 `None`；`None` 表示行列同时对齐。 |
| `fill_value` | `CipherFloat`，默认 `nan`。 |

## 返回值

二元组 `(left_aligned, right_aligned)`，类型与输入对应。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

a = ct.encrypt_df(pd.Series([1, 2, 4, np.nan], index=list("abcd")))
b = ct.encrypt_df(pd.Series([3, np.nan, 5, np.nan], index=list("abde")))
left, right = a.align(b, join="outer", axis=None)
# ct.decrypt_df(left); ct.decrypt_df(right)
```

```python
# a.align(b, join="outer", fill_value=ct.encrypt(2))
# cipher_df.align(cipher_other, join="outer", axis=1)  # 仅列对齐
```
