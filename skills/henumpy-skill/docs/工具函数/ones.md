# ones

### 返回 1 标量密文

## 参数

无

## 返回值

标量密文

`ones`： 1 密文标量 $ ones()=cc1 $

注：cc1为 1 的密文，随计算字典的不同而改变

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 创建 1 密文标量
res = hp.ones()
print(ct.decrypt(res))
# 输出 0.9999999999999998
```
