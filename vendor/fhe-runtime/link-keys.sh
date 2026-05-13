#!/usr/bin/env bash
# Link user-supplied FHE key/dict/authorization files into the vendored
# packages' expected `file/` locations.
#
# Source of truth:  ~/.openclaw/fhe-keys/{skf,dictf,user_authorization}
# Targets:
#   crypto_toolkit-64_dev/crypto_toolkit/file/skf
#   henumpy-dev/henumpy/file/dictf
#   henumpy-dev/henumpy/file/user_authorization

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEYS_DIR="${OPENCLAW_FHE_KEYS_DIR:-$HOME/.openclaw/fhe-keys}"

mkdir -p "$KEYS_DIR"

# (source_filename, target_relative_path_under_SCRIPT_DIR)
LINKS=(
    "skf|crypto_toolkit-64_dev/crypto_toolkit/file/skf"
    "dictf|henumpy-dev/henumpy/file/dictf"
    "user_authorization|henumpy-dev/henumpy/file/user_authorization"
)

missing=0
linked=0
for entry in "${LINKS[@]}"; do
    src_name="${entry%|*}"
    dst_rel="${entry#*|}"
    src_path="$KEYS_DIR/$src_name"
    dst_path="$SCRIPT_DIR/$dst_rel"

    if [[ ! -e "$src_path" ]]; then
        echo "⚠️  MISSING: $src_path"
        missing=$((missing + 1))
        continue
    fi

    mkdir -p "$(dirname "$dst_path")"
    # Replace existing symlink/file
    [[ -e "$dst_path" || -L "$dst_path" ]] && rm -f "$dst_path"
    ln -s "$src_path" "$dst_path"
    echo "✅ Linked: $dst_path  →  $src_path"
    linked=$((linked + 1))
done

echo ""
echo "Summary: $linked linked, $missing missing"
echo "Keys directory: $KEYS_DIR"

if [[ "$missing" -gt 0 ]]; then
    echo ""
    echo "To supply missing files:"
    echo "  1. Put skf, dictf, user_authorization into $KEYS_DIR/"
    echo "  2. Re-run: bash vendor/fhe-runtime/link-keys.sh"
    echo "  (Or use ClawWorker Settings → FHE Keys to upload them.)"
    exit 2
fi
