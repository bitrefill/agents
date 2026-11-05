# Wallet: Alby

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Lightning payments over a Nostr Wallet Connect (NWC) connection — Alby MCP pays Lightning invoices, Alby CLI also pays Lightning 402s. Funds stay in the connected wallet (e.g. Alby Hub).

Docs: [Alby MCP](https://github.com/getAlby/mcp), [Alby CLI](https://github.com/getAlby/payments-skill)

## Capabilities

| Capability | Alby |
| --- | --- |
| HTTP proxy | Alby CLI `fetch` |
| x402 | Lightning, via Alby CLI |
| SIWX | None — the payment preimage proves the order |
| Send | Lightning — Alby MCP `pay_invoice` |
| HITL | None per payment; budget on the wallet connection |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| x402 REST Path 2 | Alby CLI `fetch` on the x402 routes; status with header `x-lightning-preimage` |
| Bitrefill MCP / CLI | `buy-products` with `lightning` → `pay_invoice` on `payment_info.lightningInvoice` |

**User hears:** "[Product] — [amount]: [total] sats. Confirm?" → "Your code is ready."
