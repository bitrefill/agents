# Wallet: Kite Passport

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Kite AI's agent wallet — `kpass` CLI + skills. Kite holds the wallets and makes the HTTP calls; the user approves spending with a passkey.

Docs: [docs.gokite.ai/passport](https://docs.gokite.ai/passport/install)

## Capabilities

| Capability | Kite Passport |
| --- | --- |
| HTTP proxy | **Yes** — `kpass session execute` |
| x402 | **Automatic** within an allowance or session the user approved |
| SIWX | **Automatic** |
| Send | USDC — `kpass wallet send` |
| HITL | Passkey per allowance, session or send |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| x402 REST Path 1 | `kpass session execute` on the x402 routes; `merchant_not_allowed` → use MCP / CLI |
| Bitrefill MCP / CLI | `buy-products` with a USDC method → `kpass wallet send` to `payment_info.address` |

**User hears:** "Approve the payment with your passkey" → "Your code is ready."
