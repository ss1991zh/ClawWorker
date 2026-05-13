# decrypt_csv
CSV 文件解密。
## 签名
`ct.decrypt_csv(input_file, output_file, decrypt_by_column=True, extract_header=True)`
## 参数
- `input_file`：待解密的 CSV 文件路径。
- `output_file`：解密后输出的 CSV 文件路径。
- `decrypt_by_column`：是否按列解密。默认 `True`。缺省即可，接口会自动判断。
- `extract_header`：解密时是否忽略表头。默认 `True`。
## 返回值
无（直接写入输出文件）。
## 示例
```python
import crypto_toolkit as ct

ct.initSK()

ct.decrypt_csv("data/encrypted.csv", "data/decrypted.csv", decrypt_by_column=True)
```
