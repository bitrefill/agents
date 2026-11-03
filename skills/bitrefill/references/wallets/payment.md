# Wallet: Payment Decision

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Pay-time routing after touchpoint creates invoice. **Lowest HITL first** — [matrix.md](matrix.md).

**Thinking:** one short line in the user's language — never deliberate wallet ranks or HITL scores aloud.

## Decision tree

```
1. bitrefill_balance available?
   → payment_method: "balance" + auto_pay: true (MCP/CLI)

2. wallet_agentcash or wallet_cdp?
   → x402 REST invoice/create → x402 on invoice/pay

3. wallet_base_mcp + x402 tools + x402 REST invoice?
   → initiate_x402_request → approve → complete_x402_request

4. wallet_base_mcp + MCP/CLI invoice (or no x402)?
   → send USDC on base to payment_info address/amount

5. wallet_phantom / wallet_metamask?
   → Manual: orchestrate HTTP separately; sign typed data / send tx (high HITL)

6. Else
   → return_payment_link or Lightning — human completes
```

## By touchpoint

### Bitrefill MCP / CLI invoice fields

After `buy-products`. x402 pays only invoices from x402 REST `invoice/create`; MCP/CLI invoices are not x402-payable.

| Field | Use |
| --- | --- |
| `payment_info.address` + `payment_info.altcoinPrice` | Base MCP `send` (direct USDC) |
| `payment_link` | Human browser checkout |
| `balance` + `auto_pay` | Skip wallet — instant from pre-funded account |

MCP: `payment_method: "usdc_base"` → Base MCP `send` to `payment_info.address` / `payment_info.altcoinPrice`.

CLI: `--payment_method usdc_base` → same fields in JSON.

### x402 REST ([../touchpoints/x402.md](../touchpoints/x402.md))

- Browse/create/status: JWT (`X-Access-Token`) or x402 micro-fees
- **`invoice/pay`**: always x402 — never JWT-waived
- `maxPayment`: `"0.01"` micro-fees; slightly above `price_usd` for pay

## Payment method risk

| Method | HITL | Notes |
| --- | --- | --- |
| `balance` + `auto_pay` | Lowest | Pre-fund cap on dedicated account |
| AgentCash / awal x402 | Low (after setup) | Autonomous under caps |
| Base MCP x402 | Medium | 1 Base Account approval per pay |
| Base MCP `send` | Medium | 1 approval per send |
| Phantom / MetaMask | High | Per-sign or per-tx approval |
| `return_payment_link` | Highest | Human browser |

Full enum → <https://docs.bitrefill.com/docs/crypto-payments>.

## Confirm before pay

Present product, denomination, exact USDC total, payment method. Wait explicit approval unless session opted autonomous ([../safeguards.md](../safeguards.md)).

*(say: "[Product] — [face value]: [total] USDC on [network]. Your balance: [balance]. Valid [N] min. Confirm?")*

## Related

- [base-mcp.md](base-mcp.md) — x402 + send
- [siwx.md](siwx.md) — JWT for fee-free browse
- [agentcash.md](agentcash.md), [cdp-awal.md](cdp-awal.md) — autonomous x402
- [phantom.md](phantom.md), [metamask.md](metamask.md) — manual signing

**User hears:** "[Product] — [amount]: [total] USDC. Confirm?" → "Approve the payment in your Base Account" → "Your code is ready."
