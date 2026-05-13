# pandaseal API 索引

所有可用 API 的查找表。格式：`签名` — 描述 → `文档路径`

标注 `[op: X]` 表示支持运算符重载 `X`。

---

## 生成对象

- `ps.CipherDataFrame(data, index, columns, copy)` — 从 CipherArray 构造密文 DataFrame → `docs/生成对象/CipherDataFrame.md`
- `ps.CipherSeries(data, index, name, copy)` — 从 CipherArray 构造密文 Series → `docs/生成对象/CipherSeries.md`

## 数据输入/输出

- `ps.read_csv(path, header)` — 从 CSV 文件读取密文数据 → `docs/数据输入输出/read_csv.md`
- `ps.read_excel(path, index_col, header, sheet_name)` — 从 Excel 文件读取密文数据 → `docs/数据输入输出/read_excel.md`
- `ps.read_json(path, typ)` — 从 JSON 文件读取密文数据 → `docs/数据输入输出/read_json.md`
- `cdf.to_csv(path)` — 将 CipherDataFrame 导出为 CSV → `docs/数据输入输出/to_csv.md`
- `cdf.to_excel(path, sheet_name, header, index)` — 将 CipherDataFrame 导出为 Excel → `docs/数据输入输出/to_excel.md`
- `cdf.to_json(path)` — 将 CipherDataFrame 导出为 JSON → `docs/数据输入输出/to_json.md`

## 属性

- `cdf.size` — 返回元素总数 → `docs/属性/size.md`
- `cdf.shape` — 返回 (行数, 列数) 元组 → `docs/属性/shape.md`
- `cdf.ndim` — 返回维度数 → `docs/属性/ndim.md`

## 选择

- `cdf[key]` — 按列名或布尔数组选择数据 → `docs/选择/brackets.md`
- `cdf.loc[label]` — 基于标签的行列访问 → `docs/选择/loc.md`
- `cdf.iloc[pos]` — 基于整数位置的行列访问 → `docs/选择/iloc.md`
- `cdf.at[label, col]` — 按标签访问单个标量值 → `docs/选择/at.md`
- `cdf.iat[row, col]` — 按整数位置访问单个标量值 → `docs/选择/iat.md`
- `cdf[bool_array]` — 布尔索引筛选行 → `docs/选择/boolean_indexing.md`

## 查看数据

- `cdf.head(n)` — 返回前 n 行，默认 5 → `docs/查看数据/head.md`
- `cdf.tail(n)` — 返回后 n 行，默认 5 → `docs/查看数据/tail.md`
- `cdf.index` — 获取行索引 → `docs/查看数据/index_attr.md`
- `cdf.columns` — 获取列标签 → `docs/查看数据/columns.md`
- `cdf.to_cipherarray()` — 转换为 CipherArray → `docs/查看数据/to_cipherarray.md`
- `cdf.sort_index(axis, ascending, inplace, na_position)` — 按索引排序 → `docs/查看数据/sort_index.md`
- `cdf.sort_values(by, axis, ascending, na_position)` — 按值排序 → `docs/查看数据/sort_values.md`

## 二元操作函数

- `cdf.add(other, fill_value)` — 逐元素加法 [op: `+`] → `docs/二元操作函数/add.md`
- `cdf.sub(other, fill_value)` — 逐元素减法 [op: `-`] → `docs/二元操作函数/sub.md`
- `cdf.mul(other, fill_value)` — 逐元素乘法 [op: `*`] → `docs/二元操作函数/mul.md`
- `cdf.div(other, fill_value)` — 逐元素除法 [op: `/`] → `docs/二元操作函数/div.md`
- `cdf.radd(other, fill_value)` — 反向加法 → `docs/二元操作函数/radd.md`
- `cdf.rsub(other, fill_value)` — 反向减法 → `docs/二元操作函数/rsub.md`
- `cdf.rmul(other, fill_value)` — 反向乘法 → `docs/二元操作函数/rmul.md`
- `cdf.rdiv(other, fill_value)` — 反向除法 → `docs/二元操作函数/rdiv.md`
- `cdf.lt(other)` — 逐元素小于 [op: `<`] → `docs/二元操作函数/lt.md`
- `cdf.gt(other)` — 逐元素大于 [op: `>`] → `docs/二元操作函数/gt.md`
- `cdf.le(other)` — 逐元素小于等于 [op: `<=`] → `docs/二元操作函数/le.md`
- `cdf.ge(other)` — 逐元素大于等于 [op: `>=`] → `docs/二元操作函数/ge.md`
- `cdf.ne(other)` — 逐元素不等于 [op: `!=`] → `docs/二元操作函数/ne.md`
- `cdf.eq(other)` — 逐元素等于 [op: `==`] → `docs/二元操作函数/eq.md`

## 缺失值

- `cdf.dropna(axis, how, thresh, subset)` — 删除含缺失值的行或列 → `docs/缺失值/dropna.md`
- `cdf.fillna(value, method, axis, inplace)` — 填充缺失值 → `docs/缺失值/fillna.md`
- `cdf.isna()` — 检测缺失值，返回布尔 DataFrame → `docs/缺失值/isna.md`

## 运算

- `cdf.mean(axis, skipna)` — 指定轴上的均值 → `docs/运算/mean.md`
- `cdf.std(axis, skipna, ddof)` — 指定轴上的标准差 → `docs/运算/std.md`
- `cdf.var(axis, skipna, ddof)` — 指定轴上的方差 → `docs/运算/var.md`
- `cdf.max(axis, skipna)` — 指定轴上的最大值 → `docs/运算/max.md`
- `cdf.min(axis, skipna)` — 指定轴上的最小值 → `docs/运算/min.md`
- `cdf.quantile(q, axis)` — 指定分位数 → `docs/运算/quantile.md`
- `cdf.cov(min_periods, ddof)` — 协方差矩阵 → `docs/运算/cov.md`
- `cdf.pct_change(periods)` — 百分比变化 → `docs/运算/pct_change.md`
- `cdf.shift(periods, axis, fill_value)` — 数据偏移 → `docs/运算/shift.md`
- `cdf.cumsum(axis, skipna)` — 累积求和 → `docs/运算/cumsum.md`

## 合并

- `ps.merge(left, right, how, on)` — 合并两个 CipherDataFrame → `docs/合并/merge.md`
- `ps.concat(objs, axis, join, ignore_index)` — 拼接多个对象 → `docs/合并/concat.md`
- `cdf.join(other, on, how, lsuffix, rsuffix)` — 按索引合并 → `docs/合并/join.md`
- `cdf.align(other, join, axis)` — 对齐两个对象 → `docs/合并/align.md`

## 去重

- `cdf.drop_duplicates(subset, keep, inplace)` — 删除重复行 → `docs/去重/drop_duplicates.md`

## 分桶

- `ps.cut(x, bins, right, labels, ordered)` — 将连续值分段为离散区间 → `docs/分桶/cut.md`

## 分组

- `cdf.groupby(level)` — 按索引分组，返回 GroupBy 对象 → `docs/分组/groupby.md`
- `group.sum()` — 分组求和 → `docs/分组/sum.md`
- `group.mean()` — 分组均值 → `docs/分组/mean.md`
- `group.median()` — 分组中位数 → `docs/分组/median.md`
- `group.std(ddof)` — 分组标准差 → `docs/分组/std.md`
- `group.var(ddof)` — 分组方差 → `docs/分组/var.md`
- `group.quantile(q)` — 分组分位数 → `docs/分组/quantile.md`
