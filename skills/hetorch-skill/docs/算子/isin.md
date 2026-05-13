# isin

元素是否在集合中，返回明文 bool Tensor（非密文），对应 `torch.isin`。

## 签名

`hetorch2.isin(input, test_elements)`

## 参数

- `input`: CipherTensor 或明文张量
- `test_elements`: 明文张量或标量 — 候选集合

## 返回值

torch.BoolTensor（明文）— 逐元素是否在集合中。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float64)
cand = torch.tensor([2.0, 4.0], dtype=torch.float64)
xc = ct.encrypt_tensor(x)
mask = hetorch2.isin(xc, cand)
print(mask)
```
