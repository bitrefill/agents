# Path: CLI

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Shell + `npm install`, **no MCP client** (CLI talks to Bitrefill MCP under hood). Runtimes: Claude Code, Codex CLI, Cursor terminal, Gemini CLI, OpenCode, OpenClaw, Jules, ChatGPT Agent.

Requires **`@bitrefill/cli` ≥ 0.3.0**. Sandboxed shells: allowlist `registry.npmjs.org` + `api.bitrefill.com`.

## Install

```bash
npm install -g @bitrefill/cli@0.3
```

From source: `git clone https://github.com/bitrefill/cli.git && cd cli && pnpm install && pnpm build && npm link`.

## Guest checkout (fastest first try)

**No `login` / `verify`.** Works while `whoami` shows `identity: unregistered`. Fastest autonomous path — search, quote, invoice, pay crypto or payment link.

```bash
bitrefill search-products --query "Amazon" --country IT --intent "Amazon gift card"
bitrefill get-product-details --product_id "amazon_it-italy"

bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_value":"10"}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "agent@example.com"
```

Response: `invoice_id`, `invoice_access_token`, `payment_link`; `payment_info` (address and amount, or Lightning invoice) needs `--return_payment_link false`. Poll `get-invoice-by-id --invoice_id <uuid> --invoice_access_token <token>`. Guests must pass the token; without it the call returns `RESOURCE_NOT_FOUND`. The token and `payment_link` (which embeds the token) unlock the codes, so treat them like a password. Receipt → `--email`. Expiry → `expiration_minutes`.

Guest payment: crypto from a wallet (`--return_payment_link false`) or `payment_link`; card / Apple Pay / Google Pay: `--payment_method fiat_card` (or `apple_pay` / `google_pay`) `--billing_address '{"country":"US","city":"…","postal_code":"…","address_line1":"…"}'` (Apple Pay / Google Pay: `country` only) → send `payment_link`. Pay → [../wallets/payment.md](../wallets/payment.md). **`balance` / `cashback` need signed-in account** (below).

## Sign up / sign in (balance, cashback, order history)

After guest try, sign in when human wants **managed agent spending** or **rewards**:

| Signed-in benefit | Why |
|-------------------|-----|
| **`--payment_method balance`** | Instant from pre-funded store credit — spending cap, no on-chain wait |
| **`--payment_method cashback`** | Pay from rewards balance (BTC) |
| **Cashback on purchases** | Eligible products earn rewards |
| **`list-invoices`** + `get-balances` | Paid-invoice history (codes via `get-invoice-by-id`, no token needed for your own invoices) + store-credit and cashback balances |

Commands come from the server's tool list. Guests see 7 (`search-products`, `get-product-details`, `buy-products`, `get-invoice-by-id`, plus 3 help-article tools). After sign-in, `list-invoices`, `get-balances`, `list-saved-fiat-cards`, `submit-prepayment-step` and `update-order` also appear.

Same `login` for new + existing. Headless inbox → [cli-headless-auth.md](cli-headless-auth.md).

```bash
bitrefill login --email you@example.com
bitrefill verify --code GGWK87DR              # email magic-link code
bitrefill verify --code GGWK87DR --otp 122407   # + TOTP when 2FA
bitrefill whoami --json

# signed-in buy — debits balance at once
bitrefill get-balances
bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_value":"10"}]' \
  --payment_method balance --balance_currency EUR
```

Check `get-balances` before paying by balance. Short → offer a balance top-up (Bitrefill Gift Card, `bitrefill-giftcard-usd` / `-eur`) or the next wallet. Without `--balance_currency` the buy debits the primary sub-account, which can be BTC: name the sub-account in the confirm.

**Verify gotchas:**

- Email code → `verify --code <value>`, **not** `login --code`.
- `--otp` = **authenticator TOTP only** when 2FA — not email code. Both `--code` + `--otp` when enrolled.
- After sign-in, `login` gone from `--help`; `logout` first to switch accounts.

## Bootstrap (optional)

```bash
bitrefill init                    # optional OpenClaw wiring only
```

`init` no longer stores API keys. OpenClaw only: merges MCP config + generates `~/.openclaw/skills/bitrefill/SKILL.md`.

## Auth

CLI 0.3.0: **guest checkout needs no sign-in.** Account auth = OAuth client_credentials (auto on first MCP connect) + email magic-link. No `--api-key`, no `credentials.json`.

| Step | Command | Notes |
|------|---------|-------|
| Register client | any command (or `login`) | MCP connect mints `access_token`; stored `~/.config/bitrefill-cli/<host>.v1.json` |
| Sign up or sign in | `login --email <addr>` | same for new + existing |
| Complete auth | `verify --code <code> [--otp <totp>]` | email code; `--otp` when TOTP |
| Check session | `whoami [--json]` | `identity: registered` + `email` when signed in |
| Sign out | `logout` | revokes session; keeps `client_id` |
| Full reset | `reset` | clears all local state + revokes session |

**TOTP via 1Password** ([`op read`](https://www.1password.dev/cli/reference/commands/read)):

```bash
bitrefill verify --code "$CODE" --otp "$(op read 'op://Vault/Bitrefill/one-time password?attribute=otp')"
```

Shorthand ([`op item get --otp`](https://www.1password.dev/cli/reference/management-commands/item#item-get)):

```bash
bitrefill verify --code "$CODE" --otp "$(op item get Bitrefill --otp)"
```

Server may return `browser_url` for passkey/WebAuthn — open in browser, retry.

**Developer API keys** (Personal REST / key-in-path MCP) separate from CLI auth. → [mcp.md](mcp.md), [api.md](api.md).

## Global flags

Before subcommand:

- **`--json`** — stdout single JSON per run (TOON → JSON); status messages on **stderr**. Use with `jq`. A call failed if the exit code is 1, or the JSON has an `error` key or a key starting `MCP error` (those exit 0).

```bash
bitrefill --json search-products --query "Amazon" --intent "Amazon gift card" --per_page 1 | jq '.products[0].name'
```

## Agent discovery

`manifest` — JSON schema for every built-in + MCP command:

```bash
bitrefill manifest --json | jq '.commands[].name'
bitrefill manifest -o bitrefill-manifest.json
```

`llm-context` embeds manifest in fenced JSON block.

## `llm-context`

Regenerates Markdown from live MCP `tools/list`. For **CLAUDE.md**, Cursor rules, **`.github/copilot-instructions.md`**. Connection line = redacted MCP URL — safe to commit.

```bash
bitrefill llm-context -o BITREFILL-MCP.md
```

## OpenClaw quick-bootstrap

Optional `bitrefill init --openclaw`: MCP stub in `~/.openclaw/openclaw.json` + skill SKILL.md. **Not required for guest CLI** — install CLI, guest checkout via `exec`. OpenClaw prefers guest CLI first → [../harnesses/openclaw.md](../harnesses/openclaw.md). Hardening → exec-approvals for `buy-products`.

## Workflow

Subcommands from remote MCP (`bitrefill --help` after connect). Core:

```
search-products  →  get-product-details  →  buy-products  →  get-invoice-by-id
```

1. **Search** — `search-products`. *(say: "Searching for [product]…")*
2. **Get price** — `get-product-details`. *(silent)*
3. **Prepare order** — `buy-products`. Confirm with user first. *(say: "[Product] — [amount]: [total] USDC. Confirm?")*
4. **Pay** → [../wallets/payment.md](../wallets/payment.md). *(say: "Approve the payment in your Base Account")*
5. **Deliver** — `get-invoice-by-id` until complete. *(say: "Your code is ready.")*

Help-center questions: `search_help_articles --query "…" [--category <slug>]`, then `get_help_article --id <id>`. `list_help_articles` returns no articles; browse a topic by searching within a category (valid slugs in `availableCategories` of every help reply).

### 1. Search

```bash
bitrefill search-products --query "Netflix" --country US --intent "Netflix subscription"
bitrefill --json search-products --query "Netflix" --country US --intent "Netflix subscription" --per_page 5 | jq '.products'
bitrefill search-products --query "eSIM" --product_type esim --country IT --intent "trip to Italy"
bitrefill search-products --query "*" --category games --country US --intent "gaming gift"
```

`--country` = uppercase Alpha-2 (omitted = `US`). `--product_type` = `giftcard`, `esim` or `refill` (results say `giftcards`; the filter takes the singular). `--intent` required, non-empty: the user's broad goal, context only (results unchanged). Categories: `--query "*"` returns `categories` array with slugs; an unknown `--category` fails with the valid list.

### 2. Details

```bash
bitrefill get-product-details --product_id "steam-usa" --currency USDC
```

Each package lists `package_value`, `package_currency`, `payment_price`, `payment_currency`. Pass `packages[].package_value` as `cart_items[].package_value`.

Denomination types:

- **Numeric**: `"5"`, `"50"`, `"200"`. Always a JSON string, never a number. Ranged products: any multiple of `range.step` within `range.min`–`range.max`, still a string.
- **Duration**: `"1 Month"`, `"12 Months"` (exact, case-sensitive).
- **Named**: `"1GB, 7 Days"`, `"PUBG New State 300 NC"` (exact, case-sensitive).

Only values from `get-product-details` accepted.

### 3. Buy

`--cart_items` = JSON **array**, even single item. Max 15. **`--email`** = receipt (required for guests; signed-in receipts go to the account email).

```bash
# Guest — crypto + payment link
bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_value":"10"}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "agent@example.com"

# Signed-in — instant from store credit (no --email: the receipt goes to the account email)
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_value": "5"}]' \
  --payment_method balance --balance_currency USD

# Signed-in — crypto: a wallet sends to payment_info
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_value": "5"}]' \
  --payment_method usdc_base --return_payment_link false

# Duration package
bitrefill buy-products \
  --cart_items '[{"product_id": "spotify-usa", "package_value": "1 Month"}]' \
  --payment_method balance --balance_currency USD

# Named eSIM
bitrefill buy-products \
  --cart_items '[{"product_id": "bitrefill-esim-europe", "package_value": "1GB, 7 Days"}]' \
  --payment_method usdc_base
```

Options:

- **Top-up** (`recipient_type` ≠ `none` in `get-product-details`): `refill_input` in the cart item, e.g. `{"product_id":"<slug>","package_value":"5","refill_input":"4915123456789"}` (`phone_number`: country code + number, digits only).
- **Bill payment** (product has a `prepayment` block): loop `submit-prepayment-step` until `step: "final"`, then pass its `billPaymentId` as `bill_payment_id` in the cart item.
- **Saved card** (signed-in): `--payment_method fiat_card --saved_fiat_card_id <id from list-saved-fiat-cards>`; no `--billing_address`.
- **Coupon**: `--coupon_code <code>`; an invalid one fails the purchase.
- **Balance**: `--balance_currency USD|EUR|BTC` picks the sub-account.

Response: `invoice_id`, `invoice_access_token`, `payment_link`; `payment_info` (`address`, `paymentUri`, `altcoinPrice`) needs `--return_payment_link false`.

**Pay** → [../wallets/payment.md](../wallets/payment.md): a wallet sends to `payment_info`, or `balance` when signed in.

### 4. Track / Redeem

```bash
# Guest: both values come from the buy-products response; the token is required
bitrefill get-invoice-by-id --invoice_id "UUID" --invoice_access_token "TOKEN"

# Signed-in: your own invoices need no token
bitrefill get-invoice-by-id --invoice_id "UUID"
bitrefill list-invoices                                         # paid only, newest first, 10/page (--limit max 20)
bitrefill list-invoices --product "amazon" --after 2026-09-01   # filter by product name/id or ISO date
bitrefill list-invoices --cursor "<next.cursor>" --limit <next.limit> --product "<next.product>"   # next page: pass every key of `next` (omit product if absent)
```

Poll every 10–30 s until `invoice_status: complete`. Codes are in `orders[].redemption_info`; eSIMs in `orders[].esim_install_link`. `list-invoices` returns no codes and never lists unpaid or guest invoices, so use `get-invoice-by-id` for those. Don't combine `--cursor` with `--after`/`--before`.

`invoice_id` + `invoice_access_token` give read access to the codes. Never log them or the `payment_link`, and don't write them to shared dirs (`/tmp`, `/workspace`). For polling across turns (cron or heartbeat), use a private file (`chmod 600`) and delete it after delivery.

Invoices expire per `expiration_minutes`. Expired = create new.

## Critical gotchas

- `--cart_items` = **array** `[...]`, not object `{...}`. Single quotes outside, double inside.
- Named/duration `package_value` exact, case-sensitive. WRONG `"1GB"`. RIGHT `"1GB, 7 Days"`.
- Country uppercase Alpha-2. WRONG `us`, `USA`. RIGHT `US`.
- `login`/`verify` only when not signed in. `logout` before switching accounts.
- Guest: `--payment_method balance`/`cashback` fail — crypto or sign in first.
- Signed-in + 2FA: `verify` needs **both** `--code` (email) + `--otp` (authenticator).

## Payment methods

Pay-time routing → [../wallets/payment.md](../wallets/payment.md). Signed-in: prefer `balance` + pre-funded cap. Guest: `usdc_base` or `lightning` + wallet from [../wallets/matrix.md](../wallets/matrix.md); card / Apple Pay / Google Pay + `--billing_address` → `payment_link`.

## Source of truth

- <https://github.com/bitrefill/cli> — commands, options, flags
- <https://docs.bitrefill.com/docs/crypto-payments> — payment methods
- `bitrefill manifest --json` / `bitrefill llm-context` — live tool list + schemas

**User hears:** "Searching for [product]…" → "[Product] — [amount]: [total] USDC. Confirm?" → "Approve the payment" → "Your code is ready."
