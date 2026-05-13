# hp.where

根据条件选择元素。

## 签名

```python
hp.where(condition, x=None, y=None)
```

## 参数

- `condition`: 布尔数组或条件表达式 — 选择条件
- `x` (可选): 标量密文/数组密文 — condition 为 True 时选取的值
- `y` (可选): 标量密文/数组密文 — condition 为 False 时选取的值

若省略 x 和 y，返回满足条件的元素索引（元组形式）。

## 返回值

- 提供 x, y 时：数组密文 — 根据 condition 从 x 或 y 选取的新数组
- 仅提供 condition 时：索引元组 — 满足条件的坐标

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 布尔数组作为条件
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
b = ct.encrypt(np.array([2.1, 4.0, 5.2, 40.5]))
condition = np.array([True, False, True, True])
res = hp.where(condition, a, b)
print(ct.decrypt(res))
# 输出 [0.5 4.  4.3 0.1]

# 条件表达式
x = ct.encrypt(5.0)
y = ct.encrypt(3.0)
t = hp.arange(4)
res = hp.where(t > 1, x, y)
print(ct.decrypt(res))
# 输出 [3. 3. 5. 5.]

# 标量和向量混合
res = hp.where(t > 1, x, a)
print(ct.decrypt(res))
# 输出 [0.5 0.3 5.  5. ]

# 仅传 condition — 返回满足条件的索引
res = hp.where(t > 1)
print(res)
# 输出 (array([2, 3], dtype=int64),)
```
