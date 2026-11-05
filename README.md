# Bitrefill Agent Skills

A unified, capability-aware agent skill for [Bitrefill](https://www.bitrefill.com) — enabling AI agents to browse, buy, and manage gift cards, mobile top-ups, and eSIMs across 180+ countries with crypto, Lightning, USDC via x402, pre-funded account balance, card, Apple Pay or Google Pay.

## Status

| Item | Status |
|------|--------|
| Repo | `bitrefill/agents` on GitHub |
| Skill | `bitrefill` v3.4.1 — capability-aware shopping and payment routing |
| Plugin | Portable [plugin.json](plugin.json) + [mcp.json](mcp.json); compatibility manifests for Codex, Claude and Cursor; includes [eCommerce MCP](https://docs.bitrefill.com/docs/ecommerce-mcp) |
| Spec | [Agent Skills](https://agentskills.io/specification) compliant |

## Installation

### ChatGPT / Codex (plugin: skill + MCP)

Download `bitrefill.zip` from the [latest GitHub release](https://github.com/bitrefill/agents/releases/latest). It contains root Agent Plugins 1.0 manifests, OpenAI listing metadata, a Codex compatibility manifest, the skill and its resources, and the logo. Connect your Bitrefill account through the host's OAuth flow; no credentials are bundled. Install from an available local or development plugin source using your host's supported flow. A GitHub release does not install the plugin into OpenAI's public directory.

OpenAI public-directory review is separate. Bitrefill supports digital-goods purchases, which require resolution with OpenAI under the current commerce guidelines. See [OpenAI review preparation](https://github.com/bitrefill/agents/blob/main/docs/openai-review.md) for verified checks, review cases, and remaining materials. This package is not an approved directory listing.

### Claude Code / Cowork (plugin: skill + MCP)

```bash
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
/reload-plugins
```

Registers the **bitrefill** skill and eCommerce MCP ([`.mcp.json`](.mcp.json)); OAuth on first MCP call. Pin: `bitrefill/agents@v3.4.1`.

Update:

```bash
/plugin marketplace update bitrefill-skills
/plugin update bitrefill@bitrefill-skills
/reload-plugins
```

**Cowork:** Customize → Plugins → add `bitrefill/agents` → install **bitrefill**. **claude.ai:** Connectors only → [claude-chat.md](skills/bitrefill/references/harnesses/claude-chat.md). Other hosts → [mcp.md](skills/bitrefill/references/touchpoints/mcp.md).

### Cursor / Grok Bot (plugin: skill + MCP)

Cursor: **Customize** → search **Bitrefill** → **Install**. Grok Bot: **Connect apps** → **Bitrefill** → **Add**. Both get the skill and the connector in [`.mcp.json`](.mcp.json) (OAuth with your Bitrefill account). Each purchase is confirmed with you unless you opt into autonomous buying; without a connected account the skill checks out as a guest through npm `@bitrefill/cli`. Host guide → [grok-bot.md](skills/bitrefill/references/harnesses/grok-bot.md). Bitrefill [Terms](https://www.bitrefill.com/terms/) and [Privacy Policy](https://www.bitrefill.com/privacy/) apply.

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

## Skill

| Skill | Description |
|-------|-------------|
| `bitrefill` | Capability-driven routing: probe harness (exec, egress, MCP), pick touchpoint (Bitrefill MCP, x402 REST, CLI, API, browse), then wallet (balance, x402, send). Includes OpenClaw, Hermes, ChatGPT + Coinbase Wallet MCP, and a matrix of agent wallets that can pay. |

### Structure

```
plugin.json                  # Agent Plugins 1.0 identity and OpenAI metadata
mcp.json                     # Portable Streamable HTTP MCP connection
.codex-plugin/plugin.json    # Codex compatibility manifest
assets/logo.png
.mcp.json                    # Claude / Cursor / older Codex MCP configuration
.claude-plugin/
├── plugin.json
└── marketplace.json
skills/bitrefill/
├── SKILL.md
└── references/
    ├── harnesses/
    │   ├── decision-engine.md
    │   ├── capability-matrix.md
    │   ├── openclaw.md
    │   └── claude-chat.md
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

Build and validate with Python 3.13 or newer:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/package_plugin.py --tag v3.4.1
python scripts/package_plugin.py --validate dist/bitrefill.zip --tag v3.4.1
```

The release workflow validates tagged versions, packages the complete plugin as `bitrefill.zip`, and publishes it with `SHA256SUMS`. It excludes marketplace catalogs, development files and credentials. Keep versions synchronized across the portable, Codex, Claude and Cursor manifests, marketplace metadata and skill metadata.

To add a new skill:

1. Create a new directory under `skills/` (e.g., `skills/my-skill/`)
2. Add a `SKILL.md` file with valid YAML frontmatter (`name`, `description`) and agent instructions
3. Optionally add a `references/` subdirectory with supporting documentation
4. Update `.claude-plugin/marketplace.json` to register the skill

Skill names must be lowercase with hyphens and match the directory name exactly.

## Documentation

For the full Agent Skills specification, see [agentskills.io/specification](https://agentskills.io/specification).

## License

[MIT](LICENSE)
