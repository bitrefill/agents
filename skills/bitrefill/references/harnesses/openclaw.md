# Host: OpenClaw

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

[OpenClaw](https://docs.openclaw.ai/) — self-hosted Gateway bridging chat apps (Telegram, WhatsApp, Slack, Discord, iMessage, Signal, Matrix, Teams, …) to coding agents like **Pi**. **Superset host:** full shell, agentskills.io skill loader, MCP, mobile-node camera/canvas, cron, multi-channel routing.

Install + harden Bitrefill skill here; path files for workflow.

**Priority:** **guest CLI via `exec`** (no auth, fastest) → MCP reads → authorized REST two-step balance when available → API → Browse. Sign-in may supply account identity, but never makes CLI/MCP auto-pay safe.

## 1. Detect OpenClaw

Any of:

- `~/.openclaw/openclaw.json` exists
- `~/.openclaw/skills/` exists
- `command -v openclaw` succeeds
- Tools: `gateway`, `cron`, `nodes`, `canvas`, `sessions_*` (OpenClaw-only)

Yes → continue. Else → [SKILL.md](../../SKILL.md) + [decision-engine.md](decision-engine.md).

## 2. Install skill

Same-name precedence, highest first: `<workspace>/skills` → `<workspace>/.agents/skills` → `~/.agents/skills` → `~/.openclaw/skills` → bundled → plugin/`skills.load.extraDirs`. Any higher copy can shadow this complete skill.

Manual/current local source:

```bash
openclaw skills install ./path/to/bitrefill --as bitrefill --global
openclaw skills check --agent <agent_id>
openclaw skills info bitrefill --agent <agent_id> --json
openclaw gateway restart   # or /new in chat
```

Never overlay an existing same-named directory: stop and have the operator inspect every higher-precedence root first. `skills check` proves eligibility, not the resolved path. Verify `skills info` reports the expected `filePath`/`baseDir`, then inspect that resolved `SKILL.md` plus its budget and safeguards references. If source, version, path, or content cannot be proved, disable purchase tools until the stale copy is removed or replaced. Do not install the bare ClawHub slug `bitrefill`; it is not an owner-qualified Bitrefill release.

**agentskills.io-compatible** — no rewrite. Source: <https://docs.openclaw.ai/tools/skills.md>.

## 3. Install Bitrefill CLI (preferred — guest checkout)

Pi has `exec` on Gateway host (sandboxing **off** default). **Start here:** no login, no MCP — search, buy, pay crypto or payment link.

Before any `buy-products` command, establish a current-session budget and apply [budget-guard.md](../budget-guard.md). The guest example may create one non-paying invoice after a coarse budget check; withhold its payment link/details until its exact components are confirmed and reserved. Do not use this command for balance/cashback auto-pay.

```bash
exec: npm install -g @bitrefill/cli
exec: bitrefill search-products --query "Netflix" --country US
exec: bitrefill buy-products \
  --cart_items '[{"product_id":"steam-usa","package_id":10}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "user@example.com"
```

Guest flow → [../touchpoints/cli.md](../touchpoints/cli.md) § Guest checkout. Avoid `bitrefill init --openclaw` for skill installation: its generated high-priority copy may shadow the complete current skill. Configure MCP alone or install and validate the complete skill manually.

**Upgrade signed-in** when the human needs account identity, order history, or rewards/balance visibility:

```bash
exec: bitrefill login --email you@example.com
exec: bitrefill verify --code <email-code> [--otp <totp>]
```

Signing in does not make CLI/MCP balance auto-pay safe. Guarded balance checkout also needs direct authorized REST access for `auto_pay: false` invoice creation and later payment; otherwise use a non-balance route. Keep `cashback` blocked until its exact debit semantics are authoritative.

Headless inbox → [../touchpoints/cli-headless-auth.md](../touchpoints/cli-headless-auth.md).

Docker sandbox: `setupCommand: "npm install -g @bitrefill/cli"`, `network` not `none`. Source: <https://docs.openclaw.ai/gateway/sandboxing.md>.

## 4. Install Bitrefill MCP (optional)

Use MCP for typed search, detail, and status calls. Keep purchase-capable MCP tools filtered out because host exec approvals do not cover direct MCP calls; purchases use the approval-gated CLI below.

```bash
openclaw mcp add bitrefill \
  --url https://api.bitrefill.com/mcp \
  --transport streamable-http \
  --auth oauth \
  --include 'search-products,get-product-details,list-invoices,get-invoice-by-id'
openclaw mcp login bitrefill
openclaw mcp doctor bitrefill --probe
```

Or edit `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "bitrefill": {
        "url": "https://api.bitrefill.com/mcp",
        "transport": "streamable-http",
        "auth": "oauth",
        "toolFilter": {
          "include": ["search-products", "get-product-details", "list-invoices", "get-invoice-by-id"]
        }
      }
    }
  }
}
```

Capability-probe `openclaw mcp --help` first. The CLI setup requires `add`, `login`, and `doctor`; older builds such as 2026.5.22 may lack them. On those builds use the JSON definition, restart the Gateway, and keep MCP disabled unless OAuth plus the exact probed read-only tool catalog can be verified. Developer API key (optional): [../touchpoints/mcp.md](../touchpoints/mcp.md). Do not embed credentials in persisted URLs; OAuth is preferred. Guest CLI avoids MCP auth entirely.

Transport: SSE/HTTP or `transport: "streamable-http"`. Restrict per-agent via `agents.list[].tools.allow`/`deny`. Source: <https://docs.openclaw.ai/cli/mcp.md>.

Then → [../touchpoints/mcp.md](../touchpoints/mcp.md).

## 5. Raw API path

`web_fetch` is GET-only and may be used for public reads. Route every authenticated create/pay POST through approval-gated `exec` with a pinned `curl` binary or reviewed wrapper. → [../touchpoints/api.md](../touchpoints/api.md).

## 6. Browser

Pi `browser` tool uses **Gateway host IP** — residential on user machine; VPS → Cloudflare 403. Playwright/Chrome MCP for DOM. Mac menubar app = user's Chrome, fully residential. → [../touchpoints/browse.md](../touchpoints/browse.md).

## 7. OpenClaw-only scenarios

Differentiators — no other host can do these.

### Buy gift card from Telegram (away from desk)

User DMs: "buy $50 Steam US". Pi runs guest CLI via approval-gated `exec`, or the authorized REST two-step balance route when available, confirms in chat, and returns a payment link or code after polling.

**Risk:** codes = cash. Never deliver to groups or `MEDIA:` URLs. Lock channel:

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

### Monthly mobile top-up reminder

`cron` may search, quote, and notify for a fixed SKU. It must not create or pay an invoice.

Create the job with `--session isolated`. Every scheduled execution treats any visible prior state as carrying no budget or purchase authority. It only quotes; the operator continues in a live session, explicitly sets that session's budget, confirms the current exact product and total, completes the reservation, and approves the CLI purchase. A recurring purchase needs a separate bounded recurring-authorization design; this session guard does not provide one.

### Multi-channel handoff

First set `openclaw config set session.dmScope per-channel-peer`; OpenClaw otherwise may share DMs through the main session. Trigger from Slack and deliver to a private Signal DM only through an explicitly reviewed `identityLinks` mapping for that same operator. Never link unrelated peers or let budgets/codes cross identities implicitly.

### Mobile camera context

Paired iOS/Android node: `camera.snap`, `canvas.*`. User photos request ("100 EUR Decathlon France"), Pi OCRs, then searches and buys only after the same explicit session cap, exact-total reservation, and operator approval gate as every other flow. Source: <https://docs.openclaw.ai/nodes/index.md>.

### Heartbeat invoice polling

Default heartbeat or custom `cron` may run read-only `get-invoice-by-id`. Deduplicate unchanged polls; notify the originating operator only on a new relevant transition, blocker, or final delivery. It never mutates a session ledger or authorizes a retry; the live session reconciles per [budget-guard.md](../budget-guard.md), and missing session state remains blocked. Delivery failure never releases payment. Push each code only when the invoice is `complete`, that target order is `delivered`, and `redemption_available` plus its redemption payload are present; handle failed/refunded orders separately and keep delivery private.

## 8. OpenClaw safeguards

Defaults permissive: sandboxing off, `security: full`, `ask: off`. **Tighten before agent buys.**

- **Restrict triggers:** `channels.<ch>.allowFrom: ["<your_id>"]` + `dmPolicy: "pairing"`. All channels.
- **Isolate DMs:** set `session.dmScope: "per-channel-peer"`; add `identityLinks` only for explicitly reviewed same-operator cross-channel handoff.
- **Separate reads from buys:** allowlist only `search-products`, `get-product-details`, `list-invoices`, and `get-invoice-by-id` on the Bitrefill MCP server; verify the probed catalog contains no other tools. Exec approvals apply only to host commands, never direct MCP calls.
- **Approval for CLI/API buys:** choose the actual execution host. Set requested `tools.exec.mode: ask`, then apply `security: allowlist`, `ask: always`, `askFallback: deny`, and `autoAllowSkills: false` to that exact Gateway (`openclaw approvals set --gateway --stdin`) or node (`--node <id>`). Allowlist only the resolved absolute Bitrefill CLI and, when needed, `curl` binary paths. Verify with `openclaw approvals get --gateway` or `--node <id>`, inspect `/exec` in the purchasing session for overrides, and set `/exec ask=always`; never allow `security=full`. Every host command then needs operator approval; MCP handles reads without that prompt.
- **Session budget before buys:** apply [budget-guard.md](../budget-guard.md) for every chat and mobile flow. Cron is quote-only. New or isolated sessions never inherit a prior cap.
- **Isolate Bitrefill agent:** `agents.list[]` persona with `tools.deny: ["gateway"]` — can't rewrite Gateway config. Source: <https://docs.openclaw.ai/tools/exec-approvals.md>.
- **Guest first:** guest CLI can create a non-paying invoice; reserve before exposing its payment instrument. Balance additionally needs the authorized REST two-step flow above. **Never** give agent crypto seeds. Skill not a wallet.
- **No voice readback:** disable `audio_as_voice` / TTS for Bitrefill agent.
- **No `MEDIA:<url>` for codes:** text-only delivery.

Do not use `openclaw approvals set` with a partial document: it replaces the complete approvals file. In Control UI → Nodes → Exec approvals, select the actual Gateway or node and the `bitrefill` agent, then set `security: allowlist`, `ask: always`, `askFallback: deny`, `autoAllowSkills: false`, and save. Add only resolved absolute binaries without replacing other agents' policy:

```bash
openclaw config set tools.exec.host gateway
openclaw config set tools.exec.mode ask
openclaw approvals allowlist add --agent bitrefill --gateway /absolute/reviewed/path/to/bitrefill
openclaw approvals allowlist add --agent bitrefill --gateway /absolute/reviewed/path/to/curl
openclaw approvals get --gateway
```

For node execution, use `--node <id>` for both allowlist and verification and select that same node in Control UI.

Also inspect `/exec` in the live purchasing chat and set `/exec ask=always`; a session-level `security=full` is a blocker.

## Source of truth

- OpenClaw: <https://docs.openclaw.ai/>
- Skills: <https://docs.openclaw.ai/tools/skills.md> | Creating: <https://docs.openclaw.ai/tools/creating-skills.md>
- MCP CLI: <https://docs.openclaw.ai/cli/mcp.md> | Exec: <https://docs.openclaw.ai/tools/exec.md>
- Sandboxing: <https://docs.openclaw.ai/gateway/sandboxing.md> | Exec approvals: <https://docs.openclaw.ai/tools/exec-approvals.md>
- Nodes: <https://docs.openclaw.ai/nodes/index.md> | Channels: <https://docs.openclaw.ai/channels/telegram>
- Bitrefill paths: [../touchpoints/mcp.md](../touchpoints/mcp.md), [../touchpoints/cli.md](../touchpoints/cli.md), [../touchpoints/api.md](../touchpoints/api.md), [../touchpoints/browse.md](../touchpoints/browse.md), [../safeguards.md](../safeguards.md)

**User hears:** same concierge flow — "Searching for [product]…" → "[Product] — [amount]: [total]. Confirm?" → "Your code is ready." Match channel language (Telegram, WhatsApp, etc.).
