# Wallet: Coinbase Wallet MCP

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Coinbase Wallet MCP (`https://wallet-mcp.coinbase.com`, formerly Base MCP) — wallet ops + **proxied HTTP** to allowlisted partners, **`api.bitrefill.com`** included — not `docs.bitrefill.com`.

Pair with [../touchpoints/x402.md](../touchpoints/x402.md) (Path 1/2) or Bitrefill MCP invoice pay. Sign-in → [siwx.md](siwx.md).

## Tool split

| Tool | Proxied / remote | Wallet action |
|------|------------------|---------------|
| `web_request` | **Server proxies HTTP** to allowlisted hosts incl. `api.bitrefill.com` | No signing |
| `get_wallets`, `get_portfolio` | Remote read | No |
| `sign` | Remote orchestration | **User approves in Base Account** |
| `send`, `swap`, `send_calls` | Remote orchestration | **User approves each tx** |
| `initiate_x402_request` / `complete_x402_request` | **Server handles x402 handshake** | **User approves each payment** |
| `chain_rpc_request` | Server RPC proxy | No |

## Bitrefill submission table

| Bitrefill step | Tool | User-facing |
| --- | --- | --- |
| Catalog / browse | `web_request` | *(silent — or "Searching…")* |
| Wallet sign-in / codes | `get_wallets`, `sign` | "Sign in with your Base wallet once" |
| Pay x402 REST invoice | x402 tools | "Approve the payment in your Base Account" |
| Pay MCP / CLI invoice | `send` to `payment_info` (EVM tokens) | "Approve the payment in your Base Account" |

All writes need Base Account approval. Poll `get_request_status(requestId)` after approval.

## x402 workflow

x402 buyer supports **Base and Base-Sepolia only**.

1. **Approve payment** — `initiate_x402_request(url, method, maxPayment)` → user approves in Base Account. *(say: "Approve the payment in your Base Account" — tool title: "Approve USDC payment")*
2. User approves in Base Account
3. `complete_x402_request(requestId)` → paid response body. *(silent — poll delivery)*

Micro-fees: `maxPayment: "0.01"`. Invoice pay: `price_usdc`.

## Headers

- **`X-Access-Token`**: raw JWT from connect — **not** `Authorization` (rejected).
- **`sign-in-with-x`**: base64 decomposed SIWX payload — [siwx.md](siwx.md).

## Source of truth

- [Coinbase Wallet MCP](https://docs.cdp.coinbase.com/ai-agents/coinbase-for-agents/wallet-mcp)

**User hears:** "Sign in with your Base wallet once" → "Approve the payment in your Base Account" → "Your code is ready."
