# cumsum

累积求和，对应 `torch.cumsum`。

## 签名

`hetorch2.cumsum(input, dim=-1)`

## 参数

- `input`: CipherTensor
- `dim` (可选): 累积方向，默认最后一维

## 返回值

CipherTensor — 前缀和。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.cumsum(xc, dim=-1)
print(ct.decrypt_tensor(out))
```
