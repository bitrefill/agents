# Host: Hermes Agent

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

The Bitrefill plugin gives Hermes this skill and the Bitrefill connector; its tools arrive as `mcp__bitrefill__<tool>` (`-` → `_`). The connector's sign-in belongs to the Hermes profile owner and is shared by every chat of that profile. Route silently:

1. **Connected** (`mcp__bitrefill__get_balances` available) → [../touchpoints/mcp.md](../touchpoints/mcp.md).
2. **Not connected**, `terminal` and `command -v npx` → guest checkout ([../touchpoints/cli.md](../touchpoints/cli.md) § Guest checkout), every call as `npx -y @bitrefill/cli@0.3.0 <command> … --json` with `--payment_method <method>` last before `--json`; `cart_items` take `package_value` as a string (`[{"product_id":"steam-usa","package_value":"20"}]`). Buy only while `whoami --json` returns `"identity":"unregistered"`. A bare-string result, or `error` / `message` instead of the expected fields, failed, even on exit 0 (the CLI drops `isError`). Offer "Connect your Bitrefill account" first in the confirm; if picked, the owner signs in on the Hermes machine ([../touchpoints/mcp.md](../touchpoints/mcp.md) § Hermes Agent), never in chat: never ask for a password, code, key or sign-in address here. Guest `purchase_limit_reached` → offer the connect again.
3. **Neither**, or the method is rejected → send the `https://www.bitrefill.com` product link.

Product, confirm and payment → [grok-bot.md](grok-bot.md) § Product first, one confirm and § Pay; no address came back → offer the `payment_link` checkout, never a second `buy-products` without a new confirm. `x402_payment_url`: only through a wallet that asks the user to approve each payment ([../wallets/base-mcp.md](../wallets/base-mcp.md)); else post the address or `payment_link`.

## Hermes

- After the confirm, call `buy-products` once: Hermes asks the user to approve every order, `/yolo` included, and each answer covers only that order. Never answer that prompt; never suggest **Always**, `/yolo`, `approvals.mode: off` or a higher spend limit; never run `hermes` commands or `manage_connections`, or change Hermes settings. Denied, cancelled, timed out or spend limit reached → stop: nothing was bought; never retry, rephrase or switch route. Uncertain outcome (`outcome_uncertain` in the tool error) → check `list-invoices` first and tell the user; never buy again without a new confirm. Autonomous buying still gets that prompt; only the user changes it, in their own settings.
- Buy only in a local session (CLI, TUI, Desktop) or where **Source** is a chat app followed by `("DM with …")`, never when Source is Api_Server, Email, Sms, Ntfy or Webhook. Groups, channels and threads are read by others: reply there only "DM me to finish this". Use the connector only in the owner's chat; anyone else shops as a guest. Cron jobs, one-shot runs (`hermes -z`, `-Q`, piped `-q`), webhooks and other unattended runs never buy.
- `terminal` is guest checkout only: never `login`, `verify`, `--payment_method balance` / `cashback`, `--saved_fiat_card_id`, AgentCash, `awal`, `scripts/` or any payer that settles without its own approval; never `execute_code` for Bitrefill or `hermes`; never read `~/.config/bitrefill-cli/` or Hermes token files. Balance, cashback and saved cards only through the connector.
- Codes, `invoice_access_token` and `payment_link` stay in this chat: never `memory`, files, `cronjob_manage` or `text_to_speech`.

**User hears:** "Searching for [product]…" → "[Product] [amount]: [total] [currency] (≈ $X) by [method]. Confirm?" → "Approve the order in the prompt." → "Send [amount] [coin] on [network] to [address]" or "Pay here: [link]" → "Your code is ready." / "Done — topped up."
