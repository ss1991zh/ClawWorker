# hp.sin

逐元素正弦函数。

## 签名

```python
hp.sin(x, output_encrypt_type=None)
```

## 参数

- `x`: 标量密文/数组密文 — 弧度制角度
- `output_encrypt_type` (可选): int — 输出加密方式。省略=与输入一致, 0=行加密, 1=列加密

## 返回值

标量密文或数组密文 — `x` 的正弦值。

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5.0)
print(ct.decrypt(hp.sin(x)))
# 输出 -0.9589242746631375

# 验证 sin(pi/6) = 0.5
t = ct.encrypt(np.pi / 6)
print(ct.decrypt(hp.sin(t)))
# 输出 0.4999999999999997

# 向量
a = ct.encrypt(np.array([0.5, 0.3, 4.3, 0.1]))
print(ct.decrypt(hp.sin(a)))
# 输出 [ 0.47942554  0.29552021 -0.91616594  0.09983342]

# 矩阵
A = ct.encrypt(np.array([[1., 2., 3.], [2., -3., 4.], [3., 1., 4.]]))
print(ct.decrypt(hp.sin(A)))
# 输出 [[ 0.84147098  0.90929743  0.14112001]
#       [ 0.90929743 -0.14112001 -0.7568025 ]
#       [ 0.14112001  0.84147098 -0.7568025 ]]
```
