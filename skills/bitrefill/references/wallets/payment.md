# Wallet: Payment Decision

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Pay-time routing after touchpoint creates invoice. Wallets → [matrix.md](matrix.md).

**Thinking:** one short line in the user's language — never deliberate wallet choice aloud.

## Decision tree

```
1. User named a payment method or wallet?
   → card, Apple Pay, Google Pay (priced in USD) or iDEAL, EPS, P24, Bancontact (EUR):
     saved card when signed in, else billing address → payment_link
   → a wallet or coin: use it in 3 or 4

2. bitrefill_balance available?
   → get-balances covers the total? payment_method: "balance" (debits at once)
   → short: offer a Bitrefill Gift Card top-up (bitrefill-giftcard-usd / -eur) or go to 3
   → no balance_currency = primary sub-account (can be BTC): name it in the confirm

3. Bitrefill MCP / CLI + wallet that sends one of the product's payment methods?
   → buy-products with that payment_method and return_payment_link: false → wallet pays payment_info

4. x402 wallet?
   → x402 REST checkout

5. Else
   → return_payment_link — human completes
```

## By touchpoint

### Bitrefill MCP / CLI invoice fields

After `buy-products`:

| Field | Use |
| --- | --- |
| `payment_info.address` + `payment_info.altcoinPrice` (`altBasePrice`: atomic units) | Wallet sends exactly this amount of the invoice's coin on the `payment_method` network (`usdc_polygon` → Polygon) |
| `payment_info.lightningInvoice` | Lightning wallet pays it |
| `payment_link` | Human browser checkout |
| `balance` | Skip wallet — debits the pre-funded account at once |

MCP: `payment_method` = a coin the wallet holds, e.g. `"usdc_base"`, and `return_payment_link: false` to get `payment_info`. Send once, before `expiration_minutes` runs out; then poll `get-invoice-by-id`.

CLI: `--payment_method usdc_base --return_payment_link false` → same fields in JSON.

### x402 REST ([../touchpoints/x402.md](../touchpoints/x402.md))

- Browse/create/status: JWT (`X-Access-Token`) or x402 micro-fees
- **`invoice/pay`**: always x402 — never JWT-waived
- `maxPayment`: `"0.01"` micro-fees; `price_usdc` from `invoice/create` for pay
- The 402 amount must equal the invoice price before paying; otherwise stop
- Wallet's x402 cap below `price_usdc` → pay by send instead (step 3)

## Payment method risk

| Method | HITL | Notes |
| --- | --- | --- |
| `balance` | Lowest | Pre-fund cap on dedicated account |
| Wallet without per-payment approval | Low (after setup) | Bounded by its funds and caps |
| Wallet that approves each payment | Medium | 1 approval per payment |
| `return_payment_link` | Highest | Human browser |

Full enum → <https://docs.bitrefill.com/docs/crypto-payments>.

## Confirm before pay

Present product, denomination, the real charge for the chosen method (`payment_price`, e.g. 10 EUR Vodafone costs 10.61 EUR; on x402 `price_usdc`), its coin and network, the sub-account for balance (debited as soon as `buy-products` runs) and the recipient for top-ups. Wait for explicit approval unless the user opted into autonomous buying in chat ([../safeguards.md](../safeguards.md)).

*(say: "[Product] — [face value]: [total] [coin] on [network]. Your balance: [balance]. Valid [N] min. Confirm?")*

## Related

- [matrix.md](matrix.md) — wallets that can pay Bitrefill
- [siwx.md](siwx.md) — JWT for fee-free browse

**User hears:** "[Product] — [amount]: [total] [coin]. Confirm?" → "Approve the payment in your wallet" (only when the wallet asks) → "Your code is ready."
