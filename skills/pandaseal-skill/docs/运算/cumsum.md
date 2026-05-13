# cumsum

## 描述

沿指定轴累积求和；`skipna=False` 时遇 NA 后结果全为 NA。

## 参数

| 参数 | 说明 |
|------|------|
| `axis` | `0`/`'index'` 或 `1`/`'columns'`，默认 `0`；`CipherSeries` 忽略。 |
| `skipna` | `bool`，默认 `True`，跳过 NA 继续累加。 |

## 返回值

与输入同形状的 `CipherSeries` 或 `CipherDataFrame`。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

s = pd.Series([2, np.nan, 5, -1, 0])
cipher_s = ct.encrypt_df(s)
# ct.decrypt_df(cipher_s.cumsum())
# ct.decrypt_df(cipher_s.cumsum(skipna=False))
```

```python
df = pd.DataFrame([[2.0, 1.0], [3.0, np.nan], [1.0, 0.0]], columns=list("AB"))
cipher_df = ct.encrypt_df(df)
# ct.decrypt_df(cipher_df.cumsum())
# ct.decrypt_df(cipher_df.cumsum(axis=1))
```
