# chunk

分块，对应 `torch.chunk`。

## 签名

`hetorch2.chunk(input, chunks, dim=0)`

## 参数

- `input`: CipherTensor
- `chunks`: 块数
- `dim` (可选): 切分维度

## 返回值

tuple[CipherTensor, ...] — 均分成 `chunks` 块。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.arange(12, dtype=torch.float64).reshape(2, 6)
xc = ct.encrypt_tensor(x)
parts = hetorch2.chunk(xc, 3, dim=1)
print([ct.decrypt_tensor(p).shape for p in parts])
```
