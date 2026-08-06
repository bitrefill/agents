# Bitrefill Agent Skills

A unified, capability-aware agent skill for [Bitrefill](https://www.bitrefill.com) — enabling AI coding agents to browse, buy, and manage gift cards, mobile top-ups, and eSIMs across 180+ countries with crypto, Lightning, USDC via x402, or pre-funded account balance.

## Status

| Item | Status |
|------|--------|
| Repo | `bitrefill/agents` on GitHub |
| Skill | `bitrefill` v3.3 — harness × touchpoint × wallet routing with a per-session purchase budget guard |
| Plugin | `.claude-plugin/marketplace.json` + manifest; includes [eCommerce MCP](https://docs.bitrefill.com/docs/ecommerce-mcp) via root [`.mcp.json`](.mcp.json) (Claude Code / Cowork) |
| Spec | [Agent Skills](https://agentskills.io/specification) compliant |

## Installation

### Claude Code / Cowork (plugin: skill + MCP)

```bash
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
/reload-plugins
```

Registers the **bitrefill** skill and eCommerce MCP ([`.mcp.json`](.mcp.json)); OAuth on first MCP call. Latest published release pin: `bitrefill/agents@v3.2.0`.

Update:

```bash
/plugin marketplace update bitrefill-skills
/plugin update bitrefill@bitrefill-skills
/reload-plugins
```

**Cowork:** Customize → Plugins → add `bitrefill/agents` → install **bitrefill**. **claude.ai:** Connectors only → [claude-chat.md](skills/bitrefill/references/harnesses/claude-chat.md). Other hosts → [mcp.md](skills/bitrefill/references/touchpoints/mcp.md).

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

Or from a reviewed local checkout of this repository:

```bash
openclaw skills install ./skills/bitrefill --as bitrefill --global
openclaw skills info bitrefill --agent <agent_id> --json
openclaw gateway restart
```

Do not use the bare ClawHub slug `bitrefill`: it is not an owner-qualified Bitrefill release. Verify the resolved source before enabling purchases.

Then wire eCommerce MCP for typed read/status tools; keep purchase tools filtered so buys remain CLI-approval-gated:

```bash
openclaw mcp add bitrefill \
  --url https://api.bitrefill.com/mcp \
  --transport streamable-http \
  --auth oauth \
  --include 'search-products,get-product-details,list-invoices,get-invoice-by-id'
openclaw mcp login bitrefill
openclaw mcp doctor bitrefill --probe
```

These commands require an OpenClaw build whose `openclaw mcp --help` lists `add`, `login`, and `doctor`; otherwise use the JSON fallback in the full guide and keep MCP disabled if OAuth or the read-only allowlist cannot be verified.

Full setup, channel-aware scenarios, and hardening: [skills/bitrefill/references/harnesses/openclaw.md](skills/bitrefill/references/harnesses/openclaw.md).

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
    ├── budget-guard.md
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
