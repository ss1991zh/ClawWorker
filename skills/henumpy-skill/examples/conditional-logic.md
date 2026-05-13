# 示例：条件选择与比较

使用 `hp.where` 和比较运算在密文上实现条件逻辑。

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
b = ct.encrypt(np.array([2.1, 4.0, 5.2, 40.5]))

# 布尔数组作为条件
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

# 比较函数返回布尔值（非密文）
x1 = ct.encrypt(5.0)
x2 = ct.encrypt(3.0)
print(hp.greater(x1, x2))    # True
print(x1 > x2)               # True（运算符等价）
print(a > 0.5)               # [False False  True False]
```
