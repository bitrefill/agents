# Wallet: Coinbase CDP (awal)

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Coinbase Agentic Wallet — TEE-backed signing, configurable spending caps. Strong autonomous x402 under limits.

Docs: [docs.cdp.coinbase.com/agentic-wallet](https://docs.cdp.coinbase.com/agentic-wallet/welcome)

## Surfaces

| Surface | Use |
| --- | --- |
| `npx awal@2.12 x402 pay <url>` | CLI x402 buyer from shell |
| `npx awal@2.12 send <amount> <address> --chain <network>` | Send to an invoice address |
| `@coinbase/payments-mcp` | MCP `make_http_request_with_x402` |
| AgentKit `@x402/fetch` | In-agent code with supplied signer |

## Capabilities

| Capability | CDP awal |
| --- | --- |
| HTTP proxy | Agent/shell makes HTTP; awal wraps x402 pay |
| x402 | **Auto within session/tx caps** |
| SIWX | **None** — pay-per-call; a status call paid from this wallet returns the codes |
| Keys | Remote TEE — agent never holds keys |
| Base USDC | Yes (+ Polygon, Solana x402) |
| Send | USDC on Base, Polygon, Solana; ETH; SOL — `awal send` |
| HITL | Email OTP auth once; autonomous under caps |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| x402 REST | `awal x402 pay https://api.bitrefill.com/x402/...` |
| MCP/CLI invoice | `awal send` to `payment_info.address` with `--chain` = the invoice's network; USDC amount = `payment_info.altBasePrice` (atomic units) |

## Setup

1. CDP Agentic Wallet auth (email OTP).
2. Set session + per-transaction spending limits.
3. Fund USDC on Base within cap.

## Hosts

Codex CLI, OpenClaw (`exec`), Hermes (`terminal`), any shell host.

## Example

```bash
npx awal@2.12 x402 pay "https://api.bitrefill.com/x402/gift-cards/search?q=amazon&country=US"
```

Invoice pay: URL/method/body from the 402 envelope.

## Security

- Caps = primary blast-radius control.
- Never unlimited awal caps on production accounts.

**User hears:** "[Product] — [amount]: [total] USDC. Confirm?" → "Your code is ready." (never "awal" or "x402")
