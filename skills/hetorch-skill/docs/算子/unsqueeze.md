# unsqueeze

增加维度，对应 `torch.unsqueeze`。

## 签名

`hetorch2.unsqueeze(input, dim)`

## 参数

- `input`: CipherTensor
- `dim`: 插入大小为 1 的维度

## 返回值

CipherTensor — 在 `dim` 处升维。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.ones(2, 3, dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.unsqueeze(xc, 0)
print(ct.decrypt_tensor(out).shape)
```
