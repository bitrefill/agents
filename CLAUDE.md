# Bitrefill Skills — Agent Guide

This repository is a monorepo of agent skills for Bitrefill. Skills live in the `skills/` directory.

## Repository Structure

```
skills/
  <skill-name>/
    SKILL.md          # Required — frontmatter + agent instructions
    references/       # Optional — supporting docs, examples
.claude-plugin/
  marketplace.json    # Plugin manifest listing all skills
```

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
5. Register the skill in `.claude-plugin/marketplace.json` under the `plugins[0].skills` array

## Naming Conventions

- Skill names: lowercase, hyphens only (e.g., `bitrefill-buy`, `bitrefill-esim`)
- Directory name **must match** the `name` field in SKILL.md frontmatter
- Prefix with `bitrefill-` for Bitrefill product skills

## Specification

See the Agent Skills specification: https://agentskills.io/specification
