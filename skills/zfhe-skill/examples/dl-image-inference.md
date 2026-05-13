# 示例：密文 MLP 深度学习推理

> 用户需求："对加密数据用 MLP 做分类推理"

**路由结果**：hetorch2 单独  
**数据源**：加密 Tensor  
**任务类型**：DL 推理

```python
import hetorch2
import hetorch2.nn as nn
import hetorch2.nn.functional as F
import crypto_toolkit as ct
import torch
import os

hetorch2.initDict()
ct.initSK()

# ── 定义密文 MLP 模型 ──
class CipherMLP(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.fc3 = nn.Linear(128, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.fc3(x)
        x = F.log_softmax(x, dim=1)
        return x

# ── 加载模型权重 ──
model_path = 'mlp_model.pth'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"模型文件不存在: {model_path}")

model = CipherMLP()
model.load_state_dict(torch.load(model_path))
model.eval()

# ── 加密输入数据 ──
x = torch.randn(1, 784, dtype=torch.float64)
assert x.dtype == torch.float64, f"hetorch2 要求 float64，当前 dtype: {x.dtype}"
cx = ct.encrypt_tensor(x)

# ── 密文推理 ──
output = model(cx)

# ── 解密结果 ──
result = ct.decrypt_tensor(output)
predicted_class = torch.argmax(result, dim=1).item()
print(f"推理结果 logits: {result}")
print(f"预测类别: {predicted_class}")

# 注意：同态加密计算结果存在浮点精度误差，这是 FHE 的固有特性，非 bug。
```
