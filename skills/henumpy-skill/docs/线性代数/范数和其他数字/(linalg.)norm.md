# (linalg.)norm

### 计算向量范数

## 参数

- `a`：数组密文，输入数组
- `ord`： $ None $、正整数、0、inf、-inf，可选 范数类型选择，默认为 2-范数

## 返回值

标量密文 `norm`：$ a $指定类型的范数 + 0-范数（表示不为零的元素个数） + 1-范数（表示向量元素绝对值之和） $ \parallel a \parallel _1=\sum\limits_{i=0}^{N-1}\mid a_i\mid   $ + 2-范数 $ \parallel a \parallel _2=\sqrt{\sum\limits_{i=0}^{N-1} a_i^2}  $ + p-范数（向量元素绝对值的 p 次幂加和之后，开 p 次方根） $ \parallel a \parallel _p=\left(\sum\limits_{i=0}^{N-1} \mid a_i\mid ^p\right)^{1/p} $ + inf 范数（所有向量元素绝对值中的最大值） $ \parallel a \parallel _\infty=\max_i\mid a_i\mid $ + -inf 范数（所有向量元素绝对值中的最小值） $ \parallel a \parallel _{-\infty}=\min_i\mid a_i\mid $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量, 默认 ord=2
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.norm(a)
print(ct.decrypt(res))
# 输出 4.340506882842139

# 向量, ord=0
print(hp.norm(a,0))
# 输出 4

# 向量, ord=1
res = hp.norm(a, 1)
print(ct.decrypt(res))
# 输出 5.1999999999999975

# 向量, ord=4
res = hp.norm(a, 4)
print(ct.decrypt(res))
# 输出 4.300222290232113

# 向量, ord=inf
res = hp.norm(a, np.PINF)
print(ct.decrypt(res))
# 输出 4.299999999999999

# 向量, ord=-inf
res = hp.norm(a, np.NINF)
print(ct.decrypt(res))
# 输出 0.1
```
