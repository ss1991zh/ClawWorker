# Multilingual T5 文本生成模型

## 简介

mT5（Multilingual T5）是 Google 在 text-to-text 框架上的多语言扩展。以下为在密文侧处理注意力掩码的示意代码。

## 初始化

```python
import hetorch2
from hetorch2 import CipherTensor
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()
```

## 模型定义（核心代码）

```python
class CipherMT5PreTrainedModel(torch.nn.Module):
    main_input_name = "input_ids"
    dtype = torch.float32
    device = torch.device("cpu")

    def __init__(self, config, *inputs, **kwargs):
        super().__init__()
        self.config = config
        self.name_or_path = config.name_or_path

    def invert_attention_mask(self, encoder_attention_mask):
        if encoder_attention_mask.dim() == 4:
            encoder_extended_attention_mask = encoder_attention_mask[:, None, :, :, :]
        elif encoder_attention_mask.dim() == 3:
            encoder_extended_attention_mask = encoder_attention_mask[:, None, None, :, :]
        else:
            raise ValueError(
                "encoder_attention_mask 维度应为 3 或 4，实际为 %d"
                % encoder_attention_mask.dim()
            )

        encoder_extended_attention_mask = encoder_extended_attention_mask.to(dtype=torch.float64)
        sub = CipherTensor(encoder_extended_attention_mask) - 1.0
        sub = hetorch2.where(sub < 1e-5, CipherTensor(torch.zeros_like(sub, dtype=torch.float64)), sub)
        encoder_extended_attention_mask = CipherTensor(sub) * torch.finfo(self.dtype).max
        return encoder_extended_attention_mask
```

## 要点说明

- **`invert_attention_mask`**：将「有效位置为 1」的掩码转为注意力 logits 上的大负数屏蔽。
- **`CipherTensor` 运算**：密文张量支持 `+` `-` `*` `/` 运算符重载。
- **`hetorch2.where`**：条件选择操作，condition 为明文 bool，x/y 可以是 CipherTensor 或标量。
- **完整模型**还需要 `nn.LayerNorm`、`nn.Linear`、`nn.Embedding` 与跨层残差。

## 使用的 hetorch2 算子

| 算子 | 用途 |
|------|------|
| `CipherTensor` | 密文张量包装与运算 |
| `hetorch2.where` | 条件选择 |
| `nn.LayerNorm` | 层归一化（完整 mT5 堆叠中使用） |
| `nn.Linear` | 线性变换与前馈 |
| `nn.Embedding` | Token 嵌入 |
| `hetorch2.matmul` | 注意力矩阵乘法 |
| `hetorch2.softmax` | 注意力权重归一化 |
