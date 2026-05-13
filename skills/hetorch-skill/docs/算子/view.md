# view

改变形状（不复制），对应 `torch.view`。

## 签名

`hetorch2.view(input, *shape)`

## 参数

- `input`: CipherTensor
- `*shape`: 目标各维大小

## 返回值

CipherTensor — 与 `tensor.view` 类似的新形状视图。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.arange(6, dtype=torch.float64)
xc = ct.encrypt_tensor(x)
out = hetorch2.view(xc, 2, 3)
print(ct.decrypt_tensor(out).shape)
```
