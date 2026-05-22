# Host: OpenClaw

[OpenClaw](https://docs.openclaw.ai/) is a self-hosted Gateway that bridges chat apps (Telegram, WhatsApp, Slack, Discord, iMessage, Signal, Matrix, Teams, etc.) to coding agents like **Pi**. It is a **superset host**: full host shell, agentskills.io-compatible skill loader, first-class MCP, mobile-node camera/canvas, cron, and multi-channel routing.

This file explains how to install + harden the Bitrefill skill inside OpenClaw and lists scenarios no other host can do. After setup, use the regular path files for the actual workflow.

**OpenClaw path priority:** **guest CLI via `exec`** (no auth, fastest try) → signed-in CLI (`login`/`verify`, `balance`, cashback) → MCP → API → Browse. OpenClaw has shell + MCP — prefer guest CLI for purchases unless you need typed MCP tool calls or are already signed in for `balance`.

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

## 3. Install Bitrefill CLI (preferred — guest checkout)

Pi has first-class `exec` tool on Gateway host (sandboxing **off** by default). **Start here:** no login, no MCP config — search, buy, pay crypto or send payment link.

```bash
exec: npm install -g @bitrefill/cli
exec: bitrefill search-products --query "Netflix" --country US
exec: bitrefill buy-products \
  --cart_items '[{"product_id":"steam-usa","package_id":10}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "user@example.com"
```

Guest flow → [cli.md](cli.md) § Guest checkout. Optional: `bitrefill init --openclaw` (skill + MCP stub only — not required for guest).

**Upgrade to signed-in** when human wants store-credit cap (`balance`), cashback, or order history:

```bash
exec: bitrefill login --email you@example.com
exec: bitrefill verify --code <email-code> [--otp <totp>]
```

Headless sign-in inbox → [cli-headless-auth.md](cli-headless-auth.md) (AgentMail or equivalent).

Docker sandbox: `setupCommand: "npm install -g @bitrefill/cli"`, `network` not `none`. Source: <https://docs.openclaw.ai/gateway/sandboxing.md>.

## 4. Install Bitrefill MCP (optional)

Use when: typed MCP tool calls in Pi loop without shell, or MCP-native integrations. **Not required for guest try** — guest CLI is faster (zero config).

```bash
openclaw mcp set bitrefill --url "https://api.bitrefill.com/mcp"
```

Or hand-edit `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "bitrefill": {
        "url": "https://api.bitrefill.com/mcp"
      }
    }
  }
}
```

Developer API key (optional): see [mcp.md](mcp.md). Guest MCP checkout may still need OAuth; **guest CLI avoids this.**

Transport: SSE/HTTP or `transport: "streamable-http"`. Restrict per-agent via `agents.list[].tools.allow`/`deny`. Source: <https://docs.openclaw.ai/cli/mcp.md>.

Then: see [mcp.md](mcp.md).

## 5. Raw API path

`exec` + `curl`, or built-in `web_fetch` tool. No special config. See [api.md](api.md).

## 6. Browser

Pi has `browser` tool. **It uses the Gateway host's IP** — usually residential when Gateway runs on user's machine, but a VPS will hit Cloudflare 403. For richer DOM control attach a Playwright/Chrome MCP. The Mac menubar app drives user's actual Chrome and is fully residential. See [browse.md](browse.md).

## 7. OpenClaw-only scenarios

These are the differentiators. None of the other hosts can do them.

### Buy a gift card from Telegram (away from desk)

User DMs the bot: "buy a $50 Steam US card for me". Pi runs guest CLI via `exec` (or signed-in CLI with `balance` if human pre-funded account), prompts confirmation in chat, returns payment link or redemption code after poll.

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

Use `cron` + `exec: bitrefill buy-products ...` for fixed SKU. Guest: crypto + poll `get-invoice-by-id`. Signed-in: `--payment_method balance` for instant pay without on-chain wait.

### Multi-channel handoff

Trigger purchase from Slack, deliver redemption code only to user's private Signal DM. Same Gateway, isolated session per channel/sender.

### Mobile camera context

Paired iOS/Android node exposes `camera.snap` and `canvas.*`. User photographs a request ("100 EUR Decathlon France"), Pi OCRs/parses, runs `exec: bitrefill search-products` + `exec: bitrefill buy-products` (guest or signed-in). Source: <https://docs.openclaw.ai/nodes/index.md>.

### Heartbeat-driven invoice polling

Default 30-min heartbeat or custom `cron` runs `exec: bitrefill get-invoice-by-id` until `status: complete`, then pushes redemption code to originating channel.

## 8. OpenClaw-specific safeguards

OpenClaw defaults are permissive: sandboxing off, `security: full`, `ask: off`. **Tighten before letting an agent buy on your behalf.**

- **Restrict who triggers purchases**: `channels.<ch>.allowFrom: ["<your_id>"]` + `dmPolicy: "pairing"`. Same for WhatsApp, Signal, Slack, Discord.
- **Require approval for buys**: `~/.openclaw/exec-approvals.json` with `security: allowlist` + `ask: on-miss`. Allowlist read-only CLI (`bitrefill search-products`, `bitrefill get-product-details`, `bitrefill get-invoice-by-id`); force `/approve` for `bitrefill buy-products`. Same pattern if using MCP `buy-products`.
- **Isolate Bitrefill agent**: under `agents.list[]` declare a Bitrefill-scoped persona with `tools.deny: ["gateway"]` so the agent **cannot rewrite Gateway config** to bypass approvals. Source: <https://docs.openclaw.ai/tools/exec-approvals.md>.
- **Guest first, balance when ready**: guest CLI + payment link = lowest friction; human pre-funds account + `login`/`verify` when agent needs capped `balance` spend. **Never** give the agent crypto wallet seeds. Skill is not a wallet.
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
