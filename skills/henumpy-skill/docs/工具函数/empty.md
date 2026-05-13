# empty

### 创建空密文标量

## 参数

无

## 返回值

标量密文

`empty`： 空密文标量 $ empty()=[x_1,\ x_2,\ y_1,\ y_2,\ nan] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 创建空密文标量
res = hp.empty()
print(ct.decrypt(res))
# 输出 nan
```
