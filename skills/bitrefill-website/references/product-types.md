# Product Types on Bitrefill

Bitrefill offers four main product families. Use this reference when the user needs to understand what each type is, where to find it on the site, or how it works.

## Gift Cards

**What they are:** Digital gift cards for brands (shopping, streaming, gaming, food, travel). Delivered as redeemable codes, usually by email and on the order page.

**On the site:** bitrefill.com/{country}/{lang}/gift-cards/ — filter by category, country, or search by brand.

**Important:**
- **Region-locked:** Most brands have per-country cards (e.g. Amazon US, UK, DE). Always match the user's (or recipient's) country.
- **Denominations:** Fixed tiers (e.g. $25, $50) or custom amounts depending on brand. Shown on each product page.
- **Use:** User redeems the code on the brand's website or app. See references/use-and-activate.md.

**Categories (from API):** automobiles, top-products, retail, apparel, health-beauty, home, electronics, pets, food, restaurants, food-delivery, streaming, games, travel, entertainment, and many more. Full list: references/supported-categories.md.

---

## Mobile Top-ups

**What they are:** Prepaid airtime (and sometimes data bundles) applied directly to a phone number. Available in 200+ countries.

**On the site:** bitrefill.com/refill/ — select country, then carrier, then amount.

**Important:**
- **Carrier and number:** User must provide the phone number and (if needed) select the correct carrier. The site often detects carrier from number.
- **Denominations:** Vary by carrier and country; shown after selecting carrier.
- **Refill subcategories (from API):** refill, data, pin, bundles, dth.
- **Delivery:** Airtime is applied to the number shortly after payment (usually minutes).
- **Use:** No code to redeem; confirm balance on the phone or carrier account. See references/use-and-activate.md.

---

## eSIMs

**What they are:** Data-only travel plans. User installs an eSIM via QR code; no physical SIM. For use when traveling (190+ countries).

**On the site:** Browse all: bitrefill.com/esim/all-destinations. Locale listing and product pages: bitrefill.com/{country}/{lang}/esims/. Single product URLs follow `/{country}/{lang}/esims/bitrefill-esim-{destination-slug}/` (e.g. Japan, Global, Taiwan).

**Important:**
- **Data only:** No voice/SMS; data only.
- **Durations:** e.g. 1, 7, 15, 30 days; data caps vary (e.g. 1GB to unlimited).
- **Regional plans:** Some plans cover multiple countries (e.g. Europe, Asia).
- **Activation:** QR code provided after purchase; install eSIM before or during travel. Compatible with most modern smartphones (e.g. iPhone XS+, recent Android). See references/use-and-activate.md.

---

## Bitcoin & Lightning Services

**What they are:** Services for Bitcoin and Lightning Network users (e.g. channel opening, liquidity, payment tools).

**On the site:** Relevant sections linked from the main site and product catalog. Less central than gift cards, top-ups, and eSIMs for typical “buy something” flows.

**When to mention:** If the user asks about paying with Bitcoin or Lightning, point to checkout options (see references/buy-and-checkout.md). If they ask specifically about Lightning channels or liquidity, direct them to the Bitcoin/Lightning sections on bitrefill.com.

---

## Account & Authentication

**What it is:** Signup, login, password reset, and account management on Bitrefill.

**On the site:** bitrefill.com/signup and bitrefill.com/login (no locale prefix on auth pages).

**When to mention:** If the user wants to create an account, log in, reset a password, access order history, or use the referral program. See references/account-and-auth.md for full details.
