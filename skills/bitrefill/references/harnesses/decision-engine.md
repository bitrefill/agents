# Decision Engine

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Capability-driven Bitrefill routing. Three phases — same order as [SKILL.md](../../SKILL.md) § How to route:

1. **Harness** — probe host, read harness guide.
2. **Wallets** — probe payment tools, read wallet guides.
3. **Combine** — pick touchpoint × wallet with lowest HITL for intent.

**Thinking:** one short line in the user's language — never deliberate paths, ranks, fees, or auth state. Choose stack silently; act.

**Internal labels only:** Path 1/2, touchpoint, harness, SIWX — agent docs; never repeat in any visible surface → [SKILL.md](../../SKILL.md) § User-facing language.

Per-host defaults → [capability-matrix.md](capability-matrix.md). Wallets → [../wallets/matrix.md](../wallets/matrix.md).

## Step 0 — Intent

- Browse-only vs purchase
- Bitrefill account (OAuth / signed-in CLI) vs guest agent-commerce (x402 wallet, no signup)

## Phase 1 — Probe harness

```
sandbox_exec        = host code sandbox (Python/Node/bash) — Claude Chat: always true
exec_available      = agent shell | exec | terminal | @bitrefill/cli — Claude Chat: false
egress_direct       = sandbox or agent HTTP to api.bitrefill.com without MCP proxy — Claude Chat: probe
egress_mcp_proxy    = wallet HTTP tool → api.bitrefill.com (e.g. Coinbase Wallet MCP web_request)
egress_none         = chat-only; sandbox no outbound net
browser_residential = user-network browser (not datacenter)
bitrefill_mcp_live  = search-products / buy-products visible (OAuth or API key)
base_mcp_live       = get_wallets / web_request / initiate_x402_request visible
```

**Claude Chat:** code sandbox and chat MCP are separate network layers; shop via MCP when connectors are live → [claude-chat.md](claude-chat.md) §4.

**Legacy Analysis tool** (browser JS, no net) mutually exclusive with code execution — ignore if code execution on.

ChatGPT Code Interpreter: **no sandbox egress**. Coinbase Wallet MCP `web_request` proxies `api.bitrefill.com` even when agent can't curl.

## Phase 2 — Probe wallets

```
wallet_x402         = wallet pays x402 (HTTP tool or fetch)
wallet_send         = wallet sends a coin Bitrefill accepts to an address
wallet_sign         = wallet signs a sign-in message
wallet_none         = payment_link / human browser only
bitrefill_balance   = signed-in MCP/CLI with pre-funded balance
```

## Phase 3 — Combine: touchpoint × wallet

### Derive touchpoint

| Condition | Touchpoint |
|-----------|------------|
| `bitrefill_mcp_live` | [../touchpoints/mcp.md](../touchpoints/mcp.md) |
| `!bitrefill_mcp_live` ∧ (`egress_mcp_proxy` ∨ `egress_direct`) ∧ guest/USDC | [../touchpoints/x402.md](../touchpoints/x402.md) Path 1 (JWT) |
| `exec_available` ∧ `!bitrefill_mcp_live` | [../touchpoints/cli.md](../touchpoints/cli.md) |
| `egress_direct` ∧ no MCP | [../touchpoints/api.md](../touchpoints/api.md) |
| browse-only ∧ `browser_residential` | [../touchpoints/browse.md](../touchpoints/browse.md) |
| else | send user `bitrefill.com` link |

**OpenClaw override:** detect first → [openclaw.md](openclaw.md). Guest CLI via `exec` before MCP when no OAuth.

**Grok Bot / Cursor override:** detect → [grok-bot.md](grok-bot.md). Connector signed in (`get-balances` visible) → MCP + `balance`; else guest CLI; no shell → `bitrefill.com` link.

**Claude Chat override:** detect in Phase 1 → [claude-chat.md](claude-chat.md) §1. Signals: `show_widget` **or** `read_me`; MCP connector tools on claude.ai. **`sandbox_exec` true, `exec_available` false** — has code sandbox, not agent shell. Probe **`egress_direct`**. MCP-first for shopping; no pay-per-call browse when the wallet can sign in; `show_widget` when available.

### Derive wallet (pay time)

1. User named a method or wallet → use it
2. **`bitrefill_balance`** → `payment_method: "balance"`
3. **`wallet_send`** on Bitrefill MCP / CLI → `buy-products` with a coin the wallet holds and `return_payment_link: false` → send to `payment_info`
4. **`wallet_x402`** → x402 REST; Path 1 sign-in when `wallet_sign` ([../wallets/siwx.md](../wallets/siwx.md)) — **never Path 2** if Path 1 JWT possible
5. **`wallet_none`** → `payment_link`

Details → [../wallets/payment.md](../wallets/payment.md).

## When capabilities conflict

| Situation | Resolution |
|-----------|------------|
| ChatGPT sandbox no net + Coinbase Wallet MCP yes | Coinbase Wallet MCP `web_request` for x402 REST; ignore sandbox for API |
| Bitrefill MCP OAuth'd + wallet yes | Bitrefill MCP catalog; wallet sends to `payment_info` |
| x402 wallet yes, no Bitrefill MCP | x402 REST Path 1 via the wallet (ChatGPT+: Coinbase Wallet MCP) |

**User hears:** open with the product goal — never "checking harness" or "Path 1 vs Path 2". Two steps max: "Sign in with your wallet once" → "Approve the payment."
