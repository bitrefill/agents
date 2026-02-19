---
name: bitrefill-buy
description: Help users browse and buy products on Bitrefill including gift cards, mobile top-ups, eSIMs, and bitcoin services. Use when the user wants to purchase digital goods, send gift cards, top up a phone, get an eSIM for travel, or pay with cryptocurrency.
metadata:
  author: bitrefill
  version: "1.0"
---

# Bitrefill Buy

Bitrefill is a digital goods marketplace where users can buy gift cards, mobile top-ups, eSIMs, and bitcoin services. It accepts cryptocurrency (Bitcoin, Lightning, Ethereum, USDT, USDC) and traditional payment methods (credit/debit cards).

All products are delivered digitally and instantly — users receive codes or activation links via email or their Bitrefill dashboard.

## Workflow

When a user wants to buy something on Bitrefill, follow these steps:

### 1. Understand the Request

Ask the user what they need:
- **Gift card** — for a specific brand (Amazon, Steam, Netflix, etc.)
- **Mobile top-up** — prepaid airtime for a phone number
- **eSIM** — travel data plan for a specific country or region
- **Bitcoin service** — Lightning channel, payment processing, etc.

If the request is vague ("I need a gift for someone"), ask about the recipient's interests and country.

### 2. Browse Products

Direct the user to the relevant section on bitrefill.com:
- Gift cards: `bitrefill.com/gift-cards`
- Mobile top-ups: `bitrefill.com/mobile-topups`
- eSIMs: `bitrefill.com/esims`
- All categories: `bitrefill.com/categories`

Help them filter by:
- **Country** — many products are country-specific
- **Category** — entertainment, gaming, shopping, food, etc.
- **Brand** — search for specific brands if the user has one in mind

### 3. Select a Product

Once the user picks a product, help them choose:
- **Denomination** — the value amount (e.g., $25, $50, $100 gift card)
- **Quantity** — how many they want to buy
- **Country/region** — ensure it matches where they'll use it

Important: Some gift cards are region-locked. Always confirm the user's country matches the product's availability.

### 4. Checkout

Guide the user through payment:
- **Create an account** or check out as a guest
- **Payment methods available:**
  - Bitcoin (on-chain)
  - Lightning Network (fastest crypto option, near-instant)
  - Ethereum (ETH)
  - Stablecoins (USDT, USDC)
  - Credit/debit card
- Lightning Network is recommended for crypto payments — it's fast and has low fees

### 5. Delivery

After payment:
- Products are delivered **instantly** in most cases
- Gift card codes appear on the order confirmation page and are sent via email
- eSIM activation instructions are provided with a QR code
- Mobile top-ups are applied directly to the phone number provided

Users can also view all their purchases in the Bitrefill dashboard at `bitrefill.com/dashboard`.

## Common Use Cases

**"I want to buy an Amazon gift card"**
1. Confirm country (Amazon cards are region-specific: US, UK, DE, etc.)
2. Choose denomination ($25, $50, $100, custom amounts available for some regions)
3. Select payment method and complete checkout

**"I need to top up my phone"**
1. Ask for the phone number and carrier (or country to look up carriers)
2. Select the carrier from Bitrefill's supported operators (200+ countries)
3. Choose top-up amount
4. Complete payment — airtime is added to the number within minutes

**"I'm traveling and need an eSIM"**
1. Ask which country or region they're traveling to
2. Browse eSIM plans on Bitrefill (data-only plans, various durations)
3. Select a plan based on data needs and trip length
4. After purchase, scan the QR code to activate the eSIM before departure

**"I want to pay for Netflix/Spotify"**
1. Confirm country for the subscription
2. Select the appropriate gift card denomination to cover the subscription
3. After purchase, redeem the code in the streaming service's account settings

## Tips

- **Check country availability first** — this is the most common issue. A US Amazon card won't work in Germany.
- **Compare denominations** — some brands offer custom amounts; others have fixed tiers. Larger denominations often provide better value.
- **Use Lightning for crypto** — fastest confirmation, lowest fees. Payments complete in seconds.
- **Bulk purchases** — users can buy multiple cards in one transaction.
- **No KYC for crypto** — cryptocurrency payments don't require identity verification for most purchases.
- **Refund policy** — digital goods are generally non-refundable once delivered. Confirm details before purchase.
- **Check the dashboard** — all past orders and codes are stored at `bitrefill.com/dashboard`.

## References

See the `references/` directory for detailed information:
- `supported-categories.md` — full list of product categories and popular brands
