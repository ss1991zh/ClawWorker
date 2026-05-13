# random.choice

### 抽样函数

## 参数

- `a`：一维数组 待抽样样本，新的样本元素来自这个数组
- `size`：整数，可选 输出大小，如果是整数，输出该数量元素的一维数组，默认返回单个元素。

## 返回值

标量密文或数组密文 `random.choice`：随机从$ a $中抽取$ size $个样本

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.random.choice(a)
print(ct.decrypt(res))
# 输出 [0.3]

# 向量, size=2
res = hp.random.choice(a, 2)
print(ct.decrypt(res))
# 输出 [4.3 0.1]
```
