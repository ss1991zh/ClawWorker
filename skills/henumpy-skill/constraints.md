# henumpy 约束与注意事项

## 初始化（必须）

每个脚本在调用任何计算前必须执行初始化：

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()   # 初始化计算字典
ct.initSK()     # 初始化密钥
```

## 加密与解密

| 操作 | 函数 | 说明 |
|------|------|------|
| 加密标量/向量/矩阵 | `ct.encrypt(data)` | data 为 Python 数值或 numpy 数组 |
| 按列加密 | `ct.encrypt(data, encrypt_by_column=True)` | 默认行加密 |
| 加密为 ndarray | `ct.encrypt_ndarray(data)` | 替代方式 |
| 离散加密 | `ct.encrypt_ndarray(data, discrete=True)` | 生成离散密文数组 |
| 解密 | `ct.decrypt(cipher)` | 返回 numpy 数组或标量 |
| 解密 ndarray | `ct.decrypt_ndarray(cipher)` | 替代方式 |

## 密文类型

通过 `a.get_cipher_type()` 查询：

| 返回值 | 含义 |
|--------|------|
| 1 | 标量密文 |
| 2 | 数组密文（连续） |
| 3 | 离散数组密文 |

加密方式通过 `a.get_encryption_type()` 查询：
- `0` = 行加密（默认）
- `1` = 列加密
- 转换方法：`a.transEncType()`

## 与 numpy 的命名差异

| numpy | henumpy | 说明 |
|-------|---------|------|
| `np.multiply` | `hp.mul` | 乘法 |
| `np.subtract` | `hp.sub` | 减法 |
| `np.divide` | `hp.div` | 除法 |
| `np.power` | `hp.pow` | 幂运算 |
| `np.abs` | `hp.absolute` | 绝对值 |
| `np.linalg.inv` | `hp.linalg.inv` | 逆矩阵 |
| — | `hp.invers` | henumpy 独有：求逆 |
| — | `hp.decimal` | henumpy 独有：取小数部分 |
| — | `hp.rounding` | henumpy 独有：四舍五入 |
| `scipy.special.expit` | `hp.expit` | sigmoid 函数 |

## 运算符重载

密文对象支持以下运算符：

```python
a + b       # hp.add(a, b)
a - b       # hp.sub(a, b)
a * b       # hp.mul(a, b)
a / b       # hp.div(a, b)
a // b      # hp.floor_divide(a, b)
a % b       # hp.mod(a, b)
a ** b      # hp.pow(a, b)
a @ b       # hp.matmul(a, b)
a.T         # hp.transpose(a)
a > b       # hp.greater(a, b)
a >= b      # hp.greater_equal(a, b)
a < b       # hp.less(a, b)
a <= b      # hp.less_equal(a, b)
a == b      # hp.equal(a, b)
a != b      # hp.not_equal(a, b)
```

## 比较函数返回布尔值

比较操作（`hp.greater`、`hp.less` 等）返回 Python `True`/`False` 或 numpy 布尔数组，**不是密文**。布尔结果可直接用于 `hp.where` 的 condition 参数。

## output_encrypt_type 参数

多数计算函数支持可选的 `output_encrypt_type` 参数：
- 省略：输出加密方式与输入一致
- `output_encrypt_type=0`：输出为行加密
- `output_encrypt_type=1`：输出为列加密

## discrete 参数

部分函数（如 `hp.mul`）支持 `discrete` 参数：
- `discrete=False`（默认）：返回连续密文数组
- `discrete=True`：返回离散密文数组

## 索引和切片

密文数组支持标准 numpy 索引语法：

```python
a[0]        # 取第 0 个元素
a[0:2]      # 切片
A[0]        # 取第 0 行
A[1, 1]     # 取 (1,1) 元素
A[0:2, 0:2] # 子矩阵切片
A[0:2, 1]   # 取列切片
```

## 并行化配置

```python
hp.set_parallelization(0)    # 全部非并行（数据量 < 百万）
hp.set_parallelization(1)    # 全部并行（数据量 >= 百万）
hp.set_parallelization(2)    # 默认配置（推荐）
hp.set_parallelization()     # 恢复默认，等价于 2
hp.set_parallelization({"add": "True", "sub": "True"})  # 按函数指定
```

## 精度特性

同态加密计算结果存在浮点精度误差（如 `5 + 3` 可能输出 `7.999999999999999`），这是同态加密的固有特性。
