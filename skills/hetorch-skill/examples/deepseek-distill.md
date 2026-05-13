# DeepSeek-LLaMA3 蒸馏模型

## 简介

DeepSeek-R1-Distill-Llama-8B 在 LLaMA 系架构上做知识蒸馏。以下示例聚焦单层 Decoder 中注意力子层与 MLP 子层之间的残差，以及如何用 `CipherTensor` 与 `+` 完成密文残差相加。

## 初始化

```python
import hetorch2
from hetorch2 import CipherTensor
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch
from typing import Optional, Tuple

hetorch2.initDict()
ct.initSK()
```

## 模型定义（核心 Decoder Layer）

```python
class CipherLlamaDecoderLayer(torch.nn.Module):
    def __init__(self, config, layer_idx):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.self_attn = CipherLlamaAttention(config=config, layer_idx=layer_idx)
        self.mlp = CipherLlamaMLP(config)
        self.input_layernorm = CipherLlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = CipherLlamaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(self, hidden_states, attention_mask=None, position_ids=None,
                past_key_value=None, output_attentions=False, use_cache=False,
                cache_position=None, position_embeddings=None, **kwargs):

        residual = hidden_states
        hidden_states = self.input_layernorm(hidden_states)

        hidden_states, self_attn_weights, present_key_value = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_value=past_key_value,
            output_attentions=output_attentions,
            use_cache=use_cache,
            cache_position=cache_position,
            position_embeddings=position_embeddings,
            **kwargs,
        )

        hidden_states = CipherTensor(residual.contiguous()) + CipherTensor(hidden_states.contiguous())

        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)

        hidden_states = CipherTensor(residual.contiguous()) + CipherTensor(hidden_states.contiguous())

        outputs = (hidden_states,)
        if output_attentions:
            outputs += (self_attn_weights,)
        if use_cache:
            outputs += (present_key_value,)
        return outputs
```

## 要点说明

- **残差与 `CipherTensor`**：两段残差均对分支结果做 `contiguous()` 后包成 `CipherTensor`，再用 `+` 做密文加法。
- **`CipherLlamaRMSNorm`**：自定义 RMSNorm 模块，内部可用 `hetorch2.mean`、`hetorch2.rsqrt` 等算子实现。
- **`CipherLlamaAttention`**：自注意力层，内部用 `nn.Linear` 做 QKV 投影、`hetorch2.matmul` 做注意力计算、`hetorch2.softmax` 做归一化。
- **`CipherLlamaMLP`**：前馈层，内部用 `nn.Linear` + `nn.SiLU` 等。

## 使用的 hetorch2 算子

| 算子 | 用途 |
|------|------|
| `CipherTensor` | 密文张量包装（残差连接） |
| `nn.Linear` | 线性变换（MLP 与投影中） |
| `nn.Embedding` | Token 嵌入（模型前端） |
| `nn.LayerNorm` | 层归一化 |
| `nn.SiLU` | SwiGLU 中的激活函数 |
| `hetorch2.matmul` | 注意力矩阵乘法 |
| `hetorch2.softmax` | 注意力权重归一化 |
| `hetorch2.masked_fill` | 注意力掩码填充 |
