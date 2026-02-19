# Search and Browse on Bitrefill

Use this reference when the user wants to **find** a product: search by brand, browse by category, or filter by country/amount.

## Entry Points by Product Type

| Product type      | Main URL                              | How to narrow down |
|-------------------|---------------------------------------|---------------------|
| Gift cards        | bitrefill.com/{lang}/{country}/gift-cards/ | Category, country, brand search |
| Mobile top-ups    | bitrefill.com/refill/                 | Country → carrier → amount |
| eSIMs             | bitrefill.com/{lang}/{country}/esims/ | Country/region → data/duration |
| All categories    | bitrefill.com/categories              | Overview of everything |

## How to Search

- **Site search:** Use the search on bitrefill.com (brand names, product names) to jump to relevant product pages.
- **Gift cards:** Search by brand (e.g. "Netflix", "Amazon") or browse categories. Then filter by **country** — critical for region-locked cards.
- **Top-ups:** No generic "search"; at bitrefill.com/refill/, user selects **country** first, then **carrier** (or enter number for carrier detection), then **amount**.
- **eSIMs:** Filter by **destination country or region**, then by **data size** and **validity** (e.g. 7 days, 30 days).

## Filters That Matter

1. **Country / region**  
   Most gift cards and all top-ups/eSIMs are country- or region-specific. Always establish the user's country (and for top-ups, carrier) before recommending a product.

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

- **Locale-prefixed:** `/{lang}/{country}/gift-cards/`, `/{lang}/{country}/esims/` — e.g. `/en/us/gift-cards/`, `/it/it/gift-cards/`
- **Query-param locale:** `/refill/?hl=it`, `/card/?hl=it` — older pages use `?hl=` parameter
- **No locale:** `/login`, `/signup`, `/refer-a-friend`, `/blog/`
- **Product pages:** `/{lang}/{country}/gift-cards/{slug}/` — e.g. `/en/us/gift-cards/amazon_com-usa/`

**Note:** `/mobile-topups` does NOT exist. The correct path for phone top-ups is `/refill/`.

## Internal Search Endpoint

The site uses `/api/omni` as its internal product search endpoint (browser-only, requires cookies). For programmatic access, use the official API at `api.bitrefill.com/v2` instead.

For a full list of categories and popular brands, use references/supported-categories.md.
