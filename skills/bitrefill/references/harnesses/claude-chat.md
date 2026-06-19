# Host: Claude Chat (claude.ai)

[Claude Chat](https://claude.ai) — **no agent shell** (`exec` / npm / bundled scripts). **Chat-level MCP connectors** work independent of code-execution sandbox.

Covers **claude.ai** + custom MCP (Pro+ for connector URLs; Free has code execution, not custom MCP). Claude Code / Desktop / Cowork → [capability-matrix.md](capability-matrix.md) + [../touchpoints/mcp.md](../touchpoints/mcp.md). Only **claude.ai** has **`show_widget`** generative UI.

**Priority:** Bitrefill MCP → Base MCP x402 pay → x402 REST Path 1 via Base MCP `web_request` → payment link. Route all Bitrefill API via **MCP tools**, not sandbox.

## 1. Detect Claude Chat

All must hold:

- Host = **claude.ai** web chat (not Claude Code, not Cowork desktop shell).
- Tools include **`show_widget`** + **`read_me`**.
- Settings → Connectors can add custom MCP URLs (**Pro+** for custom MCP).
- **`exec` / shell / npm** **not** available.

Yes → continue. OpenClaw → [openclaw.md](openclaw.md). Else → [decision-engine.md](decision-engine.md) + [capability-matrix.md](capability-matrix.md).

## 2. Install connectors

Settings → Connectors → Add custom connector:

| Connector | URL | Role |
| --- | --- | --- |
| Bitrefill eCommerce MCP | `https://api.bitrefill.com/mcp` | OAuth; `search-products`, `buy-products`, poll |
| Base MCP | `https://mcp.base.org` | `web_request`, `sign`, x402 pay, optional `send` |

First Bitrefill call → OAuth (allow pop-ups / third-party cookies if loop — [../troubleshooting.md](../troubleshooting.md)). Keep **per-tool approval on**; never auto-approve `buy-products` ([../safeguards.md](../safeguards.md)).

Setup → [../touchpoints/mcp.md](../touchpoints/mcp.md) § Claude.ai. Guide → <https://docs.bitrefill.com/docs/use-with-claude-chat>.

## 3. Sandbox vs MCP (network layers)

Two separate paths. Don't conflate.

| Environment | What | Network | Bitrefill routing |
| --- | --- | --- | --- |
| **Chat MCP** | Connectors as host tools | Always reaches MCP URLs | **Preferred** — catalog, checkout, x402 pay |
| **Code execution sandbox** | Server-side Ubuntu (Python/Node/shell inside Claude sandbox) | Admin/user controlled allowlist | **Don't use** for Bitrefill API |
| **Analysis tool (legacy)** | Browser JS (mutually exclusive with code execution) | **None** | N/A — disable if using code execution |

**MCP traffic independent of sandbox egress** — connectors work when sandbox egress off. [Create and edit files with Claude](https://support.anthropic.com/en/articles/12111783-create-and-edit-files-with-claude).

### Plan defaults (sandbox egress)

Source: Anthropic Help Center (Apr 2026). Org: **Organization settings → Capabilities → Code execution and file creation**.

| Plan | Code execution default | Sandbox egress default |
| --- | --- | --- |
| **Free / Pro / Max** | Off until user enables **Settings → Capabilities** | When on: **Allow network egress ON** — package managers only |
| **Team** | **On** at org level | **On** — package managers only; owner can disable |
| **Enterprise** | **On** for new orgs | **Off** — owner enables + domain whitelist |

**Team egress enabled** ≠ open internet. Default = package managers only (`pypi.org`, `registry.npmjs.org`, `github.com`, …). **`api.bitrefill.com` not on default allowlist.**

### Admin egress levels (Team / Enterprise)

| Setting | Sandbox can reach | Bitrefill via sandbox? |
| --- | --- | --- |
| Egress **off** | Pre-installed packages only | No |
| **Package managers only** (Team default when on) | npm, PyPI, GitHub, Ubuntu mirrors, … | No (unless admin whitelists `api.bitrefill.com`) |
| Package managers **+ custom domains** | Above + owner-whitelisted hosts | Only if `api.bitrefill.com` whitelisted |
| **All domains** | Internet except Anthropic blocklist | Yes — still **avoid**; use MCP |

Even with sandbox egress: **no `exec` tool** — can't run [`siwx_build_message.js`](../../scripts/siwx_build_message.js) locally. Sandbox = Claude-internal, not agent shell.

## 4. Fixed capability profile

| Probe | Claude Chat value |
| --- | --- |
| `exec_available` | **false** (sandbox ≠ agent exec) |
| `egress_direct` | **false** |
| `egress_mcp_proxy` | **true** when Base MCP connected |
| `browser_residential` | Chrome extension only (explore — [../touchpoints/browse.md](../touchpoints/browse.md)) |
| `bitrefill_mcp_live` | `search-products` visible after OAuth (Pro+) |
| `base_mcp_live` | `get_wallets` / `web_request` / `initiate_x402_request` visible |

**Rule:** probe **`bitrefill_mcp_live`** + **`base_mcp_live`** — ignore sandbox egress for touchpoint. SIWX for x402 REST → Base MCP in-context assembly only → [../wallets/siwx.md](../wallets/siwx.md).

## 5. Ranked stack (autonomy-first)

| Rank | Touchpoint | Wallet | Residual HITL |
| --- | --- | --- | --- |
| 1 | Bitrefill MCP | `balance` + `auto_pay: true` | Confirm purchase only |
| 2 | Bitrefill MCP | Base MCP x402 on `x402_payment_url` | OAuth + 1 Base approval/pay |
| 3 | x402 REST Path 1 | Base MCP SIWX + x402 | 1 connect + 1 pay / ~2 h JWT |
| 4 | Bitrefill MCP | Base MCP `send` | OAuth + 1 send/pay |
| 5 | Bitrefill MCP | `payment_link` / Lightning | Human completes pay |

**Avoid:** CLI, bundled Node scripts, x402 Path 2 (per-call micro-fees), datacenter browse checkout.

**Dual-MCP:** both live → **Bitrefill MCP owns catalog/checkout**; **Base MCP owns pay** — don't duplicate browse via Base `web_request` when Bitrefill MCP OAuth'd.

## 6. Primary workflow — Bitrefill MCP + Base MCP

1. **Search** — `search-products(query, country=<Alpha-2>, product_type=...)`.
2. **Detail** — `get-product-details(product_id, currency="USDC")` → exact `package_value` / `package_id`.
3. **Confirm** — product, denomination, exact price with user before buy.
4. **Buy** — `buy-products(cart_items=[...], payment_method="usdc_base", return_payment_link=true)` (or `"balance"` + `auto_pay: true` when pre-funded).
5. **Pay** ([../wallets/payment.md](../wallets/payment.md)):
   - **Best:** `payment_method: "balance"` + `auto_pay: true`.
   - **Default USDC:** Base MCP `initiate_x402_request(url=x402_payment_url, method, maxPayment)` → user approves Base Account → `complete_x402_request(requestId)`. `maxPayment` slightly above `price_usd`.
   - **Fallback:** Base MCP `send` to `payment_info.address` / `payment_info.altcoinPrice`.
6. **Poll** — `get-invoice-by-id(invoice_id)` until `invoice_status: complete` / `orders_delivery_status: all_delivered`.
7. **Deliver** — `orders[].redemption_info`; log per safeguards; never paste codes in shared channels.

MCP tools → [../touchpoints/mcp.md](../touchpoints/mcp.md). Base MCP pay → [../wallets/base-mcp.md](../wallets/base-mcp.md).

## 7. Fallback — x402 REST via Base MCP

When Bitrefill MCP unavailable (no OAuth, connector cap, guest commerce):

Path 1 → [../touchpoints/x402.md](../touchpoints/x402.md). Summary:

1. SIWX connect → JWT (`X-Access-Token`, ~2 h) via Base MCP `web_request` + `sign` (no scripts).
2. Search → detail → `invoice/create` with token.
3. User confirms → x402 pay on `invoice/pay` via Base MCP x402 tools.
4. Poll `invoice/status` → SIWX on status route if codes missing.

Every gated x402 response embeds **`next_step: { url, body }`** — use for widget primary CTAs (§8).

## 8. `show_widget` — generative UI

Inline shopping UI via host **`show_widget`** — not Artifacts, not HTML in prose. **Narrative in assistant message; visual in `widget_code` only.**

### Prerequisites — `read_me`

Once per session before first widget:

```json
{ "modules": ["interactive"] }
```

Every `show_widget` → **`i_have_seen_read_me`: true**.

### Parameters

| Parameter | Required | Notes |
| --- | --- | --- |
| `i_have_seen_read_me` | yes | `true` after `read_me` |
| `title` | yes | snake_case id (e.g. `bitrefill_search_results`) |
| `widget_code` | yes | HTML fragment — structure below |
| `loading_messages` | optional | 1–4 strings while streaming |

### `widget_code` structure

Order: **`<style>` → HTML → `<script>`**. No `<html>`, `<head>`, `<body>`.

External scripts: CDN allowlist only — `cdnjs.cloudflare.com`, `cdn.jsdelivr.net`, `unpkg.com`, `esm.sh`.

### When to call

| Flow stage | Widget title | Data source |
| --- | --- | --- |
| Search results | `bitrefill_search_results` | MCP `search-products` or x402 `products[]` |
| Product detail | `bitrefill_product_detail` | MCP `get-product-details` or x402 `packages[]` |
| Invoice summary | `bitrefill_invoice_created` | MCP `buy-products` or x402 create |
| Delivery / codes | `bitrefill_delivery_status` | MCP `get-invoice-by-id` or x402 `invoice/status` |

**One widget per turn** at shopping state change. Explanatory text outside widget.

### Primary CTA — `sendPrompt(...)`

Primary button → host **`sendPrompt(text)`**. Prompt must carry context for next MCP/x402 step (slug, `package_value`, `invoice_id`).

**x402 REST:** primary CTA follows response **`next_step`** — not generic label.

**Bitrefill MCP:** map verb patterns by flow stage:

| State | Primary CTA label | Agent action after `sendPrompt` |
| --- | --- | --- |
| Search results | "See details for [product name]" | `get-product-details` or x402 detail |
| Product detail | "Buy [amount] on [product name]" | `buy-products` or x402 create |
| Invoice created | "Confirm and pay [amount] USDC" | Base MCP x402 pay |
| Payment confirmed | "Check delivery status" | `get-invoice-by-id` or x402 status poll |

**Secondary CTA** = lateral escape only (new search, help, different product). Never forward in funnel.

### UI/UX rules (host + Bitrefill)

**Typography:** no `font-family` (inherit host). Body/interactive ≥ **16px**; 14px meta only (non-interactive). **`font-weight: 500`** labels/names/primary button; **`400`** else. **`font-variant-numeric: tabular-nums`** on prices. **`text-wrap: balance`** on headings.

**Selectable components (cards, toggles):** no CLS on select. Resting: `border: 2px solid transparent` + `outline: 0.5px solid var(--color-border-tertiary)` + `outline-offset: -1px`. Selected: `border-color: var(--color-border-info)` + `background: var(--color-background-info)`; remove outline. Toggles: **`aria-pressed`**. List options: **`aria-selected`**. Keyboard: **`Enter`** + **`Space`** with `event.preventDefault()` on keydown.

**Hit areas:** interactive elements **`min-height: 44px`**, flex-centered.

**Buttons:** exactly one primary + one secondary, full-width, left-aligned, leading Tabler outline icon (`font-size: 18px`). Primary: `font-weight: 500`, `border: 0.5px solid var(--color-border-secondary)`. Secondary: `font-weight: 400`, `color: var(--color-text-secondary)`, `border: 0.5px solid var(--color-border-tertiary)`. Both: `display: flex; align-items: center; gap: 10px`. Press: `transform: scale(0.97)` on `:active`. Below primary: one-line **14px** hint in `var(--color-text-tertiary)`.

**CTA logic — x402 `next_step`:**

| State | `next_step` target | Primary CTA label |
| --- | --- | --- |
| Search results | `products/detail` | "See details for [product name]" |
| Product detail | `invoice/create` | "Buy [amount] on [product name]" |
| Invoice created | `invoice/pay` | "Confirm and pay [amount] USDC" |
| Payment confirmed | `invoice/status` | "Check delivery status" |

**Microcopy:** user world ("Buy 10 EUR on Amazon.it" not "Create invoice"). Dynamic labels: changing part first. **Pre-select defaults** (smallest denomination) so primary CTA works on first paint. Warnings just above CTA.

**Accessibility:** dynamic CTA regions `aria-live="polite" aria-atomic="true"`. Card grids: `role="listbox"` + `role="option"`. Toggle groups: `role="group"` + `aria-label`. Start with visually hidden `<h2 class="sr-only">`. Never color-only — pair with `aria-selected` / `aria-pressed`.

**Color:** CSS variables only. No hardcoded hex except amber star **`#EF9F27`** + warning note borders.

**Constraints:** no shadows, gradients, blur, glow, or `transition: all`. Use `transition: background .15s, border-color .15s, color .15s`. Press scale **`0.97`** only.

## 9. Claude Chat safeguards

- Per-tool approval on; **never whitelist `buy-products`**.
- Confirm product, denomination, exact USDC total before pay.
- JWT / tokens in-memory only (~2 h); never log or paste in chat.
- Redemption codes: deliver privately; never shared project threads.
- **`show_widget` = presentation only** — payment still needs explicit MCP pay approval.

Full policy → [../safeguards.md](../safeguards.md).

## 10. What not to do

- Route Bitrefill API via **code sandbox** — default allowlist excludes `api.bitrefill.com`; use MCP even when Team egress on.
- Assume sandbox egress replaces MCP — MCP works regardless.
- Use **`Authorization`** on Base MCP (stripped) — use `X-Access-Token` + `sign-in-with-x`.
- Base MCP `web_request` to `docs.bitrefill.com` (not allowlisted).
- Datacenter browse checkout (Cloudflare) — MCP/x402 only.
- Shopping UI in **Artifacts** or raw HTML when `show_widget` available.
- **x402 Path 2** when Path 1 JWT possible.

## 11. Troubleshooting

| Issue | Fix |
| --- | --- |
| Free tier — cannot add MCP | Upgrade Pro+ or send `bitrefill.com` link |
| OAuth loop | Allow pop-ups; retry; [../troubleshooting.md](../troubleshooting.md) |
| MCP tools not visible | Re-auth connector; check Pro+ |
| `show_widget` rejected | `read_me` with `interactive` first; `i_have_seen_read_me: true` |
| Sandbox egress but Bitrefill fails | Expected — use MCP connectors |
| `INVOICE_NOT_PAYABLE` on pay | Already settled — poll status |
| Widget CTA dead | `<script>` must call `sendPrompt(...)` after stream completes |

## Source of truth

- Bitrefill Claude Chat: <https://docs.bitrefill.com/docs/use-with-claude-chat>
- Anthropic code execution + network: <https://support.anthropic.com/en/articles/12111783-create-and-edit-files-with-claude>
- MCP: [../touchpoints/mcp.md](../touchpoints/mcp.md) | x402: [../touchpoints/x402.md](../touchpoints/x402.md) | Base MCP: [../wallets/base-mcp.md](../wallets/base-mcp.md)
- Routing: [decision-engine.md](decision-engine.md), [capability-matrix.md](capability-matrix.md)
