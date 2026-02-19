# Bitrefill Agent Skills

A collection of agent skills for [Bitrefill](https://www.bitrefill.com) — enabling AI coding agents to browse, buy, and manage Bitrefill products.

## Status

| Item | Status |
|------|--------|
| Repo | `bitrefill/agents` on GitHub |
| Skills | 1 skill (`bitrefill-website`) |
| Plugin | `.claude-plugin/marketplace.json` (Claude Code / skills CLI compatible) |
| Spec | [Agent Skills](https://agentskills.io/specification) compliant |

## Installation

```bash
npx skills add bitrefill/agents
```

With a specific agent (e.g. Cursor):

```bash
npx skills add bitrefill/agents -a cursor -y
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `bitrefill-website` | Browse and search Bitrefill (gift cards, top-ups, eSIMs), get product/pricing info, buy and pay with crypto or card, redeem or use purchases. Use when the user mentions Bitrefill, gift cards, phone top-up, eSIM, or paying with Bitcoin/Lightning. |

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
