# cut

## 描述

将 `CipherSeries` 连续值切到离散区间；可等宽分箱（`bins` 为整数）或用手动边界（`CipherArray`）。返回 pandas `Series`，通常为 `category` dtype。

## 参数

| 参数 | 说明 |
|------|------|
| `x` | `CipherSeries`，一维。 |
| `bins` | `int`（等宽箱数，端点各扩 0.1%）或边界 `CipherArray`。 |
| `right` | `bool`，默认 `True`；区间是否包含右端点。 |
| `labels` | 与区间数一致的标签数组。 |
| `ordered` | `bool`，默认 `True`；分类是否有序；与 `labels` 配合使用。 |

## 返回值

`Series`（分箱标签）；输入中的 NA 仍为 NA，越界为 NA。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd
import pandaseal as ps

s = pd.Series([1, 7, np.nan, 4, 6, 3], name="price")
x = ct.encrypt_df(s)
res = ps.cut(x, 3, labels=["bad", "medium", "good"])
# res 为明文 category Series
```

```python
# ps.cut(x, ct.encrypt([1, 3, 4, 7]), labels=["bad", "medium", "good"])
# ps.cut(x, 3, labels=["B", "A", "B"], ordered=False)
```
