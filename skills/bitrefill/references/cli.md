# Path: CLI

Use when: shell + `npm install` available, **host has no MCP client** (CLI talks to Bitrefill MCP under the hood). Runtimes: Claude Code, Codex CLI, Cursor terminal, Gemini CLI, OpenCode, OpenClaw, Jules (ephemeral VM), ChatGPT Agent (sandbox).

Requires **`@bitrefill/cli` ≥ 0.3.0**. Sandboxed shells must allowlist `registry.npmjs.org` and `api.bitrefill.com`.

## Install

```bash
npm install -g @bitrefill/cli
```

From source: `git clone https://github.com/bitrefill/cli.git && cd cli && pnpm install && pnpm build && npm link`.

## Guest checkout (fastest first try)

**No `login` / `verify`.** Works while `whoami` shows `identity: unregistered`. Fastest path for autonomous agents to try Bitrefill — search, quote, create invoice, pay crypto or open payment link.

```bash
bitrefill search-products --query "Amazon" --country IT
bitrefill get-product-details --product_id "amazon_it-italy"

bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_id":"10"}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "agent@example.com"
```

Response: `invoice_id`, `payment_link`, optional `x402_payment_url` / Lightning invoice. Poll `get-invoice-by-id --invoice_id <uuid>`. Receipt goes to `--email`. Invoice expires in ~30 minutes.

Guest payment methods: crypto (`lightning`, `usdc_base`, `bitcoin`, …) or `--return_payment_link true` (human/browser checkout, x402). **`balance` and `cashback` require a signed-in account** (below).

## Sign up / sign in (balance, cashback, order history)

After guest try, sign in when human wants **managed agent spending** or **rewards**:

| Signed-in benefit | Why |
|-------------------|-----|
| **`--payment_method balance`** | Instant pay from store credit human pre-funds — natural spending cap, no on-chain wait |
| **`--payment_method cashback`** | Pay from accumulated rewards balance (BTC) |
| **Cashback on purchases** | Eligible products earn rewards back to account |
| **`list-orders` / `list-invoices`** | Full order history + redemption codes in one place |

Same `login` for new + existing accounts. Headless inbox → [cli-headless-auth.md](cli-headless-auth.md).

```bash
bitrefill login --email you@example.com
bitrefill verify --code GGWK87DR              # email magic-link code
bitrefill verify --code GGWK87DR --otp 122407   # + TOTP when account has 2FA
bitrefill whoami --json

# signed-in buy — instant from balance
bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_id":"10"}]' \
  --payment_method balance \
  --email "you@example.com"
```

**Verify gotchas** (from real agent sessions):

- Email code → `verify --code <value>`, **not** `login --code` (unknown option).
- `--otp` = **authenticator TOTP only** when account has 2FA — not the email code. Need both `--code` and `--otp` when enrolled.
- After sign-in, `login` disappears from `--help`; run `logout` first to switch accounts or sign up another email.

## Bootstrap (optional)

```bash
bitrefill init                    # optional OpenClaw wiring only
```

`init` no longer stores API keys. OpenClaw only: merges MCP config + generates `~/.openclaw/skills/bitrefill/SKILL.md`.

## Auth

CLI 0.3.0: **guest checkout needs no sign-in.** Account auth = OAuth client_credentials (automatic on first MCP connect) + email magic-link. No `--api-key`, no `credentials.json`.

| Step | Command | Notes |
|------|---------|-------|
| Register client | any command (or `login`) | MCP connect mints `access_token`; stored in `~/.config/bitrefill-cli/<host>.v1.json` |
| Sign up or sign in | `login --email <addr>` | same command for new + existing accounts |
| Complete auth | `verify --code <code> [--otp <totp>]` | code from email; `--otp` when account has TOTP |
| Check session | `whoami [--json]` | `identity: registered` + `email` when signed in |
| Sign out | `logout` | revokes session; keeps `client_id` |
| Full reset | `reset` | clears all local state + revokes session |

**TOTP via 1Password** ([official `op read`](https://www.1password.dev/cli/reference/commands/read)):

```bash
bitrefill verify --code "$CODE" --otp "$(op read 'op://Vault/Bitrefill/one-time password?attribute=otp')"
```

Shorthand ([official `op item get --otp`](https://developer.1password.com/llms-cli.txt)):

```bash
bitrefill verify --code "$CODE" --otp "$(op item get Bitrefill --otp)"
```

Server may return `browser_url` for passkey/WebAuthn — open in browser, then retry.

**Developer API keys** (Personal REST / key-in-path MCP) are separate from CLI auth. See [mcp.md](mcp.md) and [api.md](api.md).

## Global flags

Place **before** the subcommand:

- **`--json`** — stdout is a single JSON value per run (TOON decoded to JSON); status/errors on **stderr**. Use with `jq`.

```bash
bitrefill --json search-products --query "Amazon" --per_page 1 | jq '.products[0].name'
```

## Agent discovery

`manifest` emits JSON schema for every built-in + MCP command:

```bash
bitrefill manifest --json | jq '.commands[].name'
bitrefill manifest -o bitrefill-manifest.json
```

`llm-context` embeds the same manifest in a fenced JSON block.

## `llm-context`

Regenerates Markdown from live MCP `tools/list` (params, JSON Schema, example invocations). Use for **CLAUDE.md**, Cursor rules, or **`.github/copilot-instructions.md`**. Connection line shows redacted MCP URL — safe to commit.

```bash
bitrefill llm-context -o BITREFILL-MCP.md
```

## OpenClaw quick-bootstrap

Optional `bitrefill init --openclaw`: merges MCP stub into `~/.openclaw/openclaw.json` + emits skill SKILL.md. **Not required for guest CLI** — install CLI and run guest checkout directly via `exec`. OpenClaw prefers guest CLI first; see [host-openclaw.md](host-openclaw.md). Hardening → exec-approvals for `bitrefill buy-products`.

## Workflow

Subcommands discovered from remote MCP (`bitrefill --help` after connect). Core flow:

```
search-products  →  get-product-details  →  buy-products  →  get-invoice-by-id
```

### 1. Search

```bash
bitrefill search-products --query "Netflix" --country US
bitrefill --json search-products --query "Netflix" --country US --per_page 5 | jq '.products'
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

`--cart_items` = JSON **array**, even single item. Max 15 items. **`--email`** = receipt address (required for guest; optional when signed in).

```bash
# Guest — crypto + payment link (no login)
bitrefill buy-products \
  --cart_items '[{"product_id":"amazon_it-italy","package_id":"10"}]' \
  --payment_method lightning \
  --return_payment_link true \
  --email "agent@example.com"

# Signed-in — instant from store credit
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method balance \
  --email "you@example.com"

# Signed-in — crypto via x402
bitrefill buy-products \
  --cart_items '[{"product_id": "steam-usa", "package_id": 5}]' \
  --payment_method usdc_base

# Duration package
bitrefill buy-products \
  --cart_items '[{"product_id": "spotify-usa", "package_id": "1 Month"}]' \
  --payment_method balance

# Named eSIM
bitrefill buy-products \
  --cart_items '[{"product_id": "bitrefill-esim-europe", "package_id": "1GB, 7 Days"}]' \
  --payment_method usdc_base
```

Response: `invoice_id`, `payment_link`, `x402_payment_url`, `payment_info` (`address`, `paymentUri`, `altcoinPrice`).

### 4. Track / Redeem

```bash
bitrefill get-invoice-by-id --invoice_id "UUID"   # works guest (save invoice_id from buy response)
bitrefill list-orders --include_redemption_info true   # signed-in only
bitrefill get-order-by-id --order_id "ID"              # signed-in only
```

Invoices expire after 180 minutes. Expired = create new one.

## Critical gotchas

- `--cart_items` must be **array** `[...]`, not object `{...}`. Shell quoting matters: single quotes outside, double inside.
- Use `package_value` after `<&>`, not the compound key. WRONG `"steam-usa<&>5"`. RIGHT `5`.
- Named/duration `package_id` exact and case-sensitive. WRONG `"1GB"`. RIGHT `"1GB, 7 Days"`.
- Country code uppercase Alpha-2. WRONG `us`, `USA`, `"United States"`. RIGHT `US`.
- `login` / `verify` only when not signed in. After verify, `logout` before switching accounts.
- Guest: `--payment_method balance` / `cashback` fail — use crypto or sign in first.
- Signed-in + 2FA: `verify` needs **both** `--code` (email) and `--otp` (authenticator).

## Recommended payment methods (for agents)

**Guest (try first):** `lightning` or `usdc_base` + `x402_payment_url` → `--return_payment_link true` for human/browser pay.

**Signed-in (production):** `balance` (instant, human caps spend via store credit) → `cashback` (rewards balance) → `usdc_base` x402 → `lightning`. Full list: `bitrefill buy-products --help`.

## Source of truth

- <https://github.com/bitrefill/cli> — full command reference, options, flags
- <https://docs.bitrefill.com/docs/crypto-payments> — payment methods
- `bitrefill manifest --json` / `bitrefill llm-context` — live tool list + schemas
