# encrypt_csv
CSV 文件加密。
## 签名
`ct.encrypt_csv(input_file, output_file, encrypt_by_column=True, extract_header=True)`
## 参数
- `input_file`：待加密的 CSV 文件路径。
- `output_file`：加密后输出的 CSV 文件路径。
- `encrypt_by_column`：是否按列加密。默认 `True`。
- `extract_header`：加密时是否忽略表头。默认 `True`。
## 返回值
无（直接写入输出文件）。
## 示例
```python
import crypto_toolkit as ct

ct.initSK()

ct.encrypt_csv("data/input.csv", "data/encrypted.csv", encrypt_by_column=True)
```
