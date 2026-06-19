# Bitrefill Agent Skills

A unified, capability-aware agent skill for [Bitrefill](https://www.bitrefill.com) — enabling AI coding agents to browse, buy, and manage gift cards, mobile top-ups, and eSIMs across 180+ countries with crypto, Lightning, USDC via x402, or pre-funded account balance.

## Status

| Item | Status |
|------|--------|
| Repo | `bitrefill/agents` on GitHub |
| Skill | `bitrefill` v3.0 — harness × touchpoint × wallet routing |
| Plugin | `.claude-plugin/marketplace.json` + manifest; includes [eCommerce MCP](https://docs.bitrefill.com/docs/ecommerce-mcp) via root [`.mcp.json`](.mcp.json) (Claude Code / Cowork) |
| Spec | [Agent Skills](https://agentskills.io/specification) compliant |

## Installation

### Claude Code / Cowork (plugin: skill + MCP)

Installing the **bitrefill** plugin registers the `bitrefill` skill and the eCommerce MCP server (no separate `claude mcp add` needed):

```bash
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
```

First MCP tool call triggers OAuth in your Claude client (no API key configuration). Other hosts (Cursor, Codex CLI, etc.) still configure MCP manually — see [skills/bitrefill/references/touchpoints/mcp.md](skills/bitrefill/references/touchpoints/mcp.md).

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

Full setup, channel-aware scenarios, and hardening: [skills/bitrefill/references/harnesses/openclaw.md](skills/bitrefill/references/harnesses/openclaw.md).

**Claude Chat (claude.ai):** MCP-first + inline `show_widget` shopping UI → [skills/bitrefill/references/harnesses/claude-chat.md](skills/bitrefill/references/harnesses/claude-chat.md).

## Skill

| Skill | Description |
|-------|-------------|
| `bitrefill` | Capability-driven routing: probe harness (exec, egress, MCP), pick touchpoint (Bitrefill MCP, x402 REST via Base MCP, CLI, API, browse), then wallet (balance, x402, send). Includes OpenClaw, Hermes, ChatGPT+Base MCP, and wallet matrix (Base MCP, AgentCash, CDP awal, Phantom, MetaMask). |

### Structure

```
.mcp.json
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
    │   └── phantom.md
    ├── safeguards.md
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
