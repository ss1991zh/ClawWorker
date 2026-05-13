# embedding

密文嵌入查找，对应 PyTorch `F.embedding`。

## 签名

`hetorch2.nn.functional.embedding(input, weight)`

## 参数

- `input`: 索引张量（与 PyTorch 一致，通常为整型），形状任意；用于在词表维度上查表。
- `weight`: 嵌入矩阵，形状 `(num_embeddings, embedding_dim)`，元素为 `dtype=torch.float64` 的浮点权重。

## 返回值

密文 Tensor（CipherTensor）。

## 示例

```python
import hetorch2
import hetorch2.nn.functional as F
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

indices = torch.tensor([[0, 2], [1, 3]], dtype=torch.long)
weight = torch.randn(10, 8, dtype=torch.float64)
w_enc = ct.encrypt_tensor(weight)
out_enc = F.embedding(indices, w_enc)
out = ct.decrypt_tensor(out_enc)
```
