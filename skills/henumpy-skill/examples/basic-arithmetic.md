# 示例：基础算术运算

在密文上执行 `result = (a + b) * c - d`。

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

a = ct.encrypt(np.array([1.0, 2.0, 3.0, 4.0]))
b = ct.encrypt(np.array([5.0, 6.0, 7.0, 8.0]))
c = ct.encrypt(2.0)
d = ct.encrypt(1.0)

# 函数调用方式
sum_ab = hp.add(a, b)
prod   = hp.mul(sum_ab, c)
result = hp.sub(prod, d)

# 运算符方式（等价）
result2 = (a + b) * c - d

# 密文与明文混合运算
result3 = hp.add(a, 10)       # 密文 + 明文标量
result4 = hp.mul(a, 2)        # 密文 * 明文标量
result5 = a + 10              # 运算符同样支持

print(ct.decrypt(result))   # [11. 15. 19. 23.]
print(ct.decrypt(result3))  # [11. 12. 13. 14.]
```
