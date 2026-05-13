# reshape

重塑，对应 `torch.reshape`。

## 签名

`hetorch2.reshape(input, shape)`

## 参数

- `input`: CipherTensor
- `shape`: 目标形状（tuple 或 list）

## 返回值

CipherTensor — 新视图/拷贝语义与实现一致。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.arange(6, dtype=torch.float64).reshape(2, 3)
xc = ct.encrypt_tensor(x)
out = hetorch2.reshape(xc, (3, 2))
print(ct.decrypt_tensor(out).shape)
```
