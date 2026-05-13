# expand_as

按目标扩展，对应 `torch.expand_as`。

## 签名

`hetorch2.expand_as(input, other)`

## 参数

- `input`: CipherTensor
- `other`: 参考张量（明文或密文）— 输出与其形状一致

## 返回值

CipherTensor — 形状与 `other` 相同。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0], [2.0]], dtype=torch.float64)
ref = torch.zeros(2, 5, dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.expand_as(xc, ref)
print(ct.decrypt_tensor(out).shape)
```
