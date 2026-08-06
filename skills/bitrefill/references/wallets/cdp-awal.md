# Wallet: Coinbase CDP (awal)

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Coinbase Agentic Wallet — TEE-backed signing, configurable spending caps. Strong autonomous x402 under limits.

Docs: [docs.cdp.coinbase.com/agentic-wallet](https://docs.cdp.coinbase.com/agentic-wallet/welcome)

## Surfaces

| Surface | Use |
| --- | --- |
| `npx awal x402 pay <url>` | CLI x402 buyer from shell |
| `@coinbase/payments-mcp` | Guarded payment blocked unless its current tool schema proves a per-call cap bound to the reserved challenge |
| AgentKit `@x402/fetch` | Guarded payment blocked unless a wrapper proves live-challenge validation and a per-call cap bound to this reservation |

## Capabilities

| Capability | CDP awal |
| --- | --- |
| HTTP proxy | Agent/shell makes HTTP; awal wraps x402 pay |
| x402 | **Auto within session/tx caps** |
| SIWX | Manual in agent code (or Bitrefill JWT path via Base MCP) |
| Keys | Remote TEE — agent never holds keys |
| Base USDC | Yes (+ Polygon, Solana x402) |
| HITL | Email OTP auth once; autonomous under caps |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| x402 REST | `awal x402 pay` only after the current challenge terms, fees, and stable request ID are known and reserved |
| MCP/CLI invoice | Pay a known `x402_payment_url` only after its current challenge terms and fees are reserved |

Rank **#3** in [matrix.md](matrix.md).

## Setup

1. CDP Agentic Wallet auth (email OTP).
2. Set session + per-transaction spending limits.
3. Fund USDC on Base within a small independent wallet cap; it is not the session budget.

## Hosts

Codex CLI, OpenClaw (`exec`), Hermes (`terminal`), any shell host.

## Example

```bash
# After a non-paying 402 inspection and exact component reservations:
npx awal x402 pay "<x402_payment_url>" \
  --max-amount <authorized_usdc_minor> \
  --correlation-id "<attempt_id>"
```

Invoice pay: URL/method/body from 402 envelope or `x402_payment_url`.

## Security

- Caps = primary blast-radius control.
- Never unlimited awal caps on production accounts.
- Apply [budget-guard.md](../budget-guard.md) and the [payment route contract](payment.md#route-contract) before every automatic payment. Do not probe a paid route through `awal` when it can pay before exposing the exact atomic asset amount and stable identifier; use a non-paying client or block.
- Pass `--max-amount` as the selected USDC authorization in 6-decimal atomic units—not budget currency or fees. A changed higher challenge must fail, then be re-priced and re-confirmed. Reconcile the actual wallet debit and invoice/payment state after one call; never retry automatically after a timeout or lost response.
- Prefer the CLI route above. A wallet-UI transaction/session limit is not the purchase reservation. Do not call Payments MCP `make-x402-request` unless the live schema provides and the client enforces a per-call payable cap no greater than this attempt's reserved challenge; otherwise a changed challenge could auto-pay up to the broader wallet limit, so block. Apply the same rule to AgentKit `@x402/fetch`: without a reviewed wrapper that rejects any changed asset, network, destination, or amount and enforces that cap before signing, do not use it for guarded payment.

**User hears:** "[Product] — [amount]: [total] USDC. Confirm?" → "Your code is ready." (never "awal" or "x402")
