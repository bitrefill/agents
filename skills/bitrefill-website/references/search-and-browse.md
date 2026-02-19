# Search and Browse on Bitrefill

Use this reference when the user wants to **find** a product: search by brand, browse by category, or filter by country/amount.

## Entry Points by Product Type

| Product type      | Main URL                              | How to narrow down |
|-------------------|---------------------------------------|---------------------|
| Gift cards        | bitrefill.com/{country}/{lang}/gift-cards/ | Category, country, brand search |
| Mobile top-ups    | bitrefill.com/refill/                 | Country → carrier → amount |
| eSIMs             | bitrefill.com/{country}/{lang}/esims/ | Country/region → data/duration |
| eSIM all-destinations | bitrefill.com/esim/all-destinations | Browse 190+ countries/regions; then open locale-specific product page |
| All categories    | bitrefill.com/categories              | Overview of everything |

## Country in URL vs Geolock

- **Country in URL:** URL path is **country** then **language** (e.g. `/us/en/gift-cards/`, `/mx/es/gift-cards/`). The country segment **filters which gift cards are listed** — only those usable in that country. To see a specific country's inventory, use that country as the first path segment.
- **Geolock:** Enforced at **IP level**. Whether a product is purchasable depends on the user's IP/location, not on the country in the URL. A product may appear in the listing but be unavailable at checkout if the user's IP is outside the allowed region.

## How to Search

- **Quick discovery (direct URL):** Use `https://www.bitrefill.com/{country}/{lang}/gift-cards/?q={query}` — e.g. `https://www.bitrefill.com/us/en/gift-cards/?q=amazon`. The page **prioritizes in-country products** but **shows results from all countries**. Search covers **gift cards, phone top-ups, and eSIMs**.
- **Site search:** Use the search on bitrefill.com (brand names, product names) to jump to relevant product pages.
- **Gift cards:** Search by brand or browse categories. Use the **country in the URL** to focus on cards usable in that country (in-country results are prioritized).
- **Top-ups:** No generic "search"; at bitrefill.com/refill/, user selects **country** first, then **carrier** (or enter number for carrier detection), then **amount**.
- **eSIMs:** Filter by **destination country or region**, then by **data size** and **validity** (e.g. 7 days, 30 days).

## eSIM discovery

- For "which countries/regions exist" or "browse all eSIMs": send the user to **https://www.bitrefill.com/esim/all-destinations**.
- From that hub, "View plans" links go to `/{country}/{lang}/esims/bitrefill-esim-{slug}/` (locale may differ by user; slug is country/region name in kebab-case, e.g. `bitrefill-esim-japan`, `bitrefill-esim-global`, `bitrefill-esim-taiwan`).

## Listing Filters and Sort (Gift Cards)

Applicable to **all gift-card listings** (all gift cards, category, or subcategory), e.g. `/{country}/{lang}/gift-cards/` or `/{country}/{lang}/gift-cards/food/`.

| Param | Values | Description |
|-------|--------|-------------|
| `redemptionMethod` | `online`, `instore` | Redemption method filter |
| `minRating` | `2`, `3`, `4`, `5` | Minimum review vote (stars) |
| `minRewards` | `1`–`10` | Minimum cashback (rewards) |
| `s` | `2` = A–Z, `3` = recently added, `4` = cashback | Sort; default = popularity |

**Example:** `https://www.bitrefill.com/us/en/gift-cards/food/?minRating=5&minRewards=4&redemptionMethod=instore`  
**Sort example:** `https://www.bitrefill.com/us/en/gift-cards/?s=2` (A–Z).

## Filters That Matter

1. **Country / region**  
   Set via **URL** (first path segment = country, e.g. `/us/en/`) to show inventory for that country. Most gift cards and all top-ups/eSIMs are country- or region-specific. Establish the user's country (and for top-ups, carrier) before recommending a product.

2. **Category (gift cards)**  
   Shopping, Entertainment, Gaming, Food & Delivery, Travel, etc. Helps when the user says "streaming" or "gaming" rather than a brand. See references/supported-categories.md for full list.

3. **Brand**  
   When the user names a brand (e.g. Amazon, Steam), search or go directly to that brand’s page and then check country/denomination.

4. **Denomination / amount**  
   Shown on the product page. For gift cards, fixed or custom; for top-ups, carrier-specific; for eSIMs, data + duration.

## Suggested Flow for the Agent

1. **Clarify:** Product type (gift card / top-up / eSIM) and country (and carrier for top-ups if possible).
2. **Direct:** Send user to the right URL (gift-cards, refill, esims) or use search.
3. **Remind:** Check country and (for gift cards) denomination so the card is usable for the recipient.

## URL Patterns

Bitrefill uses different URL patterns depending on the page:

- **Category listing (gift cards):** `/{country}/{lang}/gift-cards/{category-slug}/` — use the path for a category or subcategory (e.g. `/us/en/gift-cards/flights/`). Do not use `?category=...` for “only this category”; it can return the full catalog filtered. Add listing filters/sort as query params (see "Listing Filters and Sort" above).
- **Locale-prefixed:** `/{country}/{lang}/gift-cards/`, `/{country}/{lang}/esims/`. Single eSIM: `/{country}/{lang}/esims/bitrefill-esim-{destination-slug}/`. Product: `/{country}/{lang}/gift-cards/{product-slug}/`.
- **Query-param locale:** `/refill/?hl=it`, `/card/?hl=it` — older pages use `?hl=` parameter
- **No locale:** `/login`, `/signup`, `/refer-a-friend`, `/blog/`, `/esim/all-destinations` (eSIM hub)

For “which X are supported” or “how does this work,” use **help.bitrefill.com** or the product page; category pages often don’t expose full product/coverage lists in static HTML.

## Internal Search Endpoint

The site uses `/api/omni` as its internal product search endpoint (browser-only, requires cookies). For programmatic access, use the official API at `api.bitrefill.com/v2` instead.

For a full list of categories and popular brands, use references/supported-categories.md.
