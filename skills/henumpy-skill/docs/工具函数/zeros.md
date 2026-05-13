# zeros

### 返回 0 标量密文

## 参数

无

## 返回值

标量密文

`zeros`： 0 密文标量 $ zeros()=cc0 $

注：cc0为 0 的密文，随计算字典的不同而改变

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# 创建 0 密文标量
res = hp.zeros()
print(ct.decrypt(res))
# 输出 9.999999999999999e-16
```
