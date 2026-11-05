# Capability Matrix

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

Per-host harness capabilities + **autonomy-first ranked stacks**. Probe at runtime — [decision-engine.md](decision-engine.md).

Legend: **MCP** → [../touchpoints/mcp.md](../touchpoints/mcp.md) | **x402** → [../touchpoints/x402.md](../touchpoints/x402.md) | **CLI** → [../touchpoints/cli.md](../touchpoints/cli.md) | **API** → [../touchpoints/api.md](../touchpoints/api.md) | **Browse** → [../touchpoints/browse.md](../touchpoints/browse.md) | **OpenClaw** → [openclaw.md](openclaw.md) | **Claude Chat** → [claude-chat.md](claude-chat.md) | **Grok Bot / Cursor** → [grok-bot.md](grok-bot.md)

Columns: **Exec** = code/shell | **Egress** = net to Bitrefill | **Ranked stack** = touchpoint + wallet (lowest HITL first)

## Anthropic

Claude Chat: `show_widget` **or** `read_me` **or** MCP connectors on claude.ai → [claude-chat.md](claude-chat.md) §1. Sandbox exec always; egress — probe.

| Host | Exec | Egress | MCP | Browser | Ranked stack (autonomy-first) |
|------|------|--------|-----|---------|------------------------------|
| Claude.ai Free | Sandbox exec yes; no agent shell | MCP: no custom connectors; egress: probe | No | Chrome ext only | Link only |
| Claude.ai Pro+ | Sandbox exec yes; no agent shell | **MCP** connectors; sandbox egress: **probe** | Yes | Chrome ext | MCP + balance → MCP + wallet send → x402 REST |
| Cowork | Desktop shell | MCP + host | Yes | Chrome ext | MCP + balance → MCP + wallet send → CLI |
| Claude Desktop | No | MCP only | Yes | Chrome ext | MCP + balance → MCP + wallet send |
| Claude Code | Full shell | Direct + MCP | Yes | Chrome ext | MCP + balance → MCP + wallet send → CLI → x402 REST |

**Claude Chat network:** shop via MCP connectors, not the code sandbox → [claude-chat.md](claude-chat.md) §4.

## OpenAI

| Host | Exec | Egress | MCP | Browser | Ranked stack |
|------|------|--------|-----|---------|--------------|
| ChatGPT Chat / Work (web, desktop, mobile) | Inspect session tools | Inspect session tools; sandbox egress varies | Installed plugins and workspace policy determine access | Inspect session tools | Bitrefill MCP + balance → available authorized payment tools → Bitrefill checkout link |
| Codex desktop / CLI | Inspect shell availability and permissions | Inspect network policy | Installed plugin or configured MCP | Inspect session tools | Bitrefill MCP + balance → CLI when available → authorized wallet |

**OpenAI:** ChatGPT and Codex share a plugin directory. Desktop-only capabilities and workspace restrictions can differ. Do not infer plugin, network or wallet availability from the plan name. Use the tools exposed in the current session; a sandbox and a remote MCP connection can have different network access. If direct HTTP is unavailable, use Bitrefill MCP; use a wallet proxy only when already connected and explicitly authorized. The bundled Bitrefill MCP does not require another wallet plugin for catalog, account balance checkout or order history.

## Google

| Host | Exec | Egress | MCP | Browser | Ranked stack |
|------|------|--------|-----|---------|--------------|
| Gemini Free | No | None | No | No | Link only |
| Gemini Pro/Ultra | Limited | Google IPs | Limited | Auto Browse (often blocked) | MCP → CLI → link |
| Gemini CLI | Full shell | Direct + MCP | Yes | MCP | MCP + balance → CLI → API |
| Jules | VM shell | VM egress | No | No | CLI → API (batch only) |

## Other hosts

| Host | Exec | Egress | MCP | Browser | Ranked stack |
|------|------|--------|-----|---------|--------------|
| Cursor | Terminal | Direct + MCP | Yes | Built-in | MCP + balance → wallet send; not signed in → guest CLI ([grok-bot.md](grok-bot.md)) |
| **Grok Bot** | Cloud computer | Direct + MCP | Yes (plugin connector) | — | Connected account: MCP + balance; else guest CLI → link ([grok-bot.md](grok-bot.md)) |
| OpenCode | Full shell | Direct + MCP | Yes | MCP | MCP + balance → CLI |
| **OpenClaw / Pi** | `exec` | Host IP | Yes | Host IP | **Guest CLI exec** → balance → MCP → x402 |
| **Hermes** | `terminal` | Backend-dependent | Yes | Local/CDP | MCP (API key cron) → CLI → avoid cloud browse |

## Wallet availability by host

| Wallet | Typical hosts | Bitrefill pairing |
|--------|---------------|-------------------|
| Bitrefill balance | Any OAuth'd MCP/CLI | Lowest HITL — pre-fund cap |
| Coinbase Wallet MCP | Cursor, ChatGPT+, Claude+connector | x402 REST Path 1, MCP invoice `send` |
| AgentCash | OpenClaw, Hermes, Codex (local MCP) | Autonomous x402 |
| CDP awal | Codex, OpenClaw, Hermes | Autonomous x402 under caps; `send` |
| MetaMask mm CLI | Codex, Claude Code, OpenClaw | x402 or `send`; user confirms each payment |
| Kite, Bankr, Alby, Tether WDK, Pay | Shell or local MCP hosts | x402 REST or MCP / CLI send |

Full wallet matrix → [../wallets/matrix.md](../wallets/matrix.md).

## Quick decision

1. OpenClaw? → [openclaw.md](openclaw.md) — guest CLI first.
2. Claude Chat (claude.ai + `show_widget`)? → [claude-chat.md](claude-chat.md) — MCP-first + generative UI.
3. Grok Bot or Cursor? → [grok-bot.md](grok-bot.md) — connected account via MCP, else guest CLI.
4. `search-products` visible? → [../touchpoints/mcp.md](../touchpoints/mcp.md) + [../wallets/payment.md](../wallets/payment.md).
5. x402 wallet, no Bitrefill account? → [../touchpoints/x402.md](../touchpoints/x402.md) Path 1.
6. Shell, no MCP? → [../touchpoints/cli.md](../touchpoints/cli.md).
7. Else → [decision-engine.md](decision-engine.md) full probe.

**User hears:** never host names or ranked stacks — open with the product goal.
