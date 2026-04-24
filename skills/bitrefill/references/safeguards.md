# Spending Safeguards

This skill enables **real-money transactions**. Purchases are fulfilled instantly after payment confirms. Digital codes are non-refundable per EU consumer rights once delivered.

This page is the **agent-policy layer** — not in upstream Bitrefill or host docs. Read fully before any purchase tool call.

## Universal rules

- **Default: always confirm before purchasing.** Present product, denomination, price, payment method. Wait for explicit user approval. Autonomous purchasing only when user explicitly opts in for the current session.
- **Codes are cash-like.** A gift card code or eSIM QR is bearer money. Store securely. Never share publicly.
- **Prefer in-memory storage.** Don't write codes to plain-text logs, transcripts, or unencrypted files. Programmatically read code → use it → discard.
- **If user asks for the code**: return it but advise to (a) store securely, (b) not share, (c) redeem ASAP.
- **Dedicated, low-balance account.** Never give the agent access to high-balance accounts. Pre-fund only what the agent may spend in the current session.
- **Not a wallet.** This skill does not store private keys or manage crypto wallets. Never give the agent seed phrases, hardware-wallet PINs, or signing keys.
- **Log every purchase.** `invoice_id`, product slug, amount, payment method, timestamp.
- **Refunds**: digital goods refundable only if they don't work as expected (defective code). EU 14-day change-of-mind does **not** apply.
- **Browser redemption fallback.** If trying to redeem on a brand site triggers anti-bot, ask the user to complete redemption manually and return the code.

Terms: <https://www.bitrefill.com/terms/>.

## Per-host hardening

### OpenClaw

Defaults are permissive (sandboxing off, `security: full`, `ask: off`). Tighten:

- `channels.<ch>.allowFrom: ["<your_id>"]` + `dmPolicy: "pairing"` on every channel.
- `~/.openclaw/exec-approvals.json`: `security: allowlist` + `ask: on-miss`. Allowlist read tools (`bitrefill search-products`, `bitrefill list-*`, `bitrefill get-*`). Force `/approve` for `bitrefill buy-products` and the MCP `buy-products` call.
- `agents.list[]` Bitrefill persona with `tools.deny: ["gateway"]` so the agent cannot rewrite Gateway config.
- Disable voice readback (`audio_as_voice` / TTS) for the Bitrefill agent. Codes spoken aloud over voice notes leak.
- Force text-only delivery — no `MEDIA:<url>` for redemption code output.

Full detail in [host-openclaw.md](host-openclaw.md) §8.

### Cursor

`.cursor/mcp.json` `autoApprove` may include read tools. **Never** include `buy-products`:

```json
{
  "mcpServers": {
    "bitrefill": {
      "url": "https://api.bitrefill.com/mcp",
      "autoApprove": [
        "search-products", "product-details",
        "list-invoices", "get-invoice-by-id",
        "list-orders", "get-order-by-id"
      ]
    }
  }
}
```

### Codex CLI

Run with sandbox + approval:

```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

Put `BITREFILL_API_KEY` in a profile (`~/.codex/config.toml` `[profiles.bitrefill]`), not in committed config.

### Claude Code

In `~/.claude/settings.json` (or project `.claude/settings.json`):

```json
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/.ssh", ".env", "*.pem", "**/.bitrefill_token"],
      "denyWrite": ["~/.ssh", ".env"]
    },
    "network": {
      "allow": ["api.bitrefill.com", "registry.npmjs.org"]
    }
  }
}
```

### Claude Desktop / Claude.ai web

Per-tool approval prompts on by default. Keep them on. Don't whitelist `buy-products`.

### ChatGPT (web / Desktop / Atlas / Agent)

Developer Mode required for write tools. Keep it **off** unless actively purchasing. Confirm in-chat before every `buy-products`.

### Gemini CLI

Run with `--sandbox` (Seatbelt / Docker / gVisor). Per-shell command confirmation prompts on by default.

### OpenCode

Set permissions per agent:

```jsonc
{
  "agents": {
    "bitrefill": {
      "permissions": {
        "edit": "ask",
        "bash": { "*": "ask", "bitrefill list-*": "allow", "bitrefill get-*": "allow" },
        "webfetch": "ask"
      }
    }
  }
}
```

## Payment method risk

- `balance` — instant, capped by pre-funded amount. **Lowest blast radius.**
- `usdc_base` via x402 — autonomous payment from agent-controlled wallet. Bound the wallet balance.
- `lightning` — fast, low fee. Manual pay or Lightning-capable agent.
- Other on-chain crypto — slow, requires polling. Higher chance of expired invoices (180 min).

Default recommendation: pre-fund `balance` with low cap → use `payment_method: "balance"` + `auto_pay: true`.

## What to NEVER do

- Pass redemption codes through group chats, public channels, screen-shared sessions, or shared documents.
- Speak codes aloud via TTS / voice notes.
- Store codes in version control, even private repos.
- Give the agent seed phrases or hardware-wallet PINs.
- Auto-approve `buy-products` in any host's MCP config.
- Run the Bitrefill skill from an account with stored payment cards or high balances.

## Source of truth

- Bitrefill ToS: <https://www.bitrefill.com/terms/>
- Refund policy: <https://docs.bitrefill.com/docs/refunds>
- Path setup: [path-mcp.md](path-mcp.md), [path-cli.md](path-cli.md), [path-api.md](path-api.md), [path-browse.md](path-browse.md)
- OpenClaw hardening: [host-openclaw.md](host-openclaw.md)
