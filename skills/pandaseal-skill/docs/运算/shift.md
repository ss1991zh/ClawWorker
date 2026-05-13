# shift

## 描述

按周期平移数据；可选 `freq` 平移时间索引。无 `freq` 时只移动数据，不对齐到全局时间轴。

## 参数

| 参数 | 说明 |
|------|------|
| `periods` | `int` 或可迭代整数；多值时结果列会带后缀。 |
| `freq` | 偏移量；索引为 Datetime 时可用；`"infer"` 从索引推断。 |
| `fill_value` | `CipherFloat`，可选，填充新出现的空位。 |

## 返回值

平移后的 `CipherSeries` 或 `CipherDataFrame` 副本。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

a = pd.Series([1, 4, 3, np.nan, 6], index=list("abcde"))
cipher_a = ct.encrypt_df(a)
res = cipher_a.shift(periods=2)
# ct.decrypt_df(res) -> 前两位 NaN，数据下移
```

```python
df = pd.DataFrame({"C": [10, 20]}, index=pd.date_range("2020-01-01", periods=2))
cipher_df = ct.encrypt_df(df)
# cipher_df.shift(1, fill_value=ct.encrypt(0))
# cipher_df.shift(3, freq="D")
```
