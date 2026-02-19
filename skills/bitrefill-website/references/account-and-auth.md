# Account & Authentication on Bitrefill

Use this reference when the user wants to **sign up**, **log in**, **reset a password**, or access **account features** on Bitrefill.

## Signup (`/signup`)

**Page:** bitrefill.com/signup (no locale prefix)

### OAuth / External Auth (4 methods, in order)
1. **Lightning wallet** — "Continue with Lightning"
2. **Crypto wallet** — "Continue with your wallet"
3. **Google** — "Continue with Google"
4. **Apple** — "Continue with Apple"

### Email Registration
- **E-mail** (required)
- **Password** (required)
- **Confirm password** (required)

**Password rules:** More than 8 characters, must include uppercase, lowercase, numbers, and at least one special character.

### Optional Fields
- **Referral code** — optional checkbox to reveal referral code input
- **Marketing opt-in** — receive exclusive offers via email

### Legal
- Submit button: "Register"
- By clicking, the user accepts [Terms & Conditions](/terms) and [Privacy Policy](/privacy)
- Link to login: "Already have an account? Login" → `/login`

---

## Login (`/login`)

**Page:** bitrefill.com/login (no locale prefix)

### OAuth / External Auth
Same 4 methods as signup: Lightning, Crypto wallet, Google, Apple.

### Email Login
- **E-mail** + **Password**
- **Forgot password** link (password reset flow)

### Links
- "Register" link → `/signup`

---

## Password Reset

Accessible from the "Forgot password" link on the login page. Sends a reset link to the registered email.

---

## Account Areas (Post-Login)

| Area | URL | Description |
|------|-----|-------------|
| Dashboard | `/dashboard` | Past orders, codes, activation links |
| Referral program | `/refer-a-friend` | Invite friends, earn rewards |
| Bitrefill Card | `/card` | Physical crypto-linked card |
| Settings | (via dashboard) | Account preferences |

---

## URL Patterns

- **Auth pages** (`/login`, `/signup`) do **not** use a locale prefix.
- **Referral** (`/refer-a-friend`) also has no locale prefix.
- **Footer links** to these pages may append `?hl=` for language hints (e.g. `/refer-a-friend/?hl=it`).

---

## Notes for the Agent

- Signup and login can be completed without an account for most purchases (guest checkout exists).
- Account is recommended for order history, dashboard access, and referral rewards.
- **No KYC** is required for crypto purchases; card payments may require verification.
- For visual auth flows (signup, account creation), use **Chrome DevTools** — these flows are not covered by the API.
