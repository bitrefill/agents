# Host: Hermes Agent

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

The Bitrefill plugin gives Hermes this skill and the Bitrefill connector; its tools arrive as `mcp__bitrefill__<tool>` (`-` → `_`). The connector's sign-in belongs to the Hermes profile owner and is shared by every chat of that profile.

Product, confirm and payment → [grok-bot.md](grok-bot.md) § Product first, one confirm and § Pay. This page takes precedence over both and over the wallet pages; for crypto, § 6 replaces § Pay's no-address line and sets when invoice checks start.

## 1. Where buying is allowed

Read the **Source** line first; it decides what you may do.

| Source | Connector | Checkout |
|---|---|---|
| None, or `Local` (local session) | All tools | Connector, guest, wallet, x402 |
| Chat-app DM: Telegram, Discord, Slack, WhatsApp (`Whatsapp`, `Whatsapp_Cloud`), Signal, Matrix or Mattermost, then `("DM with …")` with no `, thread:` (Slack threads every DM, so there it may follow) | `search-products` and `get-product-details` only; never balances, invoices, orders or codes | Guest or x402 |
| Any other Source on those platforms (group, channel, thread) | — | Reply only "DM me to finish this" |
| Every other Source (other platforms, webhooks, API server), and cron jobs (Hermes tells you when you run as one) | — | Never buy or pay; say "I can't buy from here." |

- The connector buys only in a local session: in a chat app, Hermes's order prompt goes to whoever is in that chat, who may not be the owner.
- A one-shot run looks local; Hermes declines its order prompt itself.
- Autonomous buying (`trust: full` and a higher `spend_limit`, set by the owner) only removes the prompt in a local session; it never makes cron or chat apps buy.

## 2. Route

Route silently:

1. **Connected**: an `mcp__bitrefill__*` tool in your tool list, or a `bitrefill` server in the deferred-tool catalog (load its tools with `tool_describe`, call them with `tool_call`) → [../touchpoints/mcp.md](../touchpoints/mcp.md) and § 4. Neither = not connected (the connector is signed out); at most one `tool_search` for `bitrefill`, then 2.
2. **Not connected**, with `terminal` and `command -v npx` → § 5 Guest checkout.
3. **Neither**, or the method is rejected → a wallet that pays only x402 runs § 8; else send the `https://www.bitrefill.com` product link.

Paying with an x402-only wallet runs the whole order on § 8 instead of routes 1–2.

**Connect or guest** (not connected, local session only; in a chat app skip it, since account purchases happen only on the Hermes machine):

- Once the product is settled, ask once per chat, as its own question before the quote, with no option recommended: "Connect your Bitrefill account (balance, saved cards, order history) or continue as guest?" Ask even when the user already named a payment method or wallet. Its answer is never the confirm.
- Connect → the owner signs in on the Hermes machine ([../touchpoints/mcp.md](../touchpoints/mcp.md) § Hermes Agent), never in chat: never ask for a password, code, key or sign-in address here. Once they say it's done and the tools are there → route 1; else continue as guest.
- Guest → route 2 or 3.

## 3. Confirm

- The confirm is the user's reply to your quote with the total. A yes sent before the quote doesn't count: quote and wait.
- A reply or `clarify` choice that picks a method confirms only when the quote showed that method's total in its own units (crypto: the coin amount, ≈ USD); otherwise quote that total and wait for the yes.
- Only in a local session may an in-chat autonomous opt-in with a spend cap ([../../SKILL.md](../../SKILL.md)) replace it, up to that cap; Hermes still asks per order unless the owner set `trust: full`.
- On every route: never answer a Hermes prompt; never suggest **Always**, `/yolo`, `approvals.mode: off` or a higher spend limit; never run `hermes` commands or `manage_connections`, or change Hermes settings.
- Hermes never prompts before a `terminal` command, so for guest orders the confirm is the only gate: guest `buy-products` only after the user's own reply accepts the quoted product, amount, total, method and email.

## 4. Connector orders

- After the confirm, call `buy-products` once. Hermes asks the user to approve every order, `/yolo` included, and each answer covers only that order.
- Hermes refused the order (denied, cancelled, timed out, nobody to ask, or a "spend limit was reached" error, which is Hermes's wording for every refusal) → stop and say "The order wasn't approved, so nothing was bought." Never say a spend limit was reached; never retry, rephrase or switch route. The user asking again ("try again", "same card") is a new request, not a confirm: quote again and wait for a new yes.
- `submit-prepayment-step` and `update-order` raise Hermes's trust prompt, which `/yolo` and `approvals.mode: off` may skip. When it appears, say "Approve this step in the prompt."; refused → the same stop.
- `submit_feedback` only when the user asks to send feedback, after showing them the note.
- Auth error on a connector call → the owner runs `hermes mcp login bitrefill` on the Hermes machine; no guest fallback for that order.
- `outcome_uncertain` in the tool error → check `list-invoices` first and tell the user. It never lists unpaid invoices, so nothing there → say the order may exist unpaid and point to the order history on bitrefill.com. Never buy again without a new confirm.
- Balance, cashback and saved cards only through the connector.

## 5. Guest checkout

[../touchpoints/cli.md](../touchpoints/cli.md) § Guest checkout, with these rules:

- Every call: `npx -y @bitrefill/cli@0.3.0 <command> … --json`, with `--payment_method <method>` last before `--json`. Never `npm install -g` or `npm link` (npx keeps its copy in the npm cache).
- `cart_items` take `package_value` as a string: `[{"product_id":"steam-usa","package_value":"20"}]`.
- Buy only after a separate `whoami --json` call returns `"identity":"unregistered"` (`&&` checks only its exit code). A signed-in CLI → route 3, since the owner keeps it signed out ([../safeguards.md](../safeguards.md) § Hermes).
- A bare-string result, or `error` / `message` instead of the expected fields, failed, even on exit 0 (the CLI drops `isError`).
- Guest `purchase_limit_reached` → offer the connect again, local session only.
- `terminal` is guest checkout only: never `login`, `verify`, `--payment_method balance` / `cashback`, `--saved_fiat_card_id` or `scripts/`. A wallet CLI only pays an invoice after the confirm. Never `execute_code` for Bitrefill or `hermes`. Never read `~/.config/bitrefill-cli/` or Hermes token files.

## 6. Crypto invoices

- Post the amount, network, address (or Lightning invoice) and expiry, then end the turn. Give the expiry as the minutes the invoice gives (`expiration_minutes`), never a computed clock time.
- Start checking `get-invoice-by-id` only after the user says they paid or the wallet's payment went through, then as § Pay says; never in a waiting loop before the address is out.
- No address came back → give the invoice id and offer a payment-link checkout, opened with `--return_payment_link true` only after a new yes. Never a second order without that yes.
- Invoice total above the confirmed one → say so and get a new yes before anyone pays.
- No wallet → post the address or `payment_link`.

## 7. A wallet the agent has

Any wallet MCP or CLI (Coinbase Wallet MCP, MetaMask, `awal`, Hermes `agent-wallet`… → [../wallets/matrix.md](../wallets/matrix.md)) pays instead of the user, only where § 1 allows checkout.

- Quote a coin and network it holds, and name the wallet in the confirm.
- After the yes, open the invoice with `return_payment_link: false` and send the exact `payment_info` amount to its address once. Never pay a `payment_link` or open another order through a wallet.
- The wallet's own approvals and caps apply. When it asks, say "Approve the payment in your wallet" and poll the wallet's own approval status (Coinbase Wallet MCP: `get_request_status`) until it is approved, rejected or the invoice expires. Never answer its prompt or raise its cap.
- A wallet error doesn't prove the payment failed (a wallet can pay and then return a malformed result): check `get-invoice-by-id` once; paid → deliver.
- Declined, failed and unpaid, over its cap, or unable to pay this invoice → stop: the invoice stays unpaid. Post the address so the user can pay by hand. Never retry or switch wallet without a new yes.
- Invoice expired while the wallet request is open → tell the user to reject it and not to pay the old address, and offer a new quote.

## 8. A wallet that pays only x402

A wallet with no send (AgentCash) can't pay connector or CLI invoices, so paying with it runs the whole order on x402 checkout ([../touchpoints/x402.md](../touchpoints/x402.md) § Path 1), only where § 1 allows checkout.

- Every call goes through the wallet's HTTP tool; never `scripts/`. AgentCash `fetch` signs in and pays a 402 by itself. Hermes asks before it only when the owner priced it ([../safeguards.md](../safeguards.md) § Hermes), and a refusal stops the order as below, so the confirm and the wallet's caps are the gates.
- Steps:
  1. `POST /x402/connect` once.
  2. Search, `products/detail` and `invoice/create` with its `X-Access-Token` and `maxAmount` `0.01`.
  3. Quote `price_usdc`, the wallet and `expires_in_minutes`.
  4. After the yes, `POST /x402/invoice/pay` with that `invoice_id` once, `maxAmount` the quoted `price_usdc`.
  5. Poll `invoice/status` with the token until `delivery_status` is `all_delivered` (codes in `redemption_info`).
- Pay refused, failed or above the quote → stop, nothing was bought; offer the product link.
- 409 → already paid: poll status.
- Expired → a new invoice, quote and yes; never pay one twice.
- `/x402/my/*` only in a local session.

## 9. Secrets

- Codes, `invoice_access_token`, `X-Access-Token` and `payment_link` stay in this chat: never `memory`, files, `cronjob_manage` or `text_to_speech`. Never echo the token to the user (Hermes already keeps tool results in its session history).
- [../safeguards.md](../safeguards.md) § Universal rules' token file doesn't apply on Hermes, and its in-chat autonomous opt-in applies only as in § 3.

**User hears:** "Searching for [product]…" → "[Product] [amount]: [total] [currency] (≈ $X) by [method]. Confirm?" → connector only: "Approve the order in the prompt." (a guest order has no Hermes prompt; never promise one) → wallet that asks: "Approve the payment in your wallet." → "Send [amount] [coin] on [network] to [address] within [N] minutes" or "Pay here: [link]" → "Your code is ready." / "Done — topped up."
