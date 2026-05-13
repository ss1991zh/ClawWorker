# cov

## 描述

**CipherSeries：** 与另一条 `CipherSeries` 计算协方差（内部会对齐索引，长度可不同），无偏估计用 `N-1` 归一化。

**CipherDataFrame：** 无参时返回列间协方差矩阵；NA 在计算中排除。

## 参数（CipherSeries）

| 参数 | 说明 |
|------|------|
| `other` | 另一条 `CipherSeries`。 |

## 参数（CipherDataFrame）

无参调用：对全部列两两协方差。

## 返回值

- `CipherSeries.cov(other)` → `CipherFloat`
- `CipherDataFrame.cov()` → `CipherDataFrame`（协方差矩阵）

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import pandas as pd

s1 = pd.Series([0.9, 0.13, 0.62])
s2 = pd.Series([0.12, 0.27, 0.51])
c1, c2 = ct.encrypt_df(s1), ct.encrypt_df(s2)
cf = c1.cov(c2)
# ct.decrypt(cf) -> 标量协方差
```

```python
df = pd.DataFrame([(1, 2), (0, 3), (2, 0), (1, 1)], columns=["dogs", "cats"])
cipher_df = ct.encrypt_df(df)
mat = cipher_df.cov()
# ct.decrypt_df(mat) -> 2x2 协方差矩阵
```
