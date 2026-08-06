# Path: MCP

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

**Preferred purchase channel.** Typed tool calls, OAuth or API key, no shell, 10+ hosts.

## Two MCP servers

### eCommerce MCP — purchases

URL: `https://api.bitrefill.com/mcp` (OAuth) **or** `https://api.bitrefill.com/mcp/YOUR_API_KEY` (key-in-path).

7 tools:

- `search-products` — keyword + country + category
- `get-product-details` — packages (denominations) + pricing
- `buy-products` — create invoice
- `submit-prepayment-step` — multi-step bill-payment forms
- `get-invoice-by-id` — poll status + redemption info
- `list-invoices` — history
- `update-order` — track balance / archive orders

Auth: OAuth (interactive) or API key from <https://www.bitrefill.com/account/developers>.

### Development MCP — docs only

URL: `https://docs.bitrefill.com/mcp`. Docs index for code-help. **Not purchases.** Integration authoring only.

## Per-client setup

### Cursor — `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)

```json
{
  "mcpServers": {
    "bitrefill": {
      "url": "https://api.bitrefill.com/mcp",
      "autoApprove": [
        "search-products", "get-product-details",
        "list-invoices", "get-invoice-by-id"
      ]
    }
  }
}
```

Keep every purchase-capable or state-changing tool, including `buy-products` and `submit-prepayment-step`, **out** of `autoApprove`. 40-tool cap across all servers.

### Claude Code

**bitrefill** plugin from this repo auto-registers eCommerce MCP via `.mcp.json`. Manual setup if plugin not installed:

```bash
claude mcp add bitrefill --url https://api.bitrefill.com/mcp
```

Or edit `~/.claude.json`. Output cap: `MAX_MCP_OUTPUT_TOKENS` (default 25000).

### Claude Desktop — `claude_desktop_config.json`

macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`. Windows: `%APPDATA%\Claude\claude_desktop_config.json`.

```json
{
  "mcpServers": {
    "bitrefill": { "url": "https://api.bitrefill.com/mcp" }
  }
}
```

### Claude.ai (web) — Pro / Max / Team / Enterprise

Settings → Connectors → Add → `https://api.bitrefill.com/mcp`. Free can't add custom URLs.

Harness (MCP-first + `show_widget`) → [../harnesses/claude-chat.md](../harnesses/claude-chat.md).

### ChatGPT (Plus / Pro / Business / Enterprise / Edu)

Settings → Apps & Connectors → Add → `https://api.bitrefill.com/mcp`. **Developer Mode** for `buy-products` (write tool). Free blocked.

### Codex CLI — `~/.codex/config.toml`

```toml
[mcp_servers.bitrefill]
url = "https://api.bitrefill.com/mcp"
bearer_token_env_var = "BITREFILL_API_KEY"
```

OAuth: `codex mcp login bitrefill`.

### Gemini CLI — `~/.gemini/settings.json` (or project `.gemini/settings.json`)

```json
{
  "mcpServers": {
    "bitrefill": {
      "url": "https://api.bitrefill.com/mcp",
      "headers": { "Authorization": "Bearer ${BITREFILL_API_KEY}" }
    }
  }
}
```

OAuth: `gemini mcp auth bitrefill`.

### OpenCode — `opencode.jsonc`

```jsonc
{
  "mcp": {
    "bitrefill": {
      "url": "https://api.bitrefill.com/mcp",
      "headers": { "Authorization": "Bearer ${BITREFILL_API_KEY}" }
    }
  }
}
```

### OpenClaw → [../harnesses/openclaw.md](../harnesses/openclaw.md)

```bash
openclaw mcp add bitrefill --url https://api.bitrefill.com/mcp --transport streamable-http --auth oauth --include 'search-products,get-product-details,list-invoices,get-invoice-by-id'
openclaw mcp login bitrefill
openclaw mcp doctor bitrefill --probe
```

Capability-probe first: these subcommands require a build whose `openclaw mcp --help` lists `add`, `login`, and `doctor`. On older builds use the JSON definition in [openclaw.md](../harnesses/openclaw.md), restart, and keep MCP disabled unless OAuth and the exact read-only tool allowlist can be verified.

## Workflow

Apply [the session budget guard](../budget-guard.md) before `buy-products`, any `submit-prepayment-step` that can commit a purchase, and every later payment call. `get-product-details` supplies estimates only. For balance, use REST `auto_pay: false` then pay that same pre-reserved invoice, but only when direct REST egress and an authorized REST credential are available; MCP OAuth alone does not provide that route. Otherwise skip balance. Block `cashback` unless its exact pre-call total and debit semantics are authoritative. Never create a second invoice merely to change payment method.

```
search-products  →  get-product-details  →  buy-products  →  get-invoice-by-id
```

1. **Search** — `search-products(...)`. *(say: "Searching for [product]…" — tool title: "Search gift cards")*
2. **Get estimate** — `get-product-details(..., currency="USDC")`; use it to validate product and denomination, but do not call it the exact payable total. *(silent)*
3. **Establish terms** — after a coarse budget check, create one non-balance, non-paying invoice with `buy-products` under a proposed attempt; attach its invoice ID and withhold its payment instrument. For balance, create one REST `auto_pay: false` invoice when that capability exists. Max 15 items. *(silent)*
4. **Confirm, reserve, and pay once** — show every exact invoice/challenge component and total budget impact, reserve them under that attempt, then [pay](../wallets/payment.md). Settle authoritative actual debits and release only unused authorization. *(say: "[Product] — [amount]: [payable total] [asset]. Confirm?")*
5. **Reconcile and deliver** — `get-invoice-by-id` until payment and delivery state are authoritative; settle the actual debit or release an authoritatively unpaid reservation once. *(say: "Your code is ready.")*

Record the purchase in the session-local ledger per [../safeguards.md](../safeguards.md).

## Caveats

- **ChatGPT** custom MCP needs Plus+; write tools need Developer Mode (admin on workspaces).
- **Cursor** 40-tool cap.
- **Claude.ai** consumer needs Pro+ for custom URLs.
- **Claude Chat network:** sandbox egress varies by plan; **MCP connectors work regardless**. Legacy Analysis tool (browser JS) has no net. Route Bitrefill via MCP — not sandbox curl. → [../harnesses/claude-chat.md](../harnesses/claude-chat.md) §3.

## Source of truth

- <https://docs.bitrefill.com/docs/ecommerce-mcp> | <https://docs.bitrefill.com/docs/development-mcp> | <https://docs.bitrefill.com/docs/setup-guides>
- Per-client: <https://docs.bitrefill.com/docs/use-with-cursor>, `/use-with-claude-chat`, `/use-with-claude-code`, `/use-with-chatgpt`

**User hears:** "Searching for [product]…" → "[Product] — [amount]: [exact total] [payment asset]. Confirm?" → "Approve the payment" → "Your code is ready."
