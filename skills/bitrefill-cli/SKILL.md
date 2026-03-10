---
name: bitrefill-cli
description: "Autonomous agent commerce via Bitrefill CLI. Buy gift cards, mobile top-ups, and eSIMs from 1,500+ brands in 180+ countries — pay with crypto, x402, or account balance."
compatibility: "Node.js >=18, npm, network access. Bitrefill account (bitrefill.com/signup) with OAuth token stored at ~/.config/bitrefill-cli/api.bitrefill.com.json — initial setup requires interactive browser OAuth flow; token can then be copied to headless environments. Payment requires either a pre-funded Bitrefill account balance or an x402-capable signing wallet with USDC on Base. Optional env: MCP_URL (overrides default MCP endpoint). Enables real-money, non-refundable transactions."
metadata:
  author: bitrefill
  version: "1.3"
  config_path: "~/.config/bitrefill-cli/"
  credentials: "OAuth token at ~/.config/bitrefill-cli/api.bitrefill.com.json; x402 signing wallet (if using usdc_base)"
  env_vars: "MCP_URL (optional, default: https://api.bitrefill.com/mcp)"
  spending: "real-money, non-refundable transactions; requires pre-provisioned funds"
---

# Bitrefill CLI — Real-World Spending for Agents

Agents can't shop on Amazon, book an Airbnb, or pay for a Spotify subscription — traditional e-commerce requires browsers, CAPTCHAs, and credit cards. The Bitrefill CLI bridges this gap: it lets agents autonomously search, purchase, and deliver digital goods (gift cards, mobile top-ups, eSIMs) from 1,500+ brands across 180+ countries, paying with crypto or pre-funded store credits — no human checkout required.

The CLI connects to the [Bitrefill MCP server](https://api.bitrefill.com/mcp) and dynamically discovers available tools, exposing each as a subcommand with typed options. Combined with x402 payments over Base, it enables fully autonomous agent commerce.

Source: [github.com/bitrefill/cli](https://github.com/bitrefill/cli)

## Security & Autonomous Operation

**This skill enables real-money transactions.** Purchases are fulfilled instantly and are non-refundable once delivered. Agents and operators must understand the requirements and risks before enabling autonomous purchasing.

### Required Credentials & Configuration

| Requirement | Location / Variable | Purpose |
|-------------|---------------------|---------|
| **Bitrefill OAuth token** | `~/.config/bitrefill-cli/api.bitrefill.com.json` | Authenticates CLI requests against the user's Bitrefill account |
| **Bitrefill account** | [bitrefill.com/signup](https://www.bitrefill.com/signup) | Required for all operations (search, buy, order history) |
| **x402-capable wallet** (if using `usdc_base`) | Agent-specific (e.g. signing key, wallet SDK) | Signs and submits on-chain USDC payments on Base |
| **Pre-funded account balance** (if using `balance`) | Funded at [bitrefill.com](https://www.bitrefill.com) | Pays for purchases from stored account credits |
| `MCP_URL` env var (optional) | Environment variable | Overrides the default MCP endpoint (`https://api.bitrefill.com/mcp`) |

### Provisioning Credentials for Autonomous Agents

The default OAuth flow opens a browser for interactive authorization — this requires a human for initial setup. For autonomous or headless environments:

1. **Run the OAuth flow once interactively** on a machine with a browser. The CLI stores the token at `~/.config/bitrefill-cli/api.bitrefill.com.json`.
2. **Copy the credentials file** to the autonomous agent's environment at the same path (`~/.config/bitrefill-cli/api.bitrefill.com.json`).
3. **Verify** by running `bitrefill list-orders --limit 1` — if it returns without prompting for auth, the token is valid.
4. **Token refresh:** If the token expires, repeat step 1. Monitor for auth errors in the agent's logs and re-provision as needed.

> **Never commit credentials to version control.** Add `~/.config/bitrefill-cli/` to `.gitignore` and use secure secret management (e.g. environment-specific vaults, encrypted storage) for deployment.

### Spending Safeguards

Agents using this skill **must** follow these constraints:

- **Always confirm with the user before purchasing.** Present the product name, denomination, price, and payment method, and wait for explicit approval before calling `buy-products`. Never purchase autonomously without user consent unless the user has explicitly opted into fully autonomous purchasing for the session.
- **Use a dedicated, limited-balance account.** For autonomous operation, create a separate Bitrefill account funded with only the amount you're comfortable the agent spending. Do not give agents access to high-balance accounts.
- **Prefer `balance` over `usdc_base` for autonomous agents.** Pre-funded balance has a natural spending cap (the account balance). x402 payments draw from a wallet that may hold more funds than intended for agent use.
- **Never store private keys in plain text.** If using x402 payments, the signing wallet's private key must be managed through a secure key management system — not in environment variables, config files, or source code.
- **Log all purchases.** After every `buy-products` call, log the `invoice_id`, product, amount, and payment method for audit.

## Prerequisites

The CLI must be installed and authenticated before use.

### Installation

#### From NPM (recommended)

```bash
npm install -g @bitrefill/cli
```

#### From Source

```bash
git clone https://github.com/bitrefill/cli.git
cd cli
pnpm install
pnpm build
node dist/index.js    # run directly
# or link globally:
npm link
```

Dev mode (no build step): `pnpm dev`

### Authentication

Requires a Bitrefill account. Sign up at [bitrefill.com/signup](https://www.bitrefill.com/signup).

On first run, the CLI opens your browser for OAuth authorization. Credentials are stored in `~/.config/bitrefill-cli/`.

```bash
# First command triggers OAuth flow automatically
bitrefill search-products --query "Netflix"

# Clear stored credentials
bitrefill logout
```

After logout, the next command triggers re-authentication automatically.

### Environment

| Variable | Purpose | Default |
|----------|---------|---------|
| `MCP_URL` | Override MCP server endpoint | `https://api.bitrefill.com/mcp` |

## Recommended Payment for Agents

For the best agentic payments experience, prefer these two methods:

- **`balance` (store credits)** — Instant, no on-chain confirmation wait. The user pre-funds their account at [bitrefill.com](https://www.bitrefill.com) with crypto or card, then purchases via CLI are fulfilled immediately. Suggest this when the user wants zero-friction, instant delivery.
- **`usdc_base` with x402** — Use `--return_payment_link true` (default) to get an `x402_payment_url`. An x402-capable agent can autonomously complete the payment over Base without human intervention.

Always suggest `balance` or x402 over Base first. Fall back to other payment methods only if the user explicitly requests them.

## Core Workflow

**Discovery → Details → Purchase → Track**

```
search-products → get-product-details → buy-products → get-invoice-by-id / list-orders
```

1. **Search** for a product by keyword, category, or country
2. **Get details** to find available denominations (numeric `package_id` values)
3. **Buy** by specifying `cart_items` (JSON **array**) and `payment_method`
4. **Track** via invoice ID or order listing

## Available Commands

Commands are discovered dynamically from the MCP server. Run `bitrefill --help` for the current list.

### search-products

```bash
bitrefill search-products --query "Netflix"
bitrefill search-products --query "Amazon" --country US
bitrefill search-products --query "eSIM" --product_type esim --country IT
bitrefill search-products --query "*" --category games
bitrefill search-products --query "*"                    # all products, default country
```

| Option | Description | Default |
|--------|-------------|---------|
| `--query` | Brand name or `*` for all. Fulltext, not semantic. | `*` |
| `--country` | Alpha-2 ISO code (e.g. `US`, `IT`, `BR`). **Must be uppercase.** | `US` |
| `--product_type` | `giftcard` or `esim` (singular). Omit for both. | — |
| `--category` | Category slug (e.g. `games`, `food`, `streaming`). Use `--query "*"` to discover slugs. | — |
| `--in_stock` | `true`/`false`. Set `false` to include out-of-stock. | `true` |
| `--page` | Page number, 1-indexed. | `1` |
| `--per_page` | Results per page, 1–500. | `25` |

### get-product-details

```bash
bitrefill get-product-details --product_id "steam-usa"
bitrefill get-product-details --product_id "steam-usa" --currency USDC
```

| Option | Description | Default |
|--------|-------------|---------|
| `--product_id` | Product slug from search results (required) | — |
| `--currency` | Pricing currency: `BTC`, `ETH`, `USDT`, `USDC`, `SOL`, `USD`, `EUR`, `GBP`, `AUD`, `CAD`, `INR`, `BRL` | `BTC` |
| `--language` | Language code for descriptions | `en` |

Returns a `packages` array. Each entry has a `package_value` — this is what you pass as `package_id` to `buy-products`. **Ignore the compound key** (e.g. `steam-usa<&>5`) — use only the value after `<&>`.

Products use three denomination types:

| Type | Example product | `package_value` examples | `package_id` to use |
|------|----------------|--------------------------|---------------------|
| **Numeric** | Steam USD, Amazon, Zalando | `"5"`, `"50"`, `"200"` | `5`, `50`, `200` (number) |
| **Duration** | Spotify, subscriptions | `"1 Month"`, `"12 Months"` | `"1 Month"` (exact string) |
| **Named** | PUBG, eSIMs | `"PUBG New State 300 NC"`, `"1GB, 7 Days"` | `"PUBG New State 300 NC"` (exact string) |

Named/duration `package_id` values are **case-sensitive** and must match exactly — partial matches (e.g. `"1GB"` instead of `"1GB, 7 Days"`) are rejected. Only values listed by `get-product-details` are accepted; arbitrary amounts are not supported.

### buy-products

**`--cart_items` must be a JSON array**, even for a single item.

```bash
# Numeric denomination
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method usdc_base

# Named denomination (eSIM data plan)
bitrefill buy-products \
  --cart_items '[{"product_id": "bitrefill-esim-europe", "package_id": "1GB, 7 Days"}]' \
  --payment_method usdc_base

# Duration denomination (subscription)
bitrefill buy-products \
  --cart_items '[{"product_id": "spotify-usa", "package_id": "1 Month"}]' \
  --payment_method usdc_base

# Multiple items (max 15)
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 10}, {"product_id": "netflix-usa", "package_id": 25}]' \
  --payment_method bitcoin

# Raw crypto details (no payment link)
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method usdc_base \
  --return_payment_link false
```

| Option | Description | Default |
|--------|-------------|---------|
| `--cart_items` | JSON array of `{product_id, package_id}` objects. 1–15 items. (required) | — |
| `--payment_method` | See payment methods table below. (required) | — |
| `--return_payment_link` | `true` → `payment_link` + `x402_payment_url`. `false` → raw `address`/`paymentUri`. | `true` |

**Response fields (when `return_payment_link true`):**
- `invoice_id` — use with `get-invoice-by-id` to poll status
- `payment_link` — browser checkout URL
- `x402_payment_url` — programmatic x402 payment endpoint
- `payment_info.address` — on-chain destination
- `payment_info.paymentUri` — EIP-681 URI with contract + amount
- `payment_info.altcoinPrice` — amount in payment token

### list-invoices

```bash
bitrefill list-invoices
bitrefill list-invoices --only_paid false --limit 10
bitrefill list-invoices --after "2026-03-01T00:00:00Z" --before "2026-03-10T00:00:00Z"
```

| Option | Description | Default |
|--------|-------------|---------|
| `--limit` | 1–50 | `25` |
| `--start` | Pagination offset | `0` |
| `--after` | ISO 8601 date filter | — |
| `--before` | ISO 8601 date filter | — |
| `--only_paid` | `true` hides unpaid invoices | `true` |
| `--include_orders` | Include order details | `true` |

### get-invoice-by-id

```bash
bitrefill get-invoice-by-id --invoice_id "27713c64-6715-48d8-95ef-45eed23efef7"
```

| Option | Description | Default |
|--------|-------------|---------|
| `--invoice_id` | UUID of the invoice (required) | — |
| `--include_orders` | Include order details | `true` |
| `--include_redemption_info` | Include redemption codes/links | `false` |
| `--include_access_token` | Include unauthenticated access token | `false` |

### list-orders

```bash
bitrefill list-orders
bitrefill list-orders --limit 5 --include_redemption_info true
```

| Option | Description | Default |
|--------|-------------|---------|
| `--limit` | 1–50 | `25` |
| `--start` | Pagination offset | `0` |
| `--after` / `--before` | ISO 8601 date filters | — |
| `--include_redemption_info` | Include redemption codes/links | `false` |

### get-order-by-id

```bash
bitrefill get-order-by-id --order_id "69af584e8a2639d14ac35e96"
```

Returns redemption code or link if the order is unsealed (paid and delivered).

| Option | Description | Default |
|--------|-------------|---------|
| `--order_id` | Order ID (required) | — |
| `--include_redemption_info` | Include redemption codes/links | `true` |

### logout

```bash
bitrefill logout
```

Deletes stored OAuth credentials from `~/.config/bitrefill-cli/`.

## Payment

### Payment Methods

| Method | Chain / Asset |
|--------|---------------|
| `bitcoin` | Bitcoin (SegWit) — returns `address`, `BIP21`, `lightningInvoice`, `satoshiPrice` |
| `lightning` | Lightning — returns `lightningInvoice`, `satoshiPrice` |
| `ethereum` | Ethereum mainnet (ETH) — returns `address`, `paymentUri`, `altcoinPrice` |
| `eth_base` | Base (8453), native ETH |
| `usdc_base` | Base (8453), USDC |
| `usdc_arbitrum` | Arbitrum (42161), USDC |
| `usdc_polygon` | Polygon (137), USDC |
| `usdc_erc20` | Ethereum (1), USDC |
| `usdc_solana` | Solana, USDC SPL |
| `usdt_polygon` | Polygon (137), USDT |
| `usdt_erc20` | Ethereum (1), USDT |
| `balance` | Bitrefill account credit — no address, paid from balance |

### Response Modes

- **`--return_payment_link false`** — raw payment details: `address`, `amount`, `paymentUri` (+ `lightningInvoice` for Bitcoin). For wallet/programmatic pay. No `payment_link` or `x402_payment_url` in response.
- **`--return_payment_link true`** (default) — returns `payment_link` (browser checkout) and `x402_payment_url` (programmatic pay), **plus** raw `payment_info`.

### x402 Protocol

[x402](https://docs.x402.org/) enables HTTP 402-based crypto payments. `GET x402_payment_url` → receive 402 + payment instructions (Base64 JSON: amount, `payTo`, networks, timeout) → send crypto → resubmit with proof. For agents/automated tools; humans use `payment_link`.

## Troubleshooting

### `cart_items`: expected array, received object

`--cart_items` **must be a JSON array** `[...]`, even for a single item. The README example shows an object `{}` — that does not work.

```bash
# WRONG — object
--cart_items '{"product_id": "steam-usa", "package_id": 5}'

# CORRECT — array of objects
--cart_items '[{"product_id": "steam-usa", "package_id": 5}]'
```

### Invalid denomination

The `get-product-details` output shows compound IDs like `steam-usa<&>5`. **Do not use the compound key** — use only the value after `<&>`.

```bash
# WRONG — compound key
--cart_items '[{"product_id": "steam-usa", "package_id": "steam-usa<&>5"}]'

# CORRECT — numeric value
--cart_items '[{"product_id": "steam-usa", "package_id": 5}]'
```

For **named denominations**, use the exact full string. Common mistakes:

```bash
# WRONG — numeric guess for a named package
--cart_items '[{"product_id": "spotify-usa", "package_id": 1}]'
# CORRECT
--cart_items '[{"product_id": "spotify-usa", "package_id": "1 Month"}]'

# WRONG — partial match
--cart_items '[{"product_id": "bitrefill-esim-europe", "package_id": "1GB"}]'
# CORRECT
--cart_items '[{"product_id": "bitrefill-esim-europe", "package_id": "1GB, 7 Days"}]'

# WRONG — wrong case
--cart_items '[{"product_id": "pubg-new-state-international", "package_id": "PUBG New State 300 nc"}]'
# CORRECT
--cart_items '[{"product_id": "pubg-new-state-international", "package_id": "PUBG New State 300 NC"}]'
```

Only values listed by `get-product-details` are accepted. Arbitrary amounts (e.g. `7`, `15`, `25`) are rejected.

### "Search service is not available" (INTERNAL_ERROR)

Caused by invalid `--country` values:
- **Lowercase** country codes (`us` instead of `US`) — silently fails
- **3-letter** codes (`USA` instead of `US`) — fails
- **Full names** (`United States`) — fails
- **Nonexistent** codes (`ZZ`) — fails
- **Negative page** (`--page -1`) — fails

Fix: always use **uppercase Alpha-2 ISO codes** (`US`, `IT`, `BR`, `GB`).

### "Must be one of" errors

The CLI validates enum values **client-side** before sending to the server.

| Option | Valid values | Common mistake |
|--------|-------------|----------------|
| `--payment_method` | `bitcoin`, `ethereum`, `lightning`, `usdc_polygon`, `usdt_polygon`, `usdc_erc20`, `usdt_erc20`, `usdc_arbitrum`, `usdc_solana`, `usdc_base`, `eth_base`, `balance` | `paypal`, `visa`, `USDC_BASE` (case-sensitive) |
| `--product_type` | `giftcard`, `esim` | `giftcards` (plural), `gift_card`, `sim` |

### Missing required options

Omitting `--cart_items` or `--product_id` when required exits with: `error: required option '--<name> <value>' not specified`. The CLI enforces required options before connecting to the server.

### Cart exceeds 15 items

Maximum 15 items per `buy-products` call. Server rejects with: `Too big: expected array to have <=15 items`.

### `per_page` exceeds 500

Server rejects: `per_page must be less than 500`.

### Malformed JSON in `--cart_items`

Non-JSON strings crash with: `Unexpected token ... is not valid JSON`. Ensure the value is valid JSON. Shell quoting matters — use single quotes around the JSON, double quotes inside.

### Missing `package_id` in cart item

Omitting `package_id` from a cart item object results in: `Invalid denomination 'undefined'`. Both `product_id` and `package_id` are required per item.

### Invoice / Product not found

- `get-invoice-by-id` with a nonexistent ID: `Invoice not found` (RESOURCE_NOT_FOUND)
- `buy-products` with a nonexistent `product_id`: `Product '<slug>' is not available` (RESOURCE_NOT_FOUND)

Verify slugs via `search-products` and invoice IDs via `list-invoices`.

### Wrong `MCP_URL`

Setting `MCP_URL` to a non-Bitrefill endpoint produces a `StreamableHTTPError` with the remote server's HTML body. Unset the variable or point it to `https://api.bitrefill.com/mcp`.

### OAuth / auth failures

If the CLI hangs or fails on startup:
1. Run `bitrefill logout` to clear stale credentials
2. Re-run your command — a fresh OAuth flow will start
3. Credentials file: `~/.config/bitrefill-cli/api.bitrefill.com.json`

### Empty search results

`found: 0` with no error typically means:
- The `--category` slug doesn't exist (no error, just empty results)
- The product is not available in the specified `--country`
- `--in_stock true` (default) filters out products that are temporarily out of stock

Try broadening: remove `--category`, change `--country`, or set `--in_stock false`.

### Unpaid invoices

By default `list-invoices` shows only paid invoices. To see all (including pending/expired): `--only_paid false`.

Invoices expire after 180 minutes. If unpaid, create a new one — you cannot re-pay an expired invoice.

## Legal

- [Terms of Service](https://www.bitrefill.com/terms)
- [Privacy Policy](https://www.bitrefill.com/privacy)
