# cos

### 余弦函数

## 参数

标量密文或数组密文

- `x`：弧度制角度
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

标量密文或数组密文 `cos`： $ x $的余弦值

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 标量
x = ct.encrypt(5.0)
res = hp.cos(x)
print(ct.decrypt(res))
# 输出 0.2836621854632296    
    
# 验证 cos(pi/6) = sin(pi/3)
t1 = ct.encrypt(np.pi/6)  # pi/6
t2 = ct.encrypt(np.pi/3)  # pi/3
print(ct.decrypt(hp.cos(t1)))
# 输出 0.866025403784438
print(ct.decrypt(hp.sin(t2)))
# 输出 0.8660254037844403

# 向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.cos(a)
print(ct.decrypt(res))
# 输出 [ 0.87758256  0.95533649 -0.40079917  0.99500417]

# 数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.cos(A)
print(ct.decrypt(res))
# 输出 [[ 0.54030231 -0.41614684 -0.9899925 ]
#	    [-0.41614684 -0.9899925  -0.65364362]
#		[-0.9899925   0.54030231 -0.65364362]]
```
