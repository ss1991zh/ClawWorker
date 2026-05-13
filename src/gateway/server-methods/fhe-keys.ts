/**
 * Gateway RPC handlers for FHE key management.
 *
 * Exposes four methods to the Control UI:
 *   - fhe.keys.status   (READ)   → list of {name, present, linked, sizeBytes, mtimeMs, ...}
 *   - fhe.keys.upload   (WRITE)  → install a key from a base64 payload
 *   - fhe.keys.link     (WRITE)  → re-link present store files into the runtime
 *   - fhe.keys.remove   (WRITE)  → drop a key from the store + its symlink
 *
 * Backed by src/fhe-keys/index.ts so the CLI and UI share one source of truth.
 */

import { Buffer } from "node:buffer";
import {
  FHE_KEY_NAMES,
  getStatus,
  installKeyFromBuffer,
  relinkAll,
  removeKey,
  type FheKeyName,
} from "../../fhe-keys/index.js";
import { ErrorCodes, errorShape } from "../protocol/index.js";
import type { GatewayRequestHandlers } from "./types.js";

const VALID_NAMES = new Set<string>(FHE_KEY_NAMES);

function coerceKeyName(value: unknown): FheKeyName | null {
  return typeof value === "string" && VALID_NAMES.has(value) ? (value as FheKeyName) : null;
}

function decodeBase64(value: unknown): Buffer | null {
  if (typeof value !== "string" || value.length === 0) return null;
  try {
    return Buffer.from(value, "base64");
  } catch {
    return null;
  }
}

export const fheKeysHandlers: GatewayRequestHandlers = {
  "fhe.keys.status": async ({ respond }) => {
    try {
      const status = await getStatus();
      respond(true, { status }, undefined);
    } catch (err) {
      respond(
        false,
        undefined,
        errorShape(
          ErrorCodes.UNAVAILABLE,
          err instanceof Error ? err.message : "failed to read FHE key status",
        ),
      );
    }
  },

  "fhe.keys.upload": async ({ params, respond }) => {
    const name = coerceKeyName((params as { name?: unknown }).name);
    if (!name) {
      respond(
        false,
        undefined,
        errorShape(
          ErrorCodes.INVALID_REQUEST,
          `invalid key name; expected one of: ${FHE_KEY_NAMES.join(", ")}`,
        ),
      );
      return;
    }
    const data = decodeBase64((params as { dataBase64?: unknown }).dataBase64);
    if (!data || data.length === 0) {
      respond(
        false,
        undefined,
        errorShape(ErrorCodes.INVALID_REQUEST, "missing or invalid dataBase64"),
      );
      return;
    }
    try {
      const stored = await installKeyFromBuffer(name, data);
      const status = await relinkAll();
      respond(true, { stored, status }, undefined);
    } catch (err) {
      respond(
        false,
        undefined,
        errorShape(
          ErrorCodes.UNAVAILABLE,
          err instanceof Error ? err.message : "failed to install FHE key",
        ),
      );
    }
  },

  "fhe.keys.link": async ({ respond }) => {
    try {
      const status = await relinkAll();
      respond(true, { status }, undefined);
    } catch (err) {
      respond(
        false,
        undefined,
        errorShape(
          ErrorCodes.UNAVAILABLE,
          err instanceof Error ? err.message : "failed to relink FHE keys",
        ),
      );
    }
  },

  "fhe.keys.remove": async ({ params, respond }) => {
    const name = coerceKeyName((params as { name?: unknown }).name);
    if (!name) {
      respond(
        false,
        undefined,
        errorShape(
          ErrorCodes.INVALID_REQUEST,
          `invalid key name; expected one of: ${FHE_KEY_NAMES.join(", ")}`,
        ),
      );
      return;
    }
    try {
      await removeKey(name);
      const status = await getStatus();
      respond(true, { status }, undefined);
    } catch (err) {
      respond(
        false,
        undefined,
        errorShape(
          ErrorCodes.UNAVAILABLE,
          err instanceof Error ? err.message : "failed to remove FHE key",
        ),
      );
    }
  },
};
