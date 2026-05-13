# squeeze

压缩维度，对应 `torch.squeeze`。

## 签名

`hetorch2.squeeze(input, dim=None)`

## 参数

- `input`: CipherTensor
- `dim` (可选): 仅压缩该维；`None` 表示移除所有大小为 1 的维

## 返回值

CipherTensor — 去掉长度为 1 的维。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.ones(1, 2, 1, 3, dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.squeeze(xc)
print(ct.decrypt_tensor(out).shape)
```
