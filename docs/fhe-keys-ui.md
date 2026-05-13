# FHE Keys — Settings UI integration guide

The `src/fhe-keys/` module exposes a clean programmatic API; this document
shows how to wire it into the existing Control UI as a settings tab. It
follows ClawWorker's established navigation/controller/render patterns so
the change stays minimal and reviewable.

## 1. Backend module (already shipped)

| File | Purpose |
|------|---------|
| `src/fhe-keys/index.ts` | `getStatus`, `installKey`, `installKeyFromBuffer`, `relinkAll`, `removeKey` |
| `src/fhe-keys/doctor-check.ts` | `buildFheKeysDoctorSection()` for `openclaw doctor` |
| `scripts/fhe-keys.mjs` | Standalone CLI (works without a build) |

These are usable as-is. The UI plan below wraps them in a settings panel.

## 2. Gateway RPC methods

Add to `src/gateway/server-methods/fhe-keys.ts`:

```ts
import { getStatus, installKeyFromBuffer, relinkAll, removeKey, type FheKeyName }
  from "../../fhe-keys/index.js";
import type { GatewayRequestHandler } from "./types.js";

export const fheKeysStatusHandler: GatewayRequestHandler = async () => {
  const status = await getStatus();
  return { ok: true, status };
};

export const fheKeysUploadHandler: GatewayRequestHandler = async ({ params }) => {
  const { name, dataBase64 } = params as { name: FheKeyName; dataBase64: string };
  const buf = Buffer.from(dataBase64, "base64");
  return await installKeyFromBuffer(name, buf);
};

export const fheKeysLinkHandler: GatewayRequestHandler = async () =>
  await relinkAll();

export const fheKeysRemoveHandler: GatewayRequestHandler = async ({ params }) => {
  const { name } = params as { name: FheKeyName };
  await removeKey(name);
  return await getStatus();
};
```

Register them in `src/gateway/server-methods-list.ts` (inside `BASE_METHODS`):

```diff
   "config.get",
   "config.set",
+  "fhe.keys.status",
+  "fhe.keys.upload",
+  "fhe.keys.link",
+  "fhe.keys.remove",
```

Wire the handlers in `src/gateway/server-aux-handlers.ts` next to other
config-family handlers, and grant `WRITE_SCOPE` for upload/link/remove
and `READ_SCOPE` for status in `method-scopes.ts`.

## 3. Navigation (`ui/src/ui/navigation.ts`)

```diff
   {
     label: "settings",
     tabs: [
       "config",
       "communications",
       "appearance",
       "automation",
       "infrastructure",
       "aiAgents",
+      "fheKeys",
       "debug",
       "logs",
     ],
   },
 ] as const;

 export type Tab =
   ...
   | "aiAgents"
+  | "fheKeys"
   | "debug"

 const TAB_PATHS: Record<Tab, string> = {
   ...
   aiAgents: "/ai-agents",
+  fheKeys: "/fhe-keys",
   debug: "/debug",
 };
```

## 4. Controller (`ui/src/ui/controllers/fhe-keys.ts`)

```ts
import type { GatewayBrowserClient } from "../gateway.ts";

export interface FheKeyEntryView {
  name: "skf" | "dictf" | "user_authorization";
  present: boolean;
  linked: boolean;
  sizeBytes: number;
  mtimeMs: number;
  storePath: string;
  linkTarget: string;
}

export interface FheKeysState {
  client: GatewayBrowserClient | null;
  fheKeysLoading: boolean;
  fheKeysStatus: { ready: boolean; entries: FheKeyEntryView[] } | null;
  fheKeysError: string | null;
}

export async function loadFheKeys(state: FheKeysState): Promise<void> {
  if (!state.client) return;
  state.fheKeysLoading = true;
  try {
    const res = await state.client.request<{ status: any }>("fhe.keys.status", {});
    state.fheKeysStatus = res.status;
    state.fheKeysError = null;
  } catch (err: any) {
    state.fheKeysError = err?.message ?? String(err);
  } finally {
    state.fheKeysLoading = false;
  }
}

export async function uploadFheKey(
  client: GatewayBrowserClient,
  name: FheKeyEntryView["name"],
  file: File,
): Promise<void> {
  const buf = new Uint8Array(await file.arrayBuffer());
  const dataBase64 = btoa(String.fromCharCode(...buf));
  await client.request("fhe.keys.upload", { name, dataBase64 });
}

export async function relinkFheKeys(client: GatewayBrowserClient) {
  await client.request("fhe.keys.link", {});
}

export async function removeFheKey(
  client: GatewayBrowserClient,
  name: FheKeyEntryView["name"],
) {
  await client.request("fhe.keys.remove", { name });
}
```

## 5. Refresh wiring (`ui/src/ui/app-settings.ts`)

Add to the `refreshActiveTab` switch:

```diff
       case "aiAgents":
         void loadConfigSchema(app).finally(() => host.requestUpdate?.());
         await loadConfig(app);
         break;
+      case "fheKeys":
+        await loadFheKeys(app);
+        break;
       case "overview":
```

And import:

```ts
import { loadFheKeys, type FheKeysState } from "./controllers/fhe-keys.ts";
```

Extend the `SettingsHost` / state interface (wherever it is defined) with
the four `fheKeys*` fields from the controller's `FheKeysState`.

## 6. Render (new view: `ui/src/ui/views/fhe-keys.ts`)

A minimal `lit-html` view; mirror `views/config.ts` for style helpers.

```ts
import { html, type TemplateResult } from "lit-html";
import type { FheKeysState, FheKeyEntryView } from "../controllers/fhe-keys.ts";
import { uploadFheKey, relinkFheKeys, removeFheKey } from "../controllers/fhe-keys.ts";

const KEY_LABELS: Record<FheKeyEntryView["name"], string> = {
  skf: "SKF private key",
  dictf: "Dictionary file (dictf)",
  user_authorization: "License (user_authorization)",
};

function rowStatus(e: FheKeyEntryView): { mark: string; text: string } {
  if (e.linked) return { mark: "✅", text: "linked" };
  if (e.present) return { mark: "⚠️", text: "uploaded, needs re-link" };
  return { mark: "—", text: "missing" };
}

export function renderFheKeys(
  state: FheKeysState,
  client: NonNullable<FheKeysState["client"]>,
  onChange: () => void,
): TemplateResult {
  const rows = state.fheKeysStatus?.entries ?? [];
  return html`
    <section class="settings-section">
      <h2>FHE Runtime Keys</h2>
      <p class="muted">
        ClawWorker's homomorphic-encryption skills need three secret files.
        Store them once and the runtime will keep them linked into the
        vendored Python packages.
      </p>
      <table class="settings-table">
        <thead>
          <tr><th>File</th><th>Status</th><th>Size</th><th>Modified</th><th></th></tr>
        </thead>
        <tbody>
          ${rows.map((e) => {
            const s = rowStatus(e);
            return html`
              <tr>
                <td>${KEY_LABELS[e.name]}</td>
                <td>${s.mark} ${s.text}</td>
                <td>${e.sizeBytes ? `${(e.sizeBytes / 1024).toFixed(1)} KB` : "—"}</td>
                <td>${e.mtimeMs ? new Date(e.mtimeMs).toLocaleString() : "—"}</td>
                <td>
                  <label class="btn">
                    Upload
                    <input type="file" hidden @change=${async (ev: Event) => {
                      const f = (ev.target as HTMLInputElement).files?.[0];
                      if (f) {
                        await uploadFheKey(client, e.name, f);
                        await relinkFheKeys(client);
                        onChange();
                      }
                    }} />
                  </label>
                  ${e.present
                    ? html`<button @click=${async () => {
                        await removeFheKey(client, e.name);
                        onChange();
                      }}>Remove</button>`
                    : null}
                </td>
              </tr>
            `;
          })}
        </tbody>
      </table>
      <div class="actions">
        <button @click=${async () => { await relinkFheKeys(client); onChange(); }}>
          Re-link all
        </button>
        <span class="status ${state.fheKeysStatus?.ready ? "ok" : "warn"}">
          ${state.fheKeysStatus?.ready ? "Ready" : "Not ready"}
        </span>
      </div>
    </section>
  `;
}
```

Mount it from `ui/src/ui/app-render.ts` at the appropriate tab branch
(similar to `case "config":` handling). Add an icon/label entry to the
navigation labels map.

## 7. i18n

`ui/src/i18n/locales/en.ts` adds a `tabs.fheKeys = "FHE Keys"` entry.
Then run `pnpm ui:i18n:sync` to regenerate the other locale bundles.

## 8. Tests to add

- `src/fhe-keys/index.test.ts` (already provided)
- `src/gateway/server-methods/fhe-keys.test.ts` — request handler smoke tests
- `ui/src/ui/controllers/fhe-keys.test.ts` — controller error paths

## 9. Order to land

1. Land RPC handlers + scope wiring (small PR, tests in repo).
2. Land navigation + controller + i18n stub (no-op tab visible).
3. Land view + render branch + tests.

Each step is independently testable. The CLI in `scripts/fhe-keys.mjs`
stays as the canonical CLI surface; the UI calls the same backend through
RPC.

## 10. Why we shipped the CLI first

The vendored runtime relies on dynamic library loading (ctypes / dylib
signatures), so the most critical bug surface is the install/link flow,
not the upload UI. Shipping the CLI and a `doctor` section first means:

- Power users have a complete management surface immediately.
- The UI tab can be added in a focused review without coupling to the
  vendor packaging changes.
- The doctor check is shared by both surfaces, so the "is FHE ready"
  signal stays consistent everywhere.
