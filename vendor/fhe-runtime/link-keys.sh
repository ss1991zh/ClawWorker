#!/usr/bin/env bash
# Symlink user-supplied FHE keys (managed via the config center "同态密钥"
# panel, stored under data/fhe-keys/) into the vendored packages' expected
# file/ locations.
#
#   data/fhe-keys/skf                -> crypto_toolkit-64_dev/crypto_toolkit/file/skf
#   data/fhe-keys/dictf              -> henumpy-dev/henumpy/file/dictf
#   data/fhe-keys/user_authorization -> henumpy-dev/henumpy/file/user_authorization
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEYS="${OPENCLAW_FHE_KEYS_DIR:-$HERE/../../data/fhe-keys}"

link() {
  local src="$KEYS/$1" dst="$HERE/$2"
  if [[ ! -e "$src" ]]; then echo "⚠️  缺少 $1（请在配置中心→同态密钥上传）"; return 1; fi
  mkdir -p "$(dirname "$dst")"; rm -f "$dst"; ln -s "$src" "$dst"
  echo "✅ $2  ->  $src"
}

ok=0
link skf                crypto_toolkit-64_dev/crypto_toolkit/file/skf            && ok=$((ok+1)) || true
link dictf              henumpy-dev/henumpy/file/dictf                           && ok=$((ok+1)) || true
link user_authorization henumpy-dev/henumpy/file/user_authorization              && ok=$((ok+1)) || true
echo ""; echo "完成：$ok/3 已链接"
[[ $ok -eq 3 ]]
