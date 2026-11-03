# Bitrefill Agent Skills

A unified, capability-aware agent skill for [Bitrefill](https://www.bitrefill.com) — enabling AI agents to browse, buy, and manage gift cards, mobile top-ups, and eSIMs across 180+ countries with crypto, Lightning, USDC via x402, pre-funded account balance, card, Apple Pay or Google Pay.

## Status

| Item | Status |
|------|--------|
| Repo | `bitrefill/agents` on GitHub |
| Skill | `bitrefill` v3.1 — harness × touchpoint × wallet routing |
| Plugin | Claude Code / Cowork (`.claude-plugin/`) and Cursor / Grok Bot (`.cursor-plugin/`) manifests; both bundle the [eCommerce MCP](https://docs.bitrefill.com/docs/ecommerce-mcp) in [`.mcp.json`](.mcp.json) |
| Spec | [Agent Skills](https://agentskills.io/specification) compliant |

## Installation

### Claude Code / Cowork (plugin: skill + MCP)

```bash
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
/reload-plugins
```

Registers the **bitrefill** skill and eCommerce MCP ([`.mcp.json`](.mcp.json)); OAuth on first MCP call. Pin: `/plugin marketplace add bitrefill/agents#v3.1.0`.

Update from your shell, or in a session with `/plugin` → **Installed** → **bitrefill** → **Update now**, then `/reload-plugins`:

```bash
claude plugin update bitrefill@bitrefill-skills
```

**Cowork:** Customize → Plugins → add `bitrefill/agents` → install **bitrefill**. **claude.ai:** Connectors only → [claude-chat.md](skills/bitrefill/references/harnesses/claude-chat.md). Other hosts → [mcp.md](skills/bitrefill/references/touchpoints/mcp.md).

### Cursor / Grok Bot (plugin: skill + MCP)

Cursor: copy this repo to `~/.cursor/plugins/local/bitrefill` and run **Developer: Reload Window**; once Bitrefill is listed on Cursor Marketplace, **Customize** → **Bitrefill** → **Install**. Grok Bot installs it from that listing. Both get the skill and the connector in [`.mcp.json`](.mcp.json) (OAuth with your Bitrefill account). Host guide → [grok-bot.md](skills/bitrefill/references/harnesses/grok-bot.md).

### skills CLI

```bash
npx skills add bitrefill/agents
```

With a specific agent (e.g. Cursor):

```bash
npx skills add bitrefill/agents -a cursor -y
```

### OpenClaw

Via the cross-host installer:

```bash
npx skills add bitrefill/agents -a openclaw -y
```

Or via OpenClaw's own [ClawHub](https://clawhub.ai) registry:

```bash
openclaw skills install bitrefill
openclaw gateway restart
```

Then wire the eCommerce MCP for typed purchase tools:

```bash
openclaw mcp set bitrefill '{"url":"https://api.bitrefill.com/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login bitrefill
```

Full setup, channel-aware scenarios, and hardening: [skills/bitrefill/references/harnesses/openclaw.md](skills/bitrefill/references/harnesses/openclaw.md).

## What the plugin uses

- **Connector:** `https://api.bitrefill.com/mcp` (HTTP, OAuth with your Bitrefill account, no API key): search, product details, buy, order updates, invoices, balances, saved cards, help articles.
- **Guest checkout** (no account): npm `@bitrefill/cli` from `registry.npmjs.org` and an email; else a `www.bitrefill.com` link.
- **Optional APIs:** `api.bitrefill.com/v2` (`BITREFILL_API_KEY`); `api.bitrefill.com/x402` through a wallet tool you already installed (e.g. Coinbase Wallet MCP, AgentCash), which pays any pay-per-call lookups, or direct HTTP. The skill never asks for private keys or seed phrases.
- **Bundled scripts:** `scripts/siwx_*.js` use Node built-ins only, accept sign-in challenges only from `https://api.bitrefill.com`, write an unsigned sign-in draft to `/tmp/siwx_payload.json` and send the signed one back to `api.bitrefill.com`.
- **Headless sign-in (optional):** an agent inbox such as AgentMail (`agentmail-cli` / `agentmail-mcp` from `registry.npmjs.org`, `AGENTMAIL_API_KEY`, `api.agentmail.to`); TOTP from the 1Password CLI (`op`, your own vault).

Each purchase is confirmed with you unless you opt into autonomous buying. Bitrefill [Terms](https://www.bitrefill.com/terms/) and [Privacy Policy](https://www.bitrefill.com/privacy/) apply.

## Skill

| Skill | Description |
|-------|-------------|
| `bitrefill` | Capability-driven routing: probe harness (exec, egress, MCP), pick touchpoint (Bitrefill MCP, x402 REST, CLI, API, browse), then wallet (balance, x402, send). Includes OpenClaw, Claude Chat, Grok Bot / Cursor, Hermes, ChatGPT + Coinbase Wallet MCP, and a matrix of agent wallets that can pay. |

### Structure

```
.mcp.json
.claude-plugin/
├── plugin.json
└── marketplace.json
.cursor-plugin/
└── plugin.json
.github/workflows/
├── release.yml
└── check.yml
assets/
LICENSE
skills/bitrefill/
├── SKILL.md
├── scripts/
│   ├── siwx_build_message.js
│   └── siwx_send.js
└── references/
    ├── harnesses/
    │   ├── decision-engine.md
    │   ├── capability-matrix.md
    │   ├── openclaw.md
    │   ├── claude-chat.md
    │   └── grok-bot.md
    ├── touchpoints/
    │   ├── mcp.md
    │   ├── x402.md
    │   ├── cli.md
    │   ├── cli-headless-auth.md
    │   ├── api.md
    │   └── browse.md
    ├── wallets/
    │   ├── matrix.md
    │   ├── payment.md
    │   ├── base-mcp.md
    │   ├── siwx.md
    │   ├── agentcash.md
    │   ├── cdp-awal.md
    │   ├── metamask.md
    │   ├── kite-passport.md
    │   ├── bankr.md
    │   ├── alby.md
    │   ├── tether-wdk.md
    │   └── pay.md
    ├── safeguards.md
    └── troubleshooting.md
```

## Contributing

To add a new skill:

1. Create a new directory under `skills/` (e.g., `skills/my-skill/`)
2. Add a `SKILL.md` file with valid YAML frontmatter (`name`, `description`) and agent instructions
3. Optionally add a `references/` subdirectory with supporting documentation
4. Bump the version fields → [CLAUDE.md § Releasing Updates](CLAUDE.md#releasing-updates) (skills are auto-discovered)

Skill names must be lowercase with hyphens and match the directory name exactly.

## Documentation

For the full Agent Skills specification, see [agentskills.io/specification](https://agentskills.io/specification).

## License

[MIT](LICENSE)
