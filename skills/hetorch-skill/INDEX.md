# hetorch2 API 索引

> 仅签名 + 一句话描述 + 文档路径。详细参数说明请按需读取对应文档。

## Layer 层（`hetorch2.nn`，与 PyTorch 命名对齐）

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| Linear | `nn.Linear(in_features, out_features, bias=True, device='cpu')` | 密文全连接层 | `docs/层模块/Linear.md` |
| Embedding | `nn.Embedding(num_embeddings, embedding_dim, padding_idx=None, max_norm=None, norm_type=2.0, scale_grad_by_freq=False, sparse=False, device='cpu')` | 密文嵌入层 | `docs/层模块/Embedding.md` |
| ReLU | `nn.ReLU(inplace=False)` | 密文 ReLU 激活层 | `docs/层模块/ReLU.md` |
| Sigmoid | `nn.Sigmoid()` | 密文 Sigmoid 激活层 | `docs/层模块/Sigmoid.md` |
| Tanh | `nn.Tanh()` | 密文 Tanh 激活层 | `docs/层模块/Tanh.md` |
| SiLU | `nn.SiLU()` | 密文 SiLU (Swish) 激活层 | `docs/层模块/SiLU.md` |
| PReLU | `nn.PReLU(num_parameters=1, init=0.25)` | 密文参数化 ReLU 层 | `docs/层模块/PReLU.md` |
| BatchNorm1d | `nn.BatchNorm1d(num_features, eps=1e-5, momentum=0.1, affine=True, track_running_stats=True, device='cpu')` | 密文一维批归一化 | `docs/层模块/BatchNorm1d.md` |
| BatchNorm2d | `nn.BatchNorm2d(num_features, eps=1e-5, momentum=0.1, affine=True, track_running_stats=True, device='cpu')` | 密文二维批归一化 | `docs/层模块/BatchNorm2d.md` |
| LayerNorm | `nn.LayerNorm(normalized_shape, eps=1e-5, elementwise_affine=True, device='cpu')` | 密文层归一化 | `docs/层模块/LayerNorm.md` |

## Function 层 — 函数式接口（`hetorch2.nn.functional as F`）

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| relu | `F.relu(input)` | 密文 ReLU 激活 | `docs/函数/relu.md` |
| sigmoid | `F.sigmoid(input)` | 密文 Sigmoid 激活 | `docs/函数/sigmoid.md` |
| tanh | `F.tanh(input)` | 密文 Tanh 激活 | `docs/函数/tanh.md` |
| silu | `F.silu(input)` | 密文 SiLU (Swish) 激活 | `docs/函数/silu.md` |
| prelu | `F.prelu(input, weight)` | 密文参数化 ReLU | `docs/函数/prelu.md` |
| linear | `F.linear(input, weight, bias=None)` | 密文线性变换 | `docs/函数/linear.md` |
| embedding | `F.embedding(input, weight)` | 密文嵌入查找 | `docs/函数/embedding.md` |
| batch_norm | `F.batch_norm(input, running_mean, running_var, weight=None, bias=None, eps=1e-5)` | 密文批归一化 | `docs/函数/batch_norm.md` |
| layer_norm | `F.layer_norm(input, normalized_shape, weight=None, bias=None, eps=1e-5)` | 密文层归一化 | `docs/函数/layer_norm.md` |
| softmax | `F.softmax(input, dim)` | 密文 Softmax | `docs/函数/softmax.md` |
| log_softmax | `F.log_softmax(input, dim)` | 密文 Log-Softmax | `docs/函数/log_softmax.md` |

## 顶层算子（`hetorch2.*`）

### 算术运算

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| add | `hetorch2.add(input, other)` | 密文加法 | `docs/算子/add.md` |
| sub | `hetorch2.sub(input, other)` | 密文减法 | `docs/算子/sub.md` |
| mul | `hetorch2.mul(input, other)` | 密文逐元素乘法 | `docs/算子/mul.md` |
| multiply | `hetorch2.multiply(input, other)` | mul 的别名 | `docs/算子/mul.md` |
| div | `hetorch2.div(input, other)` | 密文除法 | `docs/算子/div.md` |
| matmul | `hetorch2.matmul(input, other)` | 密文矩阵乘法 | `docs/算子/matmul.md` |

### 比较运算

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| equal | `hetorch2.equal(input, other)` | 密文判等 | `docs/算子/equal.md` |

### 数学函数

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| exp | `hetorch2.exp(input)` | 指数函数 | `docs/算子/exp.md` |
| log | `hetorch2.log(input)` | 自然对数 | `docs/算子/log.md` |
| sqrt | `hetorch2.sqrt(input)` | 平方根 | `docs/算子/sqrt.md` |
| rsqrt | `hetorch2.rsqrt(input)` | 平方根倒数 | `docs/算子/rsqrt.md` |
| pow | `hetorch2.pow(input, exponent)` | 幂运算 | `docs/算子/pow.md` |
| sin | `hetorch2.sin(input)` | 正弦 | `docs/算子/sin.md` |
| cos | `hetorch2.cos(input)` | 余弦 | `docs/算子/cos.md` |
| sinh | `hetorch2.sinh(input)` | 双曲正弦 | `docs/算子/sinh.md` |
| cosh | `hetorch2.cosh(input)` | 双曲余弦 | `docs/算子/cosh.md` |
| clamp | `hetorch2.clamp(input, min=None, max=None)` | 范围裁剪 | `docs/算子/clamp.md` |

### 统计函数

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| sum | `hetorch2.sum(input, dim=None, keepdim=False)` | 求和 | `docs/算子/sum.md` |
| mean | `hetorch2.mean(input, dim=None, keepdim=False)` | 均值 | `docs/算子/mean.md` |
| var | `hetorch2.var(input, dim=None, keepdim=False, correction=1)` | 方差 | `docs/算子/var.md` |
| cumsum | `hetorch2.cumsum(input, dim=-1)` | 累积求和 | `docs/算子/cumsum.md` |
| argmax | `hetorch2.argmax(input, dim=-1, keepdim=False)` | 最大值索引 | `docs/算子/argmax.md` |
| argmin | `hetorch2.argmin(input, dim=-1, keepdim=False)` | 最小值索引 | `docs/算子/argmin.md` |
| softmax | `hetorch2.softmax(input, dim)` | Softmax | `docs/算子/softmax.md` |

### 形状操作

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| flatten | `hetorch2.flatten(input, start_dim=0, end_dim=-1)` | 展平 | `docs/算子/flatten.md` |
| reshape | `hetorch2.reshape(input, shape)` | 重塑形状 | `docs/算子/reshape.md` |
| view | `hetorch2.view(input, *shape)` | 改变形状 | `docs/算子/view.md` |
| transpose | `hetorch2.transpose(input, dim0, dim1)` | 转置 | `docs/算子/transpose.md` |
| cat | `hetorch2.cat(tensors, dim=0)` | 拼接 | `docs/算子/cat.md` |
| stack | `hetorch2.stack(tensors, dim=0)` | 堆叠 | `docs/算子/stack.md` |
| unsqueeze | `hetorch2.unsqueeze(input, dim)` | 增加维度 | `docs/算子/unsqueeze.md` |
| squeeze | `hetorch2.squeeze(input, dim=None)` | 压缩维度 | `docs/算子/squeeze.md` |
| expand | `hetorch2.expand(input, *sizes)` | 扩展 | `docs/算子/expand.md` |
| expand_as | `hetorch2.expand_as(input, other)` | 按目标扩展 | `docs/算子/expand_as.md` |
| split | `hetorch2.split(input, split_size, dim=0)` | 分割 | `docs/算子/split.md` |
| chunk | `hetorch2.chunk(input, chunks, dim=0)` | 分块 | `docs/算子/chunk.md` |
| index_select | `hetorch2.index_select(input, dim, index)` | 索引选择 | `docs/算子/index_select.md` |

### 索引和条件操作

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| gather | `hetorch2.gather(input, dim, index)` | 收集元素 | `docs/算子/gather.md` |
| scatter | `hetorch2.scatter(input, dim, index, src)` | 散布元素 | `docs/算子/scatter.md` |
| where | `hetorch2.where(condition, x, y)` | 条件选择 | `docs/算子/where.md` |
| masked_fill | `hetorch2.masked_fill(input, mask, value)` | 掩码填充 | `docs/算子/masked_fill.md` |
| index_add | `hetorch2.index_add(input, dim, index, source)` | 索引加法 | `docs/算子/index_add.md` |
| scatter_add | `hetorch2.scatter_add(input, dim, index, src)` | 散布加法 | `docs/算子/scatter_add.md` |

### 排序和集合

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| sort | `hetorch2.sort(input, dim=-1, descending=False)` | 排序（返回 values, indices） | `docs/算子/sort.md` |
| topk | `hetorch2.topk(input, k, dim=None, largest=True, sorted=True)` | Top-K（返回 values, indices） | `docs/算子/topk.md` |
| isin | `hetorch2.isin(input, test_elements)` | 元素是否在集合中（返回 bool Tensor） | `docs/算子/isin.md` |

### 采样

| 算子 | 签名 | 描述 | 文档 |
|------|------|------|------|
| multinomial | `hetorch2.multinomial(input, num_samples, replacement=False)` | 多项式采样 | `docs/算子/multinomial.md` |

## CipherTensor 类

| 方法 | 描述 |
|------|------|
| `hetorch2.CipherTensor(data, requires_grad=False, dtype=torch.float64)` | 从 Tensor 构造密文张量 |
| `.shape` / `.size()` / `.dim()` / `.numel()` | 形状和维度信息 |
| `+` `-` `*` `/` `@` 运算符 | 算术运算符重载 |
| `==` `!=` `<` `<=` `>` `>=` | 比较运算符重载 |
| `.sum()` `.mean()` `.var()` | 统计方法 |
| `.exp()` `.log()` `.sqrt()` `.pow()` | 数学方法 |
| `.sin()` `.cos()` `.tanh()` `.sigmoid()` `.relu()` | 激活/三角方法 |
| `.flatten()` `.reshape()` `.view()` `.transpose()` | 形状方法 |
| `.unsqueeze()` `.squeeze()` `.expand_as()` `.expand()` | 维度操作方法 |
| `.split()` `.chunk()` `.index_select()` | 分割/索引方法 |
| `.softmax()` `.cumsum()` | 归一化/累积方法 |
| `.sort()` `.topk()` | 排序方法 |
| `.gather()` `.scatter_add()` `.index_add()` `.masked_fill()` | 高级索引方法 |
| `.to()` `.cuda()` `.cpu()` `.detach()` | 设备和梯度方法 |
