# sin

正弦，对应 `torch.sin`。

## 签名

`hetorch2.sin(input)`

## 参数

- `input`: CipherTensor — 弧度

## 返回值

CipherTensor — 逐元素正弦。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[0.0, 1.5707963267948966], [3.141592653589793, -1.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.sin(xc)
print(ct.decrypt_tensor(out))
```
