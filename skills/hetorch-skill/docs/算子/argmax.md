# argmax

最大值索引，对应 `torch.argmax`。

## 签名

`hetorch2.argmax(input, dim=-1, keepdim=False)`

## 参数

- `input`: CipherTensor
- `dim` (可选): 沿该维取 argmax
- `keepdim` (可选): 是否保留维度

## 返回值

torch.Tensor（明文 long）— 最大值的索引。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 5.0, 2.0], [4.0, 0.0, 3.0]], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
idx = hetorch2.argmax(xc, dim=-1)
print(idx)
```
