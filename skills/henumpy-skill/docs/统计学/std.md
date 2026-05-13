# hp.std

沿指定轴计算标准差。

## 签名

```python
hp.std(a, axis=None)
```

## 参数

- `a`: 数组密文 — 输入数组
- `axis` (可选): None 或 int — 计算轴。默认 None，对全部元素计算

## 返回值

标量密文或数组密文 — 标准差 `sqrt(mean((a - mean(a))²))`。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
print(ct.decrypt(hp.std(a)))
# 输出 1.7378147196982758

# 矩阵全局标准差
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
print(ct.decrypt(hp.std(A)))
# 输出 2.0245407953654007

# 按列标准差 (axis=0)
print(ct.decrypt(hp.std(A, axis=0)))
# 输出 [0.81649658 2.1602469  0.47140452]
```
