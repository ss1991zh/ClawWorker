# clamp

范围裁剪，对应 `torch.clamp`。

## 签名

`hetorch2.clamp(input, min=None, max=None)`

## 参数

- `input`: CipherTensor
- `min` (可选): 下界明文标量或张量
- `max` (可选): 上界明文标量或张量

## 返回值

CipherTensor — 将元素限制在 `[min, max]` 内。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[-1.0, 5.0], [2.0, 10.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.clamp(xc, min=0.0, max=4.0)
print(ct.decrypt_tensor(out))
```
