# convolve

### 返回两个一维序列的离散线性卷积

## 参数

数组密文

- `a`：第一个输入数组， $ 1\times N $维
- `v`：第二个输入数组， $ 1\times M $维
- `mode`：“full”，“same”，“valid”，可选 + 默认“full”，这将返回每个重叠点的卷积，输出长度为 $ len=N+M-1 $。在卷积的端点，信号没有完全重叠，并且可以看到边界效应。 + 模式 “same”， 返回长度 $ len=max(M,\ N) $ 的输出，边界效果仍然可见。 + 模式 “valid”，返回长度 $ len=max(M,\ N)-min(M,\ N)+1 $的输出，仅给出卷积积对于信号完全重叠的点，外部值信号边界不起作用。

## 返回值

数组密文 `convolve`：$ a $和$ v $的离散线性卷积 设$ a=[a_0,\ a_1, \dots,a_{N-1}] $,$ v=[v_0,\ v_1,\dots,v_{M-1}] $ 则$ convolve(a,v)(n)=\sum_{i=0}^na_iv_{n-i} \  \ \ \ \ n\in[0,\ len-1] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# full
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.convolve(a, b)
print(ct.decrypt(res))
# 输出 [  1.05   2.63  12.83  39.22  34.91 174.67   4.05]

# same
res = hp.convolve(a, b, "same")
print(ct.decrypt(res))
# 输出 [ 2.63 12.83 39.22 34.91]

# valid
res = hp.convolve(a, b, "valid")
print(ct.decrypt(res))
# 输出 [39.22]
```
