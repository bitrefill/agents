# Path: CLI

Use when: shell + `npm install` available, no MCP support. Runtimes: Claude Code, Codex CLI, Cursor terminal, Gemini CLI, OpenCode, OpenClaw, Jules (ephemeral VM), ChatGPT Agent (sandbox).

Sandboxed shells must allowlist `registry.npmjs.org` and `api.bitrefill.com`.

## Install

```bash
npm install -g @bitrefill/cli
```

From source: `git clone https://github.com/bitrefill/cli.git && cd cli && pnpm install && pnpm build && npm link`.

## Auth

API key (headless, preferred for agents):

```bash
export BITREFILL_API_KEY=YOUR_API_KEY
```

Generate at <https://www.bitrefill.com/account/developers>.

OAuth (interactive): run any command without an API key → browser flow. Token stored at `~/.config/bitrefill-cli/api.bitrefill.com.json`. Clear with `bitrefill logout`.

## Workflow

```
search-products  →  get-product-details  →  buy-products  →  get-invoice-by-id
```

### 1. Search

```bash
bitrefill search-products --query "Netflix" --country US
bitrefill search-products --query "eSIM" --product_type esim --country IT
bitrefill search-products --query "*" --category games --country US
```

`--country` = uppercase Alpha-2. `--product_type` = `giftcard` or `esim` (singular). Discover categories: `--query "*"` returns a `categories` array with slugs.

### 2. Details

```bash
bitrefill get-product-details --product_id "steam-usa" --currency USDC
```

Returns `packages` array. Each entry has `package_value` — that's the `package_id` for `buy-products`. Ignore the `<&>` compound key.

Three denomination types:

- **Numeric**: `5`, `50`, `200` (pass as number).
- **Duration**: `"1 Month"`, `"12 Months"` (exact, case-sensitive).
- **Named**: `"1GB, 7 Days"`, `"PUBG New State 300 NC"` (exact, case-sensitive).

Only values from `get-product-details` accepted. Arbitrary amounts rejected.

### 3. Buy

`--cart_items` = JSON **array**, even single item. Max 15 items.

```bash
# Numeric, crypto via x402
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method usdc_base

# Duration, balance (instant)
bitrefill buy-products \
  --cart_items '[{"product_id": "spotify-usa", "package_id": "1 Month"}]' \
  --payment_method balance

# Named, eSIM
bitrefill buy-products \
  --cart_items '[{"product_id": "bitrefill-esim-europe", "package_id": "1GB, 7 Days"}]' \
  --payment_method usdc_base
```

Response: `invoice_id`, `payment_link`, `x402_payment_url`, `payment_info` (`address`, `paymentUri`, `altcoinPrice`).

### 4. Track / Redeem

```bash
bitrefill get-invoice-by-id --invoice_id "UUID"
bitrefill list-orders --include_redemption_info true
bitrefill get-order-by-id --order_id "ID"
```

Invoices expire after 180 minutes. Expired = create new one.

## Critical gotchas

- `--cart_items` must be **array** `[...]`, not object `{...}`. Shell quoting matters: single quotes outside, double inside.
- Use `package_value` after `<&>`, not the compound key. WRONG `"steam-usa<&>5"`. RIGHT `5`.
- Named/duration `package_id` exact and case-sensitive. WRONG `"1GB"`. RIGHT `"1GB, 7 Days"`.
- Country code uppercase Alpha-2. WRONG `us`, `USA`, `"United States"`. RIGHT `US`.

## Recommended payment methods (for agents)

`balance` (instant, no on-chain wait, natural cap) → `usdc_base` with x402 (autonomous payment via `x402_payment_url`) → `lightning`. Other crypto requires polling. Full list: `bitrefill buy-products --help`.

## Source of truth

- <https://github.com/bitrefill/cli> — full command reference, options, flags
- <https://docs.bitrefill.com/docs/crypto-payments> — payment methods
