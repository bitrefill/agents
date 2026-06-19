---
name: bitrefill
description: "Buy or browse Bitrefill — 1,500+ gift cards, mobile top-ups, eSIMs, 180+ countries. Capability routing: probe harness (exec, egress, MCP), pick touchpoint (Bitrefill MCP, x402 REST via Base MCP, CLI, API, browse), wallet (balance, x402, send). Favors autonomous purchase, minimal HITL. Triggers: Bitrefill, gift cards, mobile top-up, eSIM, crypto, Lightning, USDC, x402."
compatibility: "Routes by harness × touchpoint × wallet. Touchpoints: Bitrefill MCP (OAuth), x402 REST (Base MCP web_request → api.bitrefill.com), CLI ≥0.3.0, v2 REST, residential browse. Wallets: Bitrefill balance, Base MCP, AgentCash, CDP awal, Phantom/MetaMask sign-only. OpenClaw + Claude Chat: dedicated harness guides."
metadata:
  author: bitrefill
  version: "3.0.0"
  homepage: "https://www.bitrefill.com"
  docs: "https://docs.bitrefill.com"
  repository: "https://github.com/bitrefill/agents"
---

# Bitrefill

Digital goods (gift cards, mobile top-ups, eSIMs) — 180+ countries, 1,500+ brands. Pay: crypto, Lightning, USDC x402, pre-funded balance.

Routes by **capability intersection**, not fixed path. Probe harness + wallets → touchpoint + payment stack. **Lowest HITL wins.**

## How to route

1. Safeguards below → full policy [safeguards.md](references/safeguards.md).
2. **Probe** → [decision-engine.md](references/harnesses/decision-engine.md).
3. **OpenClaw?** (`~/.openclaw/`, `openclaw` on PATH) → [openclaw.md](references/harnesses/openclaw.md) first.
4. **Claude Chat?** (claude.ai + `show_widget` + MCP) → [claude-chat.md](references/harnesses/claude-chat.md) first.
5. **Unknown host?** → [capability-matrix.md](references/harnesses/capability-matrix.md).
6. **Derive touchpoint** (catalog/checkout channel).
7. **Derive wallet** at pay → [payment.md](references/wallets/payment.md).

### Touchpoint (first match after probe)

| If | Read |
| --- | --- |
| `search-products` / `buy-products` visible (OAuth or API key) | [mcp.md](references/touchpoints/mcp.md) |
| Base MCP `web_request` + guest USDC, no Bitrefill account | [x402.md](references/touchpoints/x402.md) Path 1 (JWT) |
| Shell + npm, no Bitrefill MCP | [cli.md](references/touchpoints/cli.md) |
| Direct HTTP only | [api.md](references/touchpoints/api.md) |
| Browse-only + residential browser | [browse.md](references/touchpoints/browse.md) |
| None viable | Send user `bitrefill.com` link |

**Pay:** wallet supports x402 → x402; else on-chain `send`; signed-in → `balance` + `auto_pay` first. → [payment.md](references/wallets/payment.md), [matrix.md](references/wallets/matrix.md).

## Top spending safeguards

**Real-money transactions.** Codes instant; digital goods non-refundable once fulfilled.

- **Confirm before buy** unless user opted autonomous purchasing this session.
- **Codes = cash** — never paste public channels; prefer in-memory.
- **Dedicated low-balance account** — never give agent wallet seeds. Skill **not a wallet**.
- **Log every purchase** — `invoice_id`, product, amount, payment method.

Full safeguards + per-host hardening → [safeguards.md](references/safeguards.md).

## References

### Harnesses

| File | Use when |
| --- | --- |
| [decision-engine.md](references/harnesses/decision-engine.md) | Capability probe + derivation |
| [capability-matrix.md](references/harnesses/capability-matrix.md) | Per-host exec / egress / ranked stacks |
| [openclaw.md](references/harnesses/openclaw.md) | OpenClaw Gateway — guest CLI via `exec` |
| [claude-chat.md](references/harnesses/claude-chat.md) | claude.ai — MCP-first + `show_widget` |

### Touchpoints

| File | Use when |
| --- | --- |
| [mcp.md](references/touchpoints/mcp.md) | Bitrefill MCP OAuth'd |
| [x402.md](references/touchpoints/x402.md) | x402 REST via Base MCP or direct egress |
| [cli.md](references/touchpoints/cli.md) | Shell + `@bitrefill/cli` ≥ 0.3.0 |
| [cli-headless-auth.md](references/touchpoints/cli-headless-auth.md) | AgentMail / magic-link sign-in |
| [api.md](references/touchpoints/api.md) | v2 REST — Personal / Business / Affiliate |
| [browse.md](references/touchpoints/browse.md) | Residential browser explore-only |

### Wallets

| File | Use when |
| --- | --- |
| [matrix.md](references/wallets/matrix.md) | Wallet × touchpoint × HITL ranking |
| [payment.md](references/wallets/payment.md) | Pay-time decision tree |
| [base-mcp.md](references/wallets/base-mcp.md) | Base MCP `web_request`, x402, `send` |
| [siwx.md](references/wallets/siwx.md) | Connect → JWT, redemption SIWX |
| [agentcash.md](references/wallets/agentcash.md) | Autonomous x402 via `fetch` |
| [cdp-awal.md](references/wallets/cdp-awal.md) | Coinbase Agentic Wallet / awal |
| [metamask.md](references/wallets/metamask.md) | MetaMask Agent Wallet (`mm` CLI) |
| [phantom.md](references/wallets/phantom.md) | Phantom MCP sign-only |

### Cross-cutting

| File | Use when |
| --- | --- |
| [safeguards.md](references/safeguards.md) | Spending policy + host hardening |
| [troubleshooting.md](references/troubleshooting.md) | Errors across all paths |

## Source of truth

Skill summarizes + routes. Exhaustive enums → <https://docs.bitrefill.com>.
