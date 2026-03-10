# Command Reference

All commands accept `--api-key <key>` (or `BITREFILL_API_KEY` env var) for headless auth. Run `bitrefill --help` for the current list.

## search-products

```bash
bitrefill search-products --query "Netflix" --country US
```

| Option | Description | Default |
|--------|-------------|---------|
| `--query` | Brand name or `*` for all (fulltext, not semantic) | `*` |
| `--country` | Uppercase Alpha-2 ISO (`US`, `IT`, `BR`) | `US` |
| `--product_type` | `giftcard` or `esim` (singular) | — |
| `--category` | Category slug (`games`, `food`, `streaming`) | — |
| `--in_stock` | `true`/`false` | `true` |
| `--page` | 1-indexed page number | `1` |
| `--per_page` | 1–500 | `25` |

## get-product-details

```bash
bitrefill get-product-details --product_id "steam-usa" --currency USDC
```

| Option | Description | Default |
|--------|-------------|---------|
| `--product_id` | Product slug from search results (required) | — |
| `--currency` | `BTC`, `ETH`, `USDT`, `USDC`, `SOL`, `USD`, `EUR`, `GBP`, `AUD`, `CAD`, `INR`, `BRL` | `BTC` |
| `--language` | Language code for descriptions | `en` |

## buy-products

```bash
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method usdc_base
```

| Option | Description | Default |
|--------|-------------|---------|
| `--cart_items` | JSON array of `{product_id, package_id}` objects, 1–15 items (required) | — |
| `--payment_method` | See [payment.md](payment.md) (required) | — |
| `--return_payment_link` | `true` → `payment_link` + `x402_payment_url`; `false` → raw `address`/`paymentUri` | `true` |

Response fields (when `return_payment_link true`):

- `invoice_id` — poll status with `get-invoice-by-id`
- `payment_link` — browser checkout URL
- `x402_payment_url` — programmatic x402 payment endpoint
- `payment_info.address` — on-chain destination
- `payment_info.paymentUri` — EIP-681 URI with contract + amount
- `payment_info.altcoinPrice` — amount in payment token

## list-invoices

```bash
bitrefill list-invoices --only_paid false --limit 10
```

| Option | Description | Default |
|--------|-------------|---------|
| `--limit` | 1–50 | `25` |
| `--start` | Pagination offset | `0` |
| `--after` | ISO 8601 date filter | — |
| `--before` | ISO 8601 date filter | — |
| `--only_paid` | `true` hides unpaid invoices | `true` |
| `--include_orders` | Include order details | `true` |

## get-invoice-by-id

```bash
bitrefill get-invoice-by-id --invoice_id "UUID"
```

| Option | Description | Default |
|--------|-------------|---------|
| `--invoice_id` | UUID of the invoice (required) | — |
| `--include_orders` | Include order details | `true` |
| `--include_redemption_info` | Include redemption codes/links | `false` |
| `--include_access_token` | Include unauthenticated access token | `false` |

## list-orders

```bash
bitrefill list-orders --limit 5 --include_redemption_info true
```

| Option | Description | Default |
|--------|-------------|---------|
| `--limit` | 1–50 | `25` |
| `--start` | Pagination offset | `0` |
| `--after` / `--before` | ISO 8601 date filters | — |
| `--include_redemption_info` | Include redemption codes/links | `false` |

## get-order-by-id

```bash
bitrefill get-order-by-id --order_id "69af584e8a2639d14ac35e96"
```

Returns redemption code/link if the order is unsealed (paid and delivered).

| Option | Description | Default |
|--------|-------------|---------|
| `--order_id` | Order ID (required) | — |
| `--include_redemption_info` | Include redemption codes/links | `true` |

## logout

```bash
bitrefill logout
```

Deletes stored OAuth credentials from `~/.config/bitrefill-cli/`.
