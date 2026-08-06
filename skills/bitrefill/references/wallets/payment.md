# Wallet: Payment Decision

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Pay-time routing after a touchpoint creates an invoice. **Lowest HITL first** — [matrix.md](matrix.md). Every route requires an existing reservation under [the session budget guard](../budget-guard.md) before a call or user-visible payment instrument can move money.

## Route contract

For every route—including balance, x402, direct Base send, MetaMask, Phantom, Lightning, payment link, and manual transfer—reuse one stable request/invoice/payment record. Reserve the exact authoritative payment amount and its exact budget-currency impact. Also reserve authoritative network/wallet/service fees; when only a safe cap is available, reserve the cap or block. Product details, face value, and `price_usd` are estimates and cannot replace current invoice or challenge terms.

Keep `reserved` authorization exposure separate from `settled` actual debit. Bind authorization to the confirmed asset, network, recipient, and amount; changed payment terms require same-record repricing and renewed confirmation. After authoritative payment and wallet reconciliation, settle only the actual debit and release the unused portion of any cap. A timeout, signature, transaction broadcast, payment detection, abandoned link, or delivery failure is not enough to release or settle funds. Never retry a possibly money-moving action; create a replacement attempt only after the no-debit proof and freeze procedure in the budget guard.

Funding is outside this pay-time tree. A wallet or Bitrefill account deposit never creates, resets, or increases a goods budget. Require it as a separate explicit action and either guard the deposit plus fees under an all-spend policy or keep it explicitly outside the goods budget; block when the boundary is ambiguous.

**Thinking:** one short line in the user's language — never deliberate wallet ranks or HITL scores aloud.

## Decision tree

```
0. exact payment impact plus bounded fees reserved under a stable ID?
   → no: stop and apply budget-guard.md

0a. payment_method is cashback?
   → block unless the current provider contract binds its exact pre-call total
     and debit semantics; rewards do not bypass the budget

1. bitrefill_balance available?
   → require direct REST egress + authorized REST credential; otherwise skip balance
   → create REST invoice with auto_pay: false → reserve returned final total
     → pay that same invoice once
   → auto-paying create only if its final total is independently bound pre-call

2. wallet_agentcash or wallet_cdp?
   → x402 on x402_payment_url or x402 REST invoice/pay

3. wallet_base_mcp + x402 tools?
   → initiate_x402_request → approve → complete_x402_request

4. wallet_base_mcp, no x402?
   → validate current invoice payment_info; reserve amount + fee cap; send once

5. wallet_phantom / wallet_metamask?
   → validate current invoice/challenge; reserve amount + fee cap; sign/send once

6. Else
   → expose the guarded payment link or Lightning invoice; keep reserved until reconciled
```

## By touchpoint

### Bitrefill MCP / CLI invoice fields

After `buy-products`:

| Field | Use |
| --- | --- |
| `x402_payment_url` | Base MCP x402, AgentCash, awal |
| `payment_info.address` + `payment_info.altcoinPrice` | Current invoice terms for Base MCP `send`; also reserve bounded fees |
| `payment_link` | Human browser checkout; expose only after reservation |
| `balance` | Prefer REST `auto_pay: false` → reserve → pay same invoice; auto-pay only with pre-call bound total |

MCP: `payment_method: "usdc_base"`, `return_payment_link: true` → pay `x402_payment_url`.

CLI: `--payment_method usdc_base` → same fields in JSON.

### Lightning, payment links, and manual transfer

Before exposing a BOLT11 invoice, payment link, address, or other actionable instruction, attach the provider invoice ID to the stable record and reserve its exact payment amount and budget impact plus authoritative or safely capped fees. For a link, the payment method and maximum payable impact must be locked or safely capped; otherwise block instead of exposing it. Exposure leaves an outstanding reservation even if the user closes the link. Reconcile the same Bitrefill invoice and, where available, wallet/payment status until actual debit or authoritative unpaid expiry is proven; never create a replacement invoice merely because the human payment outcome is unknown.

### x402 REST ([../touchpoints/x402.md](../touchpoints/x402.md))

- Browse/create/status: JWT (`X-Access-Token`) or x402 micro-fees
- **`invoice/pay`**: always x402 — never JWT-waived
- Select the current challenge's exact atomic amount, asset, and network; never use `price_usd` as a proxy.
- `maxPayment`: format the selected atomic `authorized_minor` as a human-readable decimal with the authoritative asset scale using integer/string operations (`30000000` at USDC scale 6 → `"30"`). Never pass the atomic string directly, use `Number`/rounding, substitute the budget amount, or aggregate fees. Reserve that cap's authoritative budget impact plus separate fee components, then settle the actual debit and release unused authorization; otherwise block.

## Payment method risk

| Method | HITL | Notes |
| --- | --- | --- |
| `balance` two-step REST pay | Lowest | Server-bound invoice total before payment |
| AgentCash / awal x402 | Low (after setup) | Autonomous under caps |
| Base MCP x402 | Medium | 1 Base Account approval per pay |
| Base MCP `send` | Medium | 1 approval per send |
| Phantom / MetaMask | High | Per-sign or per-tx approval |
| `return_payment_link` | Highest | Human browser |

Full enum → <https://docs.bitrefill.com/docs/crypto-payments>.

## Confirm before pay

Present product, denomination, exact payable amount in its actual asset, payment method/network, separate bounded fees, and total budget impact. Wait explicit approval unless the session opted autonomous ([../safeguards.md](../safeguards.md)). The reservation and approval are separate controls; neither replaces the other.

*(say: "[Product] — [face value]: [payable total] [asset] on [network]. [Fees] and [budget impact]. Valid [N] min. Confirm?")*

Invoke `auto_pay`, AgentCash/awal payment, Base `initiate_x402_request` / `complete_x402_request`, Base `send`, manual wallet payment, Lightning, or a payment link only against that reservation and stable record. Apply the route contract above. Release only after authoritative failure, cancellation, or unpaid expiry; payment detection or delivery failure keeps the funds reserved or paid until reconciled.

## Related

- [base-mcp.md](base-mcp.md) — x402 + send
- [siwx.md](siwx.md) — JWT for fee-free browse
- [agentcash.md](agentcash.md), [cdp-awal.md](cdp-awal.md) — autonomous x402
- [phantom.md](phantom.md), [metamask.md](metamask.md) — manual signing

**User hears:** "[Product] — [amount]: [exact total] [payment asset]. Confirm?" → "Approve the payment" → "Your code is ready."
