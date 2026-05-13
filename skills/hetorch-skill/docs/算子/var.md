# var

方差，对应 `torch.var`。

## 签名

`hetorch2.var(input, dim=None, keepdim=False, correction=1)`

## 参数

- `input`: CipherTensor
- `dim` (可选): 归约维度
- `keepdim` (可选): 是否保留维度
- `correction` (可选): 贝塞尔校正项（与 `torch.var` 一致）

## 返回值

CipherTensor — 方差。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.var(xc, dim=1, correction=1)
print(ct.decrypt_tensor(out))
```
