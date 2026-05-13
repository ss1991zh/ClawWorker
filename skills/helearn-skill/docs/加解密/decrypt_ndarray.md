# decrypt_ndarray
数值数组解密。
## 签名
`ct.decrypt_ndarray(input_array, decrypt_by_column=False, discrete=False)`
## 参数
- `input_array`：密文数组。
- `decrypt_by_column`：是否按列解密。默认 `False`（按行解密）。缺省即可，接口会自动判断。
- `discrete`：数据是否为离散形式加密。默认 `False`。
## 返回值
解密后的明文 numpy 数组。
## 示例
```python
import crypto_toolkit as ct
import numpy as np

ct.initSK()

x = np.array([[1.0, 2.0], [3.0, 4.0]])
X = ct.encrypt_ndarray(x)
result = ct.decrypt_ndarray(X)
print(result)  # [[1. 2.] [3. 4.]]
```
