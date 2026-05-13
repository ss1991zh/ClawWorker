#!/usr/bin/env node
// scripts/fhe-agent.mjs
//
// FHE chat agent — minimal demonstration that bundled FHE skills are
// invocable end-to-end:
//
//   1. Load zfhe-skill SKILL.md (the meta-orchestrator) as system context.
//   2. Hand the user's natural-language query to Claude.
//   3. Extract the Python code block Claude generates.
//   4. Execute it inside the .venv-fhe virtualenv that has the vendored
//      FHE runtime installed.
//   5. Print the decrypted output.
//
// This is the same pipeline that the full ClawWorker chat surface will
// drive — it isolates the agent <-> skill <-> Python-runtime contract so
// you can verify each piece without spinning up the whole gateway.
//
// Usage:
//   node scripts/fhe-agent.mjs "加密 [1,2,3,4,5] 和 [10,20,30,40,50]，然后求点积"
//   node scripts/fhe-agent.mjs --show-code "..."        # print code without running
//   node scripts/fhe-agent.mjs --model sonnet "..."     # explicit model
//
// Env:
//   ANTHROPIC_API_KEY     required
//   ANTHROPIC_BASE_URL    optional (default https://api.anthropic.com)
//   FHE_AGENT_MODEL       optional override (default claude-sonnet-4-5)
//   FHE_AGENT_VENV        optional, defaults to <repo>/.venv-fhe

import { promises as fs } from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(SCRIPT_DIR, "..");
const SKILL_ROOT = path.join(REPO_ROOT, "skills");
const VENV = process.env.FHE_AGENT_VENV || path.join(REPO_ROOT, ".venv-fhe");
const PYTHON = path.join(VENV, "bin", "python");

const ANTHROPIC_BASE = (process.env.ANTHROPIC_BASE_URL || "https://api.anthropic.com").replace(/\/+$/, "");
const API_KEY = process.env.ANTHROPIC_API_KEY;
const MODEL = process.env.FHE_AGENT_MODEL || "claude-sonnet-4-5";

const args = process.argv.slice(2);
let showCodeOnly = false;
let explicitModel = null;
const queryParts = [];
for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--show-code") showCodeOnly = true;
    else if (a === "--model") explicitModel = args[++i];
    else if (a === "-h" || a === "--help") {
        console.log("Usage: node scripts/fhe-agent.mjs [--show-code] [--model NAME] <query>");
        process.exit(0);
    } else queryParts.push(a);
}
const userQuery = queryParts.join(" ").trim();

if (!API_KEY) {
    console.error("ERROR: ANTHROPIC_API_KEY is not set in the environment.");
    process.exit(2);
}
if (!userQuery) {
    console.error("ERROR: missing query. Try:");
    console.error('  node scripts/fhe-agent.mjs "加密 [1,2,3] 和 [4,5,6] 然后做点积"');
    process.exit(2);
}

// ---------------------------------------------------------------------------
// Load skill context. We pull zfhe-skill (the router) and inline its SKILL.md
// plus the helper docs it references. This is the same content the Agent
// reads under OpenClaw at runtime.
// ---------------------------------------------------------------------------

async function readSkillFile(skill, relpath) {
    const full = path.join(SKILL_ROOT, skill, relpath);
    try {
        return await fs.readFile(full, "utf8");
    } catch {
        return null;
    }
}

async function buildSkillContext() {
    const parts = [];
    const zfheMain = await readSkillFile("zfhe-skill", "SKILL.md");
    if (zfheMain) parts.push(`# skills/zfhe-skill/SKILL.md\n\n${zfheMain}`);

    const docsToLoad = [
        ["zfhe-skill", "docs/routing.md"],
        ["zfhe-skill", "docs/initialization.md"],
        ["zfhe-skill", "docs/error-handling.md"],
        ["henumpy-skill", "SKILL.md"],
        ["henumpy-skill", "INDEX.md"],
        ["henumpy-skill", "constraints.md"],
    ];
    for (const [skill, rel] of docsToLoad) {
        const text = await readSkillFile(skill, rel);
        if (text) parts.push(`# skills/${skill}/${rel}\n\n${text}`);
    }
    return parts.join("\n\n---\n\n");
}

const SYSTEM_PROMPT = `你是 ClawWorker 内嵌的 FHE 数据分析助手。

当用户请求加密数据上的计算时，你必须：
1. 阅读下方 zfhe-skill 提供的指引和路由表，找到正确的子 skill
2. 生成一段**完整可运行**的 Python 代码，使用 henumpy/crypto_toolkit 等 vendored 包
3. 代码必须以 \`\`\`python 开头、\`\`\` 结尾包裹
4. 代码顶部必须调用 \`hp.initDict()\` 和 \`ct.initSK()\` 完成初始化
5. 代码末尾必须 \`print()\` 解密后的明文结果，方便调用方验证
6. 不需要 try/except 包裹关键路径——错误直接抛出便于调试
7. 不要写解释文字之外的多余示例代码块，只输出一段最终代码

下面是 skill 内容（不要在回复里复读它）：

${"="}{"=".repeat(70)}

`;

// ---------------------------------------------------------------------------
// Anthropic Messages API call
// ---------------------------------------------------------------------------

async function callClaude(systemPrompt, userMessage, model) {
    const url = `${ANTHROPIC_BASE}/v1/messages`;
    const body = {
        model,
        max_tokens: 2048,
        system: systemPrompt,
        messages: [{ role: "user", content: userMessage }],
    };
    const resp = await fetch(url, {
        method: "POST",
        headers: {
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        body: JSON.stringify(body),
    });
    if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`Anthropic API ${resp.status}: ${text}`);
    }
    const json = await resp.json();
    const blocks = Array.isArray(json.content) ? json.content : [];
    return blocks.map((b) => (typeof b.text === "string" ? b.text : "")).join("");
}

function extractPython(text) {
    const fence = /```(?:python|py)\s*\n([\s\S]*?)```/i;
    const m = fence.exec(text);
    return m ? m[1].trim() : null;
}

// ---------------------------------------------------------------------------
// Python execution in the venv
// ---------------------------------------------------------------------------

function runPython(code) {
    return new Promise((resolve, reject) => {
        const child = spawn(PYTHON, ["-c", code], {
            stdio: ["ignore", "pipe", "pipe"],
            env: { ...process.env, PYTHONUNBUFFERED: "1" },
        });
        let stdout = "";
        let stderr = "";
        child.stdout.on("data", (chunk) => {
            const s = chunk.toString();
            stdout += s;
            process.stdout.write(s);
        });
        child.stderr.on("data", (chunk) => {
            stderr += chunk.toString();
        });
        child.on("error", reject);
        child.on("exit", (code) => resolve({ code, stdout, stderr }));
    });
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const banner = (s) => console.log(`\n${"─".repeat(60)}\n${s}\n${"─".repeat(60)}`);

banner("1. Loading skill context");
const skillCtx = await buildSkillContext();
console.log(`  skill context: ${skillCtx.length.toLocaleString()} chars`);

banner("2. User query");
console.log(`  ${userQuery}`);

banner(`3. Asking ${explicitModel || MODEL} to plan + generate code`);
const reply = await callClaude(SYSTEM_PROMPT + skillCtx, userQuery, explicitModel || MODEL);
const code = extractPython(reply);

if (!code) {
    console.error("\nERROR: model reply contained no ```python block.\nFull reply was:\n");
    console.error(reply);
    process.exit(3);
}

banner("4. Generated Python");
console.log(code);

if (showCodeOnly) process.exit(0);

banner("5. Executing in .venv-fhe");
const t0 = Date.now();
const { code: rc, stderr } = await runPython(code);
const elapsed = ((Date.now() - t0) / 1000).toFixed(2);

banner(`6. Result  (exit ${rc}, ${elapsed}s)`);
if (rc !== 0) {
    console.error("STDERR:");
    console.error(stderr);
    process.exit(rc ?? 1);
}
console.log("  ✅ Skill invocation succeeded end-to-end.");
