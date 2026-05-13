# hp.set_parallelization

配置 CPU 多核并行策略。

## 签名

```python
hp.set_parallelization(parallel_strategy=2)
```

## 参数

- `parallel_strategy` (可选): int 或 dict — 并行策略
  - `0` — 全部非并行（推荐数据量 < 百万）
  - `1` — 全部并行（推荐数据量 >= 百万）
  - `2` 或 `None` — 默认配置（推荐，各算子独立优化）
  - `dict` — 按函数指定，如 `{"add": "True", "sub": "True"}`

## 返回值

无。

## 相关函数

- `hp.get_func_parallelization_config()` — 查看所有算子的并行配置
- `hp.get_func_parallelization_config("sin")` — 查看单个算子配置

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

plain = np.random.normal(-100.0, 100.0, size=(1000, 100))
cipher = ct.encrypt(plain)

# 默认配置
res = hp.arctan(cipher)

# 全部并行
hp.set_parallelization(1)
res = hp.arctan(cipher)

# 全部非并行
hp.set_parallelization(0)
res = hp.add(cipher, cipher)

# 恢复默认
hp.set_parallelization()

# 按函数指定
hp.set_parallelization({"add": "True", "sub": "True"})

# 查看配置
print(hp.get_func_parallelization_config("sin"))
# 输出 True
```

## 默认并行配置

默认并行的算子（`set_parallelization(2)` 时）：

**并行**: sin, cos, tan, arcsin, arccos, arctan, arctan2, hypot, sinh, cosh, tanh, arcsinh, arccosh, arctanh, floor_divide, fmod, mod, remainder, divmod, float_power, decimal, modf, rounding, round, rint, fix, floor, ceil, trunc, nansum, ediff1d, exp, expm1, exp2, expit, log, log10, log2, sqrt, cbrt, sort, matrix_power, dot, inner, matmul, kron, min, max, nanmin, nanmax, ptp, percentile, nanpercentile, quantile, nanquantile, median, nanmedian, average, mean, nanmean, std, nanstd, var, nanvar, corrcoef, cov, digitize, argmin, argmax, argsort, append, transpose, trans_enctype

**非并行**: unwrap, add, sub, mul, div, invers, pow, reciprocal, positive, negative, prod, sum, nanprod, diff, gradient, trapz, compare, equal, not_equal, greater_equal, less_equal, greater, less, square, sign, interp, clip, heaviside, maximum, minimum, fmax, fmin, isclose, outer, trace, where
