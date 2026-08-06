# Wallet: AgentCash

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Local MCP wallet — **`fetch`** tool: payment-aware HTTP, handles SIWX + x402 automatically. **Highest autonomous x402** for headless agents when pre-funded.

Docs: [agentcash.dev](https://agentcash.dev/docs/mcp-mode)

## Capabilities

| Capability | AgentCash |
| --- | --- |
| HTTP proxy | **Yes** — `fetch` = full HTTP + x402 buyer |
| x402 | **Automatic** on 402 |
| SIWX | **Automatic** in `fetch` before x402 |
| Keys | Local — `~/.agentcash/wallet.json` or `X402_PRIVATE_KEY` |
| Base USDC | Yes (primary) |
| HITL | Fund once; optional env caps |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| x402 REST Path 1 | `fetch` handles connect SIWX and JWT; use automatic payment only after the current challenge is inspected and reserved |
| Bitrefill MCP / CLI | `fetch` on a known `x402_payment_url` only after its current challenge terms and fees are reserved |

Rank **#2** in [matrix.md](matrix.md) — after a pre-reserved two-step Bitrefill balance payment.

## Setup

1. Install AgentCash MCP (stdio) in host config.
2. Fund small USDC on Base.
3. Set spending caps in env if available.

## Hosts

OpenClaw, Hermes, Codex CLI, Cursor (local MCP), cron/automation.

## Security

- Local private key — treat `~/.agentcash/wallet.json` as sensitive.
- Pre-fund only a small independent wallet cap; it is not the session budget.
- Apply [budget-guard.md](../budget-guard.md) and the [payment route contract](payment.md#route-contract) before every automatic payment. Do not use `fetch` to probe a paid route when it can pay before exposing the exact charge and stable identifier; obtain the current 402 challenge through a non-paying client or use the signed-in fee-free route, otherwise block.
- For invoice payment, reserve the selected challenge's exact USDC amount, authoritative budget impact, and separate fee components under the attempt ID. Call `fetch` once with `maxAmount` equal to that selected USD/USDC payable cap; never pass the budget amount or a fee aggregate. If the host cannot preserve the exact decimal in AgentCash's JSON-number field, block. Reconcile the returned string `paymentInfo.amount`, transaction, and network plus Bitrefill status. A timeout never authorizes an automatic retry.
- Still confirm purchases per [../safeguards.md](../safeguards.md) unless user opts autonomous session.

## vs Base MCP

AgentCash: autonomous x402, no per-tx Base Account click. Base MCP: user approves each payment — better when user wants per-pay review.

**User hears:** same as any purchase — "[Product] — [amount]: [total] USDC. Confirm?" → "Your code is ready." (no wallet jargon even when autonomous)
