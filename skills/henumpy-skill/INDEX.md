# henumpy 算子索引

所有可用算子的查找表。格式：`hp.func(args)` — 描述 → `文档路径`

标注 `[op: X]` 表示支持运算符重载 `X`。

---

## 算术运算

- `hp.add(x1, x2)` — 加法 [op: `+`] → `docs/数学函数/算术运算/add.md`
- `hp.sub(x1, x2)` — 减法 [op: `-`] → `docs/数学函数/算术运算/sub.md`
- `hp.mul(x1, x2)` — 乘法 [op: `*`] → `docs/数学函数/算术运算/mul.md`
- `hp.div(x1, x2)` — 除法 [op: `/`] → `docs/数学函数/算术运算/div.md`
- `hp.invers(x)` — 求逆 → `docs/数学函数/算术运算/invers.md`
- `hp.pow(x1, x2)` — 幂运算 [op: `**`] → `docs/数学函数/算术运算/pow.md`
- `hp.float_power(x1, x2)` — 浮点幂 → `docs/数学函数/算术运算/float_power.md`
- `hp.floor_divide(x1, x2)` — 整除 [op: `//`] → `docs/数学函数/算术运算/floor_divide.md`
- `hp.reciprocal(x)` — 倒数 → `docs/数学函数/算术运算/reciprocal.md`
- `hp.positive(x)` — 正值 → `docs/数学函数/算术运算/positive.md`
- `hp.negative(x)` — 取负 → `docs/数学函数/算术运算/negative.md`
- `hp.decimal(x)` — 取小数部分 → `docs/数学函数/算术运算/decimal.md`
- `hp.fmod(x1, x2)` — 浮点取模 → `docs/数学函数/算术运算/fmod.md`
- `hp.mod(x1, x2)` — 取模 [op: `%`] → `docs/数学函数/算术运算/mod.md`
- `hp.modf(x)` — 拆分整数和小数部分 → `docs/数学函数/算术运算/modf.md`
- `hp.remainder(x1, x2)` — 余数 → `docs/数学函数/算术运算/remainder.md`
- `hp.divmod(x1, x2)` — 同时返回商和余数 → `docs/数学函数/算术运算/divmod.md`

## 三角函数

- `hp.sin(x)` — 正弦 → `docs/数学函数/三角函数/sin.md`
- `hp.cos(x)` — 余弦 → `docs/数学函数/三角函数/cos.md`
- `hp.tan(x)` — 正切 → `docs/数学函数/三角函数/tan.md`
- `hp.arcsin(x)` — 反正弦 → `docs/数学函数/三角函数/arcsin.md`
- `hp.arccos(x)` — 反余弦 → `docs/数学函数/三角函数/arccos.md`
- `hp.arctan(x)` — 反正切 → `docs/数学函数/三角函数/arctan.md`
- `hp.arctan2(y, x)` — 四象限反正切 → `docs/数学函数/三角函数/arctan2.md`
- `hp.hypot(x1, x2)` — 斜边长 → `docs/数学函数/三角函数/hypot.md`
- `hp.degrees(x)` — 弧度转角度 → `docs/数学函数/三角函数/degrees.md`
- `hp.radians(x)` — 角度转弧度 → `docs/数学函数/三角函数/radians.md`
- `hp.rad2rad(x)` — 弧度归一化 → `docs/数学函数/三角函数/rad2rad.md`
- `hp.deg2rad(x)` — 角度转弧度 → `docs/数学函数/三角函数/deg2rad.md`
- `hp.unwrap(x)` — 相位展开 → `docs/数学函数/三角函数/unwrap.md`

## 双曲函数

- `hp.sinh(x)` — 双曲正弦 → `docs/数学函数/双曲函数/sinh.md`
- `hp.cosh(x)` — 双曲余弦 → `docs/数学函数/双曲函数/cosh.md`
- `hp.tanh(x)` — 双曲正切 → `docs/数学函数/双曲函数/tanh.md`
- `hp.arcsinh(x)` — 反双曲正弦 → `docs/数学函数/双曲函数/arcsinh.md`
- `hp.arccosh(x)` — 反双曲余弦 → `docs/数学函数/双曲函数/arccosh.md`
- `hp.arctanh(x)` — 反双曲正切 → `docs/数学函数/双曲函数/arctanh.md`

## 指数和对数

- `hp.exp(x)` — 指数 e^x → `docs/数学函数/指数和对数/exp.md`
- `hp.expm1(x)` — exp(x)-1 → `docs/数学函数/指数和对数/expm1.md`
- `hp.exp2(x)` — 2^x → `docs/数学函数/指数和对数/exp2.md`
- `hp.expit(x)` — sigmoid → `docs/数学函数/指数和对数/expit.md`
- `hp.log(x)` — 自然对数 → `docs/数学函数/指数和对数/log.md`
- `hp.log10(x)` — 常用对数 → `docs/数学函数/指数和对数/log10.md`
- `hp.log2(x)` — 二进制对数 → `docs/数学函数/指数和对数/log2.md`

## 四舍五入

- `hp.rounding(x)` — 四舍五入 → `docs/数学函数/四舍五入/rounding.md`
- `hp.round(x, decimals)` — 指定精度取近似 → `docs/数学函数/四舍五入/round.md`
- `hp.rint(x)` — 最近整数 → `docs/数学函数/四舍五入/rint.md`
- `hp.fix(x)` — 向零取整 → `docs/数学函数/四舍五入/fix.md`
- `hp.floor(x)` — 下取整 → `docs/数学函数/四舍五入/floor.md`
- `hp.ceil(x)` — 上取整 → `docs/数学函数/四舍五入/ceil.md`
- `hp.trunc(x)` — 截断取整 → `docs/数学函数/四舍五入/trunc.md`

## 轴上聚合运算

- `hp.prod(x, axis)` — 沿轴乘积 → `docs/数学函数/轴上加法、乘法、减法函数/prod.md`
- `hp.sum(x, axis)` — 沿轴求和 → `docs/数学函数/轴上加法、乘法、减法函数/sum.md`
- `hp.nanprod(x, axis)` — 忽略NaN乘积 → `docs/数学函数/轴上加法、乘法、减法函数/nanprod.md`
- `hp.nansum(x, axis)` — 忽略NaN求和 → `docs/数学函数/轴上加法、乘法、减法函数/nansum.md`
- `hp.cumprod(x, axis)` — 累积乘积 → `docs/数学函数/轴上加法、乘法、减法函数/cumprod.md`
- `hp.cumsum(x, axis)` — 累积求和 → `docs/数学函数/轴上加法、乘法、减法函数/cumsum.md`
- `hp.nancumprod(x, axis)` — 忽略NaN累积乘积 → `docs/数学函数/轴上加法、乘法、减法函数/nancumprod.md`
- `hp.nancumsum(x, axis)` — 忽略NaN累积求和 → `docs/数学函数/轴上加法、乘法、减法函数/nancumsum.md`
- `hp.diff(x, n, axis)` — 离散差分 → `docs/数学函数/轴上加法、乘法、减法函数/diff.md`
- `hp.ediff1d(x)` — 连续元素差 → `docs/数学函数/轴上加法、乘法、减法函数/ediff1d.md`
- `hp.gradient(x)` — 梯度 → `docs/数学函数/轴上加法、乘法、减法函数/gradient.md`
- `hp.cross(a, b)` — 叉积 → `docs/数学函数/轴上加法、乘法、减法函数/cross.md`
- `hp.trapz(y, x, dx, axis)` — 梯形积分 → `docs/数学函数/轴上加法、乘法、减法函数/trapz.md`

## 比较函数

- `hp.compare(a, b)` — 通用比较 → `docs/数学函数/比较函数/compare.md`
- `hp.equal(a, b)` — 等于 [op: `==`] → `docs/数学函数/比较函数/equal.md`
- `hp.not_equal(a, b)` — 不等于 [op: `!=`] → `docs/数学函数/比较函数/not_equal.md`
- `hp.greater(a, b)` — 大于 [op: `>`] → `docs/数学函数/比较函数/greater.md`
- `hp.greater_equal(a, b)` — 大于等于 [op: `>=`] → `docs/数学函数/比较函数/greater_equal.md`
- `hp.less(a, b)` — 小于 [op: `<`] → `docs/数学函数/比较函数/less.md`
- `hp.less_equal(a, b)` — 小于等于 [op: `<=`] → `docs/数学函数/比较函数/less_equal.md`

## 杂项数学

- `hp.sqrt(x)` — 平方根 → `docs/数学函数/杂项/sqrt.md`
- `hp.cbrt(x)` — 立方根 → `docs/数学函数/杂项/cbrt.md`
- `hp.square(x)` — 平方 → `docs/数学函数/杂项/square.md`
- `hp.absolute(x)` — 绝对值 → `docs/数学函数/杂项/absolute.md`
- `hp.heaviside(x, h0)` — 阶跃函数 → `docs/数学函数/杂项/heaviside.md`
- `hp.convolve(a, v)` — 卷积 → `docs/数学函数/杂项/convolve.md`
- `hp.clip(x, a_min, a_max)` — 裁剪到范围 → `docs/数学函数/杂项/clip.md`
- `hp.maximum(x1, x2)` — 逐元素取最大 → `docs/数学函数/杂项/maximum.md`
- `hp.minimum(x1, x2)` — 逐元素取最小 → `docs/数学函数/杂项/minimum.md`
- `hp.fmax(x1, x2)` — 忽略NaN取最大 → `docs/数学函数/杂项/fmax.md`
- `hp.fmin(x1, x2)` — 忽略NaN取最小 → `docs/数学函数/杂项/fmin.md`
- `hp.sign(x)` — 符号函数 → `docs/数学函数/杂项/sign.md`
- `hp.interp(x, xp, fp)` — 一维线性插值 → `docs/数学函数/杂项/interp.md`
- `hp.nan_to_num(x)` — NaN替换 → `docs/数学函数/杂项/nan_to_num.md`
- `hp.isclose(a, b)` — 近似相等 → `docs/数学函数/杂项/isclose.md`
- `hp.sort(x, axis)` — 排序 → `docs/数学函数/杂项/sort.md`

## 线性代数 — 矩阵和向量积

- `hp.dot(a, b)` — 点积 → `docs/线性代数/矩阵和向量积/dot.md`
- `hp.inner(a, b)` — 内积 → `docs/线性代数/矩阵和向量积/inner.md`
- `hp.outer(a, b)` — 外积 → `docs/线性代数/矩阵和向量积/outer.md`
- `hp.matmul(A, B)` — 矩阵乘法 [op: `@`] → `docs/线性代数/矩阵和向量积/matmul.md`
- `hp.linalg.matrix_power(M, n)` — 矩阵幂 → `docs/线性代数/矩阵和向量积/(linalg.)matrix_power.md`
- `hp.kron(a, b)` — Kronecker积 → `docs/线性代数/矩阵和向量积/kron.md`

## 线性代数 — 范数与行列式

- `hp.linalg.norm(x)` — 范数 → `docs/线性代数/范数和其他数字/(linalg.)norm.md`
- `hp.det(A)` — 行列式 → `docs/线性代数/范数和其他数字/det.md`
- `hp.trace(A)` — 迹 → `docs/线性代数/范数和其他数字/trace.md`

## 线性代数 — 逆矩阵

- `hp.linalg.inv(A)` — 逆矩阵 → `docs/线性代数/解方程和逆矩阵/(linalg.)inv.md`

## 线性代数 — 其他

- `hp.vander(x, N)` — Vandermonde矩阵 → `docs/线性代数/杂项/vander.md`
- `hp.polyfit(x, y, deg)` — 多项式拟合 → `docs/线性代数/杂项/polyfit.md`

## 统计学

- `hp.min(x, axis)` — 最小值 → `docs/统计学/min.md`
- `hp.max(x, axis)` — 最大值 → `docs/统计学/max.md`
- `hp.nanmin(x, axis)` — 忽略NaN最小值 → `docs/统计学/nanmin.md`
- `hp.nanmax(x, axis)` — 忽略NaN最大值 → `docs/统计学/nanmax.md`
- `hp.ptp(x, axis)` — 极差 → `docs/统计学/ptp.md`
- `hp.percentile(x, q, axis)` — 百分位数 → `docs/统计学/percentile.md`
- `hp.nanpercentile(x, q, axis)` — 忽略NaN百分位数 → `docs/统计学/nanpercentile.md`
- `hp.quantile(x, q, axis)` — 分位数 → `docs/统计学/quantile.md`
- `hp.nanquantile(x, q, axis)` — 忽略NaN分位数 → `docs/统计学/nanquantile.md`
- `hp.median(x, axis)` — 中位数 → `docs/统计学/median.md`
- `hp.nanmedian(x, axis)` — 忽略NaN中位数 → `docs/统计学/nanmedian.md`
- `hp.average(x, axis, weights)` — 加权平均 → `docs/统计学/average.md`
- `hp.mean(x, axis)` — 算术平均 → `docs/统计学/mean.md`
- `hp.nanmean(x, axis)` — 忽略NaN平均 → `docs/统计学/nanmean.md`
- `hp.std(x, axis)` — 标准差 → `docs/统计学/std.md`
- `hp.nanstd(x, axis)` — 忽略NaN标准差 → `docs/统计学/nanstd.md`
- `hp.var(x, axis)` — 方差 → `docs/统计学/var.md`
- `hp.nanvar(x, axis)` — 忽略NaN方差 → `docs/统计学/nanvar.md`
- `hp.cosine(a, b)` — 余弦相似度 → `docs/统计学/cosine.md`
- `hp.corrcoef(x)` — 相关系数矩阵 → `docs/统计学/corrcoef.md`
- `hp.correlate(a, v)` — 互相关 → `docs/统计学/correlate.md`
- `hp.cov(x)` — 协方差矩阵 → `docs/统计学/cov.md`
- `hp.digitize(x, bins)` — 离散化 → `docs/统计学/digitize.md`

## 工具函数

- `hp.empty(shape)` — 空密文标量 → `docs/工具函数/empty.md`
- `hp.empty_array(shape)` — 空密文数组 → `docs/工具函数/empty_array.md`
- `hp.ones(shape)` — 全1密文标量 → `docs/工具函数/ones.md`
- `hp.ones_array(shape)` — 全1密文数组 → `docs/工具函数/ones_array.md`
- `hp.ones_like(x)` — 形状相同的全1 → `docs/工具函数/ones_like.md`
- `hp.zeros(shape)` — 全0密文标量 → `docs/工具函数/zeros.md`
- `hp.zeros_array(shape)` — 全0密文数组 → `docs/工具函数/zeros_array.md`
- `hp.zeros_like(x)` — 形状相同的全0 → `docs/工具函数/zeros_like.md`
- `hp.eye(n)` — 单位矩阵 → `docs/工具函数/eye.md`
- `hp.full(shape, fill_value)` — 指定值填充 → `docs/工具函数/full.md`
- `hp.arange(start, stop, step)` — 等差序列 → `docs/工具函数/arange.md`
- `hp.linspace(start, stop, num)` — 均匀分布 → `docs/工具函数/linspace.md`
- `hp.argmin(x, axis)` — 最小值索引 → `docs/工具函数/argmin.md`
- `hp.argmax(x, axis)` — 最大值索引 → `docs/工具函数/argmax.md`
- `hp.argsort(x, axis)` — 排序索引 → `docs/工具函数/argsort.md`
- `hp.random.choice(a, size)` — 随机选择 → `docs/工具函数/random.choice.md`
- `hp.random.rand(shape)` — 随机数 → `docs/工具函数/random.rand.md`
- `hp.append(arr, values)` — 追加元素 → `docs/工具函数/append.md`
- `hp.flip(x, axis)` — 翻转 → `docs/工具函数/flip.md`
- `hp.where(cond, x, y)` — 条件选择 → `docs/工具函数/where.md`
- `hp.set_parallelization(strategy)` — 并行策略配置 → `docs/工具函数/set_parallelization.md`

## 数组操作

- 下标访问 `a[i]`, `a[i:j]`, `A[i,j]` — 索引和切片
- `hp.transpose(A)` — 转置 [op: `.T`] → `docs/数组操作/transpose.md`
- `hp.insert(arr, obj, values)` — 插入元素 → `docs/数组操作/insert.md`
- `a.cipherLen()` — 密文长度 → `docs/数组操作/cipherLen.md`
- `a.cipherShape()` — 密文形状 → `docs/数组操作/cipherShape.md`
- `a.get_cipher_type()` — 密文类型(1=标量,2=数组,3=离散) → `docs/数组操作/get_cipher_type.md`
- `a.get_encryption_type()` — 加密方式(0=行,1=列) → `docs/数组操作/get_encryption_type.md`
- `a.transEncType()` — 行列加密方式转换 → `docs/数组操作/transEncType.md`
- `hp.broadcast_to(x, shape)` — 广播 → `docs/数组操作/broadcast_to.md`
- `hp.broadcast_arrays(*args)` — 多数组广播 → `docs/数组操作/broadcast_arrays.md`
