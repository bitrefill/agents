# Troubleshooting

Covers errors beyond the [critical gotchas](../SKILL.md#critical-gotchas) in the main skill file.

## "Must be one of" errors

The CLI validates enums client-side.

| Option | Valid values | Common mistakes |
|--------|-------------|-----------------|
| `--payment_method` | `bitcoin`, `ethereum`, `lightning`, `usdc_polygon`, `usdt_polygon`, `usdc_erc20`, `usdt_erc20`, `usdc_arbitrum`, `usdc_solana`, `usdc_base`, `eth_base`, `balance` | `paypal`, `visa`, `USDC_BASE` (case-sensitive) |
| `--product_type` | `giftcard`, `esim` | `giftcards` (plural), `gift_card`, `sim` |

## Missing required options

Omitting `--cart_items` or `--product_id` when required: `error: required option '--<name> <value>' not specified`. The CLI enforces this before connecting to the server.

## Cart exceeds 15 items

Server rejects: `Too big: expected array to have <=15 items`. Split into multiple `buy-products` calls.

## `per_page` exceeds 500

Server rejects: `per_page must be less than 500`.

## Malformed JSON in `--cart_items`

`Unexpected token ... is not valid JSON`. Shell quoting matters — single quotes around JSON, double quotes inside:

```bash
--cart_items '[{"product_id": "steam-usa", "package_id": 5}]'
```

## Missing `package_id` in cart item

`Invalid denomination 'undefined'`. Both `product_id` and `package_id` are required per item.

## Invoice / Product not found

- `get-invoice-by-id` with bad ID: `Invoice not found` (RESOURCE_NOT_FOUND)
- `buy-products` with bad slug: `Product '<slug>' is not available` (RESOURCE_NOT_FOUND)

Verify slugs via `search-products`, invoice IDs via `list-invoices`.

## Wrong `MCP_URL`

Setting `MCP_URL` to a non-Bitrefill endpoint: `StreamableHTTPError` with the remote server's HTML body. Unset the variable or point it to `https://api.bitrefill.com/mcp`.

## OAuth / auth failures

If the CLI hangs or fails on startup:

1. Switch to API key auth: `export BITREFILL_API_KEY=YOUR_API_KEY`
2. Or clear stale credentials: `bitrefill logout`, then re-run your command
3. Credentials file: `~/.config/bitrefill-cli/api.bitrefill.com.json`

## Empty search results

`found: 0` with no error:

- `--category` slug doesn't exist (no error, just empty)
- Product not available in the specified `--country`
- `--in_stock true` (default) filters out-of-stock products

Fix: remove `--category`, change `--country`, or set `--in_stock false`.

## Unpaid invoices

`list-invoices` shows only paid by default. See all: `--only_paid false`.

Invoices expire after 180 minutes. Expired invoices cannot be re-paid — create a new one.
