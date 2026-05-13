# empty_array

### 创建空密文数组

## 参数

无

## 返回值

数组密文

`empty_array`： 空密文数组 $ empty\_array()=[x_1,\ x_2,\ y_1,\ y_2,\ 0,\ 0] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 创建空密文数组
res = hp.empty_array()
print(ct.decrypt(res))
# 输出 [nan]
```
