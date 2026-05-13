# sinh

双曲正弦，对应 `torch.sinh`。

## 签名

`hetorch2.sinh(input)`

## 参数

- `input`: CipherTensor

## 返回值

CipherTensor — 逐元素双曲正弦。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[0.0, 0.5], [-0.5, 1.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.sinh(xc)
print(ct.decrypt_tensor(out))
```
