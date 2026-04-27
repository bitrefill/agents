# Host: OpenClaw

[OpenClaw](https://docs.openclaw.ai/) is a self-hosted Gateway that bridges chat apps (Telegram, WhatsApp, Slack, Discord, iMessage, Signal, Matrix, Teams, etc.) to coding agents like **Pi**. It is a **superset host**: full host shell, agentskills.io-compatible skill loader, first-class MCP, mobile-node camera/canvas, cron, and multi-channel routing.

This file explains how to install + harden the Bitrefill skill inside OpenClaw and lists scenarios no other host can do. After setup, use the regular path files for the actual workflow.

## 1. Detect OpenClaw

Check **any** of:

- File: `~/.openclaw/openclaw.json` exists.
- Dir: `~/.openclaw/skills/` exists.
- Binary: `command -v openclaw` succeeds.
- Tools in agent loop: `gateway`, `cron`, `nodes`, `canvas`, `sessions_*` (OpenClaw-only).

If yes → continue here. Otherwise → return to [SKILL.md](../SKILL.md) and pick a path.

## 2. Install this skill

Loader paths (increasing precedence): `skills.load.extraDirs` → bundled → `~/.openclaw/skills/` → `~/.agents/skills/` → `<workspace>/.agents/skills/` → `<workspace>/skills/`.

Manual:

```bash
cp -r path/to/bitrefill ~/.openclaw/skills/bitrefill
openclaw skills list   # verify
openclaw gateway restart   # or /new in chat
```

ClawHub (if/when published):

```bash
openclaw skills install bitrefill
openclaw skills update --all
```

Skill is **agentskills.io-compatible** — no rewriting needed. Source: <https://docs.openclaw.ai/tools/skills.md>.

## 3. Install Bitrefill MCP (preferred path)

CLI:

```bash
openclaw mcp set bitrefill --url "https://api.bitrefill.com/mcp/$BITREFILL_API_KEY"
```

Or hand-edit `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "bitrefill": {
        "url": "https://api.bitrefill.com/mcp",
        "headers": { "Authorization": "Bearer ${BITREFILL_API_KEY}" }
      }
    }
  }
}
```

Transport: SSE/HTTP (default for URL entries) or `transport: "streamable-http"`. The 7 Bitrefill MCP tools surface as ordinary Pi tool calls. Restrict per-agent via `agents.list[].tools.allow`/`deny` if running multi-agent. Source: <https://docs.openclaw.ai/cli/mcp.md>.

Then: see [mcp.md](mcp.md) for tool workflow.

## 4. Install Bitrefill CLI (fallback)

Pi has first-class `exec` tool running on the Gateway host (sandboxing **off** by default).

```bash
exec: npm install -g @bitrefill/cli
```

If Gateway runs in Docker sandbox: declare `setupCommand: "npm install -g @bitrefill/cli"` and ensure `network` is not `none`. Source: <https://docs.openclaw.ai/gateway/sandboxing.md>.

Then: see [cli.md](cli.md).

## 5. Raw API path

`exec` + `curl`, or built-in `web_fetch` tool. No special config. See [api.md](api.md).

## 6. Browser

Pi has `browser` tool. **It uses the Gateway host's IP** — usually residential when Gateway runs on user's machine, but a VPS will hit Cloudflare 403. For richer DOM control attach a Playwright/Chrome MCP. The Mac menubar app drives user's actual Chrome and is fully residential. See [browse.md](browse.md).

## 7. OpenClaw-only scenarios

These are the differentiators. None of the other hosts can do them.

### Buy a gift card from Telegram (away from desk)

User DMs the bot: "buy a $50 Steam US card for me". Pi routes to Bitrefill MCP, prompts confirmation in chat, pays from `balance`, returns redemption code.

**Risk**: redemption codes are cash-like. Never deliver to group chats or via `MEDIA:` URLs. Lock down channel:

```jsonc
{
  "channels": {
    "telegram": {
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "dmPolicy": "pairing",
      "allowFrom": ["123456789"],
      "groups": { "*": { "requireMention": true } }
    }
  }
}
```

Source: <https://docs.openclaw.ai/channels/telegram>.

### Auto-renew mobile top-up monthly

Use `cron` tool to schedule `buy-products` for a fixed phone-top-up SKU on the 1st of each month, paying from `balance`. Heartbeat (default 30 min) polls `get-invoice-by-id` until `complete` then pings the user.

### Multi-channel handoff

Trigger purchase from Slack, deliver redemption code only to user's private Signal DM. Same Gateway, isolated session per channel/sender.

### Mobile camera context

Paired iOS/Android node exposes `camera.snap` and `canvas.*`. User photographs a recipient's request ("100 EUR Decathlon France"), Pi OCRs/parses, runs `search-products` + `buy-products`. Source: <https://docs.openclaw.ai/nodes/index.md>.

### Heartbeat-driven invoice polling

Default 30-min heartbeat or custom `cron` polls `get-invoice-by-id` until `status: complete`, then pushes redemption code to originating channel.

## 8. OpenClaw-specific safeguards

OpenClaw defaults are permissive: sandboxing off, `security: full`, `ask: off`. **Tighten before letting an agent buy on your behalf.**

- **Restrict who triggers purchases**: `channels.<ch>.allowFrom: ["<your_id>"]` + `dmPolicy: "pairing"`. Same for WhatsApp, Signal, Slack, Discord.
- **Require approval for buys**: `~/.openclaw/exec-approvals.json` with `security: allowlist` + `ask: on-miss`. Allowlist `bitrefill *` for read tools; force `/approve` for `bitrefill buy-products` and the MCP `buy-products` call.
- **Isolate Bitrefill agent**: under `agents.list[]` declare a Bitrefill-scoped persona with `tools.deny: ["gateway"]` so the agent **cannot rewrite Gateway config** to bypass approvals. Source: <https://docs.openclaw.ai/tools/exec-approvals.md>.
- **Pre-fund only `balance`** with low cap. **Never** give the agent crypto wallet seeds. Skill is not a wallet.
- **No voice readback of codes**: disable `audio_as_voice` / TTS for the Bitrefill agent. Pi's media pipeline could otherwise speak a cash-like code aloud over Telegram voice notes.
- **No `MEDIA:<url>` for redemption codes**: enforce text-only delivery for the redemption tool output.

## Source of truth

- OpenClaw docs: <https://docs.openclaw.ai/>
- Skills loader: <https://docs.openclaw.ai/tools/skills.md>
- Creating skills: <https://docs.openclaw.ai/tools/creating-skills.md>
- MCP CLI: <https://docs.openclaw.ai/cli/mcp.md>
- Exec tool: <https://docs.openclaw.ai/tools/exec.md>
- Sandboxing: <https://docs.openclaw.ai/gateway/sandboxing.md>
- Exec approvals: <https://docs.openclaw.ai/tools/exec-approvals.md>
- Nodes: <https://docs.openclaw.ai/nodes/index.md>
- Channels: <https://docs.openclaw.ai/channels/telegram>
- Bitrefill skill paths: [mcp.md](mcp.md), [cli.md](cli.md), [api.md](api.md), [browse.md](browse.md), [safeguards.md](safeguards.md)
