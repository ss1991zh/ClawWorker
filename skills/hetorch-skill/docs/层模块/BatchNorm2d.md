# BatchNorm2d

密文二维批归一化（仅推理模式），对应 PyTorch `nn.BatchNorm2d`。

## 签名

```python
hetorch2.nn.BatchNorm2d(num_features, eps=1e-5, momentum=0.1, affine=True, track_running_stats=True, device='cpu')
```

## 参数

- `num_features`: 特征通道数 \(C\)（对输入形状 `(N, C, H, W)` 中的 `C`）。
- `eps`: 数值稳定项，加在方差上。
- `momentum`: 滑动平均动量（训练时更新 running 统计量用；hetorch2 当前仅实现推理路径）。
- `affine`: 是否使用可学习的 `weight`、`bias` 做仿射变换。
- `track_running_stats`: 是否维护 `running_mean` / `running_var`；推理时使用这些 buffer。
- `device`: 参数与 buffer 所在设备，默认 `'cpu'`。

推理前请调用 `eval()`，并确保 `running_mean`、`running_var` 等已与训练阶段导出的一致（例如从 PyTorch 状态字典加载）。

## 示例

```python
import hetorch2
import hetorch2.nn as nn
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

bn = nn.BatchNorm2d(32)
bn.eval()
x = torch.randn(4, 32, 8, 8, dtype=torch.float64)
cx = ct.encrypt_tensor(x)
out = bn(cx)
y = ct.decrypt_tensor(out)
print(y.shape)  # torch.Size([4, 32, 8, 8])
```
