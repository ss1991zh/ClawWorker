# hp.arange

生成等差整数序列的密文。

## 签名

```python
hp.arange(stop, start=0, step=1)
```

## 参数

- `stop`: int — 序列终止值（不包含）
- `start` (可选): int — 序列起始值，默认 0
- `step` (可选): float — 步长，默认 1

## 返回值

向量密文 — 等差序列。

`arange(n) = [0, 1, 2, ..., n-1]`
`arange(4, 1) = [1, 2, 3]`
`arange(5, 1, 2) = [1, 3]`

## 示例

```python
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()

# stop=5
print(ct.decrypt(hp.arange(5)))
# 输出 [0. 1. 2. 3. 4.]

# stop=4, start=1
print(ct.decrypt(hp.arange(4, 1)))
# 输出 [1. 2. 3.]

# stop=5, start=1, step=2
print(ct.decrypt(hp.arange(5, 1, 2)))
# 输出 [1. 3.]
```
