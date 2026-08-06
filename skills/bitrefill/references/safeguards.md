# Spending Safeguards

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

**Real-money transactions.** Instant fulfillment after payment. Digital codes non-refundable per EU consumer rights once delivered.

**Agent-policy layer** — not in upstream Bitrefill or host docs. Read fully with [budget-guard.md](budget-guard.md) before any purchase-capable call.

## Universal rules

- **Session budget required.** Apply [budget-guard.md](budget-guard.md) before any call that can create, submit, auto-pay, pay, or settle a purchase. Missing, lost, ambiguous, or inconsistent budget state blocks the call.
- **Default: confirm before purchase.** Product, denomination, exact total, payment method. Wait explicit approval. Autonomous only when user opts in this session. A budget is a separate ceiling, not approval.
- **Codes = cash-like.** Gift card / eSIM QR = bearer money. Store secure. Never share publicly.
- **In-memory preferred.** Don't write codes to plain-text logs, transcripts, unencrypted files. Read → use → discard.
- **User asks for code:** return it; advise store secure, don't share, redeem ASAP.
- **Dedicated low-balance account.** Never high-balance access. Pre-fund only session spend cap.
- **Headless CLI: agent-owned inbox.** Register with agent inbox ([AgentMail](https://www.agentmail.to/) or equivalent — [touchpoints/cli-headless-auth.md](touchpoints/cli-headless-auth.md)), not human primary email. Inbox compromise = account takeover.
- **Not a wallet.** No private keys or crypto wallets. Never seed phrases, hardware-wallet PINs, signing keys.
- **Record every purchase in the session-local ledger.** Stable transaction ID, product slug or safe description, payable and budget-impact amounts/currencies, payment method, timestamp, and state only. Never codes, auth data, or full tool responses.
- **Account funding is separate.** A purchase budget never authorizes an account deposit or wallet top-up. Keep funding user-controlled and subject to independent host/wallet approval.
- **Refunds:** digital goods only if defective code. EU 14-day change-of-mind **does not** apply.
- **Browser redemption fallback:** anti-bot on brand site → user redeems manually; return code.

Terms: <https://www.bitrefill.com/terms/>.

## Per-host hardening

### OpenClaw

Defaults permissive (sandboxing off, `security: full`, `ask: off`). Tighten:

- **Guest CLI via `exec` first** for purchases. Sign-in is for identity/history/visibility; guarded balance also requires authorized direct REST, and cashback payment remains blocked pending authoritative debit semantics. → [harnesses/openclaw.md](harnesses/openclaw.md).
- `channels.<ch>.allowFrom: ["<your_id>"]` + `dmPolicy: "pairing"` every channel.
- `session.dmScope: "per-channel-peer"`; never share a budget/code across peers, and use `identityLinks` only for a reviewed same-operator handoff.
- MCP-allowlist only `search-products`, `get-product-details`, `list-invoices`, and `get-invoice-by-id`; future or state-changing tools stay excluded. Exec approvals do not protect direct MCP calls. Route buys through CLI/API with the execution-host-scoped `security: allowlist`, `ask: always`, `askFallback: deny`, `autoAllowSkills: false`, pinned binaries, and live-session `/exec ask=always` setup in [openclaw.md](harnesses/openclaw.md#8-openclaw-safeguards).
- `agents.list[]` Bitrefill persona with `tools.deny: ["gateway"]`.
- Disable voice readback (`audio_as_voice` / TTS). Text-only — no `MEDIA:<url>` for codes.

Full → [harnesses/openclaw.md](harnesses/openclaw.md) §8.

### Cursor

`.cursor/mcp.json` `autoApprove` may include read tools. **Never** `buy-products`:

```json
{
  "mcpServers": {
    "bitrefill": {
      "url": "https://api.bitrefill.com/mcp",
      "autoApprove": [
        "search-products", "get-product-details",
        "list-invoices", "get-invoice-by-id"
      ]
    }
  }
}
```

### Codex CLI

```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

`BITREFILL_API_KEY` in profile (`~/.codex/config.toml` `[profiles.bitrefill]`), not committed config.

### Claude Code

`~/.claude/settings.json` (or project `.claude/settings.json`):

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

Per-tool approval on default. Keep on. Don't whitelist `buy-products`.

**claude.ai:** MCP-first, `show_widget`, sandbox exec (egress probe) → [harnesses/claude-chat.md](harnesses/claude-chat.md).

### ChatGPT (web / Desktop / Atlas / Agent)

Developer Mode for write tools. Keep **off** unless actively purchasing. Confirm in-chat before every `buy-products`.

### Gemini CLI

`--sandbox` (Seatbelt / Docker / gVisor). Per-shell confirmation on default.

### OpenCode

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

→ [wallets/payment.md](wallets/payment.md), [wallets/matrix.md](wallets/matrix.md).

- `balance` — instant, capped by pre-fund. **Lowest blast radius.**
- x402 (AgentCash, awal, Base MCP) — bound wallet balance + caps.
- `lightning` / payment links — higher human involvement.

Default balance flow: create a non-paying REST invoice with `auto_pay: false`, reserve its server-bound final total, then pay that same invoice once. Use an auto-paying create call only when it independently exposes and binds the final total before the call.

## NEVER

- Redemption codes through group chats, public channels, screen-share, shared docs.
- Speak codes via TTS / voice notes.
- Store codes in version control.
- Give agent seed phrases or hardware-wallet PINs.
- Auto-approve `buy-products` in any host MCP config.
- Create, pay, or retry a purchase without a valid session-budget preflight and stable ledger record.
- Treat a purchase budget as authorization to fund an account or wallet.
- Run skill from account with stored payment cards or high balances.

## Source of truth

- ToS: <https://www.bitrefill.com/terms/> | Refunds: <https://docs.bitrefill.com/docs/refunds>
- Routing: [harnesses/decision-engine.md](harnesses/decision-engine.md)
- Touchpoints: [touchpoints/mcp.md](touchpoints/mcp.md), [touchpoints/cli.md](touchpoints/cli.md), [touchpoints/x402.md](touchpoints/x402.md)
- OpenClaw: [harnesses/openclaw.md](harnesses/openclaw.md) | Claude Chat: [harnesses/claude-chat.md](harnesses/claude-chat.md)

**User hears:** confirm as a clean receipt — "[Product] — [amount]: [exact total and payment asset]. Confirm?" Non-refundable once, neutrally at delivery: "Your code is ready — keep it safe, not refundable once issued."
