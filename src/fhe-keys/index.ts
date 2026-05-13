/**
 * FHE Keys management — programmatic API.
 *
 * The vendored FHE runtime (vendor/fhe-runtime/) expects three user-supplied
 * files to live inside specific package subdirectories:
 *
 *   - skf                 → crypto_toolkit-64_dev/crypto_toolkit/file/skf
 *   - dictf               → henumpy-dev/henumpy/file/dictf
 *   - user_authorization  → henumpy-dev/henumpy/file/user_authorization
 *
 * We keep the real files in ~/.openclaw/fhe-keys/ (the "store") and symlink
 * them into the vendored package directories. This module is the single
 * source of truth for that workflow; UI panels and CLI both consume it.
 */

import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const MODULE_DIR = path.dirname(fileURLToPath(import.meta.url));

/** Logical names of the three required key files. */
export type FheKeyName = "skf" | "dictf" | "user_authorization";

export const FHE_KEY_NAMES: readonly FheKeyName[] = ["skf", "dictf", "user_authorization"] as const;

/** Per-file status entry. */
export interface FheKeyEntry {
  name: FheKeyName;
  /** Absolute path inside the user's key store. */
  storePath: string;
  /** True iff the store file exists. */
  present: boolean;
  /** File size in bytes (0 when missing). */
  sizeBytes: number;
  /** Last-modified timestamp, ms since epoch (0 when missing). */
  mtimeMs: number;
  /** Absolute target the key must be linked to inside vendor/fhe-runtime/. */
  linkTarget: string;
  /** True iff `linkTarget` is a symlink pointing at `storePath`. */
  linked: boolean;
}

/** Aggregate status for all three keys. */
export interface FheKeysStatus {
  storeDir: string;
  runtimeDir: string;
  entries: FheKeyEntry[];
  /** True iff all three files are present AND linked. */
  ready: boolean;
}

interface ResolveOptions {
  /** Override `~/.openclaw/fhe-keys/`. Honors `OPENCLAW_FHE_KEYS_DIR` env. */
  storeDir?: string;
  /** Override `<repo>/vendor/fhe-runtime/`. */
  runtimeDir?: string;
}

/** Resolve the key store directory. */
export function resolveStoreDir(opts: ResolveOptions = {}): string {
  return (
    opts.storeDir ??
    process.env.OPENCLAW_FHE_KEYS_DIR?.trim() ??
    path.join(os.homedir(), ".openclaw", "fhe-keys")
  );
}

/** Resolve the vendored FHE runtime directory. */
export function resolveRuntimeDir(opts: ResolveOptions = {}): string {
  if (opts.runtimeDir) return opts.runtimeDir;
  // Repo-root relative; this file lives at src/fhe-keys/index.ts when run from
  // source, so two levels up is the repo root. When bundled to dist/ the
  // caller should pass `runtimeDir` explicitly, or set OPENCLAW_FHE_RUNTIME_DIR.
  const envOverride = process.env.OPENCLAW_FHE_RUNTIME_DIR?.trim();
  if (envOverride) return envOverride;
  return path.resolve(MODULE_DIR, "..", "..", "vendor", "fhe-runtime");
}

/** Map a key name to its in-package target path. */
function linkTargetFor(runtimeDir: string, name: FheKeyName): string {
  switch (name) {
    case "skf":
      return path.join(runtimeDir, "crypto_toolkit-64_dev", "crypto_toolkit", "file", "skf");
    case "dictf":
      return path.join(runtimeDir, "henumpy-dev", "henumpy", "file", "dictf");
    case "user_authorization":
      return path.join(runtimeDir, "henumpy-dev", "henumpy", "file", "user_authorization");
  }
}

async function statSafe(p: string): Promise<{ size: number; mtimeMs: number } | null> {
  try {
    const st = await fs.stat(p);
    return { size: st.size, mtimeMs: st.mtimeMs };
  } catch {
    return null;
  }
}

async function isLinkedTo(target: string, expectedSource: string): Promise<boolean> {
  try {
    const lst = await fs.lstat(target);
    if (!lst.isSymbolicLink()) return false;
    const resolved = await fs.readlink(target);
    const absoluteResolved = path.isAbsolute(resolved)
      ? resolved
      : path.resolve(path.dirname(target), resolved);
    return absoluteResolved === expectedSource;
  } catch {
    return false;
  }
}

/** Read full status for all three keys. */
export async function getStatus(opts: ResolveOptions = {}): Promise<FheKeysStatus> {
  const storeDir = resolveStoreDir(opts);
  const runtimeDir = resolveRuntimeDir(opts);

  const entries: FheKeyEntry[] = await Promise.all(
    FHE_KEY_NAMES.map(async (name): Promise<FheKeyEntry> => {
      const storePath = path.join(storeDir, name);
      const linkTarget = linkTargetFor(runtimeDir, name);
      const stat = await statSafe(storePath);
      const linked = stat ? await isLinkedTo(linkTarget, storePath) : false;
      return {
        name,
        storePath,
        present: stat !== null,
        sizeBytes: stat?.size ?? 0,
        mtimeMs: stat?.mtimeMs ?? 0,
        linkTarget,
        linked,
      };
    }),
  );

  const ready = entries.every((e) => e.present && e.linked);
  return { storeDir, runtimeDir, entries, ready };
}

/** Install a key by copying it from a source path into the store directory. */
export async function installKey(
  name: FheKeyName,
  sourcePath: string,
  opts: ResolveOptions = {},
): Promise<{ stored: string; sizeBytes: number }> {
  const storeDir = resolveStoreDir(opts);
  await fs.mkdir(storeDir, { recursive: true });
  const destination = path.join(storeDir, name);
  await fs.copyFile(sourcePath, destination);
  // Keys are sensitive — make read-only to the owner. (chmod is a no-op on Windows.)
  try {
    await fs.chmod(destination, 0o400);
  } catch {
    /* best-effort */
  }
  const stat = await fs.stat(destination);
  return { stored: destination, sizeBytes: stat.size };
}

/** Install a key from an in-memory buffer (e.g. a UI file upload). */
export async function installKeyFromBuffer(
  name: FheKeyName,
  data: Buffer | Uint8Array,
  opts: ResolveOptions = {},
): Promise<{ stored: string; sizeBytes: number }> {
  const storeDir = resolveStoreDir(opts);
  await fs.mkdir(storeDir, { recursive: true });
  const destination = path.join(storeDir, name);
  await fs.writeFile(destination, data);
  try {
    await fs.chmod(destination, 0o400);
  } catch {
    /* best-effort */
  }
  const stat = await fs.stat(destination);
  return { stored: destination, sizeBytes: stat.size };
}

/** Re-link all present store files into their vendor target locations. */
export async function relinkAll(opts: ResolveOptions = {}): Promise<FheKeysStatus> {
  const status = await getStatus(opts);
  for (const entry of status.entries) {
    if (!entry.present) continue;
    await fs.mkdir(path.dirname(entry.linkTarget), { recursive: true });
    // Remove any existing file or symlink at the target before creating a fresh link.
    try {
      await fs.unlink(entry.linkTarget);
    } catch {
      /* ignore: nothing to remove */
    }
    await fs.symlink(entry.storePath, entry.linkTarget);
  }
  return getStatus(opts);
}

/** Remove a key from the store (and best-effort drop its dangling link). */
export async function removeKey(name: FheKeyName, opts: ResolveOptions = {}): Promise<void> {
  const storeDir = resolveStoreDir(opts);
  const runtimeDir = resolveRuntimeDir(opts);
  const storePath = path.join(storeDir, name);
  const target = linkTargetFor(runtimeDir, name);
  try {
    await fs.unlink(storePath);
  } catch {
    /* not present */
  }
  try {
    await fs.unlink(target);
  } catch {
    /* not linked */
  }
}
