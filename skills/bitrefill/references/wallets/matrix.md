# Wallet Matrix

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Agent wallets that can pay Bitrefill. The user picks the wallet; its own docs and tools cover setup and use.

| Wallet | x402 REST | MCP / CLI invoice | Approval |
| --- | --- | --- | --- |
| **Bitrefill balance** | — | `balance` | Purchase confirm only |
| [AgentCash](agentcash.md) | Yes | — | None per payment |
| [Coinbase Agentic Wallet](cdp-awal.md) | Yes | Sends USDC, ETH, SOL (awal CLI) | None per payment, within caps |
| [Coinbase Wallet MCP](base-mcp.md) | Yes | Sends EVM tokens | Each payment |
| [MetaMask](metamask.md) | Yes | Sends EVM tokens | Each payment |
| [Kite Passport](kite-passport.md) | Yes | Sends USDC | Passkey |
| [Bankr](bankr.md) | Yes | Sends EVM and Solana tokens | None per payment, within limits |
| [Alby](alby.md) | Yes (Lightning) | Pays Lightning invoices | None per payment, within budget |
| [Tether WDK](tether-wdk.md) | — | Sends USDT, bitcoin, Lightning | None while unlocked |
| [Pay](pay.md) | Yes | Sends Solana USDC, USDT | Each payment |

## Pairing rules

- **x402 REST** ([../touchpoints/x402.md](../touchpoints/x402.md)) — no Bitrefill account; the wallet signs in once and pays the invoice.
- **Bitrefill MCP / CLI** — `balance`, or `buy-products` with a `payment_method` the wallet holds, then the wallet pays `payment_info` ([payment.md](payment.md)).
- **Any other wallet** that can send the invoice's coin pays the same way.
- **No wallet** → `payment_link`, the human pays.

Pay-time tree → [payment.md](payment.md). Harness routing → [../harnesses/decision-engine.md](../harnesses/decision-engine.md).

**User hears:** never wallet comparisons or tool names — only "Sign in with your wallet once" and "Approve the payment."
