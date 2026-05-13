# LLaMA3 大语言模型

## 简介

LLaMA3 是基于解码器的 Transformer 大语言模型。以下示例展示在密文侧用 `nn.Linear` 作为 LM Head、并用 `CipherTensor` 包装 logits 的核心写法。

## 初始化

```python
import hetorch2
import hetorch2.nn as nn
from hetorch2 import CipherTensor
import crypto_toolkit as ct
import torch
from typing import Optional

hetorch2.initDict()
ct.initSK()
```

## 模型定义（核心代码）

```python
class CipherLlamaForCausalLM(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.model = CipherLlamaModel(config)
        self.vocab_size = config.vocab_size
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

    def forward(self, input_ids, attention_mask=None, position_ids=None,
                past_key_values=None, inputs_embeds=None, use_cache=None,
                output_attentions=None, output_hidden_states=None,
                return_dict=None, cache_position=None):

        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            cache_position=cache_position,
        )

        hidden_states = outputs[0]
        logits = self.lm_head(hidden_states)
        logits = CipherTensor(logits.data.float())

        return logits
```

## 要点说明

- **`nn.Linear`**：hetorch2 的 Linear 层与 PyTorch 命名一致，不再使用 `HeLinear` 前缀。
- **`CipherTensor`**：将线性层输出转为密文张量类型。
- **`config.hidden_size`**：隐藏层维度，需与主干模型及 Linear 输入维一致。

## 使用的 hetorch2 算子

| 算子 | 用途 |
|------|------|
| `nn.Linear` | LM Head 线性映射 |
| `CipherTensor` | 密文张量包装 |
| `nn.Embedding` | Token 嵌入（在 `CipherLlamaModel` 内） |
| `nn.LayerNorm` | 层归一化 |
| `hetorch2.matmul` | 注意力计算中的矩阵乘法 |
| `hetorch2.softmax` | 注意力权重归一化 |
