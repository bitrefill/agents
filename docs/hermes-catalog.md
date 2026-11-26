# Hermes plugin catalog

The Hermes Marketplace lists a plugin after a maintainer merges one file, `plugin-catalog/bitrefill.yaml`, into [`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent). The admission rules are in that repository's `plugin-catalog/README.md`, and the submission guide is `website/docs/developer-guide/plugins/catalog-submission.md`. Every update is a new PR that moves `sha`, and reviewers read the commits between the old and new pins.

## Before opening the PR

1. Merge the release commit here and copy its full 40-character sha into the entry below. Keep that commit reachable, because a weekly job delists entries whose pinned commit disappears.
2. Check that the `hermes` job in `.github/workflows/check.yml` passed on that commit. It runs the catalog's `hermes plugins validate` at the Hermes release it pins. The `caution` findings it lists are explained in the disclosures.
3. Open the PR from a Bitrefill account. The catalog declines entries submitted by anyone other than the owner or a major contributor.

## Entry

```yaml
name: bitrefill
title: Bitrefill
repo: https://github.com/bitrefill/agents
sha: <40-character release commit>
version: "4.0.0"
description: "Browse and buy gift cards, mobile top-ups and eSIMs from 1,500+ brands in 180+ countries, paid by card, Apple Pay, Google Pay, crypto or Bitrefill balance. Bundles the Bitrefill MCP server and the bitrefill skill. Disclosure — hosted connector: every tool call goes to api.bitrefill.com (remote tool list not covered by the pin), and what the tools return, including orders, gift card codes and saved cards, reaches your model provider and Hermes's session history; buy-products spends real money and Hermes asks before every order; guest checkout runs the Bitrefill CLI from npm through terminal with no Hermes prompt; submit_feedback sends Bitrefill the note with the account id, IP, user agent and country."
maintainer: Bitrefill
tier: community
category: tools
requires_hermes: ">=0.22.3"
docs_url: https://github.com/bitrefill/agents/blob/main/skills/bitrefill/references/harnesses/hermes.md
platforms: []
known_issues:
  - "Sign-in needs one extra step after install, because a portable mcp.json cannot declare OAuth: run `hermes mcp add bitrefill --url https://api.bitrefill.com/mcp --auth oauth --connect-timeout 300`, then `hermes config set mcp_servers.bitrefill.trust untrusted` (mcp add resets trust), then /reload-mcp. Until then Hermes logs a 401 from the bitrefill connector at startup."
capabilities:
  provides_tools: []
  provides_hooks: []
  provides_middleware: []
  requires_env: []
```

`requires_hermes` is v0.22.3 because that is the first release that reads the `costs` and `spend_limit` server keys the per-order prompt depends on. Earlier builds ignore them and would run `buy-products` without asking.

## PR description

Title: `feat(plugin-catalog): add bitrefill plugin`

> Adds the official Bitrefill plugin, submitted from Bitrefill's own repository. We ask for `tier: verified`.
>
> **What it does.** It lets the agent browse and buy gift cards, mobile top-ups and eSIMs on Bitrefill, check prices and availability, and read the user's orders and balance. It is a portable Agent Plugins v1 package with no Python: the `bitrefill` skill and one remote MCP server, `https://api.bitrefill.com/mcp`. The Hermes rules live in [hermes.md](https://github.com/bitrefill/agents/blob/<sha>/skills/bitrefill/references/harnesses/hermes.md) and [safeguards.md § Hermes](https://github.com/bitrefill/agents/blob/<sha>/skills/bitrefill/references/safeguards.md#hermes).
>
> **Hermes surfaces.** The skill loads through `skills_list` and `skill_view`. The MCP server goes through Hermes's remote MCP client. `plugin.json` declares `extensions."com.nousresearch.hermes".servers.bitrefill` with `trust: "untrusted"`, a cost of 1 order on `buy-products` and `spend_limit: 0.5`, so Hermes asks before every order, also under `/yolo`, and each answer covers only that order.
>
> **Sign-in.** The server requires OAuth and answers 401 with `WWW-Authenticate: Bearer resource_metadata=...`. A package server cannot complete sign-in: it gets no `auth: oauth` (#115429) and `hermes mcp login` cannot find it (#87253, in scope for #152002). So `known_issues` and the README give the one-time `hermes mcp add … --auth oauth` plus `hermes config set mcp_servers.bitrefill.trust untrusted`; the native entry keeps the package's costs and spend limit. We tested it end to end: Hermes signed in with its hosted client-metadata document and listed 13 tools. We will drop the step in a SHA-bump PR once a Hermes release signs in a package server by itself.
>
> **Approvals.**
> - The nine read-only tools are annotated `readOnlyHint: true`. Hermes asks before `buy-products` (every order), `submit-prepayment-step`, `update-order` and `submit_feedback`.
> - The skill quotes first and treats only the user's reply to the quote as a confirm. It never answers Hermes's prompt, never suggests **Always**, `/yolo`, `approvals.mode: off` or a higher limit, never runs `hermes` commands or changes Hermes settings, and never retries a refused order another way.
> - The connector buys only in a local session. In chat apps it only searches and quotes, because a profile's sign-in is shared by every chat and the order prompt goes to whoever is in the chat. Cron, one-shot and other unattended runs never buy.
> - Guest checkout before sign-in runs `npx -y @bitrefill/cli@0.3.0` through `terminal`, which has no Hermes prompt, so it rests on the confirm. It buys only while the CLI reports `"identity":"unregistered"`, and a guest invoice moves no money until the user pays its link or address. `safeguards.md` § Hermes gives an `approvals.deny` list that blocks signed-in CLI buys and self-reconfiguration.
> - A wallet the agent already has pays an invoice once, after the confirm, under that wallet's own approvals and caps. A wallet that pays only x402 (AgentCash) runs the order on Bitrefill's x402 checkout through the wallet's own HTTP tool.
>
> **Disclosures.**
> - Network: `api.bitrefill.com` (MCP server, CLI, x402 checkout), the npm registry when `npx` fetches `@bitrefill/cli`, and `www.bitrefill.com` for payment links the user opens.
> - The server's tool list and instructions are not covered by the pin. The server's instructions tell the model to read `https://www.bitrefill.com/agents/SKILL.md` when no `bitrefill` skill is loaded.
> - Tool results, including orders, gift card codes, saved cards and a guest invoice's access token, reach the model provider and stay in Hermes's session history. On a gateway, `session_search` lets any allowed user read earlier sessions, so the README tells the owner to allow only themselves.
> - Purchases spend the user's money, each after the user's confirm in chat; an autonomous opt-in with a spend cap applies only in a local session and only after the owner sets `trust: full`.
> - Credentials: Hermes stores and refreshes the OAuth tokens. The Bitrefill CLI keeps its own guest token in `~/.config/bitrefill-cli/`, which the skill never reads; on Hermes the skill never signs the CLI in. The x402 session token stays in the chat and is never written to memory or files. The wallet sign-in scripts in `skills/bitrefill/scripts/` serve other hosts; on Hermes the skill never runs them.
> - Shell commands: `npx -y @bitrefill/cli@0.3.0` for guest checkout, and a wallet CLI the user already has when it pays an invoice.
> - Feedback: `submit_feedback` sends Bitrefill a note of up to 2,000 characters with the agent's name, model, harness and capabilities, and the server records the account id, IP, user agent and country. Hermes prompts before it runs. There is no other telemetry.
> - `hermes plugins validate` reports three `caution` findings, all `ssh_dir_access` in `skills/bitrefill/references/safeguards.md`. They are sandbox and permission deny rules (`denyRead: ["~/.ssh", ...]`) that block access to SSH keys.
> - Rule 20: payments in stablecoins and broadly adopted coins (USDC, BTC, ETH, SOL). The plugin promotes no coin or token.
