# Wallet: MetaMask

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

**No official MetaMask-branded payment MCP** for agent commerce. Don't confuse with Embedded Wallets MCP (`https://mcp.web3auth.io`) — **docs/SDK help only**, not signing wallet.

## Surfaces

| Surface | Link | Role for Bitrefill |
| --- | --- | --- |
| **MetaMask Agent Wallet (official)** | [docs.metamask.io/agent-wallet](https://docs.metamask.io/agent-wallet/) | `mm` CLI + agent skills |
| Product / Early Access | [metamask.io/agent-wallet](https://metamask.io/agent-wallet) | Guard/Beast modes, spending limits |
| Architecture | [docs.metamask.io/agent-wallet/reference/architecture](https://docs.metamask.io/agent-wallet/reference/architecture/) | Server-wallet TEE; `pollingId` + MFA |
| Embedded Wallets MCP | [docs.metamask.io/embedded-wallets/build-with-ai](https://docs.metamask.io/embedded-wallets/build-with-ai/) | **Exclude** from wallet matrix |

## Capabilities (mm CLI)

| Capability | MetaMask mm |
| --- | --- |
| HTTP proxy | **None** — agent orchestrates HTTP |
| x402 | Skill's bundled x402 pay script |
| Send | EVM tokens — `mm transfer` |
| SIWX | `mm wallet sign-message` |
| HITL | **Confirm every payment**; 2FA on policy violations |
| Base USDC | Yes (multi-EVM) |

## Bitrefill pairing

1. **x402 REST** — the skill's x402 pay script pays `invoice/pay` after the user confirms; sign-in via `mm wallet sign-message`.
2. **Bitrefill MCP / CLI** — `buy-products` with an EVM method → `mm transfer` to `payment_info.address` → user confirms.

## Hosts

Codex, Claude Code, OpenClaw, Hermes, Cursor (shell + mm installed).

## vs Coinbase Wallet MCP / AgentCash

MetaMask = user confirms each payment, like Coinbase Wallet MCP. AgentCash pays without per-payment approval.

**User hears:** "Approve the payment in your wallet" — never "mm CLI" or tool names
