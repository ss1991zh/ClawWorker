# isna

## 描述

返回与输入同形状的布尔掩码：`None` / `NaN` 等为 `True`，其余为 `False`。空字符串、`inf` 等是否视为 NA 与 pandas 选项一致。

## 参数

无（实例方法）。

## 返回值

`Series` / `DataFrame`，dtype 为 `bool`，表示每个位置是否为 NA。

## 示例

假定已调用 `hp.initDict()` 与 `ct.initSK()`。

```python
import numpy as np
import pandas as pd

df = pd.DataFrame([[1.0, np.nan], [3.0, 4.0]])
cipher_df = ct.encrypt_df(df)
mask = cipher_df.isna()
# mask 明文等价于各元素是否为 NaN
```

```python
ser = pd.Series([5.0, 6.0, np.nan])
cipher_ser = ct.encrypt_df(ser)
mask = cipher_ser.isna()
# 最后一行为 True
```
