# FHE Runtime — vendored Python packages

This directory contains the four Python packages that power ClawWorker's
pre-installed FHE (Fully Homomorphic Encryption) skills.

```
vendor/fhe-runtime/
├── crypto_toolkit-64_dev/    Low-level FHE primitives  (needs: skf)
├── henumpy-dev/              Ciphertext NumPy          (needs: dictf, user_authorization)
├── pandaseal-dev/            Ciphertext Pandas
├── helearn-dev/              Ciphertext scikit-learn
├── install.sh                One-shot installer
├── link-keys.sh              Links user keys into package file/ dirs
└── README.md                 This file
```

Dependency chain: `crypto_toolkit → henumpy → {pandaseal, helearn}`

## Prerequisites

- **Python 3.11** (exact). The packages are pinned to 3.11; later versions are
  not supported.
- **numpy < 2** (the installer pins this for you).
- Three secret files supplied by the FHE vendor (see "Key files" below).

## Key files (you supply these)

These files are **NOT** in git and **MUST** be provided by you. Put them here:

```
~/.openclaw/fhe-keys/
├── skf                  ← SKF private key  (→ crypto_toolkit)
├── dictf                ← Operation authorization dictionary (→ henumpy)
└── user_authorization   ← Software license identity file     (→ henumpy)
```

Override the location with `OPENCLAW_FHE_KEYS_DIR=/path/to/keys`.

## Install

```bash
# 1. Put your key files in place
mkdir -p ~/.openclaw/fhe-keys
cp /path/to/skf                ~/.openclaw/fhe-keys/
cp /path/to/dictf              ~/.openclaw/fhe-keys/
cp /path/to/user_authorization ~/.openclaw/fhe-keys/

# 2. Install into the system Python 3.11
bash vendor/fhe-runtime/install.sh

# Or into a venv:
bash vendor/fhe-runtime/install.sh --venv .venv-fhe
```

## Re-link keys only

If you swap key files but don't need to reinstall packages:

```bash
bash vendor/fhe-runtime/link-keys.sh
```

## Verify install

```bash
python3.11 -c "import crypto_toolkit, henumpy, pandaseal, helearn; print('ok')"
```

## How ClawWorker uses this

The bundled skills under `skills/{zfhe,henumpy,pandaseal,hetorch,helearn}-skill/`
generate Python code that imports from these packages. The skills themselves
are documentation; this directory provides the actual runtime.

When the user invokes one of these skills, Claude generates Python code that
the gateway hands to a Python subprocess. As long as `python3.11` resolves
the four packages (i.e. this directory has been `pip install -e`'d) and the
three key files are linked, the code will run.
