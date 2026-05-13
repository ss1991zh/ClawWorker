import type { GatewayBrowserClient } from "../gateway.ts";

/**
 * Mirror of src/fhe-keys/index.ts payload shapes — declared explicitly
 * here so the Control UI bundle does not import server-side modules.
 */
export type FheKeyName = "skf" | "dictf" | "user_authorization";

export interface FheKeyEntryView {
  name: FheKeyName;
  storePath: string;
  linkTarget: string;
  present: boolean;
  linked: boolean;
  sizeBytes: number;
  mtimeMs: number;
}

export interface FheKeysStatusView {
  storeDir: string;
  runtimeDir: string;
  ready: boolean;
  entries: FheKeyEntryView[];
}

export interface FheKeysState {
  client: GatewayBrowserClient | null;
  connected?: boolean;
  fheKeysLoading: boolean;
  fheKeysStatus: FheKeysStatusView | null;
  fheKeysError: string | null;
  fheKeysBusyKey: FheKeyName | null;
}

const VALID_NAMES: readonly FheKeyName[] = ["skf", "dictf", "user_authorization"];

export function isFheKeyName(value: unknown): value is FheKeyName {
  return typeof value === "string" && (VALID_NAMES as readonly string[]).includes(value);
}

/** Refresh the keys status into state.fheKeysStatus. Idempotent + safe to chain. */
export async function loadFheKeys(state: FheKeysState): Promise<void> {
  if (!state.client) {
    state.fheKeysStatus = null;
    state.fheKeysError = null;
    return;
  }
  if (state.fheKeysLoading) return;
  state.fheKeysLoading = true;
  try {
    const reply = await state.client.request<{ status: FheKeysStatusView }>("fhe.keys.status", {});
    state.fheKeysStatus = reply?.status ?? null;
    state.fheKeysError = null;
  } catch (err) {
    state.fheKeysError = err instanceof Error ? err.message : String(err);
  } finally {
    state.fheKeysLoading = false;
  }
}

/** Upload a single key file (e.g. from an <input type=file>) and auto-relink. */
export async function uploadFheKey(
  state: FheKeysState,
  name: FheKeyName,
  file: File,
): Promise<void> {
  if (!state.client) return;
  state.fheKeysBusyKey = name;
  state.fheKeysError = null;
  try {
    const buf = new Uint8Array(await file.arrayBuffer());
    const dataBase64 = bufferToBase64(buf);
    const reply = await state.client.request<{ status: FheKeysStatusView }>("fhe.keys.upload", {
      name,
      dataBase64,
    });
    state.fheKeysStatus = reply?.status ?? state.fheKeysStatus;
  } catch (err) {
    state.fheKeysError = err instanceof Error ? err.message : String(err);
  } finally {
    state.fheKeysBusyKey = null;
  }
}

/** Re-link present store files into the vendored runtime directories. */
export async function relinkFheKeys(state: FheKeysState): Promise<void> {
  if (!state.client) return;
  state.fheKeysLoading = true;
  state.fheKeysError = null;
  try {
    const reply = await state.client.request<{ status: FheKeysStatusView }>("fhe.keys.link", {});
    state.fheKeysStatus = reply?.status ?? state.fheKeysStatus;
  } catch (err) {
    state.fheKeysError = err instanceof Error ? err.message : String(err);
  } finally {
    state.fheKeysLoading = false;
  }
}

/** Drop a key from the store and clear its symlink. */
export async function removeFheKey(state: FheKeysState, name: FheKeyName): Promise<void> {
  if (!state.client) return;
  state.fheKeysBusyKey = name;
  state.fheKeysError = null;
  try {
    const reply = await state.client.request<{ status: FheKeysStatusView }>("fhe.keys.remove", {
      name,
    });
    state.fheKeysStatus = reply?.status ?? state.fheKeysStatus;
  } catch (err) {
    state.fheKeysError = err instanceof Error ? err.message : String(err);
  } finally {
    state.fheKeysBusyKey = null;
  }
}

/** Convert a binary buffer to base64 inside the browser without exhausting the call stack. */
function bufferToBase64(bytes: Uint8Array): string {
  const CHUNK = 0x8000;
  let binary = "";
  for (let i = 0; i < bytes.length; i += CHUNK) {
    const slice = bytes.subarray(i, Math.min(i + CHUNK, bytes.length));
    binary += String.fromCharCode.apply(null, Array.from(slice));
  }
  return btoa(binary);
}
