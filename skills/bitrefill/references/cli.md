# Path: CLI

Use when: shell + `npm install` available, **host has no MCP client** (the CLI talks to Bitrefill MCP under the hood). Runtimes: Claude Code, Codex CLI, Cursor terminal, Gemini CLI, OpenCode, OpenClaw, Jules (ephemeral VM), ChatGPT Agent (sandbox).

Sandboxed shells must allowlist `registry.npmjs.org` and `api.bitrefill.com`.

## Install

```bash
npm install -g @bitrefill/cli
```

**First-time setup** (validates API key against MCP, stores credentials, auto-configures OpenClaw if `~/.openclaw/openclaw.json` exists):

```bash
bitrefill init                                          # interactive
bitrefill init --api-key $KEY --non-interactive         # CI / agents
bitrefill init --openclaw                               # force OpenClaw integration
```

From source: `git clone https://github.com/bitrefill/cli.git && cd cli && pnpm install && pnpm build && npm link`.

## Auth

Resolution order (first match wins):

1. **`--api-key <key>`** — global flag; can appear before any subcommand.
2. **`BITREFILL_API_KEY`** — environment variable.
3. **`~/.config/bitrefill-cli/credentials.json`** — written by `bitrefill init` (mode `0600`). Overwrite or remove to change the key.
4. **OAuth** — only when no key is available **and** the session is interactive (TTY, not `CI=true`). Browser flow; state under `~/.config/bitrefill-cli/<host>.json` (e.g. `api.bitrefill.com.json`). Clear with `bitrefill logout` (OAuth only; no-op when using API key only).

Generate keys at <https://www.bitrefill.com/account/developers>.

## Global flags

Place **before** the subcommand:

- **`--api-key <key>`** — override env and stored file.
- **`--json`** — stdout is a single JSON value per run (TOON responses decoded to JSON); status and errors go to **stderr**. Use with `jq`.
- **`--no-interactive`** — skip browser OAuth and prompts; also implied when `CI=true` or stdin is not a TTY. Fails fast if no API key.

```bash
bitrefill --json search-products --query "Amazon" --per_page 1 | jq '.products[0].name'
```

## `llm-context`

Regenerates Markdown from the live MCP `tools/list` (params, JSON Schema, example `bitrefill …` and `tools/call` payloads). Use for **CLAUDE.md**, Cursor rules, or **`.github/copilot-instructions.md`**. Connection line shows `…/mcp/<API_KEY>` (redacted), safe to commit.

```bash
bitrefill llm-context -o BITREFILL-MCP.md
# or: bitrefill llm-context > BITREFILL-MCP.md
```

## OpenClaw quick-bootstrap

If OpenClaw is detected (`~/.openclaw/openclaw.json` readable) or you pass `--openclaw`, `bitrefill init` can: write `BITREFILL_API_KEY` to `~/.openclaw/.env`, merge the Bitrefill MCP server into `~/.openclaw/openclaw.json` (env-var reference, no plaintext key in JSON), and emit `~/.openclaw/skills/bitrefill/SKILL.md`. Hardening and channel setup → [host-openclaw.md](host-openclaw.md).

## Workflow

Subcommands are discovered from the remote MCP server (`bitrefill --help` after connect). Core flow:

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
- `bitrefill llm-context` — live tool list + schemas from the MCP server
