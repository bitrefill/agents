---
name: bitrefill-website
description: Help users accomplish tasks on Bitrefill (bitrefill.com): browse and search gift cards, mobile top-ups, and eSIMs; get product and pricing info; buy and pay with crypto or card; redeem, activate, or use purchases. Use when the user mentions Bitrefill, gift cards, phone top-up, eSIM for travel, or paying with Bitcoin/Lightning for digital goods.
metadata:
  author: bitrefill
  version: "1.0"
references:
  - product-types
  - search-and-browse
  - get-info
  - buy-and-checkout
  - use-and-activate
  - supported-categories
  - account-and-auth
---

# Bitrefill Website Skill

Use this skill when the user wants to do anything on **Bitrefill** (bitrefill.com): learn about products, search, compare, buy, or use what they bought. Bitrefill sells digital goods (gift cards, mobile top-ups, eSIMs) and offers Bitcoin/Lightning services; payment can be crypto or card. All products are delivered digitally and usually instantly.

## When to Use This Skill

Activate when the user:
- Mentions **Bitrefill** or bitrefill.com
- Wants to **buy** gift cards, mobile top-up, or eSIM (with crypto or card)
- Asks how to **search**, **find**, or **compare** products on Bitrefill
- Needs **information** (pricing, availability, country restrictions, denominations)
- Wants to **use** a purchase: redeem a gift card, activate an eSIM, or confirm a top-up

If the request is vague (e.g. "I need a gift"), ask what type of product and for whom (country/interests).

## Quick Decision: What Does the User Want to Do?

```
User intent?
├─ Learn what Bitrefill offers / product types     → See "Product types at a glance" below; details in references/product-types.md
├─ Search or browse for a product                 → references/search-and-browse.md
├─ Get detailed info (price, country, how it works)→ references/get-info.md
├─ Buy / checkout                                 → references/buy-and-checkout.md
├─ Use / redeem / activate after purchase         → references/use-and-activate.md
└─ Sign up / log in / manage account              → references/account-and-auth.md
```

## Product Types at a Glance

| Product type | What it is | Main URL | Load details when needed |
|--------------|------------|----------|---------------------------|
| **Gift cards** | Digital gift cards (shopping, streaming, gaming, food, travel) | bitrefill.com/{lang}/{country}/gift-cards/ | references/product-types.md, references/supported-categories.md |
| **Mobile top-ups** | Prepaid airtime/data for a phone number (200+ countries) | bitrefill.com/refill/ | references/product-types.md |
| **eSIMs** | Travel data plans (data-only, QR activation, 150+ countries) | bitrefill.com/{lang}/{country}/esims/ | references/product-types.md |
| **Bitcoin / Lightning** | Channel opening, liquidity, payment tools | bitrefill.com (relevant sections) | references/product-types.md (brief) |
| **Account & Auth** | Signup, login, password reset, referral program | bitrefill.com/signup, /login | references/account-and-auth.md |

**Critical:** Many products are **country- or region-specific**. Always confirm or infer the user's country (and, for top-ups, carrier) before recommending a product or flow.

## Task Flows (High Level)

### Browse or search

1. Identify **product type** (gift card / top-up / eSIM) and **country** (and carrier for top-ups if known).
2. Direct to the right section or use site search; help filter by category, brand, or amount.
3. For depth (categories, brands, denominations): **references/search-and-browse.md**, **references/supported-categories.md**.

### Get information

1. User needs price, availability, denominations, or country rules.
2. Use product pages, category pages, or dashboard; emphasize **country/region** and **denomination** constraints.
3. Details: **references/get-info.md**.

### Buy / checkout

1. User has chosen a product (or needs help choosing — combine with browse/get-info).
2. Guide: account vs guest, payment method (Lightning recommended for crypto), delivery expectations.
3. Full flow: **references/buy-and-checkout.md**.

### Use after purchase

1. User has paid and wants to **redeem**, **activate**, or **confirm**.
2. Gift card → redeem on merchant site; eSIM → scan QR / install; top-up → confirm on phone/dashboard.
3. All codes and orders: **references/use-and-activate.md**, dashboard at bitrefill.com/dashboard.

## Tips and Common Pitfalls

- **Country first:** Region-locked products (e.g. Amazon US vs UK) are the main source of errors. Always align product country with the user's.
- **Lightning for crypto:** Fast and low-fee; recommend for Bitcoin users.
- **No KYC for crypto:** Most crypto purchases do not require identity verification.
- **Refunds:** Digital goods are typically non-refundable once delivered; set expectations before purchase.
- **Dashboard:** Past orders and codes: bitrefill.com/dashboard.

## Agent Tools

Use the right tool for each task:

| Tool | When to use |
|------|-------------|
| **Official API** (`api.bitrefill.com/v2`) | Primary for product search, product details, purchases, order management. Requires auth (Bearer token or Basic auth). See [docs.bitrefill.com](https://docs.bitrefill.com) for full reference. |
| **MCP endpoint** (`api.bitrefill.com/mcp`) | For Claude Code integration. Provides search-products, product-details, buy-products, list-invoices, list-orders tools via JSON-RPC/SSE. Connect with: `claude mcp add --transport http bitrefill https://api.bitrefill.com/mcp` |
| **Chrome DevTools** | Only for visual flows not covered by the API: signup, login, account creation, visual page inspection. |
| **NOT recommended: scraping** | Cloudflare blocks all automated access to www.bitrefill.com. Do not use firecrawl or direct scraping — requests return 403. |

> **How we verified:** URLs and flows verified via chrome-devtools + API probing on bitrefill.com (2026-02-19).

## References

Load only when the agent needs more detail:

| Reference | Use when |
|-----------|----------|
| [product-types](references/product-types.md) | Explaining gift cards vs top-ups vs eSIMs, or how each works on the site |
| [search-and-browse](references/search-and-browse.md) | User wants to find or filter products |
| [get-info](references/get-info.md) | User asks about pricing, availability, or restrictions |
| [buy-and-checkout](references/buy-and-checkout.md) | User is ready to pay or asks about payment/delivery |
| [use-and-activate](references/use-and-activate.md) | User has bought and needs to redeem, activate, or use |
| [supported-categories](references/supported-categories.md) | Listing categories or popular brands (gift cards, etc.) |
| [account-and-auth](references/account-and-auth.md) | User wants to sign up, log in, reset password, or manage account |
