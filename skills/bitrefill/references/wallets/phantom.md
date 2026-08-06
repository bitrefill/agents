# Wallet: Phantom MCP

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Official Phantom embedded wallet MCP for agent signing. **No HTTP proxy** — pair with Bitrefill MCP or Base MCP for API calls.

Docs: [docs.phantom.com/phantom-mcp-server](https://docs.phantom.com/phantom-mcp-server)

## Tools (representative)

| Tool | Role |
| --- | --- |
| `wallet_status` | Session check (no re-auth) |
| `wallet_addresses` | Solana, Ethereum (incl. Base), Bitcoin, Sui |
| `wallet_balances` | Token balances — **may fail MCP schema validation** (known issue) |
| `evm_sign` | EIP-191 `personal_sign` — SIWX |
| `evm_sign-typed` | EIP-712 — x402 EIP-3009 |
| `evm_send` | EVM tx — simulation preview, then `confirmed: true` |
| `simulate` | Tx/message preview without sending |
| `pay` | **Phantom API quota only** — not generic x402 HTTP |

## Capabilities

| Capability | Phantom MCP |
| --- | --- |
| HTTP proxy | **None** |
| x402 buyer | **None** — manual typed-data + agent HTTP retry |
| SIWX | `evm_sign` (chainId `8453` for Base) |
| HITL | `evm_send` requires simulation + `confirmed: true` |
| Base USDC | Yes via EVM address |

## Bitrefill pairing

**Paired-MCP pattern (Cursor):**

1. **Bitrefill MCP** — catalog + expressly non-paying invoice when OAuth'd; store its stable invoice/request ID.
2. **Base MCP payer (preferred)** — inspect the current x402 challenge, apply [budget-guard.md](../budget-guard.md) and the [payment route contract](payment.md#route-contract), then use the Base x402 tools. Base—not Phantom—is then the payer and must sign any later payer-only request.
3. **Phantom payer fallback** — use a non-paying HTTP client for the current challenge, reserve it under the invoice record, sign its typed data with Phantom `evm_sign-typed`, and retry HTTP once. Use Phantom `evm_sign` for payer-only SIWX afterward.

Don't use Phantom `pay` for Bitrefill x402.

Rank **#7** in [matrix.md](matrix.md) — sign-only fallback.

## Smoke-tested (Cursor)

| Test | Result |
| --- | --- |
| `wallet_status` | Connected |
| `wallet_addresses` | EVM address returned |
| `evm_sign` (Base, test message) | Signature returned |
| `wallet_balances` networks=`base` | Schema validation error (server-side) |

## Security

- Agent embedded wallet — not user's main Phantom extension.
- Confirm every on-chain send after simulation preview. For a direct send, validate the current invoice recipient, exact amount, asset, and network; reserve its authoritative budget impact plus a safe simulated network/wallet fee cap under the invoice ID before `confirmed: true`.
- For manual x402 signing, reserve the selected challenge's exact atomic asset amount and bounded fees, never `price_usd`; send/retry once, then reconcile actual wallet debit and Bitrefill status under the same record. A timeout or transaction hash never authorizes another send.
- Never deliver redemption codes via voice/TTS.

## vs Base MCP

Base MCP proxies Bitrefill HTTP + x402 buyer. Phantom signs only — higher orchestration burden. Prefer Base MCP for pay when both available.

**User hears:** "Approve in your wallet" / "Approve the payment" — never "evm_sign" or "SIWX"
