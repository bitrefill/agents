# Bitrefill Agent Skills

A collection of agent skills for [Bitrefill](https://www.bitrefill.com) — enabling AI coding agents to browse, buy, and manage Bitrefill products.

## Installation

```bash
npx skills add bitrefill/skills
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `bitrefill-buy` | Buy gift cards, mobile top-ups, eSIMs, and more on Bitrefill |

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
