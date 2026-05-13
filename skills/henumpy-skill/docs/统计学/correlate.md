# correlate

### 返回两个一维序列的互相关

## 参数

数组密文

- `a`：第一个输入数组， $ 1\times N $维
- `v`：第二个输入数组， $ 1\times M $维
- `mode`：“valid”，“same”，“full”，可选 + 默认 “valid”，返回长度 $ len=max(M,\ N)-min(M,\ N)+1 $的输出，仅给出卷积积对于信号完全重叠的点，外部值信号边界不起作用。 + 模式 “same”， 返回长度 $ len=max(M,\ N) $ 的输出，边界效果仍然可见。 + 模式“full”，这将返回每个重叠点的卷积，输出长度为 $ len=N+M-1 $。在卷积的端点，信号没有完全重叠，并且可以看到边界效应。

## 返回值

数组密文 `correlate`：$ a $和$ v $的互相关 设$ a=[a_0,\ a_1, \dots,a_{N-1}] $,$ v=[v_0,\ v_1,\dots,v_{M-1}] $ 则$ correlate(a,v)(k)=\sum_{i=0}^{N-1}a_iv_{i-k}  $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# valid
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.correlate(a, b)
print(ct.decrypt(res))
# 输出 [28.66]

# same
res = hp.correlate(a, b, "same")
print(ct.decrypt(res))
# 输出 [ 14.75 177.71  28.66  18.35]

# full
res = hp.correlate(a, b, "full")
print(ct.decrypt(res))
# 输出 [ 20.25  14.75 177.71  28.66  18.35   9.43   0.21]
```
