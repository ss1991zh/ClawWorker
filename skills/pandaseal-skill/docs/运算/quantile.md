# quantile

## 描述

计算指定分位数；`q` 可为标量或序列。

## 参数

| 参数 | 说明 |
|------|------|
| `q` | `float` 或类数组，默认 `0.5`；取值范围 `0 <= q <= 1`。 |
| `axis` | `0`/`'index'` 或 `1`/`'columns'`，默认 `0`。 |

## 返回值

- `q` 为标量：返回 `CipherSeries`（列为原列名，值为各列分位数）。
- `q` 为数组：返回 `CipherDataFrame`，行索引为 `q`，列为原列。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

ser = pd.Series([1, 2, 3, 4])
cipher_ser = ct.encrypt_df(ser)
med = cipher_ser.quantile(0.5)
# ct.decrypt(med) -> 中位数
```

```python
import numpy as np

df = pd.DataFrame(np.array([[1, 1], [2, 10], [3, 100], [4, 100]]), columns=["a", "b"])
cipher_df = ct.encrypt_df(df)
# ct.decrypt_df(cipher_df.quantile(0.1))
# ct.decrypt_df(cipher_df.quantile([0.1, 0.5]))
```
