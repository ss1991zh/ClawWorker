# encrypt_ndarray
数值数组加密，支持单值、一维和二维数组。
## 签名
`ct.encrypt_ndarray(input_array, encrypt_by_column=False, discrete=False)`
## 参数
- `input_array`：待加密数据。可以是单个数、一维或二维数组，支持整型和浮点型。
- `encrypt_by_column`：是否按列加密。默认 `False`（按行加密）。按行加密适合列维度不变而行维度变化的场景；按列加密适合行维度不变而列维度变化的场景。
- `discrete`：是否离散形式加密。默认 `False`（连续形式）。离散形式将每个元素单独加密，适合元素独立运算的场景；连续形式有计算加速效果。
## 返回值
加密后的密文数组。
## 示例
```python
import crypto_toolkit as ct
import numpy as np

ct.initSK()

a = 5
A = ct.encrypt_ndarray(a)
print(ct.decrypt_ndarray(A))  # 5.0

x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
X = ct.encrypt_ndarray(x)
print(ct.decrypt_ndarray(X))  # [[1. 2. 3.] [4. 5. 6.]]

X_col = ct.encrypt_ndarray(x, encrypt_by_column=True)
print(ct.decrypt_ndarray(X_col, decrypt_by_column=True))  # [[1. 2. 3.] [4. 5. 6.]]
```
