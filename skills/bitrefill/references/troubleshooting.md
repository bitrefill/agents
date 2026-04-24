# Troubleshooting

Common errors across all paths. Full enum: <https://docs.bitrefill.com/docs/error-codes> and <https://docs.bitrefill.com/docs/References>.

## Browse path

### `403 Forbidden` when fetching bitrefill.com

Cloudflare blocks datacenter IPs. Fix: switch to residential browser (ChatGPT Atlas, Cursor browser, Claude+Chrome ext, OpenClaw on user host) or pivot to MCP/CLI/API.

### Product appears in listing but not purchasable

Geolock at IP level. URL country only filters listed inventory; checkout enforces user's IP. Tell user to access from the matching country (or VPN) — but warn this may violate ToS.

## MCP path

### Tool not visible to agent

- Cursor: 40-tool cap exceeded across all servers. Disable an unused MCP server.
- ChatGPT: Developer Mode off → write tools (`buy-products`) hidden. Toggle in Settings.
- Claude.ai consumer: Free tier cannot add custom MCP URLs. Upgrade to Pro+.
- OpenClaw: `tools.deny: ["bundle-mcp"]` accidentally hiding the server, or per-agent `tools.allow` whitelist excluding it.

### `StreamableHTTPError` with HTML body

Wrong `MCP_URL` — pointing at non-Bitrefill endpoint. Unset `MCP_URL` env var or set to `https://api.bitrefill.com/mcp`.

### OAuth loop in Cursor / Claude.ai

Clear browser cookies for `bitrefill.com`, try a different browser, ensure pop-ups not blocked.

### MCP server filtered out (OpenClaw)

OpenClaw startup safety filter rejects env keys: `NODE_OPTIONS`, `PYTHONSTARTUP`, `PYTHONPATH`, `PERL5OPT`, `RUBYOPT`, `SHELLOPTS`, `PS4`. Use only standard `*_API_KEY` / `GITHUB_TOKEN` / proxy vars in MCP server `env` blocks.

### MCP output truncated

Default cap varies by host. Claude Code: `MAX_MCP_OUTPUT_TOKENS=50000` to raise. OpenClaw: `tools.toolResultMaxChars` (default 16000). Use pagination: `--per_page 25`, multiple `list-orders` calls.

## CLI path

### `cart_items` JSON shape error

```
# WRONG (object)
--cart_items '{"product_id": "steam-usa", "package_id": 5}'

# RIGHT (array)
--cart_items '[{"product_id": "steam-usa", "package_id": 5}]'
```

### `Invalid denomination 'undefined'`

Both `product_id` AND `package_id` required per item.

### `Too big: expected array to have <=15 items`

Split into multiple `buy-products` calls.

### `per_page must be less than 500`

Server limit. Use 500 max.

### `error: required option '--<name>' not specified`

Client-side validation. Add the missing option.

### "Must be one of" enum errors

| Option | Valid values | Common mistakes |
|--------|--------------|-----------------|
| `--payment_method` | `bitcoin`, `lightning`, `ethereum`, `usdc_polygon`, `usdt_polygon`, `usdc_erc20`, `usdt_erc20`, `usdc_arbitrum`, `usdc_solana`, `usdc_base`, `eth_base`, `balance` | `paypal`, `visa`, `USDC_BASE` (case-sensitive) |
| `--product_type` | `giftcard`, `esim` | `giftcards`, `gift_card`, `sim` |
| `--country` | `US`, `IT`, `BR` (uppercase Alpha-2) | `us`, `USA`, `"United States"` |

### Wrong `package_id` for named denominations

Exact, case-sensitive. WRONG `"1GB"`, `"300 nc"`. RIGHT `"1GB, 7 Days"`, `"PUBG New State 300 NC"`. Get exact strings from `get-product-details` `packages` array.

### Compound key in `package_id`

```
# WRONG
--cart_items '[{"product_id": "steam-usa", "package_id": "steam-usa<&>5"}]'

# RIGHT (value after <&>)
--cart_items '[{"product_id": "steam-usa", "package_id": 5}]'
```

### OAuth hang or auth failure

```bash
export BITREFILL_API_KEY=YOUR_API_KEY   # switch to headless
# or
bitrefill logout                          # clear stale OAuth
```

Cred file: `~/.config/bitrefill-cli/api.bitrefill.com.json`.

### Empty search results, no error

`found: 0` with no error message. Causes:

- `--category` slug doesn't exist (silent miss).
- Product not available in `--country`.
- `--in_stock true` (default) filters out-of-stock.

Fix: drop `--category`, change `--country`, or `--in_stock false`.

### Unpaid invoices missing from list

`list-invoices` defaults `--only_paid true`. Use `--only_paid false`.

## API path

### `401 Unauthorized`

- Personal: `Authorization: Bearer $BITREFILL_API_KEY` missing or wrong key.
- Business / Affiliate: `Authorization: Basic $(echo -n "$ID:$SECRET" | base64)` malformed.

### `429 Too Many Requests`

Rate limited. Defaults: 60 req / 10 min on most endpoints, 60 req/min on `/products` + `/products/search` plus 1000 product req/hr quota, 1 req / 3 s on `/ping`. Back off + retry. Cache product catalog locally.

### `RESOURCE_NOT_FOUND` on `GET /invoices/{id}`

Bad invoice ID. Verify via `list-invoices`.

### `Product '{slug}' is not available`

Bad product slug. Verify via `search-products`.

### Invoice expired

Invoices expire after **180 minutes**. Cannot re-pay. Create new one.

## OpenClaw-specific

### Cron purchase failed silently

`exec-approvals.json` set to `ask: on-miss` but no operator online to `/approve`. Either pre-approve `bitrefill buy-products` for trusted SKU/amount, or schedule when operator available.

### Pi agent can't see the Bitrefill MCP

Check:

1. `openclaw mcp list` shows entry.
2. `~/.openclaw/openclaw.json` parses (no trailing commas).
3. Agent profile not denying `bundle-mcp` or whitelisting tools narrowly.
4. `BITREFILL_API_KEY` env var set in Gateway environment, not just current shell.

### Mobile node camera tool unavailable

Node not paired or paired but offline. Check `openclaw nodes list`. Re-pair via Control UI (`openclaw dashboard`).

### Telegram message not reaching agent

`channels.telegram.dmPolicy: "pairing"` and sender not paired. Run `openclaw pairing approve telegram <CODE>` (codes expire 1 hr).

## Source of truth

- Bitrefill error codes: <https://docs.bitrefill.com/docs/error-codes>
- Bitrefill error handling: <https://docs.bitrefill.com/docs/References>
- Rate limits: <https://docs.bitrefill.com/docs/rate-limits>
- OpenClaw troubleshooting: <https://docs.openclaw.ai/help> + per-tool pages
