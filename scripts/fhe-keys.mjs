#!/usr/bin/env node
// scripts/fhe-keys.mjs
//
// Standalone CLI for managing FHE key files used by ClawWorker's vendored
// runtime. Mirrors the API in src/fhe-keys/index.ts but ships as plain ESM
// so it runs without a build step.
//
// Usage:
//   node scripts/fhe-keys.mjs status
//   node scripts/fhe-keys.mjs set <skf|dictf|user_authorization> <path>
//   node scripts/fhe-keys.mjs link
//   node scripts/fhe-keys.mjs remove <skf|dictf|user_authorization>
//   node scripts/fhe-keys.mjs install            (runs vendor/fhe-runtime/install.sh)

import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(SCRIPT_DIR, "..");
const RUNTIME_DIR =
    process.env.OPENCLAW_FHE_RUNTIME_DIR?.trim() ||
    path.join(REPO_ROOT, "vendor", "fhe-runtime");
const STORE_DIR =
    process.env.OPENCLAW_FHE_KEYS_DIR?.trim() ||
    path.join(os.homedir(), ".openclaw", "fhe-keys");

const KEY_NAMES = ["skf", "dictf", "user_authorization"];

function linkTargetFor(name) {
    switch (name) {
        case "skf":
            return path.join(RUNTIME_DIR, "crypto_toolkit-64_dev", "crypto_toolkit", "file", "skf");
        case "dictf":
            return path.join(RUNTIME_DIR, "henumpy-dev", "henumpy", "file", "dictf");
        case "user_authorization":
            return path.join(RUNTIME_DIR, "henumpy-dev", "henumpy", "file", "user_authorization");
        default:
            throw new Error(`unknown key name: ${name}`);
    }
}

async function statSafe(p) {
    try {
        return await fs.stat(p);
    } catch {
        return null;
    }
}

async function isLinked(target, expected) {
    try {
        const lst = await fs.lstat(target);
        if (!lst.isSymbolicLink()) return false;
        const resolved = await fs.readlink(target);
        const abs = path.isAbsolute(resolved)
            ? resolved
            : path.resolve(path.dirname(target), resolved);
        return abs === expected;
    } catch {
        return false;
    }
}

async function getStatus() {
    const entries = [];
    for (const name of KEY_NAMES) {
        const storePath = path.join(STORE_DIR, name);
        const linkTarget = linkTargetFor(name);
        const st = await statSafe(storePath);
        const linked = st ? await isLinked(linkTarget, storePath) : false;
        entries.push({
            name,
            storePath,
            present: st !== null,
            sizeBytes: st?.size ?? 0,
            mtimeMs: st?.mtimeMs ?? 0,
            linkTarget,
            linked,
        });
    }
    return {
        storeDir: STORE_DIR,
        runtimeDir: RUNTIME_DIR,
        entries,
        ready: entries.every((e) => e.present && e.linked),
    };
}

function fmtBytes(n) {
    if (!n) return "—";
    if (n < 1024) return `${n} B`;
    if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
    return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

function fmtDate(ms) {
    if (!ms) return "—";
    return new Date(ms).toISOString().replace("T", " ").slice(0, 19);
}

async function cmdStatus() {
    const status = await getStatus();
    console.log("");
    console.log(`  Store:   ${status.storeDir}`);
    console.log(`  Runtime: ${status.runtimeDir}`);
    console.log("");
    console.log(`  ${"Name".padEnd(22)}${"Present".padEnd(10)}${"Linked".padEnd(10)}${"Size".padEnd(12)}Modified`);
    console.log(`  ${"-".repeat(22)}${"-".repeat(10)}${"-".repeat(10)}${"-".repeat(12)}${"-".repeat(19)}`);
    for (const e of status.entries) {
        const present = e.present ? "✅" : "—";
        const linked = e.linked ? "✅" : e.present ? "⚠️" : "—";
        console.log(
            `  ${e.name.padEnd(22)}${present.padEnd(10)}${linked.padEnd(10)}${fmtBytes(e.sizeBytes).padEnd(12)}${fmtDate(e.mtimeMs)}`,
        );
    }
    console.log("");
    console.log(
        status.ready
            ? "  Status: READY — all keys present & linked, FHE runtime can start."
            : "  Status: NOT READY — supply missing keys, then run `link`.",
    );
}

async function cmdSet(name, sourcePath) {
    if (!KEY_NAMES.includes(name)) {
        console.error(`error: name must be one of: ${KEY_NAMES.join(", ")}`);
        process.exit(2);
    }
    if (!sourcePath) {
        console.error("error: missing <path> argument");
        process.exit(2);
    }
    const src = path.resolve(sourcePath);
    const st = await statSafe(src);
    if (!st) {
        console.error(`error: source not found: ${src}`);
        process.exit(2);
    }
    await fs.mkdir(STORE_DIR, { recursive: true });
    const dest = path.join(STORE_DIR, name);
    await fs.copyFile(src, dest);
    try {
        await fs.chmod(dest, 0o400);
    } catch {
        /* best-effort */
    }
    console.log(`✅ Stored ${name} (${fmtBytes(st.size)}) → ${dest}`);
    console.log("   Run `link` to wire it into the vendored runtime.");
}

async function cmdLink() {
    const status = await getStatus();
    let linked = 0;
    let missing = 0;
    for (const e of status.entries) {
        if (!e.present) {
            console.log(`⚠️  ${e.name}: missing in store (${e.storePath})`);
            missing++;
            continue;
        }
        await fs.mkdir(path.dirname(e.linkTarget), { recursive: true });
        try {
            await fs.unlink(e.linkTarget);
        } catch {
            /* nothing to remove */
        }
        await fs.symlink(e.storePath, e.linkTarget);
        console.log(`✅ Linked ${e.linkTarget}  →  ${e.storePath}`);
        linked++;
    }
    console.log("");
    console.log(`Summary: ${linked} linked, ${missing} missing`);
    if (missing > 0) process.exit(2);
}

async function cmdRemove(name) {
    if (!KEY_NAMES.includes(name)) {
        console.error(`error: name must be one of: ${KEY_NAMES.join(", ")}`);
        process.exit(2);
    }
    const storePath = path.join(STORE_DIR, name);
    const target = linkTargetFor(name);
    try {
        await fs.unlink(storePath);
        console.log(`removed: ${storePath}`);
    } catch {
        console.log(`not present in store: ${storePath}`);
    }
    try {
        await fs.unlink(target);
        console.log(`removed link: ${target}`);
    } catch {
        /* not linked */
    }
}

function cmdInstall() {
    return new Promise((resolve, reject) => {
        const script = path.join(RUNTIME_DIR, "install.sh");
        const child = spawn("bash", [script], { stdio: "inherit" });
        child.on("error", reject);
        child.on("exit", (code) =>
            code === 0 ? resolve() : reject(new Error(`install.sh exited with ${code}`)),
        );
    });
}

function printHelp() {
    console.log(`Usage:
  node scripts/fhe-keys.mjs status
  node scripts/fhe-keys.mjs set <name> <path>
  node scripts/fhe-keys.mjs link
  node scripts/fhe-keys.mjs remove <name>
  node scripts/fhe-keys.mjs install

Names: skf | dictf | user_authorization

Environment:
  OPENCLAW_FHE_KEYS_DIR     override store dir (default ~/.openclaw/fhe-keys)
  OPENCLAW_FHE_RUNTIME_DIR  override vendor runtime dir
`);
}

const [, , cmd, ...args] = process.argv;
try {
    switch (cmd) {
        case "status":
        case undefined:
            await cmdStatus();
            break;
        case "set":
            await cmdSet(args[0], args[1]);
            break;
        case "link":
            await cmdLink();
            break;
        case "remove":
            await cmdRemove(args[0]);
            break;
        case "install":
            await cmdInstall();
            break;
        case "-h":
        case "--help":
        case "help":
            printHelp();
            break;
        default:
            console.error(`unknown command: ${cmd}\n`);
            printHelp();
            process.exit(2);
    }
} catch (err) {
    console.error(err.stack || err.message);
    process.exit(1);
}
