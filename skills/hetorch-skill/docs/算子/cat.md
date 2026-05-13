# cat

拼接，对应 `torch.cat`。

## 签名

`hetorch2.cat(tensors, dim=0)`

## 参数

- `tensors`: CipherTensor 序列
- `dim` (可选): 拼接维度

## 返回值

CipherTensor — 沿 `dim` 连接。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

a = torch.ones(2, 3, dtype=torch.float64)
b = torch.zeros(2, 3, dtype=torch.float64)
ac = ct.encrypt_tensor(a)
bc = ct.encrypt_tensor(b)
out = hetorch2.cat([ac, bc], dim=0)
print(ct.decrypt_tensor(out).shape)
```
