# 初始化模式

不同子 skill 组合对应的 import 和初始化模板。每个生成脚本必须包含正确的初始化代码。

## 核心原则

1. 每个子 skill 都有自己的初始化需求，遗漏任何一个都会导致运行时错误。
2. `ct.initSK()` 是所有场景都需要的（只要涉及加解密）。
3. `hp.initDict()` 和 `hetorch2.initDict()` 不互通，不可互相替代。
4. 初始化语句必须在所有计算/加密操作之前。

## 模板一览

### pandaseal 单独

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np

hp.initDict()
ct.initSK()
```

### henumpy 单独

```python
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()
```

### helearn 单独

```python
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct

hp.initDict()
ct.initSK()
```

### hetorch2 单独

```python
import hetorch2
import crypto_toolkit as ct
import torch

hetorch2.initDict()
ct.initSK()
```

注意：hetorch2 不需要 `import henumpy`，也不需要 `hp.initDict()`。

### pandaseal + henumpy

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np

hp.initDict()
ct.initSK()
```

pandaseal 依赖 henumpy 的初始化，两者共享 `hp.initDict()`。

### pandaseal + helearn

```python
import helearn as hl
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np

hp.initDict()
ct.initSK()
```

### henumpy + helearn

```python
import helearn as hl
import henumpy as hp
import crypto_toolkit as ct
import numpy as np

hp.initDict()
ct.initSK()
```

### hetorch2 + pandaseal（混合流水线）

```python
import hetorch2
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd
import numpy as np
import torch

hp.initDict()
hetorch2.initDict()
ct.initSK()
```

**关键**：同时使用 hetorch2 和 henumpy/pandaseal 时，必须调用两个 initDict。

### hetorch2 + henumpy

```python
import hetorch2
import henumpy as hp
import crypto_toolkit as ct
import numpy as np
import torch

hp.initDict()
hetorch2.initDict()
ct.initSK()
```

## 初始化检查清单

生成代码后，对照以下检查清单确认初始化完整性：

| 代码中出现的符号 | 需要的 import | 需要的 init |
|----------------|--------------|------------|
| `hp.*` | `import henumpy as hp` | `hp.initDict()` |
| `ps.*` | `import pandaseal as ps` + `import henumpy as hp` | `hp.initDict()` |
| `hl.*` | `import helearn as hl` + `import henumpy as hp` | `hp.initDict()` |
| `hetorch2.*` | `import hetorch2` | `hetorch2.initDict()` |
| `ct.*` | `import crypto_toolkit as ct` | `ct.initSK()` |
| `np.*` | `import numpy as np` | — |
| `pd.*` | `import pandas as pd` | — |
| `torch.*` | `import torch` | — |
