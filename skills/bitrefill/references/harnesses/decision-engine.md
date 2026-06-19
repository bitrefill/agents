# Decision Engine

Capability-driven Bitrefill routing. Probe harness + wallets → touchpoint + payment stack. **Lowest HITL wins.**

Per-host defaults → [capability-matrix.md](capability-matrix.md). Wallet ranking → [../wallets/matrix.md](../wallets/matrix.md).

## Step 0 — Intent

- Browse-only vs purchase
- Bitrefill account (OAuth / signed-in CLI) vs guest agent-commerce (USDC Base, no signup)

## Step 1 — Probe harness

```
exec_available      = shell | exec | terminal | WebFetch+curl
egress_direct       = agent HTTP to api.bitrefill.com without MCP proxy
egress_mcp_proxy    = Base MCP web_request → api.bitrefill.com (hybrid plugin)
egress_none         = chat-only; sandbox no outbound net
browser_residential = user-network browser (not datacenter)
bitrefill_mcp_live  = search-products / buy-products visible (OAuth or API key)
base_mcp_live       = get_wallets / web_request / initiate_x402_request visible
```

**Claude Chat — two network layers:** (1) **Code sandbox** — plan/admin controlled (Team default: package mgrs only; Enterprise: off; Free/Pro/Max: user toggle). Default allowlist **excludes** `api.bitrefill.com`. (2) **Chat MCP** — works **regardless of sandbox egress**. Route Bitrefill API via MCP, not sandbox code.

**Legacy Analysis tool** (browser JS, no net) mutually exclusive with code execution — ignore if code execution on.

ChatGPT Code Interpreter: **no sandbox egress**. Base MCP `web_request` proxies `api.bitrefill.com` even when agent can't curl.

## Step 2 — Probe wallets

```
wallet_agentcash    = AgentCash fetch + local key
wallet_cdp          = CDP awal CLI or @coinbase/payments-mcp
wallet_base_mcp     = Base MCP sign + x402 + send
wallet_metamask     = mm CLI agent wallet
wallet_phantom      = Phantom MCP evm_sign / evm_send
wallet_none         = payment_link / human browser only
bitrefill_balance   = signed-in MCP/CLI with pre-funded balance
```

## Step 3 — Derive touchpoint

| Condition | Touchpoint |
|-----------|------------|
| `bitrefill_mcp_live` | [../touchpoints/mcp.md](../touchpoints/mcp.md) |
| `!bitrefill_mcp_live` ∧ (`egress_mcp_proxy` ∨ `egress_direct`) ∧ guest/USDC | [../touchpoints/x402.md](../touchpoints/x402.md) Path 1 (JWT) |
| `exec_available` ∧ `!bitrefill_mcp_live` | [../touchpoints/cli.md](../touchpoints/cli.md) |
| `egress_direct` ∧ no MCP | [../touchpoints/api.md](../touchpoints/api.md) |
| browse-only ∧ `browser_residential` | [../touchpoints/browse.md](../touchpoints/browse.md) |
| else | send user `bitrefill.com` link |

**OpenClaw override:** detect first → [openclaw.md](openclaw.md). Guest CLI via `exec` before MCP when no OAuth.

**Claude Chat override:** claude.ai + `show_widget` + MCP → [claude-chat.md](claude-chat.md). MCP-first; no shell/CLI/scripts; shopping UI via `show_widget`.

**Triple-MCP (Bitrefill + Base + Phantom):** Bitrefill MCP catalog/checkout when OAuth'd → Base MCP x402 pay → Phantom sign-only if Phantom is payer (HTTP via Base MCP or Bitrefill MCP).

## Step 4 — Derive wallet (pay time)

Global autonomy rank ([../wallets/matrix.md](../wallets/matrix.md)):

1. **`bitrefill_balance`** → `balance` + `auto_pay: true`
2. **`wallet_agentcash` or `wallet_cdp`** → x402 on `x402_payment_url` or x402 REST `invoice/pay`
3. **`wallet_base_mcp`** → `initiate_x402_request` / `complete_x402_request`; else `send` to `payment_info`
4. **x402 REST Path 1** → SIWX via [../wallets/siwx.md](../wallets/siwx.md) + [../wallets/base-mcp.md](../wallets/base-mcp.md) or AgentCash
5. **Never Path 2** if Path 1 JWT possible

Details → [../wallets/payment.md](../wallets/payment.md).

## When capabilities conflict

| Situation | Resolution |
|-----------|------------|
| ChatGPT sandbox no net + Base MCP yes | Base MCP `web_request` for x402 REST; ignore sandbox for API |
| Bitrefill MCP OAuth'd + Base MCP yes | Bitrefill MCP catalog; Base MCP x402 for `usdc_base` pay |
| Bitrefill MCP OAuth'd + Phantom yes | Bitrefill MCP + balance/x402; Phantom only if user wants Phantom as payer |
| Base MCP yes, no Bitrefill MCP | x402 REST Path 1 via Base MCP (ChatGPT+ dual connector) |
| Phantom yes, no HTTP proxy | Don't use Phantom for API — pair with Base MCP or Bitrefill MCP |

## Autonomy-ranked stacks (global)

| Rank | Touchpoint | Wallet | Residual HITL |
|------|------------|--------|---------------|
| 1 | Bitrefill MCP | `balance` + `auto_pay` | Purchase confirm only |
| 2 | x402 REST Path 1 | AgentCash `fetch` | Fund once + confirm |
| 3 | x402 REST Path 1 | CDP awal (caps set) | Auth + caps once |
| 4 | Bitrefill MCP | Base MCP x402 | OAuth + 1 Base approval/pay |
| 5 | x402 REST Path 1 | Base MCP | 1 SIWX + 1 pay / ~2h JWT |
| 6 | CLI guest | AgentCash / awal / Base MCP | Shell + payment as above |
| 7 | Bitrefill MCP | Base MCP `send` | OAuth + 1 send/pay |
| 8 | x402 REST Path 2 | Any x402 | Approval per micro-fee |
| 9 | CLI / MCP | payment_link / Lightning | Human completes pay |
| 10 | Browse | Human browser | Full checkout UI |

**Avoid autonomous agents:** x402 Path 2 (per-search fees), MetaMask per-tx confirm, Phantom per-tx simulation, payment links alone.
