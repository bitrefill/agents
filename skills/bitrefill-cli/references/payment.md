# Payment Reference

## Recommended for Agents

- **`balance`** — Instant fulfillment, no on-chain wait. User pre-funds at [bitrefill.com](https://www.bitrefill.com). Natural spending cap.
- **`usdc_base`** with x402 — Use `--return_payment_link true` (default) to get `x402_payment_url`. An x402-capable agent completes payment autonomously over Base.

Suggest `balance` or `usdc_base` first. Fall back to other methods only if the user explicitly requests them.

## Payment Methods

| Method | Chain / Asset |
|--------|---------------|
| `bitcoin` | Bitcoin (SegWit) — `address`, `BIP21`, `lightningInvoice`, `satoshiPrice` |
| `lightning` | Lightning — `lightningInvoice`, `satoshiPrice` |
| `ethereum` | Ethereum mainnet (ETH) — `address`, `paymentUri`, `altcoinPrice` |
| `eth_base` | Base (8453), native ETH |
| `usdc_base` | Base (8453), USDC |
| `usdc_arbitrum` | Arbitrum (42161), USDC |
| `usdc_polygon` | Polygon (137), USDC |
| `usdc_erc20` | Ethereum (1), USDC |
| `usdc_solana` | Solana, USDC SPL |
| `usdt_polygon` | Polygon (137), USDT |
| `usdt_erc20` | Ethereum (1), USDT |
| `balance` | Bitrefill account credit — paid from balance, no address |

## Response Modes

- **`--return_payment_link true`** (default) — returns `payment_link` (browser checkout), `x402_payment_url` (programmatic pay), plus raw `payment_info`.
- **`--return_payment_link false`** — raw payment details only: `address`, `amount`, `paymentUri` (+ `lightningInvoice` for Bitcoin). No `payment_link` or `x402_payment_url`.

## x402 Protocol

[x402](https://docs.x402.org/) enables HTTP 402-based crypto payments:

1. `GET x402_payment_url` → receive 402 + payment instructions (Base64 JSON: amount, `payTo`, networks, timeout)
2. Send crypto to the specified address
3. Resubmit request with payment proof

For agents and automated tools. Humans use `payment_link` instead.
