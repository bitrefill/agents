# Troubleshooting

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Common errors all paths. Full enum: <https://docs.bitrefill.com/docs/error-codes>, <https://docs.bitrefill.com/docs/References>.

## Browse path

### `403 Forbidden` on bitrefill.com

Cloudflare blocks datacenter IPs. Fix: residential browser (ChatGPT Atlas, Cursor browser, Claude+Chrome ext, OpenClaw on user host) or pivot MCP/CLI/API.

### Product in listing but not purchasable

Geolock at IP. URL country filters inventory; checkout enforces IP. User needs to be in a supported country — don't suggest VPNs or other workarounds ([ToS](https://www.bitrefill.com/terms/)); offer a product for the user's country.

## MCP path

### Tool not visible

- Cursor: 40-tool cap exceeded. Disable unused MCP server.
- ChatGPT: Developer Mode off → write tools hidden. Toggle Settings.
- Claude.ai Free: can't add custom MCP URLs. Upgrade Pro+.
- OpenClaw: `tools.deny: ["bundle-mcp"]` hiding server, or per-agent `tools.allow` too narrow.

### `StreamableHTTPError` with HTML body

Wrong `MCP_URL`. Unset env or set `https://api.bitrefill.com/mcp`.

### OAuth loop (Cursor / Claude.ai)

Clear cookies for `bitrefill.com`, different browser, allow pop-ups.

### MCP server filtered (OpenClaw)

Startup filter rejects: `NODE_OPTIONS`, `PYTHONSTARTUP`, `PYTHONPATH`, `PERL5OPT`, `RUBYOPT`, `SHELLOPTS`, `PS4`. Use standard `*_API_KEY` / `GITHUB_TOKEN` / proxy vars only.

### MCP output truncated

Claude Code: `MAX_MCP_OUTPUT_TOKENS=50000`. OpenClaw: `tools.toolResultMaxChars` (default 16000). Paginate: `search-products --per_page 25 --page N` (max 250 per page); `list-invoices --limit 10` (max 20), then pass every key of the result's `next` (cursor, limit, product) until `next` is absent.

## CLI path

A call failed if the exit code is 1, or the JSON output has an `error` key or a key starting `MCP error` (those exit 0). Missing options and bad enum values exit 1 with the message on stderr.

### `cart_items` JSON shape error

```
# WRONG (object)
--cart_items '{"product_id": "steam-usa", "package_value": "5"}'

# RIGHT (array)
--cart_items '[{"product_id": "steam-usa", "package_value": "5"}]'
```

### `Invalid denomination 'undefined'`

Only `product_id` is required by the schema; send `package_value` (string, exact from `get-product-details` `packages`) for the amount.

### `Too big: expected array to have <=15 items`

Split into multiple `buy-products` calls.

### `Too big: expected number to be <=250 at per_page`

Returned as an `MCP error -32602` key. `per_page` max 250.

### `error: required option '--<name>' not specified`

Client validation (exit 1). Add the missing option. Search needs `--intent` (`error: required option '--intent <value>' not specified`).

### `Too small: expected string to have >=1 characters at intent`

Empty `intent`, returned as an `MCP error -32602` key (`Input validation error: Invalid arguments for tool search-products: …`). Pass the user's goal as a non-empty string; MCP clients that omit it get the same `Input validation error … at intent`.

### `rate_limit_reached`

Too many calls in a short window (MCP and CLI). Wait a minute, then retry with fewer calls.

### `Search service not available`

`SERVICE_UNAVAILABLE` from `search-products` means `country` is not an uppercase 2-letter code (`us`, `USA`). Retry with `US`.

### `Product '<slug>' was not found.`

`RESOURCE_NOT_FOUND`; `details.suggestions` lists close products (`slug`, `name`). Take the slug from `search-products` (REST: `GET /products/search?q=`).

### "Must be one of" enum errors

| Option | Valid values | Common mistakes |
|--------|--------------|-----------------|
| `--payment_method` | Crypto: `bitcoin`, `lightning`, `ark`, `ethereum`, `eth_base`, `eth_arbitrum`, `bnb_bsc`, `solana`, `dogecoin`, `dash`, `litecoin`, `ton`, `sui`; USDC: `usdc_base`, `usdc_polygon`, `usdc_arbitrum`, `usdc_erc20`, `usdc_solana`, `usdc_bsc`, `usdc_sui`, `usdc_tempo`; USDT: `usdt_erc20`, `usdt_trc20`, `usdt_polygon`, `usdt_arbitrum`, `usdt_solana`, `usdt_bsc`, `usdt_sui`, `usdt_ton`, `usdt_lightning`, `usdt_tempo`; other: `brusd_arbitrum`, `brusd_bsc`, `brusd_polygon`, `brusd_erc20`, `brusd_base`, `brc_solana` · Link-only (return `payment_link`): `fiat_card`, `apple_pay`, `google_pay`, `ideal`, `eps`, `p24`, `bancontact` (need `billing_address`), `binance_pay`, `kraken_pay` · Account (signed-in): `balance`, `cashback`. Per product → `get-product-details` `payment_methods` | `paypal`, `visa`, `card` (use `fiat_card`), `USDC_BASE` (case-sensitive) |
| `--product_type` | `giftcard`, `esim`, `refill` | `giftcards` (results say `giftcards`, the filter takes the singular), `gift_card`, `sim` |
| `--category` | A slug from the error's list or from a `--query "*"` result's `categories` | Invented slugs: error `Must be one of: …` lists every valid slug |

### Wrong `package_value` for named denominations

Exact, case-sensitive. WRONG `"1GB"`, `"300 nc"`. RIGHT `"1GB, 7 Days"`, `"PUBG New State 300 NC"`. Get from `get-product-details` `packages` array.

### CLI auth failure (≥ 0.3.0)

OAuth client_credentials + email magic link — not API keys, not browser OAuth.

```bash
bitrefill reset
bitrefill login --email you@example.com
bitrefill verify --code 123456                     # add --otp for TOTP
bitrefill whoami --json
```

| Error | Fix |
|-------|-----|
| `Access token is required for login/verify` | Any command first (MCP connect), or `reset` then retry |
| `No pending login` | Run `login --email` before `verify` |
| `No OTP code provided` on verify | Account has 2FA — add `--otp` (authenticator), keep `--code` (email) |
| `Invalid code` on verify | Wrong email code or TOTP; email → `--code`, authenticator → `--otp` |
| `unknown option '--code'` on login | Code on `verify --code`, not `login` |
| `unknown command 'login'` | Already signed in — `logout` first |
| `Failed to establish a session` | `reset`, retry |
| Invalid / expired code | Re-run `login --email`; headless → poll agent inbox ([touchpoints/cli-headless-auth.md](touchpoints/cli-headless-auth.md)) |
| Missing TOTP | `verify --code … --otp "$(op read 'op://Vault/Item/one-time password?attribute=otp')"` |

State: `~/.config/bitrefill-cli/<host>.v1.json`. `logout` revokes session; `reset` clears all.

The CLI takes no `--api-key` and reads no `credentials.json`. Developer API keys work for [touchpoints/mcp.md](touchpoints/mcp.md) / [touchpoints/api.md](touchpoints/api.md) only.

### Help-center questions

`search_help_articles --query "<question>"` → `get_help_article --id <id>`. `list_help_articles` returns no articles: browse a topic by searching within a category (`--category`; an unknown one errors with the valid slugs, also listed as `availableCategories` in each reply).

### Empty search results, no error

`found: 0`, no error. Causes: product not sold in `--country` (omitted = `US`); `--query "*"` (also the default) lists in-stock products only; `--in_stock true` drops out-of-stock items. `in_stock` is unset by default, so name searches include sold-out items (`in_stock: false` = can't buy now, try again later).

Fix: set the user's `--country`, search by brand name, or drop `--in_stock true`.

### Unpaid invoices missing from list

`list-invoices` returns paid invoices only (`payment_detected`, `payment_confirmed`, `complete`), 20 per page max (follow `next`). `only_paid` is not an option: MCP servers ignore unknown arguments, the CLI rejects it as `unknown option`. Unpaid invoices are read one at a time, and guest invoices never appear in the list, even after sign-in. Check those with `get-invoice-by-id --invoice_id <id>` (guest: also `--invoice_access_token <token>`), using the values from the `buy-products` response. An empty list does not mean nothing is outstanding.

### `RESOURCE_NOT_FOUND` on `get-invoice-by-id`

Guest: `--invoice_access_token` (from `buy-products`) is missing or wrong. Signed-in: the invoice is a guest purchase or belongs to another account, so pass its token. Also check that the id is the invoice UUID, not a 24-hex order id.

## API path

### `401 Unauthorized`

- Personal: `Authorization: Bearer $BITREFILL_API_KEY` missing/wrong.
- Business / Affiliate: `Authorization: Basic $(echo -n "$ID:$SECRET" | base64)` malformed.

### `429 Too Many Requests`

Rate limited. Defaults: 60 req/10 min most endpoints; 60 req/min on `/products` + `/products/search` + 1000 product req/hr; 1 req/3 s on `/ping`. Back off + retry. Cache catalog.

### `RESOURCE_NOT_FOUND` on `GET /invoices/{id}`

Bad invoice ID. Use the `id` returned by `POST /invoices`.

### Invoice expired

Unpaid invoices expire (`expiration_minutes` on the invoice) and can't be re-paid. Create a new one.

## OpenClaw-specific

### Cron purchase failed silently

`exec-approvals.json` `ask: on-miss` but no operator for `/approve`. Pre-approve `bitrefill buy-products` for trusted SKU/amount, or schedule when operator available.

### Pi can't see Bitrefill MCP

Check: `openclaw mcp list`; `openclaw.json` parses; agent not denying `bundle-mcp`; CLI signed in (`whoami --json`) or MCP OAuth done — not just shell env vars.

### Mobile node camera unavailable

Node not paired or offline. `openclaw nodes list`. Re-pair via Control UI (`openclaw dashboard`).

### Telegram message not reaching agent

`channels.telegram.dmPolicy: "pairing"` and sender not paired. `openclaw pairing approve telegram <CODE>` (codes expire 1 hr).

## x402 / SIWX path

### `402` after SIWX send

Stale nonce (5 min expiry), wrong EIP-55 checksum, malformed payload. Re-fetch challenge, re-sign. → [wallets/siwx.md](wallets/siwx.md).

### `403` on SIWX route

Signing wallet ≠ invoice payer. Sign with payer wallet.

### HTTP `500` on `invoice/create`

Wrong `package_value` — exact string from product detail. Confirm no onchain charge before retry.

### `INVOICE_NOT_PAYABLE` on pay

Already settled — poll `invoice/status` or `get-invoice-by-id`.

### Base MCP `web_request` rejected

Hostname not allowlisted — only `api.bitrefill.com` (not `docs.bitrefill.com`). → [wallets/base-mcp.md](wallets/base-mcp.md).

### Phantom `wallet_balances` schema error

Known Phantom MCP issue — use `wallet_addresses` + external balance, or Base MCP `get_portfolio`.

## Source of truth

- Error codes: <https://docs.bitrefill.com/docs/error-codes> | Handling: <https://docs.bitrefill.com/docs/References>
- Rate limits: <https://docs.bitrefill.com/docs/rate-limits>
- OpenClaw: <https://docs.openclaw.ai/help> + per-tool pages

**User hears:** plain language — "That didn't go through — let's try again" / "Still processing, one moment" — never error codes, endpoint names, or stack traces.
