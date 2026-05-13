# append

### 拼接数组，为原始数组添加一些值

## 参数

- `a`：数组密文，需要被添加值的数组
- `values`：标量密文或数组密文 添加到数组 $ a $中的值
- `axis`：整型，可选 添加值的轴，如果 $ axis $没有给出，那么 $ a $， $ values $都将先展平成一维数组。 注：如果 $ axis $被指定了，那么 $ a $和 $ values $需要同为一维数组或者有相同的 $ shape $
- `output_encrypt_type`：标量明文，可选 输出的数组密文的加密方式，默认返回的加密方式与输入数组的加密方式一致，若设定 $ output\_encrypt\_type=0 $，则返回的数组为行加密形式；若 $ output\_encrypt\_type=1 $，则返回的为列加密形式。

## 返回值

数组密文 `append`：添加了$ values $的新数组 $ append(a,\ values)=[a,\ values] $

## 示例
```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()

# 空密文向量+密文标量
x1 = ct.encrypt(5.0)
empty = hp.empty_array()
res = hp.append(empty, x1)		# 等价于 res = empty.append(x1)
print(ct.decrypt(res))
# 输出 [5.]

# 空密文向量+密文向量
aa = np.array([0.5, 0.3, 4.3, 0.1])
a = ct.encrypt(aa)
res = hp.append(empty, a)		# 等价于 res = empty.append(a)
print(ct.decrypt(res))
# 输出 [0.5 0.3 4.3 0.1]

# 密文向量+密文标量
res = hp.append(a, x1)		# 等价于 res = a.append(x1)
print(ct.decrypt(res))
# 输出 [0.5 0.3 4.3 0.1 5. ]

# 密文向量+密文向量
bb = np.array([2.1, 4.0, 5.2, 40.5])
b = ct.encrypt(bb)
res = hp.append(a, b)		# 等价于 res = a.append(b)
print(ct.decrypt(res))
# 输出 [ 0.5  0.3  4.3  0.1  2.1  4.   5.2 40.5]

# 空密文向量+密文数组
AA = np.array([[ 1.,  2.,  3.],[ 2., -3.,  4.],[ 3.,  1.,  4.]])
A = ct.encrypt(AA)
res = hp.append(empty, A)		# 等价于 res = empty.append(A)
print(ct.decrypt(res))
# 输出 [ 1.  2.  3.  2. -3.  4.  3.  1.  4.]

# 密文向量+密文数组
res = hp.append(a, A)		# 等价于 res = a.append(A)
print(ct.decrypt(res))
# 输出 [ 0.5  0.3  4.3  0.1  1.   2.   3.   2.  -3.   4.   3.   1.   4. ]

# 密文数组+密文数组, 默认展平
BB = np.array([[ 0.5,  4.,  2.],[ 4., 5.,  -6.],[ -0.1,  0.7,  2.2]])
B = ct.encrypt(BB)
res = hp.append(A, B)		# 等价于 res = A.append(B)
print(ct.decrypt(res))
# 输出 [ 1.   2.   3.   2.  -3.   4.   3.   1.   4.   0.5  4.   2.   4.   5. -6.  -0.1  0.7  2.2]

# 密文数组+密文数组, axis=0
res = hp.append(A, B, axis=0)		# 等价于 res = A.append(B, axis=0)
print(ct.decrypt(res))
# 输出 [[ 1.   2.   3. ]
#       [ 2.  -3.   4. ]
#       [ 3.   1.   4. ]
#       [ 0.5  4.   2. ]
#       [ 4.   5.  -6. ]
#       [-0.1  0.7  2.2]]

# 密文数组+密文向量, 默认展平
res = hp.append(A, a)		# 等价于 res = A.append(a)
print(ct.decrypt(res))
# 输出 [ 1.   2.   3.   2.  -3.   4.   3.   1.   4.   0.5  0.3  4.3  0.1]

# 密文数组+密文标量, 默认展平
res = hp.append(A, x1)		# 等价于 res = A.append(x1)
print(ct.decrypt(res))
# 输出 [ 1.  2.  3.  2. -3.  4.  3.  1.  4.  5.]
```
