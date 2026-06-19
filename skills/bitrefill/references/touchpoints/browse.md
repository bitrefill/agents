# Path: Browse the Website

User wants to **explore** Bitrefill (compare prices, product types, denominations, country availability) AND runtime has **residential-IP browser**. Browse-only default — purchases prefer [mcp.md](mcp.md) or [decision-engine.md](../harnesses/decision-engine.md).

## Hard requirement: residential IP

`www.bitrefill.com` behind Cloudflare. **Datacenter egress = 403.** No Firecrawl, raw `fetch`, `curl`, scraping APIs.

Viable:

- **ChatGPT Atlas** — residential Chromium.
- **Cursor** — browser tool from user's machine.
- **Claude Code / Desktop / Cowork + Claude-for-Chrome** — local Chrome.
- **Any host + Playwright/Chrome MCP** on user's machine.
- **OpenClaw Gateway on user host** — `browser` = host IP. → [../harnesses/openclaw.md](../harnesses/openclaw.md).

Not viable: ChatGPT web/Agent (OpenAI datacenter), Gemini consumer (Google datacenter), Jules (Google VM), cloud sandbox without residential proxy.

## URL patterns

First segment = **country** (Alpha-2 lowercase). Second = **language**.

- Gift cards listing: `https://www.bitrefill.com/{country}/{lang}/gift-cards/`
- Gift card category: `https://www.bitrefill.com/{country}/{lang}/gift-cards/{category-slug}/` (e.g. `/us/en/gift-cards/food/`)
- Gift card product: `https://www.bitrefill.com/{country}/{lang}/gift-cards/{product-slug}/`
- Direct search: `https://www.bitrefill.com/{country}/{lang}/gift-cards/?q={query}` (gift cards + top-ups + eSIMs; in-country prioritized)
- Mobile top-ups: `https://www.bitrefill.com/refill/`
- eSIMs (locale): `https://www.bitrefill.com/{country}/{lang}/esims/`
- eSIMs (all destinations): `https://www.bitrefill.com/esim/all-destinations`
- Single eSIM: `https://www.bitrefill.com/{country}/{lang}/esims/bitrefill-esim-{destination-slug}/` (e.g. `bitrefill-esim-japan`, `bitrefill-esim-global`)
- Auth (no locale): `/login`, `/signup`

## Country in URL vs geolock

- **URL country** filters **listed** inventory.
- **Geolock** enforced at **IP** at checkout. Product may list but be unpurchasable outside allowed region.

Match URL country to recipient country.

## Listing filters & sort (gift cards)

Query params on `/{country}/{lang}/gift-cards/[category/]`:

- `redemptionMethod` — `online` | `instore`
- `minRating` — `2` | `3` | `4` | `5`
- `minRewards` — `1`–`10` (cashback %)
- `s` — sort: `2` = A–Z, `3` = recently added, `4` = cashback. Default = popularity.

Example: `https://www.bitrefill.com/us/en/gift-cards/food/?minRating=5&minRewards=4&redemptionMethod=instore`

## Categories (popular slugs)

`top-products`, `retail`, `apparel`, `electronics`, `food`, `restaurants`, `food-delivery`, `streaming`, `games`, `travel`, `flights`, `accommodation`, `entertainment`, `gasoline`, `vpn`, `multi-brand`, `digital-wallet`, `groceries`, `pharmacy`, `experiences`, `gifts`. Full: <https://docs.bitrefill.com/docs/Products>.

## Suggested flow

1. Clarify product type (gift card / top-up / eSIM) + country (+ carrier for top-ups).
2. Direct search URL or category path.
3. Top-ups: country → carrier → amount.
4. eSIMs: destination → data + duration.
5. Remind denomination matches recipient; geolock at checkout.

## Purchase from browser?

Possible but slow, risky. Anti-bot may block brand redemption. Prefer [mcp.md](mcp.md) or [cli.md](cli.md). Browser checkout only option → [../safeguards.md](../safeguards.md) — confirm with user, log invoice ID, treat code as cash.

## Source of truth

- <https://www.bitrefill.com> | <https://help.bitrefill.com> | <https://docs.bitrefill.com/docs/Products>
