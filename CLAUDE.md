# Bitrefill Skills — Agent Guide

Instructions:
- Be semantically dense and token efficient. Prefer concise, information-rich responses; avoid filler, repetition, and unnecessary elaboration.
- Whene editing, never mention the previous version or the changes you made. All the contents must be authoritative and up to date.
- Try abstracting instructions that can be applied to multiple cases
- Avoid creating new sections as much as possible. Try updating exisiting knowledge instead.

This repository is a monorepo of agent skills for Bitrefill, packaged as a **Claude Code / Cowork plugin marketplace**. Skills live in the `skills/` directory and are distributed through the plugin system shared by Claude Code and Claude Cowork.

## Installing the Plugin

### Claude Code

Add the marketplace and install the plugin:

```shell
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
```

### Claude Cowork

Cowork uses the same plugin system as Claude Code. Install through the Cowork plugin settings UI, or from a Cowork conversation:

1. Open **Settings > Plugins**
2. Add the marketplace source `bitrefill/agents`
3. Install the **bitrefill** plugin

Once installed, Claude gains two skills:
- **bitrefill-website** — browse, search, and buy gift cards, mobile top-ups, and eSIMs on bitrefill.com
- **bitrefill-cli** — autonomous agent commerce via the Bitrefill CLI and x402 payments

Skills activate automatically when Claude detects a relevant task.

### Local Testing

Load the plugin directly without installing from a marketplace:

```shell
claude --plugin-dir ./
```

## Repository Structure

```
.claude-plugin/
  plugin.json          # Plugin manifest (name, version, author)
  marketplace.json     # Marketplace catalog listing the plugin
skills/
  <skill-name>/
    SKILL.md            # Required — frontmatter + agent instructions
    references/         # Optional — supporting docs, examples
```

The marketplace (`marketplace.json`) lists plugins available for installation. The plugin manifest (`plugin.json`) defines the plugin's identity. Skills inside `skills/` are auto-discovered when the plugin loads.

## Adding a New Skill

1. Create a directory: `skills/<skill-name>/`
2. Add `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: Short description of what this skill does (max 1024 chars)
   ---
   ```
3. Write agent instructions in the Markdown body (step-by-step, under 500 lines)
4. Optionally add `references/` with detailed documentation
5. Bump the `version` in both `plugin.json` and `marketplace.json`

## Naming Conventions

- Skill names: lowercase, hyphens only (e.g., `bitrefill-buy`, `bitrefill-esim`)
- Directory name **must match** the `name` field in SKILL.md frontmatter
- Prefix with `bitrefill-` for Bitrefill product skills

## Publishing Updates

After modifying skills, bump the `version` field in `.claude-plugin/plugin.json` (and optionally in `marketplace.json`). Users with auto-update enabled receive changes at next Claude Code startup; others run:

```shell
/plugin marketplace update bitrefill-skills
```

## Submitting to the Official Anthropic Directory

To make the plugin available in the official Claude plugin directory (visible in both Claude Code and Cowork), submit via one of:
- **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)
- **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)

## Specification

- Plugin format: [Claude Code plugins docs](https://docs.claude.com/en/docs/claude-code/plugins)
- Marketplace format: [Plugin marketplaces docs](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- Skill format: [Agent Skills specification](https://agentskills.io/specification)
