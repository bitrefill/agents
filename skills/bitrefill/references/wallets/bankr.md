# Wallet: Bankr

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Bankr's custodial agent wallet — `bankr` CLI or Wallet API, one EVM and one Solana address.

Docs: [docs.bankr.bot](https://docs.bankr.bot)

## Capabilities

| Capability | Bankr |
| --- | --- |
| HTTP proxy | **Yes** — `bankr x402 call` |
| x402 | **Automatic** (EVM USDC) |
| Send | EVM and Solana tokens — `bankr wallet transfer` |
| Keys | Custodial — Bankr holds them |
| HITL | None per call; account spending limits |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| x402 REST Path 2 | `bankr x402 call` on each x402 route |
| Bitrefill MCP / CLI | `bankr wallet transfer` of the `payment_info` amount to its address |

**User hears:** "[Product] — [amount]: [total]. Confirm?" → "Your code is ready."
