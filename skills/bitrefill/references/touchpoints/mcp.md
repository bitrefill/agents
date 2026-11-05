# Touchpoint: MCP

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

**Preferred purchase channel.** Typed tool calls, OAuth or API key, no shell, 10+ hosts.

## Two MCP servers

### eCommerce MCP — purchases

URL: `https://api.bitrefill.com/mcp`, authenticated by OAuth **or** an API key in the `Authorization: Bearer <api key>` header. Never put the key in the URL (`/mcp/<key>` returns 410).

12 tools; **(g)** = visible to guests (7), the other 5 need a signed-in account:

- `search-products` **(g)** — keyword + country (default `US`) + category + `product_type` (`giftcard` | `esim` | `refill`); **`intent` required**, non-empty: the user's broad goal, context only (results unchanged)
- `get-product-details` **(g)** — packages (`package_value`, `package_currency`, `payment_price`, `payment_currency`) + `payment_methods` + `recipient_type`
- `buy-products` **(g)** — create invoice: `cart_items[]` (≤ 15) {`product_id`, `package_value` (string); `refill_input` per `recipient_type` (`phone_number`: country code + number, digits only, e.g. `4915123456789`; `mixed` eSIMs: omit for a new eSIM); `bill_payment_id` for prepayment products; optional `gift`} + `payment_method` + optional `coupon_code`. Fiat methods (`fiat_card`, `apple_pay`, `google_pay`, `ideal`, `eps`, `p24`, `bancontact`) take `billing_address` (country always; `fiat_card` also city, postal_code, address_line1), or signed-in `saved_fiat_card_id` with `fiat_card`, and return a `payment_link` only. `balance` takes optional `balance_currency` (USD / EUR / BTC) and debits at once. `package_id` deprecated. Guests also pass `email` (receipt); signed-in receipts go to the account email
- `submit-prepayment-step` — prepayment forms (bill payments, prepaid cards): loop until `step: "final"`, then pass its `billPaymentId` as `bill_payment_id`
- `get-invoice-by-id` **(g)** — poll status + redemption info. Guest: pass `invoice_access_token` from `buy-products` (required, else "not found"; together with `invoice_id` it unlocks the codes, so treat it like a password). Signed-in: your own invoices need no token
- `list-invoices` — paid-invoice history, newest first (no codes; `limit` ≤ 20, page with `next`)
- `update-order` — track balance / archive orders
- `get-balances` — store credit per sub-account (USD / EUR / BTC) + cashback; check it before paying by `balance`
- `list-saved-fiat-cards` — saved cards → `saved_fiat_card_id`
- `search_help_articles` **(g)** → `get_help_article` **(g)** — help center. `list_help_articles` **(g)** returns no articles: browse a topic by searching with `category`

Auth: OAuth (interactive) or API key from <https://www.bitrefill.com/account/developers> sent as the Bearer header.

### Development MCP — docs only

URL: `https://docs.bitrefill.com/mcp`. Docs index for code-help. It can also send API requests: never give it an API key or use it for orders or invoices.

## Per-client setup

### Cursor / Grok Bot

**Bitrefill** plugin (Cursor: **Customize**; Grok Bot: **Connect apps**) bundles eCommerce MCP via `.mcp.json`; sign in when asked (Cursor CLI: `agent mcp login <id>`, id from `agent mcp list`). Manual setup if plugin not installed — `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "bitrefill": { "url": "https://api.bitrefill.com/mcp" }
  }
}
```

Keep `buy-products` **out** of every allowlist → [../safeguards.md](../safeguards.md) § Cursor / Grok Bot.

### Claude Code

**bitrefill** plugin from this repo auto-registers eCommerce MCP via `.mcp.json`. Manual setup if plugin not installed:

```bash
claude mcp add --transport http bitrefill https://api.bitrefill.com/mcp
# API key instead of OAuth:
claude mcp add --transport http bitrefill https://api.bitrefill.com/mcp --header "Authorization: Bearer $BITREFILL_API_KEY"
```

OAuth: `/mcp` → bitrefill → Authenticate. Output cap: `MAX_MCP_OUTPUT_TOKENS` (default 25000).

### Claude Desktop

Settings → Connectors → Add custom connector → `https://api.bitrefill.com/mcp` (OAuth). Remote servers are connectors, not `claude_desktop_config.json` entries.

### Claude.ai (web) — Pro / Max / Team / Enterprise

Settings → Connectors → Add → `https://api.bitrefill.com/mcp`. Free can't add custom URLs.

Harness (MCP-first + `show_widget`) → [../harnesses/claude-chat.md](../harnesses/claude-chat.md).

### ChatGPT / Codex plugins

Install the Bitrefill plugin from your available plugin source and connect your Bitrefill account when prompted. The portable package uses root `plugin.json` and `mcp.json`; older Codex clients can use `.codex-plugin/plugin.json` and `.mcp.json`. Access depends on the host and workspace policy. For a custom development connection, use `https://api.bitrefill.com/mcp` with the host's current MCP connection flow. Never ask users to paste account credentials into chat.

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
      "httpUrl": "https://api.bitrefill.com/mcp",
      "headers": { "Authorization": "Bearer ${BITREFILL_API_KEY}" }
    }
  }
}
```

`httpUrl` = streamable HTTP (`url` selects the SSE transport). OAuth: run `/mcp auth bitrefill` inside Gemini CLI (omit `headers`).

### OpenCode — `opencode.jsonc`

```jsonc
{
  "mcp": {
    "bitrefill": {
      "type": "remote",
      "url": "https://api.bitrefill.com/mcp",
      "headers": { "Authorization": "Bearer {env:BITREFILL_API_KEY}" }
    }
  }
}
```

OAuth: `opencode mcp auth bitrefill` (omit `headers`).

### OpenClaw → [../harnesses/openclaw.md](../harnesses/openclaw.md)

```bash
openclaw mcp set bitrefill '{"url":"https://api.bitrefill.com/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login bitrefill
```

API key instead of OAuth: drop `"auth"`, add `"headers":{"Authorization":"Bearer ${BITREFILL_API_KEY}"}`.

## Workflow

```
search-products  →  get-product-details  →  buy-products  →  get-invoice-by-id
```

1. **Search** — `search-products(..., intent=<user's goal>)`. *(say: "Searching for [product]…" — tool title: "Search gift cards")*
2. **Get price** — `get-product-details(..., currency="USDC")` (card / Apple Pay / Google Pay: `USD`; iDEAL / EPS / P24 / Bancontact: `EUR`) → total = `packages[].payment_price` summed per cart line, never the face value. *(silent)*
3. **Prepare order** — `buy-products(...)`. Max 15 items. Confirm with user first (top-ups: with the recipient number). *(say: "[Product] — [amount]: [total] USDC. Confirm?")*
4. **Pay** → [../wallets/payment.md](../wallets/payment.md): `balance` (debits at once) → wallet send → payment link. *(say: "Approve the payment in your wallet")*
5. **Deliver** — `get-invoice-by-id` until complete. *(say: "Your code is ready.")*

Logging per [../safeguards.md](../safeguards.md).

## Caveats

- **ChatGPT / Codex** plugin and custom-MCP access depends on the current surface, account and workspace policy. Inspect actual tool access rather than assuming availability from a plan name.
- **Claude.ai** consumer needs Pro+ for custom URLs.
- **Claude Chat network:** route Bitrefill via MCP, not sandbox curl → [../harnesses/claude-chat.md](../harnesses/claude-chat.md) §4.

## Source of truth

- <https://docs.bitrefill.com/docs/ecommerce-mcp> | <https://docs.bitrefill.com/docs/development-mcp> | <https://docs.bitrefill.com/docs/setup-guides>
- Per-client: <https://docs.bitrefill.com/docs/use-with-cursor>, `/use-with-claude-chat`, `/use-with-claude-code`, `/use-with-chatgpt`

**User hears:** "Searching for [product]…" → "[Product] — [amount]: [total] USDC. Confirm?" → "Approve the payment in your wallet" → "Your code is ready."
