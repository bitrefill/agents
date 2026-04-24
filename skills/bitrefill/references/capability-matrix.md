# Capability Matrix

Per-host cheat sheet. Each entry = viable paths in priority order + one-line reason. Pick the first that fits, fall back as needed.

Legend:

- **MCP** → [path-mcp.md](path-mcp.md)
- **CLI** → [path-cli.md](path-cli.md)
- **API** → [path-api.md](path-api.md)
- **Browse** → [path-browse.md](path-browse.md) (residential IP required)
- **OpenClaw** → [host-openclaw.md](host-openclaw.md)

## Anthropic

### Claude.ai web — Free

- No MCP custom URLs (Pro+ only). No shell. No residential browser.
- **Path**: none viable for purchases. For browse: only if user installs Claude-for-Chrome extension → Browse.
- **Fallback**: send user `bitrefill.com` link.

### Claude.ai web — Pro / Max / Team / Enterprise / Cowork

- MCP custom URLs allowed. Cowork adds desktop shell.
- **Paths**: MCP first → Browse via Claude-for-Chrome ext.
- Cowork only: + CLI via desktop shell.

### Claude Desktop

- MCP first-class (stdio + remote). No native shell, no native FS, no native HTTP — wire via MCP servers.
- **Paths**: MCP first → CLI via stdio MCP wrapping `npx @bitrefill/cli` → Browse via Chrome ext or Computer Use.

### Claude Code (CLI)

- Most flexible. Full host shell, MCP, WebFetch, Chrome ext.
- **Paths**: MCP first → CLI second → API via WebFetch / curl → Browse via Chrome ext or browser-use skill.
- Tighten: sandbox allowlist `api.bitrefill.com`, `registry.npmjs.org`. Deny `~/.ssh`, `.env`.

## OpenAI

### ChatGPT web — Free

- No custom MCP, no shell, datacenter browser → Cloudflare 403.
- **Path**: none. Send user `bitrefill.com` link.

### ChatGPT web — Plus / Pro / Business / Enterprise / Edu

- Custom MCP via Apps & Connectors (Developer Mode for write tools). Code Interpreter has no network.
- **Path**: MCP only. Browser is OpenAI datacenter — **do NOT route to Browse** (Cloudflare).

### ChatGPT Desktop

- Same as ChatGPT web. "Work with Apps" can read IDE/terminal panes but not execute.
- **Path**: MCP only.

### ChatGPT Atlas

- Built-in Chromium with **residential IP** (user's network). Inherits account connectors. No shell.
- **Paths**: Browse first (its superpower) → MCP via account connectors.

### ChatGPT Agent (formerly Operator)

- Sandboxed Linux + code interpreter. Hosted browser uses **OpenAI datacenter IP**.
- **Paths**: MCP via account connectors → CLI inside sandbox shell → API via curl. **Do NOT route to Browse** (Cloudflare).

### OpenAI Codex CLI

- Full host shell (Seatbelt/Landlock sandboxable). MCP stdio + HTTP. Profiles in `config.toml`.
- **Paths**: MCP first → CLI second → API via curl. Browser via MCP only.
- Tighten: `--sandbox workspace-write --ask-for-approval on-request`. API key in profile, not committed config.

## Google

### Gemini consumer — Free

- No MCP. No shell. No residential browser.
- **Path**: none. Send user `bitrefill.com` link.

### Gemini consumer — AI Pro / Ultra (US)

- "Auto Browse" runs from Google IPs → likely Cloudflare-blocked on bitrefill.com.
- **Path**: try Auto Browse + bitrefill.com URL; if blocked, send user the link.

### Gemini CLI

- Full host shell (sandboxable: Seatbelt / Docker / gVisor). MCP stdio + SSE + streamable-http.
- **Paths**: MCP first → CLI second → API via `web_fetch` or curl. Browser via MCP (Chrome DevTools / Playwright).

### Jules (async coding agent)

- Ephemeral Ubuntu VM, Google IPs, no MCP exposed to user, no residential browser.
- **Paths**: CLI inside VM → API via curl. **Not interactive** — best for batch tasks. No purchases recommended.

## Other

### Cursor IDE

- Built-in browser tool, terminal tool, MCP (40-tool cap across servers). Cloud Agents in isolated VM.
- **Paths**: MCP first → CLI in terminal → API via shell or built-in browser → Browse via built-in browser.
- Tighten: keep `buy-products` out of `autoApprove` in `.cursor/mcp.json`.

### OpenCode (sst/opencode)

- Full host shell. MCP stdio + HTTP. Permission model per agent (`allow`/`ask`/`deny`).
- **Paths**: MCP first → CLI second → API via `webfetch` or shell. Browser via MCP.

### OpenClaw — superset host

- Agentskills.io loader. MCP via `openclaw mcp set`. Full host shell + FS. `browser` tool uses host IP. Mobile nodes (camera, canvas, voice). Cron. Multi-channel chat (Telegram, WhatsApp, Slack, Discord, iMessage, Signal, Matrix, Teams, etc.).
- **Paths**: read [host-openclaw.md](host-openclaw.md) **first** for setup + safeguards. Then MCP → CLI → API → Browse as task requires.
- Default agent: **Pi** (Anthropic / OpenAI / Google compatible via API key).
- Unique scenarios: chat-channel purchase from phone, cron auto-renew top-ups, mobile camera OCR of receipts, multi-channel handoff.

## Quick decision

If user says "what host am I in?": run `command -v openclaw` and check `~/.openclaw/`. If `command -v claude` works = Claude Code. If `command -v codex` = Codex. Look at conversation context for IDE name. When in doubt: try MCP first (broadest support), fall back to CLI, then API.
