# Wallet: Pay

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Solana Foundation's `pay` CLI — a curl that pays 402s, plus Solana stablecoin sends. Keys in the OS keychain.

Docs: [pay.sh](https://pay.sh)

## Capabilities

| Capability | Pay |
| --- | --- |
| HTTP proxy | **Yes** — `pay curl` |
| x402 | **Automatic** (Solana USDC) |
| SIWX | **Automatic** |
| Send | Solana USDC, USDT — `pay send` |
| Keys | Local — OS keychain |
| HITL | Touch ID or OS prompt per payment |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| x402 REST Path 1 | `pay curl` on the x402 routes |
| Bitrefill MCP / CLI | `buy-products` with `usdc_solana` or `usdt_solana` → `pay send` to `payment_info.address` |

**User hears:** "Approve the payment with Touch ID" → "Your code is ready."
