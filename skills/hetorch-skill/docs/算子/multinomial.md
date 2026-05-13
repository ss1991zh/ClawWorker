# multinomial

多项式采样，对应 `torch.multinomial`。

## 签名

`hetorch2.multinomial(input, num_samples, replacement=False)`

## 参数

- `input`: CipherTensor — 非负权重（每行或向量依形状）
- `num_samples`: 采样次数
- `replacement` (可选): 是否有放回

## 返回值

torch.Tensor（明文 long）— 采样下标。

## 示例

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()

probs = torch.tensor([[0.1, 0.2, 0.7]], dtype=torch.float64)
xc = ct.encrypt_tensor(probs)
idx = hetorch2.multinomial(xc, num_samples=5, replacement=True)
print(idx)
```
