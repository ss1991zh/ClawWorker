# split

分割，对应 `torch.split`。

## 签名

`hetorch2.split(input, split_size, dim=0)`

## 参数

- `input`: CipherTensor
- `split_size`: 每块大小或块大小列表
- `dim` (可选): 切分维度

## 返回值

tuple[CipherTensor, ...] — 沿 `dim` 切分。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.arange(10, dtype=torch.float64).reshape(2, 5)
xc = ct.encrypt_tensor(x)
parts = hetorch2.split(xc, 2, dim=1)
print([ct.decrypt_tensor(p).shape for p in parts])
```
