# Path: Browse the Website

Use when: user wants to **explore** Bitrefill (compare prices, learn product types, check denominations, see country availability) AND your runtime has a **residential-IP browser**. Browse-only by default — for purchases prefer [mcp.md](mcp.md).

## Hard requirement: residential IP

`www.bitrefill.com` sits behind Cloudflare. **Datacenter egress = 403.** Do NOT use Firecrawl, raw `fetch`, `curl`, or any scraping API.

Viable runtimes:

- **ChatGPT Atlas** — built-in residential Chromium.
- **Cursor** — built-in browser tool runs from user's machine.
- **Claude Code / Desktop / Cowork + Claude-for-Chrome** extension drives local Chrome.
- **Any host + Playwright/Chrome MCP** running on user's machine.
- **OpenClaw Gateway on user's host** — `browser` tool uses host IP. (See [host-openclaw.md](host-openclaw.md).)

Not viable: ChatGPT web/Agent (OpenAI datacenter), Gemini consumer (Google datacenter), Jules (Google VM), any cloud sandbox without residential proxy.

## URL patterns

First path segment = **country** (Alpha-2 lowercase). Second = **language**.

- Gift cards listing: `https://www.bitrefill.com/{country}/{lang}/gift-cards/`
- Gift card category: `https://www.bitrefill.com/{country}/{lang}/gift-cards/{category-slug}/` (e.g. `/us/en/gift-cards/food/`)
- Gift card product: `https://www.bitrefill.com/{country}/{lang}/gift-cards/{product-slug}/`
- Direct search: `https://www.bitrefill.com/{country}/{lang}/gift-cards/?q={query}` (covers gift cards + top-ups + eSIMs; in-country prioritized)
- Mobile top-ups: `https://www.bitrefill.com/refill/`
- eSIMs (locale): `https://www.bitrefill.com/{country}/{lang}/esims/`
- eSIMs (browse all destinations): `https://www.bitrefill.com/esim/all-destinations`
- Single eSIM: `https://www.bitrefill.com/{country}/{lang}/esims/bitrefill-esim-{destination-slug}/` (e.g. `bitrefill-esim-japan`, `bitrefill-esim-global`)
- Auth (no locale prefix): `/login`, `/signup`

## Country in URL vs geolock

- **URL country** filters which inventory is **listed**.
- **Geolock** is enforced at **IP level** at checkout. A product may appear in listing but be unpurchasable if user's IP is outside allowed region.

Match URL country to recipient's country to surface usable cards.

## Listing filters & sort (gift cards)

Query params on any gift-card listing (`/{country}/{lang}/gift-cards/[category/]`):

- `redemptionMethod` — `online` | `instore`
- `minRating` — `2` | `3` | `4` | `5`
- `minRewards` — `1`–`10` (cashback %)
- `s` — sort: `2` = A–Z, `3` = recently added, `4` = cashback. Default = popularity.

Example: `https://www.bitrefill.com/us/en/gift-cards/food/?minRating=5&minRewards=4&redemptionMethod=instore`

## Categories (popular slugs)

`top-products`, `retail`, `apparel`, `electronics`, `food`, `restaurants`, `food-delivery`, `streaming`, `games`, `travel`, `flights`, `accommodation`, `entertainment`, `gasoline`, `vpn`, `multi-brand`, `digital-wallet`, `groceries`, `pharmacy`, `experiences`, `gifts`. Full list: <https://docs.bitrefill.com/docs/Products>.

## Suggested flow

1. Clarify product type (gift card / top-up / eSIM) + country (+ carrier for top-ups).
2. Send user to direct search URL or category path.
3. For top-ups: country → carrier → amount.
4. For eSIMs: destination → data + duration.
5. Remind user to check denomination matches recipient's needs and that geolock applies at checkout.

## Purchase from the browser?

Possible but slow and risky. Anti-bot may block agent on brand redemption sites. Prefer [mcp.md](mcp.md) or [cli.md](cli.md) for purchases. If browser checkout is the only option, follow [safeguards.md](safeguards.md) — confirm with user, log invoice ID, treat redemption code as cash.

## Source of truth

- <https://www.bitrefill.com>
- <https://help.bitrefill.com>
- <https://docs.bitrefill.com/docs/Products>
