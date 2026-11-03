# Wallet: Payment Decision

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Pay-time routing after touchpoint creates invoice. **Lowest HITL first** — [matrix.md](matrix.md).

**Thinking:** one short line in the user's language — never deliberate wallet ranks or HITL scores aloud.

## Decision tree

```
1. User asked for card, Apple Pay, Google Pay (priced in USD) or iDEAL, EPS, P24, Bancontact (EUR)?
   → saved card when signed in, else billing address → payment_link

2. bitrefill_balance available?
   → get-balances covers the total? payment_method: "balance" (debits at once)
   → short: offer a Bitrefill Gift Card top-up (bitrefill-giftcard-usd / -eur) or go to 3
   → no balance_currency = primary sub-account (can be BTC): name it in the confirm

3. wallet_agentcash or wallet_cdp?
   → x402 on x402_payment_url or x402 REST invoice/pay

4. wallet_base_mcp + x402 tools?
   → initiate_x402_request → approve → complete_x402_request

5. wallet_base_mcp, no x402?
   → send USDC on base to payment_info address/amount

6. wallet_phantom / wallet_metamask?
   → Manual: orchestrate HTTP separately; sign typed data / send tx (high HITL)

7. Else
   → return_payment_link or Lightning — human completes
```

## By touchpoint

### Bitrefill MCP / CLI invoice fields

After `buy-products`:

| Field | Use |
| --- | --- |
| `x402_payment_url` | Base MCP x402, AgentCash, awal |
| `payment_info.address` + `payment_info.altcoinPrice` | Base MCP `send` (direct USDC) |
| `payment_link` | Human browser checkout |
| `balance` | Skip wallet — debits the pre-funded account at once |

MCP: `payment_method: "usdc_base"`, `return_payment_link: true` → pay `x402_payment_url`.

CLI: `--payment_method usdc_base` → same fields in JSON.

### x402 REST ([../touchpoints/x402.md](../touchpoints/x402.md))

- Browse/create/status: JWT (`X-Access-Token`) or x402 micro-fees
- **`invoice/pay`**: always x402 — never JWT-waived
- `maxPayment`: `"0.01"` micro-fees; slightly above `price_usd` for pay
- The 402 amount must equal the invoice price before paying; otherwise stop

## Payment method risk

| Method | HITL | Notes |
| --- | --- | --- |
| `balance` | Lowest | Pre-fund cap on dedicated account |
| AgentCash / awal x402 | Low (after setup) | Autonomous under caps |
| Base MCP x402 | Medium | 1 Base Account approval per pay |
| Base MCP `send` | Medium | 1 approval per send |
| Phantom / MetaMask | High | Per-sign or per-tx approval |
| `return_payment_link` | Highest | Human browser |

Full enum → <https://docs.bitrefill.com/docs/crypto-payments>.

## Confirm before pay

Present product, denomination, the real charge for the chosen method (`payment_price`, e.g. 10 EUR Vodafone costs 10.61 EUR; on x402 `price_usdc`), its coin and network, the sub-account for balance (debited as soon as `buy-products` runs) and the recipient for top-ups. Wait for explicit approval unless the user opted into autonomous buying in chat ([../safeguards.md](../safeguards.md)).

*(say: "[Product] — [face value]: [total] USDC on [network]. Your balance: [balance]. Valid [N] min. Confirm?")*

## Related

- [base-mcp.md](base-mcp.md) — x402 + send
- [siwx.md](siwx.md) — JWT for fee-free browse
- [agentcash.md](agentcash.md), [cdp-awal.md](cdp-awal.md) — autonomous x402
- [phantom.md](phantom.md), [metamask.md](metamask.md) — manual signing

**User hears:** "[Product] — [amount]: [total] USDC. Confirm?" → "Approve the payment in your Base Account" → "Your code is ready."
