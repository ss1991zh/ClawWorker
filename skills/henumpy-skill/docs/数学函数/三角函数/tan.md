# tan

### 正切函数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `tan`： $ x $的正切值

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt_ndarray(5.0)
res = hp.tan(x)
print(ct.decrypt_ndarray(res))
# 输出  -3.380515006246599  
    
# 验证 tan(pi/3) = sin(pi/3) / cos(pi/3)
t = ct.encrypt_ndarray(np.pi/3)  # pi/3
print(ct.decrypt_ndarray(hp.tan(t)))
# 输出 1.732050807568881
print(ct.decrypt_ndarray(hp.sin(t) / hp.cos(t)))
# 输出 1.7320508075688725

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt_ndarray(aa)
res = hp.tan(a)
print(ct.decrypt_ndarray(res))
# 输出 [0.54630249 0.30933625 2.28584788 0.10033467]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt_ndarray(AA)
res = hp.tan(A)
print(ct.decrypt_ndarray(res))
# 输出 [[ 1.55740772 -2.18503986 -0.14254654]
#	    [-2.18503986  0.14254654  1.15782128]
#		[-0.14254654  1.55740772  1.15782128]]
```
