# Buy and Checkout on Bitrefill

Use this reference when the user is ready to **pay** or asks about **payment options, account, or delivery**.

## Before Checkout

1. **Product chosen:** Correct product, country, and denomination (see references/get-info.md and references/search-and-browse.md).
2. **Account:** User can **create an account** or **check out as guest**. Account helps with order history and dashboard (bitrefill.com/dashboard).

## Payment Methods

### Crypto (recommended: Lightning for speed and low fees)

| Method | Notes |
|--------|-------|
| **Lightning Network** | Fast, low fees, no KYC. Best for Bitcoin users. |
| **Bitcoin** (on-chain) | Requires confirmations; slower than Lightning. |
| **Ethereum** | ETH on mainnet. |
| **Solana** | SOL payments. |
| **USDC** | Available on multiple chains (Ethereum, Solana, Base, Polygon, etc.) |
| **USDT** | Available on multiple chains (Ethereum, Solana, Tron, etc.) |
| **Dogecoin** | DOGE payments. |
| **Litecoin** | LTC payments. |
| **Dash** | DASH payments. |
| **BNB** (BSC) | Binance Smart Chain. |
| **Ark**, **Sui** | Additional supported chains. |

### Fiat / Card / Wallet

| Method | Notes |
|--------|-------|
| **Credit/debit card** (Visa, MasterCard) | May have different limits or KYC. |
| **Apple Pay** | Where supported. |
| **Google Pay** | Where supported. |
| **Binance Pay** | Pay via Binance account. |
| **Kraken Pay** | Pay via Kraken account. |
| **iDEAL** | Netherlands bank transfer. |
| **EPS** | Austria bank transfer. |
| **Przelewy24 (P24)** | Poland bank transfer. |
| **Bancontact** | Belgium bank transfer. |

### Other
- **Cashback balance** — Use earned cashback toward purchases.

Recommend **Lightning** when the user wants to pay with crypto.

## Checkout Flow (High Level)

1. Add product to cart (select denomination/amount and quantity).
2. Proceed to checkout; sign in or continue as guest.
3. Enter delivery details (e.g. email for codes; phone number for top-ups).
4. Choose payment method and complete payment.
5. Order confirmation: codes, links, or instructions shown on screen and often sent by email.

## Delivery Expectations

- **Gift cards:** Codes (and often links) on confirmation page and email; instant in most cases.
- **Mobile top-ups:** Airtime applied to the given number; usually within minutes.
- **eSIMs:** QR code and activation instructions on confirmation and email; user installs before or during travel.

All past orders and codes: **bitrefill.com/dashboard**.

## Tips

- **No KYC for crypto:** Most crypto payments do not require identity verification.
- **Refunds:** Digital goods are typically **non-refundable** once delivered. Mention this if the user asks about refunds.
- **Bulk:** Users can often buy multiple units (e.g. several gift cards) in one transaction.

If the user has already bought and needs to **redeem**, **activate**, or **confirm** delivery, use references/use-and-activate.md.
