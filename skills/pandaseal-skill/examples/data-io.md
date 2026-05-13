# 示例：数据输入/输出

加密 DataFrame 的文件读写操作：CSV、Excel、JSON。

```python
import henumpy as hp
import pandaseal as ps
import crypto_toolkit as ct
import pandas as pd

hp.initDict()
ct.initSK()

# ── 准备数据 ──
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
cdf = ct.encrypt_df(df)

# ── CSV 读写 ──
cdf.to_csv('cipher_data.csv')
cdf_from_csv = ps.read_csv('cipher_data.csv')
print(ct.decrypt_df(cdf_from_csv))

# ── Excel 读写 ──
cdf.to_excel('cipher_data.xlsx', index=True)
cdf_from_excel = ps.read_excel('cipher_data.xlsx', index_col=0)
print(ct.decrypt_df(cdf_from_excel))

# ── JSON 读写 ──
cdf.to_json('cipher_data.json')
cdf_from_json = ps.read_json('cipher_data.json')
print(ct.decrypt_df(cdf_from_json))

# ── 文件级别加解密（crypto_toolkit 提供） ──
# 加密整个 CSV 文件
ct.encrypt_csv('plain.csv', 'encrypted.csv', encrypt_by_column=True)
# 解密整个 CSV 文件
ct.decrypt_csv('encrypted.csv', 'decrypted.csv', decrypt_by_column=True)

# 加密整个 Excel 文件
ct.encrypt_excel('plain.xlsx', 'encrypted.xlsx')
# 解密整个 Excel 文件
ct.decrypt_excel('encrypted.xlsx', 'decrypted.xlsx')

# 加密整个 JSON 文件
ct.encrypt_json('plain.json', 'encrypted.json')
# 解密整个 JSON 文件
ct.decrypt_json('encrypted.json', 'decrypted.json')
```
