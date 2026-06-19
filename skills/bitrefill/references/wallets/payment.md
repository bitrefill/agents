# Wallet: Payment Decision

Pay-time routing after touchpoint creates invoice. **Lowest HITL first** — [matrix.md](matrix.md).

## Decision tree

```
1. bitrefill_balance available?
   → payment_method: "balance" + auto_pay: true (MCP/CLI)

2. wallet_agentcash or wallet_cdp?
   → x402 on x402_payment_url or x402 REST invoice/pay

3. wallet_base_mcp + x402 tools?
   → initiate_x402_request → approve → complete_x402_request

4. wallet_base_mcp, no x402?
   → send USDC on base to payment_info address/amount

5. wallet_phantom / wallet_metamask?
   → Manual: orchestrate HTTP separately; sign typed data / send tx (high HITL)

6. Else
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
| `balance` + `auto_pay` | Skip wallet — instant from pre-funded account |

MCP: `payment_method: "usdc_base"`, `return_payment_link: true` → pay `x402_payment_url`.

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

## Related

- [base-mcp.md](base-mcp.md) — x402 + send
- [siwx.md](siwx.md) — JWT for fee-free browse
- [agentcash.md](agentcash.md), [cdp-awal.md](cdp-awal.md) — autonomous x402
- [phantom.md](phantom.md), [metamask.md](metamask.md) — manual signing
