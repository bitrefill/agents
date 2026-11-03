# Wallet: Tether WDK

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Tether's self-custodial multi-chain wallet — `wdk` CLI and `wdk-mcp`. Keys stay on the machine; the human unlocks the wallet for a set time.

Docs: [docs.wdk.tether.io/cli](https://docs.wdk.tether.io/cli/)

## Capabilities

| Capability | Tether WDK |
| --- | --- |
| HTTP proxy | **None** |
| x402 | **None** |
| Send | USDT (incl. Tron), bitcoin, Lightning, native coins — MCP `send_token` or `wdk send` |
| Keys | Local, encrypted |
| HITL | None per send while unlocked |

## Bitrefill pairing

| Touchpoint | Flow |
| --- | --- |
| Bitrefill MCP / CLI | `buy-products` with a coin the wallet holds (e.g. `usdt_trc20`, `bitcoin`) → send the `payment_info` amount to its address (MCP `send_token` previews until `dryRun: false`) |

**User hears:** "[Product] — [amount]: [total] [coin]. Confirm?" → "Your code is ready."
