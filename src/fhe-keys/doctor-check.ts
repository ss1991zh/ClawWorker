/**
 * Doctor check for the FHE runtime keys.
 *
 * Renders a human-readable section in `openclaw doctor` output indicating
 * which of skf / dictf / user_authorization are present in
 * `~/.openclaw/fhe-keys/` and whether they are symlinked into the vendored
 * runtime directories.
 *
 * Returns null when nothing FHE-related is configured (i.e. the user has
 * never created the keys directory) so the check is silent on installs
 * that don't use FHE.
 */

import { promises as fs } from "node:fs";
import {
  getStatus,
  resolveStoreDir,
  type FheKeyEntry,
  type FheKeysStatus,
} from "./index.ts";

export interface DoctorReportSection {
  title: string;
  level: "ok" | "warn" | "error" | "info";
  lines: string[];
}

function formatEntry(entry: FheKeyEntry): string {
  const presentMark = entry.present ? "✓" : "✗";
  const linkedMark = entry.linked ? "✓" : entry.present ? "!" : "—";
  const size = entry.sizeBytes ? `${(entry.sizeBytes / 1024).toFixed(1)} KB` : "—";
  return `  [${presentMark}] [${linkedMark}] ${entry.name.padEnd(20)} ${size}`;
}

function describeStatus(status: FheKeysStatus): {
  level: DoctorReportSection["level"];
  hint: string;
} {
  const missing = status.entries.filter((e) => !e.present).map((e) => e.name);
  const unlinked = status.entries
    .filter((e) => e.present && !e.linked)
    .map((e) => e.name);

  if (status.ready) {
    return { level: "ok", hint: "FHE runtime is ready." };
  }
  if (missing.length === status.entries.length) {
    return {
      level: "info",
      hint:
        `No FHE keys installed. Place files in ${status.storeDir} ` +
        `then run \`node scripts/fhe-keys.mjs link\` (or skip if not using FHE skills).`,
    };
  }
  if (missing.length > 0) {
    return {
      level: "warn",
      hint:
        `Missing keys: ${missing.join(", ")}. ` +
        `Use \`node scripts/fhe-keys.mjs set <name> <path>\` to install.`,
    };
  }
  if (unlinked.length > 0) {
    return {
      level: "warn",
      hint:
        `Keys present but not linked into the runtime: ${unlinked.join(", ")}. ` +
        `Run \`node scripts/fhe-keys.mjs link\`.`,
    };
  }
  return { level: "warn", hint: "FHE runtime keys are in an inconsistent state." };
}

/** Build the doctor section. Returns `null` to mean "skip this check entirely". */
export async function buildFheKeysDoctorSection(): Promise<DoctorReportSection | null> {
  const storeDir = resolveStoreDir();
  // Skip silently when the user hasn't even created the store directory —
  // they're probably not using FHE features.
  try {
    await fs.access(storeDir);
  } catch {
    return null;
  }

  const status = await getStatus();
  const { level, hint } = describeStatus(status);
  const lines = [
    `Store:   ${status.storeDir}`,
    `Runtime: ${status.runtimeDir}`,
    "",
    "  Present Linked Key                  Size",
    "  ------- ------ -------------------- --------",
    ...status.entries.map(formatEntry),
    "",
    hint,
  ];
  return {
    title: "FHE runtime keys",
    level,
    lines,
  };
}
