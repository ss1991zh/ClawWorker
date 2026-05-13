# digitize

### 返回输入数组中每个值所属的 bin 的索引

## 参数

- `a`：数组密文，输入数组
- `bins`：数组密文，bin 数组，它必须是一维且单调的。
- `right`：bool 型，可选 指示间隔是包括右边还是左边箱边。默认行为为$ (right=False) $，表示间隔不包括右边缘。在这种情况下，左边的箱端是打开的，例如 $ bin[i-1] ≤ x < bin[i] $是单调递增箱的默认行为。

## 返回值

标量密文 `digitize`：$ a $中每个值所属的$ bin $的索引 + 默认$ right=False $ - $ bins $为单调递增数组，若$ bins[i-1] ≤ x < bins[i] $，则$ digitize(x) = i $ 若$  x ≥ bins  $上界，则返回$  len(bins) $，若$  x < bins  $下届，则返回 0 - $ bins $为单调递减数组，若$  bins[i-1] ≥ x > bins[i] $，则$ digitize(x) = i $ 若$  x ≥ bins  $上界，则返回 0，若$  x < bins  $下届，则返回$  len(bins) $ + $ right=True $ - $ bins $为单调递增数组，若$  bins[i-1] < x ≤ bins[i] $，则$ digitize(x) = i $ 若$  x > bins  $上界，则返回$  len(bins) $，若$  x ≤ bins  $下届，则返回 0 - $ bins $为单调递减数组，若$  bins[i-1] > x ≥ bins[i] $，则$ digitize(x) = i $ 若$  x > bins  $上界，则返回 0，若$  x ≤ bins  $下届，则返回$  len(bins) $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量, bins 递增, 默认 right=False
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bins_plain = np.array([2.1, 4.0, 5.2, 40.5])
bins = ct.encrypt(bins_plain)
res = hp.digitize(a, bins)
print(res)
# 输出 [0 0 2 0]

# 数组, bins 递增, right=True
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.digitize(A, bins, right=True)
print(res)
# 输出 [[0 0 1]
#     	[0 0 2]
#     	[1 0 1]]
```
