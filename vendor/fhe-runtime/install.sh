#!/usr/bin/env bash
# Install ClawWorker FHE runtime — the 4 vendored Python packages.
#
# Prerequisites:
#   - Python 3.11 (NOT 3.12+, vendor packages target 3.11)
#   - numpy<2
#   - Keys/dict/auth files placed in ~/.openclaw/fhe-keys/
#
# Usage:
#   bash vendor/fhe-runtime/install.sh [--venv .venv-fhe]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---- args ----
VENV_DIR=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --venv) VENV_DIR="$2"; shift 2;;
        -h|--help)
            sed -n '2,12p' "$0"
            exit 0;;
        *) echo "unknown arg: $1" >&2; exit 1;;
    esac
done

# ---- python check ----
if ! command -v python3.11 >/dev/null 2>&1; then
    echo "ERROR: python3.11 not found. Install via: brew install python@3.11" >&2
    exit 1
fi

PY_VERSION="$(python3.11 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$PY_VERSION" != "3.11" ]]; then
    echo "ERROR: expected Python 3.11, got $PY_VERSION" >&2
    exit 1
fi

# ---- venv (optional) ----
PIP="pip3.11"
if [[ -n "$VENV_DIR" ]]; then
    if [[ ! -d "$VENV_DIR" ]]; then
        echo ">> Creating venv at $VENV_DIR"
        python3.11 -m venv "$VENV_DIR"
    fi
    # shellcheck source=/dev/null
    source "$VENV_DIR/bin/activate"
    PIP="pip"
    "$PIP" install --upgrade pip
fi

# ---- ensure numpy<2 ----
echo ">> Pinning numpy<2 (required by FHE runtime)"
"$PIP" install --upgrade "numpy<2"

# ---- install in dependency order ----
PACKAGES=(
    crypto_toolkit-64_dev
    henumpy-dev
    pandaseal-dev
    helearn-dev
)

for pkg in "${PACKAGES[@]}"; do
    pkg_dir="$SCRIPT_DIR/$pkg"
    if [[ ! -d "$pkg_dir" ]]; then
        echo "ERROR: package directory not found: $pkg_dir" >&2
        exit 1
    fi
    echo ""
    echo ">> Installing $pkg (editable)"
    (cd "$pkg_dir" && "$PIP" install -e .)
done

# ---- link key files ----
echo ""
echo ">> Linking key files from ~/.openclaw/fhe-keys/"
bash "$SCRIPT_DIR/link-keys.sh" || {
    echo ""
    echo "WARNING: key linking failed. FHE runtime is installed but cannot run"
    echo "         until you place keys in ~/.openclaw/fhe-keys/ and re-run"
    echo "         bash vendor/fhe-runtime/link-keys.sh"
}

echo ""
echo "✅ FHE runtime install complete."
echo "   Verify with: python3.11 -c 'import crypto_toolkit, henumpy, pandaseal, helearn; print(\"ok\")'"
