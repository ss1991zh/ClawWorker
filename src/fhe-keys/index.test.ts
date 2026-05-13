import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import {
  FHE_KEY_NAMES,
  getStatus,
  installKey,
  installKeyFromBuffer,
  relinkAll,
  removeKey,
} from "./index.ts";

describe("fhe-keys", () => {
  let tmpRoot: string;
  let storeDir: string;
  let runtimeDir: string;

  beforeEach(async () => {
    tmpRoot = await fs.mkdtemp(path.join(os.tmpdir(), "fhe-keys-test-"));
    storeDir = path.join(tmpRoot, "store");
    runtimeDir = path.join(tmpRoot, "runtime");
    await fs.mkdir(storeDir, { recursive: true });
    await fs.mkdir(runtimeDir, { recursive: true });
  });

  afterEach(async () => {
    await fs.rm(tmpRoot, { recursive: true, force: true });
  });

  it("reports all three keys missing on an empty store", async () => {
    const status = await getStatus({ storeDir, runtimeDir });
    expect(status.entries).toHaveLength(3);
    expect(status.entries.map((e) => e.name)).toEqual([...FHE_KEY_NAMES]);
    expect(status.entries.every((e) => !e.present && !e.linked)).toBe(true);
    expect(status.ready).toBe(false);
  });

  it("installKey copies a file into the store and reports present-but-unlinked", async () => {
    const src = path.join(tmpRoot, "src-skf");
    await fs.writeFile(src, "fake-skf-bytes");
    const result = await installKey("skf", src, { storeDir, runtimeDir });
    expect(result.sizeBytes).toBe("fake-skf-bytes".length);

    const status = await getStatus({ storeDir, runtimeDir });
    const skf = status.entries.find((e) => e.name === "skf")!;
    expect(skf.present).toBe(true);
    expect(skf.linked).toBe(false);
    expect(status.ready).toBe(false);
  });

  it("relinkAll creates symlinks for present keys and marks status ready when all three are linked", async () => {
    for (const name of FHE_KEY_NAMES) {
      await installKeyFromBuffer(name, Buffer.from(`payload-${name}`), {
        storeDir,
        runtimeDir,
      });
    }
    const status = await relinkAll({ storeDir, runtimeDir });
    expect(status.ready).toBe(true);
    for (const entry of status.entries) {
      expect(entry.linked).toBe(true);
      const lst = await fs.lstat(entry.linkTarget);
      expect(lst.isSymbolicLink()).toBe(true);
      const resolved = await fs.readlink(entry.linkTarget);
      expect(resolved).toBe(entry.storePath);
    }
  });

  it("relinkAll replaces an existing target file with a symlink", async () => {
    await installKeyFromBuffer("skf", Buffer.from("real-skf"), { storeDir, runtimeDir });
    // Pre-create a stale file at the target location.
    const targetDir = path.join(runtimeDir, "crypto_toolkit-64_dev", "crypto_toolkit", "file");
    await fs.mkdir(targetDir, { recursive: true });
    await fs.writeFile(path.join(targetDir, "skf"), "stale-content");
    const status = await relinkAll({ storeDir, runtimeDir });
    const skf = status.entries.find((e) => e.name === "skf")!;
    expect(skf.linked).toBe(true);
  });

  it("removeKey clears both the store entry and the symlink", async () => {
    await installKeyFromBuffer("dictf", Buffer.from("dict-bytes"), {
      storeDir,
      runtimeDir,
    });
    await relinkAll({ storeDir, runtimeDir });
    await removeKey("dictf", { storeDir, runtimeDir });
    const status = await getStatus({ storeDir, runtimeDir });
    const dictf = status.entries.find((e) => e.name === "dictf")!;
    expect(dictf.present).toBe(false);
    expect(dictf.linked).toBe(false);
  });

  it("OPENCLAW_FHE_KEYS_DIR overrides the default store location", async () => {
    const overridden = path.join(tmpRoot, "env-override");
    await fs.mkdir(overridden, { recursive: true });
    const prev = process.env.OPENCLAW_FHE_KEYS_DIR;
    try {
      process.env.OPENCLAW_FHE_KEYS_DIR = overridden;
      const status = await getStatus({ runtimeDir });
      expect(status.storeDir).toBe(overridden);
    } finally {
      if (prev === undefined) {
        delete process.env.OPENCLAW_FHE_KEYS_DIR;
      } else {
        process.env.OPENCLAW_FHE_KEYS_DIR = prev;
      }
    }
  });
});
