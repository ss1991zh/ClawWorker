# stack

堆叠，对应 `torch.stack`。

## 签名

`hetorch2.stack(tensors, dim=0)`

## 参数

- `tensors`: CipherTensor 序列
- `dim` (可选): 插入新维的位置

## 返回值

CipherTensor — 比输入多一维。

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
out = hetorch2.stack([ac, bc], dim=0)
print(ct.decrypt_tensor(out).shape)
```
