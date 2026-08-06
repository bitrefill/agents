# Path: CLI

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Shell + `npm install`, **no MCP client** (CLI talks to Bitrefill MCP under hood). Runtimes: Claude Code, Codex CLI, Cursor terminal, Gemini CLI, OpenCode, OpenClaw, Jules, ChatGPT Agent.

Requires **`@bitrefill/cli` ≥ 0.3.0**. Sandboxed shells: allowlist `registry.npmjs.org` + `api.bitrefill.com`.

## Install

```bash
npm install -g @bitrefill/cli
```

From source: `git clone https://github.com/bitrefill/cli.git && cd cli && pnpm install && pnpm build && npm link`.

## Guest checkout (fastest first try)

**No `login` / `verify`.** Works while `whoami` shows `identity: unregistered`. Fastest autonomous path — search, quote, invoice, pay crypto or payment link.

Every `buy-products` example below is valid only after [budget-guard.md](../budget-guard.md) establishes the current-session record. A guest call may create the non-paying invoice used to learn final terms; do not expose or pay its payment instrument until that exact impact is confirmed and reserved.

```bash
bitrefill search-products --query "Amazon" --country IT
bitrefill get-product-details --product_id "amazon_it-italy"

bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_id":"10"}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "agent@example.com"
```

Response: `invoice_id`, `payment_link`, optional `x402_payment_url` / Lightning invoice. Poll `get-invoice-by-id --invoice_id <uuid>`. Receipt → `--email`. Use the returned `expiration_minutes` and authoritative status; never infer expiry from a local default.

Guest payment: crypto or `--return_payment_link true`. Pay → [../wallets/payment.md](../wallets/payment.md). A signed-in account is necessary but not sufficient for guarded `balance`; the safe route also needs authorized direct REST. Guarded `cashback` remains blocked pending authoritative debit semantics.

## Sign up / sign in (balance, cashback, order history)

After guest try, sign in when the human needs account identity, order history, or rewards visibility:

| Signed-in benefit | Why |
|-------------------|-----|
| **Balance visibility / authorization** | Enables the separate guarded REST two-step route; CLI auto-pay is not sufficient |
| **Cashback visibility** | Inspect rewards; guarded cashback payment remains blocked pending authoritative debit semantics |
| **Cashback on purchases** | Eligible products earn rewards |
| **`list-orders` / `list-invoices`** | Order history + redemption codes |

Do not use `cashback` as a guarded payment method until the current provider contract authoritatively exposes its exact pre-call total and debit semantics. A rewards balance is not permission to bypass the budget.

Same `login` for new + existing. Headless inbox → [cli-headless-auth.md](cli-headless-auth.md).

```bash
bitrefill login --email you@example.com
bitrefill verify --code GGWK87DR              # email magic-link code
bitrefill verify --code GGWK87DR --otp 122407   # + TOTP when 2FA
bitrefill whoami --json
```

Do not execute a signed-in CLI `buy-products --payment_method balance` inside the guard: the documented command can debit during invoice creation without first returning a server-bound exact total. Use [api.md](api.md)'s authorized REST `auto_pay: false` invoice, reserve its returned total, then pay that same invoice.

**Verify gotchas:**

- Email code → `verify --code <value>`, **not** `login --code`.
- `--otp` = **authenticator TOTP only** when 2FA — not email code. Both `--code` + `--otp` when enrolled.
- After sign-in, `login` gone from `--help`; `logout` first to switch accounts.

## Bootstrap (optional)

```bash
bitrefill init                    # optional OpenClaw wiring only
```

`init` no longer stores API keys. OpenClaw only: it merges MCP config and generates `~/.openclaw/skills/bitrefill/SKILL.md`. That high-priority generated skill can shadow newer plugin/`extraDirs` content. Prefer MCP-only configuration or manually install the complete current skill; do not enable purchases until the effective source, version, and mandatory budget/safeguard content are verified.

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

Shorthand ([`op item get --otp`](https://developer.1password.com/llms-cli.txt)):

```bash
bitrefill verify --code "$CODE" --otp "$(op item get Bitrefill --otp)"
```

Server may return `browser_url` for passkey/WebAuthn — open in browser, retry.

**Developer API keys** (Personal REST / key-in-path MCP) separate from CLI auth. → [mcp.md](mcp.md), [api.md](api.md).

## Global flags

Before subcommand:

- **`--json`** — stdout single JSON per run (TOON → JSON); status/errors on **stderr**. Use with `jq`.

```bash
bitrefill --json search-products --query "Amazon" --per_page 1 | jq '.products[0].name'
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

`bitrefill init --openclaw` creates an MCP stub plus a high-priority generated skill. Prefer MCP-only configuration or manually install the complete current skill. If `init` is used, verify the effective `bitrefill` source/version and confirm its resolved `SKILL.md` mandates `budget-guard.md` and `safeguards.md`; otherwise keep purchase tools disabled. → [../harnesses/openclaw.md](../harnesses/openclaw.md).

## Workflow

Apply [the session budget guard](../budget-guard.md) before `buy-products` and every later payment command. Do not use signed-in CLI balance auto-pay in the guarded flow; route balance through the authorized REST two-step path. For crypto or a payment link, attach the returned `invoice_id` to the same request record and keep its reservation until authoritative status confirms payment or non-payment.

Subcommands from remote MCP (`bitrefill --help` after connect). Core:

```
search-products  →  get-product-details  →  buy-products  →  get-invoice-by-id
```

1. **Search** — `search-products`. *(say: "Searching for [product]…")*
2. **Get estimate** — `get-product-details`; validate the product and a coarse budget estimate, but do not call catalog pricing a final total. *(silent)*
3. **Establish terms** — for guest/non-balance payment, create one expressly non-paying invoice with `buy-products` under a `proposed` attempt, attach its ID, and withhold its payment instrument. For balance, use the REST `auto_pay: false` invoice flow; do not use CLI auto-pay unless an exact cart total is independently bound and reserved before the call. Block `cashback` unless its exact pre-call debit semantics are authoritative.
4. **Confirm, reserve, and pay once** — show the invoice's exact payable components and budget impact, reserve them, then [pay](../wallets/payment.md) against that same attempt. A recreate follows [budget-guard.md](../budget-guard.md): freeze an authoritatively unpaid attempt, create one new attempt, and never let late responses cross attempts. *(say: "[Product] — [amount]: [total]. Confirm?")*
5. **Reconcile and deliver** — `get-invoice-by-id` until payment and delivery state are authoritative; settle or release the reservation once. *(say: "Your code is ready.")*

### 1. Search

```bash
bitrefill search-products --query "Netflix" --country US
bitrefill --json search-products --query "Netflix" --country US --per_page 5 | jq '.products'
bitrefill search-products --query "eSIM" --product_type esim --country IT
bitrefill search-products --query "*" --category games --country US
```

`--country` = uppercase Alpha-2. `--product_type` = `giftcard` or `esim`. Categories: `--query "*"` returns `categories` array with slugs.

### 2. Details

```bash
bitrefill get-product-details --product_id "steam-usa" --currency USDC
```

`packages` array → `package_value` = `package_id` for `buy-products`. Ignore `<&>` compound key.

Denomination types:

- **Numeric**: `5`, `50`, `200` (number).
- **Duration**: `"1 Month"`, `"12 Months"` (exact, case-sensitive).
- **Named**: `"1GB, 7 Days"`, `"PUBG New State 300 NC"` (exact, case-sensitive).

Only values from `get-product-details` accepted.

### 3. Buy

`--cart_items` = JSON **array**, even single item. Max 15. **`--email`** = receipt (required guest; optional signed-in).

```bash
# Guest — crypto + payment link
bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_id":"10"}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "agent@example.com"

# Signed-in — crypto via x402
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method usdc_base

# Duration package
bitrefill buy-products \
  --cart_items '[{"product_id": "spotify-usa", "package_id": "1 Month"}]' \
  --payment_method usdc_base

# Named eSIM
bitrefill buy-products \
  --cart_items '[{"product_id": "bitrefill-esim-europe", "package_id": "1GB, 7 Days"}]' \
  --payment_method usdc_base
```

Response: `invoice_id`, `payment_link`, `x402_payment_url`, `payment_info` (`address`, `paymentUri`, `altcoinPrice`).

**Pay** → [../wallets/payment.md](../wallets/payment.md): x402 on `x402_payment_url` or Base MCP `send` to `payment_info`. For balance, leave the CLI path and use [api.md](api.md)'s authorized REST two-step flow.

### 4. Track / Redeem

```bash
bitrefill get-invoice-by-id --invoice_id "UUID"   # guest OK (save invoice_id from buy)
bitrefill list-orders --include_redemption_info true   # signed-in only
bitrefill get-order-by-id --order_id "ID"              # signed-in only
```

Use the invoice's authoritative expiry/status. Recreate only after confirmed unpaid expiry releases its principal: freeze the attempt, retain any settled fee, then create one new attempt/idempotency key under the same logical purchase with a fresh confirmed total and reservations.

## Critical gotchas

- `--cart_items` = **array** `[...]`, not object `{...}`. Single quotes outside, double inside.
- Use `package_value` after `<&>`, not compound key. WRONG `"steam-usa<&>5"`. RIGHT `5`.
- Named/duration `package_id` exact, case-sensitive. WRONG `"1GB"`. RIGHT `"1GB, 7 Days"`.
- Country uppercase Alpha-2. WRONG `us`, `USA`. RIGHT `US`.
- `login`/`verify` only when not signed in. `logout` before switching accounts.
- Guest: `--payment_method balance`/`cashback` fail. Use crypto; guarded balance requires sign-in plus the authorized REST two-step route, and guarded cashback remains blocked.
- Signed-in + 2FA: `verify` needs **both** `--code` (email) + `--otp` (authenticator).

## Payment methods

Pay-time routing → [../wallets/payment.md](../wallets/payment.md). Prefer balance only through authorized direct REST with `auto_pay: false`, then pay that pre-reserved invoice. Guest: `usdc_base` or `lightning` + wallet from [../wallets/matrix.md](../wallets/matrix.md).

## Source of truth

- <https://github.com/bitrefill/cli> — commands, options, flags
- <https://docs.bitrefill.com/docs/crypto-payments> — payment methods
- `bitrefill manifest --json` / `bitrefill llm-context` — live tool list + schemas

**User hears:** "Searching for [product]…" → "[Product] — [amount]: [exact total and payment asset]. Confirm?" → "Approve the payment" → "Your code is ready."
