# Embedding

密文嵌入层，对应 PyTorch `nn.Embedding`。

## 签名

```python
hetorch2.nn.Embedding(num_embeddings, embedding_dim, padding_idx=None, max_norm=None, norm_type=2.0, scale_grad_by_freq=False, sparse=False, device='cpu')
```

## 参数

- `num_embeddings`: 词表大小（嵌入行数）。
- `embedding_dim`: 每个嵌入向量的维度。
- `padding_idx`: 若指定，该下标对应行在初始化时置零，且在部分场景下不参与更新（与 PyTorch 语义对齐）。
- `max_norm`: 若指定，嵌入向量将按范数裁剪（与 PyTorch 语义对齐；密文推理场景下以文档与实现为准）。
- `norm_type`: 范数类型，用于 `max_norm`，默认 `2.0`。
- `scale_grad_by_freq`: 是否按词频缩放梯度（训练相关；推理通常不涉及）。
- `sparse`: 是否使用稀疏梯度（训练相关；推理通常不涉及）。
- `device`: 嵌入权重所在设备，默认 `'cpu'`。

## 示例

```python
import hetorch2
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

emb = nn.Embedding(1000, 64)
idx = torch.randint(0, 1000, (4, 32), dtype=torch.long)
out = emb(idx)
# 嵌入查表使用整型下标；另附 float64 密文张量以符合加解密约定（可与下游层组合）
aux = torch.randn(4, 32, 64, dtype=torch.float64)
cx_aux = ct.encrypt_tensor(aux)
y = ct.decrypt_tensor(out)
print(y.shape, ct.decrypt_tensor(cx_aux).shape)  # torch.Size([4, 32, 64]) 等
```
