# Path: MCP

**Preferred purchase channel.** Typed tool calls, OAuth or API key, no shell, works in 10+ hosts.

## Two MCP servers

### eCommerce MCP — for purchases

URL: `https://api.bitrefill.com/mcp` (OAuth) **or** `https://api.bitrefill.com/mcp/YOUR_API_KEY` (header-less, key-in-path).

7 tools:

- `search-products` — keyword + country + category
- `product-details` — packages (denominations) + pricing
- `buy-products` — create invoice
- `get-invoice-by-id` — poll payment status
- `get-order-by-id` — get redemption info (codes, eSIM QR)
- `list-invoices` — invoice history
- `list-orders` — order history

Auth: OAuth (recommended for interactive use) or API key from <https://www.bitrefill.com/account/developers>.

### Development MCP — for docs only

URL: `https://docs.bitrefill.com/mcp`. Indexes the docs site for code-help. **Not for purchases.** Use only when authoring an integration against the Bitrefill API/CLI.

## Per-client setup

### Cursor — `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)

```json
{
  "mcpServers": {
    "bitrefill": {
      "url": "https://api.bitrefill.com/mcp",
      "autoApprove": [
        "search-products", "product-details",
        "list-invoices", "get-invoice-by-id",
        "list-orders", "get-order-by-id"
      ]
    }
  }
}
```

Keep `buy-products` **out** of `autoApprove`. Cursor caps at 40 active tools across all servers.

### Claude Code

With the **bitrefill** plugin installed from this repo’s marketplace, the eCommerce MCP is auto-registered; `claude mcp add` below is for manual-only setups.

```bash
claude mcp add bitrefill --url https://api.bitrefill.com/mcp
```

Or edit `~/.claude.json`. Override output cap with `MAX_MCP_OUTPUT_TOKENS` (default 25 000).

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

Settings → Connectors → Add custom connector → URL `https://api.bitrefill.com/mcp`. Free tier cannot add custom URLs.

### ChatGPT (Plus / Pro / Business / Enterprise / Edu)

Settings → Apps & Connectors → Add → URL `https://api.bitrefill.com/mcp`. Toggle **Developer Mode** to allow `buy-products` (write tool). Free tier blocked.

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

### OpenClaw — see [host-openclaw.md](host-openclaw.md)

```bash
openclaw mcp set bitrefill --url "https://api.bitrefill.com/mcp/$BITREFILL_API_KEY"
```

## Workflow

```
search-products  →  product-details  →  buy-products  →  get-invoice-by-id  →  get-order-by-id
```

1. **Search**: `search-products(query="Steam", country="US", product_type="giftcard")`. `country` is uppercase Alpha-2.
2. **Details**: `product-details(product_id="steam-usa", currency="USDC")`. Returns `packages` array with `package_id` in form `{product_id}<&>{value}`.
3. **Buy**: `buy-products(cart_items=[{product_id, package_id}], payment_method, return_payment_link=true)`. Max 15 items per call.
   - For instant fulfillment: `payment_method: "balance"` + `auto_pay: true`.
   - For agent-driven crypto: `payment_method: "usdc_base"` + `return_payment_link: true` → use `x402_payment_url`.
4. **Poll**: `get-invoice-by-id(invoice_id)`. Statuses: `unpaid` → `payment_detected` → `payment_confirmed` → `complete`.
5. **Redeem**: `get-order-by-id(order_id, include_redemption_info=true)` → returns code / link / eSIM install URL.

Confirm with user before step 3. Logging per [safeguards.md](safeguards.md).

## Caveats

- **ChatGPT** custom MCP requires Plus+; write tools require Developer Mode (admin-enabled on workspaces).
- **Cursor** 40-tool cap across all servers.
- **Claude.ai** consumer needs Pro+ for custom URLs.
- **Code-execution sandboxes** (Claude.ai analysis tool, ChatGPT Code Interpreter) have **no network egress** — they can't call MCP servers; install MCP at the chat level instead.

## Source of truth

- <https://docs.bitrefill.com/docs/ecommerce-mcp>
- <https://docs.bitrefill.com/docs/development-mcp>
- <https://docs.bitrefill.com/docs/setup-guides>
- Per-client setup: <https://docs.bitrefill.com/docs/use-with-cursor>, `/use-with-claude-chat`, `/use-with-claude-code`, `/use-with-chatgpt`
