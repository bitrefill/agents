# Bitrefill Skills — Agent Guide

Instructions:
- Be semantically dense and token efficient. Prefer concise, information-rich responses; avoid filler, repetition, and unnecessary elaboration.
- Whene editing, never mention the previous version or the changes you made. All the contents must be authoritative and up to date.
- Try abstracting instructions that can be applied to multiple cases
- Avoid creating new sections as much as possible. Try updating exisiting knowledge instead.

This repository contains Bitrefill agent skills packaged as a portable **Agent Plugins 1.0 plugin**, with Codex, Claude and Cursor compatibility manifests. Skills live in the `skills/` directory and are distributed through the plugin system shared by Claude Code and Claude Cowork.

## Installing the Plugin

### Claude Code

```shell
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
/reload-plugins
```

Bundled **eCommerce MCP** ([`.mcp.json`](.mcp.json), OAuth on first call). Pin: `bitrefill/agents@v3.4.0`.

### Claude Cowork

Customize → Plugins → add `bitrefill/agents` → install **bitrefill**.

### claude.ai (Chat)

Connectors only → [skills/bitrefill/references/harnesses/claude-chat.md](skills/bitrefill/references/harnesses/claude-chat.md).

### Local Testing

```shell
claude --plugin-dir ./
```

`/reload-plugins` after edits. `claude plugin validate .` before publish.

## Repository Structure

```
plugin.json            # Portable identity and OpenAI metadata
mcp.json               # Portable MCP configuration
.codex-plugin/
  plugin.json          # Codex compatibility fallback
.claude-plugin/
  plugin.json          # Plugin manifest (name, version, author)
  marketplace.json     # Marketplace catalog listing the plugin
.mcp.json              # Optional — MCP server definitions (eCommerce HTTP MCP for this repo)
.cursor-plugin/
  plugin.json          # Cursor / Grok Bot manifest (skills + .mcp.json)
assets/logo.png        # Plugin logo
skills/
  <skill-name>/
    SKILL.md            # Required — frontmatter + agent instructions
    references/         # Optional — supporting docs, examples
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
5. Synchronize all release versions as described under Publishing Updates

## Naming Conventions

- Skill names: lowercase, hyphens only (e.g., `bitrefill`, `bitrefill-affiliate`)
- Directory name **must match** the `name` field in SKILL.md frontmatter
- Reserved words `anthropic` and `claude` cannot appear in skill names ([agentskills.io](https://agentskills.io/specification))

## Publishing Updates

Keep the release version synchronized in root `plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.claude-plugin/marketplace.json` and skill metadata. Run `python -m unittest discover -s tests -v` and `python scripts/package_plugin.py --tag vX.Y.Z` before pushing the matching tag. The release ZIP excludes the marketplace catalog. OpenAI directory review requirements are tracked in `docs/openai-review.md`. Users run:

```shell
/plugin marketplace update bitrefill-skills
/plugin update bitrefill@bitrefill-skills
/reload-plugins
```

## Submitting to the Official Anthropic Directory

To make the plugin available in the official Claude plugin directory (visible in both Claude Code and Cowork), submit via one of:
- **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)
- **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)

## Specification

- Plugin format: [Create plugins](https://code.claude.com/docs/en/plugins)
- Marketplace format: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- Skill format: [Agent Skills specification](https://agentskills.io/specification)
