# MLP 密文分类推理

## 简介

使用多层感知机（MLP）对加密数据进行分类推理。这是 hetorch2 最基础的端到端示例，展示从加密输入到解密输出的完整流程。

## 初始化

```python
import hetorch2
import hetorch2.nn as nn
import hetorch2.nn.functional as F
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()
```

## 模型定义

```python
class CipherMLP(torch.nn.Module):
    def __init__(self, input_dim=784, hidden_dim=256, num_classes=10):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.fc3(x)
        x = F.log_softmax(x, dim=1)
        return x
```

## 密文推理

```python
model = CipherMLP(input_dim=784, hidden_dim=256, num_classes=10)
model.load_state_dict(torch.load('mlp_model.pth'))
model.eval()

x = torch.randn(1, 784, dtype=torch.float64)
cx = ct.encrypt_tensor(x)

output = model(cx)

result = ct.decrypt_tensor(output)
predicted_class = torch.argmax(result, dim=1).item()
print(f"推理结果 logits: {result}")
print(f"预测类别: {predicted_class}")
```

## 要点说明

- **`nn.Linear`**：全连接层，与 PyTorch 命名一致。
- **`nn.BatchNorm1d`**：批归一化层，仅支持推理模式（需 `model.eval()`）。
- **`nn.ReLU`**：Layer 形式的激活函数，也可用 `F.relu(x)` 替代。
- **`F.log_softmax`**：函数式 Log-Softmax，用于分类输出。
- **`dtype=torch.float64`**：输入 Tensor 推荐使用 float64。

## 使用的 hetorch2 算子

| 算子 | 用途 |
|------|------|
| `nn.Linear` | 全连接层 |
| `nn.BatchNorm1d` | 批归一化 |
| `nn.ReLU` | ReLU 激活 |
| `F.log_softmax` | 分类输出 |
| `CipherTensor` | 密文张量（由 `ct.encrypt_tensor` 生成） |
