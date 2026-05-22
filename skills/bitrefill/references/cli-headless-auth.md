# Headless CLI auth (agents)

Use when: agent must **sign up / sign in** without human at keyboard — unlock `balance`, cashback, order history.

**Guest checkout needs no inbox** — pass `--email` on `buy-products` and pay crypto. Fastest first try; see [cli.md](cli.md) § Guest checkout.

Use this doc when graduating guest → signed-in account with AgentMail or equivalent inbox.

Requires `@bitrefill/cli` ≥ 0.3.0. Agent-owned inbox via **AgentMail or equivalent** — any provider with programmatic receive (list messages, parse body).

## Why AgentMail or equivalent

Bitrefill `login` sends magic-link code to email. Agent needs inbox API or MCP to poll/read messages without human. [AgentMail](https://www.agentmail.to/) is the reference implementation below; equivalent = Gmail API, IMAP, Mailgun inbound, etc. if your runtime already has access.

## One-time inbox setup (AgentMail example)

Human verifies provider account once. Agent handles Bitrefill after. Substitute your equivalent provider's sign-up + list/receive commands.

```bash
npm install -g agentmail-cli

agentmail agent sign-up \
  --human-email you@example.com \
  --username bitrefill-agent
# → api_key, inbox_id (e.g. bitrefill-agent@agentmail.to)

export AGENTMAIL_API_KEY="am_..."   # from sign-up response

agentmail agent verify --otp-code 123456   # human reads OTP from you@example.com
```

Official refs: [quickstart](https://docs.agentmail.to/quickstart.md), [agent onboarding](https://docs.agentmail.to/agent-onboarding.md).

Optional (AgentMail): [AgentMail MCP](https://docs.agentmail.to/agent-onboarding.md) (`npx -y agentmail-mcp`) with `AGENTMAIL_API_KEY` — tools `list_threads`, `get_thread`, `get_message`. Equivalent providers: use their MCP/API instead.

## Bitrefill auth flow

Use agent inbox address as Bitrefill email (`inbox_id` from AgentMail or equivalent). Signup = login (same command).

```bash
npm install -g @bitrefill/cli

bitrefill init --openclaw    # optional

bitrefill login --email bitrefill-agent@agentmail.to
```

Poll inbox for Bitrefill verification email. AgentMail ([official list command](https://docs.agentmail.to/messages)):

```bash
agentmail inboxes:messages list --inbox-id bitrefill-agent@agentmail.to
```

Parse `extracted_text` or `text` from latest message for numeric code. Then:

```bash
bitrefill verify --code 123456
```

If Bitrefill account has TOTP, add `--otp` ([1Password](#totp-via-1password) below).

Confirm:

```bash
bitrefill whoami --json
# → { "identity": "registered", "email": "bitrefill-agent@agentmail.to", ... }
```

Then run catalog/purchase commands per [cli.md](cli.md).

## End-to-end script sketch

```bash
INBOX="bitrefill-agent@agentmail.to"

bitrefill login --email "$INBOX"
sleep 5   # allow delivery

CODE=$(agentmail inboxes:messages list --inbox-id "$INBOX" \
  | jq -r '.messages[0].extracted_text // .messages[0].text' \
  | grep -oE '[0-9]{6,8}' | head -1)

bitrefill verify --code "$CODE"
bitrefill whoami --json
```

Adjust regex/poll loop for your environment. Codes expire (~12–20 min server-side); on expiry re-run `login`.

## TOTP via 1Password

When Bitrefill account has authenticator enrolled, pass TOTP on verify.

Secret reference ([official `op read`](https://www.1password.dev/cli/reference/commands/read)):

```bash
bitrefill verify --code "$CODE" \
  --otp "$(op read 'op://Vault/Bitrefill/one-time password?attribute=otp')"
```

Item flag ([official `op item get --otp`](https://developer.1password.com/llms-cli.txt)):

```bash
bitrefill verify --code "$CODE" --otp "$(op item get Bitrefill --otp)"
```

Requires 1Password desktop app integration or service account. See [Get started with 1Password CLI](https://www.1password.dev/cli/get-started).

## Safeguards

- Dedicated low-balance Bitrefill account tied to agent inbox — not human primary email.
- Agent inbox (AgentMail or equivalent) = auth surface; restrict who can read it.
- `bitrefill reset` + re-login to rotate after compromise.
- Never log magic-link codes or redemption codes to shared transcripts.

Spending policy → [safeguards.md](safeguards.md).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Access token is required for login/verify` | Run any CLI command first (MCP connect mints token), or `bitrefill reset` then retry |
| `No pending login` | Re-run `login --email` before `verify` |
| Code invalid / expired | Re-run `login --email`; poll inbox again |
| `browser_url` in login response | Passkey/WebAuthn — human opens URL, then retry |
| Inbox empty after login | Wait + re-list; check spam; confirm inbox address matches provider setup |

More CLI errors → [troubleshooting.md](troubleshooting.md).

## Source of truth

- AgentMail (reference): <https://docs.agentmail.to/quickstart.md>, <https://docs.agentmail.to/messages>
- Bitrefill CLI: <https://github.com/bitrefill/cli> (≥ 0.3.0)
- 1Password CLI: <https://www.1password.dev/cli/reference/commands/read>
