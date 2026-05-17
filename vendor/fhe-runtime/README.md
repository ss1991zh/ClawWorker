# FHE Runtime（密态数据分析工具集）

供 Skill 接入后由 Agent 调用的同态加密计算包。

## 包

| 目录 | 包 | 对标 |
|------|----|------|
| `crypto_toolkit-64_dev` | crypto_toolkit | 底层加解密（需 skf 私钥）|
| `henumpy-dev` | henumpy | 密文 NumPy（需 dictf + user_authorization）|
| `pandaseal-dev` | pandaseal | 密文 Pandas |
| `helearn-dev` | helearn | 密文 sklearn |

依赖链：`crypto_toolkit → henumpy → {pandaseal, helearn}`

## 安装（首次）

```bash
# Python 3.11，numpy<2
python3.11 -m venv .venv-fhe && source .venv-fhe/bin/activate
pip install "numpy<2"
for d in crypto_toolkit-64_dev henumpy-dev pandaseal-dev helearn-dev; do
  (cd vendor/fhe-runtime/$d && pip install -e .)
done
```

## 密钥

三份密钥由 **配置中心 → 同态密钥** 面板上传，存到 `data/fhe-keys/`
（不入 git）。安装后或换密钥后执行：

```bash
bash vendor/fhe-runtime/link-keys.sh
```

把 `data/fhe-keys/{skf,dictf,user_authorization}` 软链进各包的 `file/` 目录。

## Agent 调用

Skill 接入后，Agent 通过工具在 Python 子进程里 `import henumpy / pandaseal /
helearn / crypto_toolkit` 执行密态计算，再返回解密结果。
