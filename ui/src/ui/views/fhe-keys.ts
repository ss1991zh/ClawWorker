import { html, nothing, type TemplateResult } from "lit";
import type { FheKeyEntryView, FheKeyName, FheKeysState } from "../controllers/fhe-keys.ts";

const KEY_LABELS: Record<FheKeyName, string> = {
  skf: "SKF 私钥 / SKF Private Key",
  dictf: "运算字典 / Dictionary",
  user_authorization: "授权许可 / Authorization",
};

const KEY_HINTS: Record<FheKeyName, string> = {
  skf: "FHE 加解密用的本地私钥。仅保存在你的设备上，不会上传。",
  dictf: "密文计算字典文件（通常 ~160 MB）。由 FHE 供应商提供。",
  user_authorization: "软件使用许可身份验证文件。由 FHE 供应商提供。",
};

function fmtBytes(n: number): string {
  if (!n) return "—";
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

function fmtDate(ms: number): string {
  if (!ms) return "—";
  try {
    return new Date(ms).toLocaleString();
  } catch {
    return "—";
  }
}

interface FheKeysHandlers {
  onUpload: (name: FheKeyName, file: File) => void;
  onRelink: () => void;
  onRemove: (name: FheKeyName) => void;
  onRefresh: () => void;
}

function renderRow(
  entry: FheKeyEntryView,
  state: FheKeysState,
  handlers: FheKeysHandlers,
): TemplateResult {
  const busy = state.fheKeysBusyKey === entry.name;
  const presentBadge = entry.present
    ? html`<span class="badge badge-ok">已上传</span>`
    : html`<span class="badge badge-pending">未上传</span>`;
  const linkedBadge = entry.linked
    ? html`<span class="badge badge-ok">已链接</span>`
    : entry.present
      ? html`<span class="badge badge-warn">未链接</span>`
      : html`<span class="badge badge-muted">—</span>`;

  return html`
    <tr>
      <td>
        <div class="fhe-key-name">${KEY_LABELS[entry.name]}</div>
        <div class="fhe-key-hint">${KEY_HINTS[entry.name]}</div>
        <code class="fhe-key-filename">${entry.name}</code>
      </td>
      <td>${presentBadge}</td>
      <td>${linkedBadge}</td>
      <td>${fmtBytes(entry.sizeBytes)}</td>
      <td>${fmtDate(entry.mtimeMs)}</td>
      <td class="fhe-key-actions">
        <label class="btn btn-primary ${busy ? "is-busy" : ""}">
          ${entry.present ? "替换" : "上传"}
          <input
            type="file"
            hidden
            ?disabled=${busy}
            @change=${(ev: Event) => {
              const inp = ev.target as HTMLInputElement;
              const f = inp.files?.[0];
              if (f) handlers.onUpload(entry.name, f);
              inp.value = "";
            }}
          />
        </label>
        ${entry.present
          ? html`<button
              class="btn btn-danger"
              ?disabled=${busy}
              @click=${() => handlers.onRemove(entry.name)}
            >
              移除
            </button>`
          : nothing}
      </td>
    </tr>
  `;
}

/**
 * Render the FHE Keys settings tab.
 *
 * @param state    UI state slice with status + loading/busy flags.
 * @param handlers Behavioral callbacks (upload / relink / remove / refresh).
 */
export function renderFheKeys(state: FheKeysState, handlers: FheKeysHandlers): TemplateResult {
  const status = state.fheKeysStatus;
  const rows = status?.entries ?? [];

  const summary = status
    ? status.ready
      ? html`<div class="fhe-status-banner fhe-status-ready">
          <strong>✅ 全部就绪</strong>
          &nbsp;FHE 运行时密钥已就位，密态计算技能可用。
        </div>`
      : html`<div class="fhe-status-banner fhe-status-warn">
          <strong>⚠️ 未完全就绪</strong>
          &nbsp;请补齐缺失的密钥后点击 <em>重新链接</em>。
        </div>`
    : state.fheKeysError
      ? html`<div class="fhe-status-banner fhe-status-error">
          <strong>读取失败</strong>: ${state.fheKeysError}
        </div>`
      : state.fheKeysLoading
        ? html`<div class="fhe-status-banner">正在读取密钥状态…</div>`
        : nothing;

  return html`
    <div class="fhe-keys-panel">
      <style>
        .fhe-keys-panel {
          padding: 16px 8px;
        }
        .fhe-keys-panel h2 {
          margin: 0 0 8px;
        }
        .fhe-keys-panel .lead {
          color: var(--text-secondary, #6b7280);
          margin: 0 0 16px;
          max-width: 760px;
        }
        .fhe-status-banner {
          margin: 12px 0 20px;
          padding: 10px 14px;
          border-radius: 8px;
          background: var(--surface-2, #f3f4f6);
          border: 1px solid var(--border, #e5e7eb);
        }
        .fhe-status-banner.fhe-status-ready {
          background: #ecfdf5;
          border-color: #34d399;
        }
        .fhe-status-banner.fhe-status-warn {
          background: #fffbeb;
          border-color: #f59e0b;
        }
        .fhe-status-banner.fhe-status-error {
          background: #fef2f2;
          border-color: #ef4444;
        }
        .fhe-keys-table {
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 16px;
        }
        .fhe-keys-table th,
        .fhe-keys-table td {
          padding: 12px 10px;
          text-align: left;
          border-bottom: 1px solid var(--border, #e5e7eb);
          vertical-align: top;
        }
        .fhe-keys-table th {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: var(--text-secondary, #6b7280);
        }
        .fhe-key-name {
          font-weight: 600;
        }
        .fhe-key-hint {
          font-size: 12px;
          color: var(--text-secondary, #6b7280);
          margin-top: 2px;
          max-width: 460px;
        }
        .fhe-key-filename {
          display: inline-block;
          margin-top: 4px;
          padding: 1px 6px;
          font-size: 11px;
          background: var(--surface-2, #f3f4f6);
          border-radius: 4px;
        }
        .fhe-key-actions {
          white-space: nowrap;
        }
        .fhe-key-actions .btn {
          margin-right: 6px;
        }
        .badge {
          display: inline-block;
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 500;
        }
        .badge-ok {
          background: #d1fae5;
          color: #065f46;
        }
        .badge-warn {
          background: #fef3c7;
          color: #92400e;
        }
        .badge-pending {
          background: #fee2e2;
          color: #991b1b;
        }
        .badge-muted {
          background: var(--surface-2, #f3f4f6);
          color: var(--text-secondary, #6b7280);
        }
        .fhe-paths {
          margin-top: 18px;
          font-size: 12px;
          color: var(--text-secondary, #6b7280);
        }
        .fhe-paths code {
          background: var(--surface-2, #f3f4f6);
          padding: 1px 6px;
          border-radius: 4px;
        }
        .fhe-bottom-actions {
          margin-top: 14px;
          display: flex;
          gap: 8px;
        }
        .btn {
          cursor: pointer;
          padding: 6px 12px;
          border-radius: 6px;
          border: 1px solid var(--border, #d1d5db);
          background: white;
          font-size: 13px;
        }
        .btn:hover {
          background: var(--surface-2, #f9fafb);
        }
        .btn-primary {
          background: #2563eb;
          color: white;
          border-color: #2563eb;
        }
        .btn-primary:hover {
          background: #1d4ed8;
        }
        .btn-danger {
          color: #991b1b;
          border-color: #fecaca;
        }
        .btn-danger:hover {
          background: #fef2f2;
        }
        .btn.is-busy {
          opacity: 0.6;
          pointer-events: none;
        }
      </style>

      <h2>🦞 FHE 密钥管理 / FHE Keys</h2>
      <p class="lead">
        ClawWorker 的密态计算技能（HENumpy / PandaSeal / HELearn / HETorch）需要三份用户私有文件。
        在这里上传一次，系统会自动把它们链接进 vendor 运行时，所有 FHE 技能立即可用。 密钥文件
        <strong>只保存在你的本地设备</strong>，不会上传到任何远程服务。
      </p>

      ${summary}

      <table class="fhe-keys-table">
        <thead>
          <tr>
            <th>密钥</th>
            <th>已上传</th>
            <th>已链接</th>
            <th>大小</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          ${rows.length > 0
            ? rows.map((e) => renderRow(e, state, handlers))
            : html`<tr>
                <td colspan="6" style="text-align: center; padding: 24px;">
                  ${state.fheKeysLoading ? "加载中…" : "暂无数据"}
                </td>
              </tr>`}
        </tbody>
      </table>

      <div class="fhe-bottom-actions">
        <button class="btn" @click=${handlers.onRelink} ?disabled=${state.fheKeysLoading}>
          🔗 重新链接全部
        </button>
        <button class="btn" @click=${handlers.onRefresh} ?disabled=${state.fheKeysLoading}>
          🔄 刷新状态
        </button>
      </div>

      ${status
        ? html`<div class="fhe-paths">
            <div>密钥存储目录：<code>${status.storeDir}</code></div>
            <div>FHE 运行时目录：<code>${status.runtimeDir}</code></div>
          </div>`
        : nothing}
    </div>
  `;
}
