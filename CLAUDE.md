# Bitrefill Skills — Agent Guide

Instructions:
- Be semantically dense and token efficient. Prefer concise, information-rich responses; avoid filler, repetition, and unnecessary elaboration.
- When editing, never mention the previous version or the changes you made. All the contents must be authoritative and up to date.
- Try abstracting instructions that can be applied to multiple cases
- Avoid creating new sections as much as possible. Try updating existing knowledge instead.

This repository is a monorepo of agent skills for Bitrefill, packaged as a **Claude Code / Cowork plugin marketplace** and a **Cursor plugin** (also installed by Grok Bot). Skills live in the `skills/` directory; both manifests bundle them with the eCommerce MCP in `.mcp.json`.

## Installing the Plugin

### Claude Code

```shell
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
/reload-plugins
```

Bundled **eCommerce MCP** ([`.mcp.json`](.mcp.json), OAuth on first call). Pin: `/plugin marketplace add bitrefill/agents#v3.3.1`.

### Claude Cowork

Customize → Plugins → add `bitrefill/agents` → install **bitrefill**.

### Cursor / Grok Bot

Manifest [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json). Cursor: **Customize** → **Bitrefill** → **Install** when listed on Cursor Marketplace, else a local copy (§ Local Testing). Grok Bot installs it from that listing. Host guide → [grok-bot.md](skills/bitrefill/references/harnesses/grok-bot.md).

### claude.ai (Chat)

Connectors only → [skills/bitrefill/references/harnesses/claude-chat.md](skills/bitrefill/references/harnesses/claude-chat.md).

### Local Testing

```shell
claude --plugin-dir ./
```

`/reload-plugins` after edits. Cursor: copy (not symlink) the repo to `~/.cursor/plugins/local/bitrefill`, run **Developer: Reload Window**, check **Customize** lists the skill and the `bitrefill` connector.

Before a release: `claude plugin validate .`. Its warning that this CLAUDE.md is not loaded as plugin context is expected, so CI runs it without `--strict`.

## Repository Structure

```
.claude-plugin/
  plugin.json          # Claude Code / Cowork manifest (name, version, directory listing links)
  marketplace.json     # Marketplace catalog listing the plugin
.cursor-plugin/
  plugin.json          # Cursor / Grok Bot manifest (skills + .mcp.json, logo)
.mcp.json              # eCommerce HTTP MCP, bundled by both manifests
.github/workflows/
  release.yml          # v*.*.* tag matching every version field → release with bitrefill.zip
  check.yml            # Pull requests: JSON parse, plugin validate, link check
assets/                # Plugin logo
LICENSE                # MIT
skills/
  <skill-name>/
    SKILL.md            # Required — frontmatter + agent instructions
    references/         # Optional — supporting docs, examples
    scripts/            # Optional — helpers (bitrefill: wallet sign-in)
```

The marketplace (`marketplace.json`) lists plugins available for installation. The plugin manifest (`plugin.json`) defines the plugin's identity. Skills inside `skills/` are auto-discovered when the plugin loads. MCP servers in `.mcp.json` start when the plugin is enabled.

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
5. Bump versions → § Releasing Updates (skills are auto-discovered)

## Naming Conventions

- Skill names: lowercase, hyphens only (e.g., `bitrefill`, `bitrefill-affiliate`)
- Directory name **must match** the `name` field in SKILL.md frontmatter
- Reserved words `anthropic` and `claude` cannot appear in skill names ([Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure))

## Releasing Updates

Bump the version in `.claude-plugin/plugin.json` (`version`), `.claude-plugin/marketplace.json` (`metadata.version`) and `skills/<name>/SKILL.md` (`metadata.version`), plus the README and CLAUDE.md pins. After merge, push tag `v<version>`: the release job fails unless every field matches, then attaches `bitrefill.zip`. Users update from the shell, or in a session with `/plugin` → **Installed** → **bitrefill** → **Update now**, then `/reload-plugins`:

```shell
claude plugin update bitrefill@bitrefill-skills
```

## Submitting to the Official Anthropic Directory

Submit from [claude.ai/directory/manage](https://claude.ai/directory/manage) (paid claude.ai plan) after the [pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist). The listing reads `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl` and `termsOfServiceUrl` from `.claude-plugin/plugin.json`.

## Specification

- Plugin format: [Create plugins](https://code.claude.com/docs/en/plugins)
- Marketplace format: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- Cursor plugin format: [Building plugins](https://cursor.com/docs/plugins/building)
- Skill format: [Agent Skills specification](https://agentskills.io/specification)
