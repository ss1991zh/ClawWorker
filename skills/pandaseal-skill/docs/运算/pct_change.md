# pct_change

## 描述

计算相对前一元素（或前 `periods` 步）的**分数变化** `(x - x_prev) / x_prev`，而非百分数；若需百分数，对结果乘以 100。

## 参数

| 参数 | 说明 |
|------|------|
| `periods` | `int`，默认 `1`。可为负表示反向。 |

## 返回值

同类型的 `CipherSeries` 或 `CipherDataFrame`；首行或位移不足处为 NA。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

s = pd.Series([90, 91, 85])
cipher_s = ct.encrypt_df(s)
r = cipher_s.pct_change()
# ct.decrypt_df(r) -> 第一行为 NaN，其后为逐期分数变化
```

```python
df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
cipher_df = ct.encrypt_df(df)
# cipher_df.pct_change(periods=2)
```
