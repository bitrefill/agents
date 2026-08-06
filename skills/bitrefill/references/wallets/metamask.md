# Wallet: MetaMask

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

**No official MetaMask-branded payment MCP** for agent commerce. Don't confuse with Embedded Wallets MCP (`https://mcp.web3auth.io`) — **docs/SDK help only**, not signing wallet.

## Surfaces

| Surface | Link | Role for Bitrefill |
| --- | --- | --- |
| **MetaMask Agent Wallet (official)** | [docs.metamask.io/agent-wallet](https://docs.metamask.io/agent-wallet/) | `mm` CLI + agent skills |
| Product / Early Access | [metamask.io/agent-wallet](https://metamask.io/agent-wallet) | Guard/Beast modes, spending limits |
| Architecture | [docs.metamask.io/agent-wallet/reference/architecture](https://docs.metamask.io/agent-wallet/reference/architecture/) | Server-wallet TEE; `pollingId` + MFA |
| **Community MetaMask MCP** | [github.com/Xiawpohr/metamask-mcp](https://github.com/Xiawpohr/metamask-mcp) | Browser extension via QR — not autonomous |
| Embedded Wallets MCP | [docs.metamask.io/embedded-wallets/build-with-ai](https://docs.metamask.io/embedded-wallets/build-with-ai/) | **Exclude** from wallet matrix |

## Capabilities (mm CLI)

| Capability | MetaMask mm |
| --- | --- |
| HTTP proxy | **None** — agent orchestrates HTTP |
| x402 | Skill-guided EIP-3009 via `mm wallet sign-typed-data` |
| SIWX | `mm wallet sign-message` |
| HITL | **Confirm every payment**; 2FA on policy violations |
| Base USDC | Yes (multi-EVM) |

## Bitrefill pairing

1. Agent creates an expressly non-paying invoice via Bitrefill MCP / CLI / x402 REST (HTTP from harness) and stores its stable invoice/request ID.
2. Fetch the current x402 402 without an auto-paying client. Validate its exact atomic amount, asset, network, recipient, and authoritative budget impact; never substitute product pricing or `price_usd`.
3. Apply [budget-guard.md](../budget-guard.md) and the [payment route contract](payment.md#route-contract), including any authoritative or safely capped wallet/network fees.
4. Build EIP-3009 typed data → `mm wallet sign-typed-data` → user confirms → agent retries HTTP once under the same record. Reconcile actual wallet debit and Bitrefill payment state; release only unused cap.

Rank **#5–6** in [matrix.md](matrix.md) — not recommended for autonomous checkout.

## Hosts

Codex, Claude Code, OpenClaw, Hermes, Cursor (shell + mm installed).

## vs Base MCP / AgentCash

MetaMask = manual payment confirm per x402. Prefer Base MCP x402 or AgentCash for agent-commerce.

Do not sign or send again after a timeout, lost response, or `payment_detected`; reconcile the stable invoice/payment ID first.

**User hears:** "Approve the payment in your wallet" — never "mm CLI" or tool names
