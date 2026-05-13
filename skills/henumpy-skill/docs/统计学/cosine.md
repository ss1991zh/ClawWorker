# cosine

### 计算一维数组之间的余弦距离

## 参数

- `u`：离散数组密文，第一个一维数组
- `v`：离散数组密文，第二个一维数组

## 返回值

标量密文 `cosine`：$ u $和$ v $的余弦距离 $ cosine(u,\ v)=1-\frac{u \cdot v}{||u||\ ||v||} $ 其中$ u \cdot v $是$ u $和$ v $的点积

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa, discrete=True)
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb, discrete=True)
res = hp.cosine(a, b)
print(ct.decrypt(res)) 
# 输出 0.8392732690372228
```
