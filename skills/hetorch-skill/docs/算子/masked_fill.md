# masked_fill

掩码填充，对应 `torch.masked_fill`。

## 签名

`hetorch2.masked_fill(input, mask, value)`

## 参数

- `input`: CipherTensor
- `mask`: 明文 bool 张量或与 `input` 可广播
- `value`: 填充值（明文标量）

## 返回值

CipherTensor — `mask` 为 True 的位置置为 `value`。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.ones(2, 3, dtype=torch.float64)
mask = torch.tensor([[True, False, True], [False, True, False]])
xc = ct.encrypt_tensor(x)
out = hetorch2.masked_fill(xc, mask, -1.0)
print(ct.decrypt_tensor(out))
```
