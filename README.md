# Bitrefill Agent Skills

A unified, capability-aware agent skill for [Bitrefill](https://www.bitrefill.com) — enabling AI coding agents to browse, buy, and manage gift cards, mobile top-ups, and eSIMs across 180+ countries with crypto, Lightning, USDC via x402, or pre-funded account balance.

## Status

| Item | Status |
|------|--------|
| Repo | `bitrefill/agents` on GitHub |
| Skill | `bitrefill` — capability-aware, routes to MCP / CLI / API / browser based on host |
| Plugin | `.claude-plugin/marketplace.json` + manifest; includes [eCommerce MCP](https://docs.bitrefill.com/docs/ecommerce-mcp) via root [`.mcp.json`](.mcp.json) (Claude Code / Cowork) |
| Spec | [Agent Skills](https://agentskills.io/specification) compliant |

## Installation

### Claude Code / Cowork (plugin: skill + MCP)

Installing the **bitrefill** plugin registers the `bitrefill` skill and the eCommerce MCP server (no separate `claude mcp add` needed):

```bash
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
```

First MCP tool call triggers OAuth in your Claude client (no API key configuration). Other hosts (Cursor, Codex CLI, etc.) still configure MCP manually — see [skills/bitrefill/references/mcp.md](skills/bitrefill/references/mcp.md).

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
openclaw mcp set bitrefill --url "https://api.bitrefill.com/mcp/$BITREFILL_API_KEY"
```

Full setup, channel-aware scenarios (Telegram purchase, cron top-up, mobile-camera context), and required hardening: [skills/bitrefill/references/host-openclaw.md](skills/bitrefill/references/host-openclaw.md).

## Skill

| Skill | Description |
|-------|-------------|
| `bitrefill` | Capability-aware skill that detects the host runtime and routes to the highest-fidelity channel: residential-IP browser (ChatGPT Atlas, Cursor, Claude+Chrome), [eCommerce MCP](https://docs.bitrefill.com/docs/ecommerce-mcp) (preferred for purchases), [@bitrefill/cli](https://github.com/bitrefill/cli) via npm, or the [REST API](https://docs.bitrefill.com/docs/api-overview) (Personal / Business / Affiliate). Includes a dedicated [OpenClaw](https://docs.openclaw.ai/) integration guide for chat-channel scenarios — Telegram purchases, cron auto-renewals, mobile-camera context. |

### Structure

```
.mcp.json                             # Claude Code plugin: eCommerce MCP (HTTP) definition
.claude-plugin/
├── plugin.json
└── marketplace.json
skills/bitrefill/
├── SKILL.md                          # capability decision tree + safeguards summary
└── references/
    ├── browse.md                     # residential browser
    ├── mcp.md                        # MCP setup per client
    ├── cli.md                        # @bitrefill/cli
    ├── api.md                        # Personal / Business / Affiliate REST
    ├── host-openclaw.md              # OpenClaw Gateway integration
    ├── capability-matrix.md          # per-client cheat sheet
    ├── safeguards.md                 # spending policy + per-host hardening
    └── troubleshooting.md
```

## Contributing

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
