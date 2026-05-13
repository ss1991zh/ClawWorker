# expand

扩展，对应 `torch.expand`。

## 签名

`hetorch2.expand(input, *sizes)`

## 参数

- `input`: CipherTensor
- `*sizes`: 目标形状（含 `-1` 或原大小占位依实现）

## 返回值

CipherTensor — 广播式扩展（通常不复制底层存储）。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0], [2.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.expand(xc, 2, 4)
print(ct.decrypt_tensor(out).shape)
```
