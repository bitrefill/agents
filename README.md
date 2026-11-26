# Bitrefill Agent Skills

A unified, capability-aware agent skill for [Bitrefill](https://www.bitrefill.com) — enabling AI agents to browse, buy, and manage gift cards, mobile top-ups, and eSIMs across 180+ countries with crypto, Lightning, USDC via x402, pre-funded account balance, card, Apple Pay or Google Pay.

## Status

| Item | Status |
|------|--------|
| Repo | `bitrefill/agents` on GitHub |
| Skill | `bitrefill` v4.0.0 — capability-aware shopping and payment routing |
| Plugin | Portable [plugin.json](plugin.json) + [mcp.json](mcp.json); compatibility manifests for Codex, Claude Code / Cowork (`.claude-plugin/`) and Cursor / Grok Bot (`.cursor-plugin/`); all bundle the [eCommerce MCP](https://docs.bitrefill.com/docs/ecommerce-mcp) |
| Spec | [Agent Skills](https://agentskills.io/specification) compliant |

## Installation

### ChatGPT / Codex (plugin: skill + MCP)

Download `bitrefill.zip` from the [latest GitHub release](https://github.com/bitrefill/agents/releases/latest). It contains root Agent Plugins 1.0 manifests, OpenAI listing metadata, a Codex compatibility manifest, the skill and its resources, and the logo. Connect your Bitrefill account through the host's OAuth flow; no credentials are bundled. Install from an available local or development plugin source using your host's supported flow. A GitHub release does not install the plugin into OpenAI's public directory.

OpenAI public-directory review is separate. Bitrefill supports digital-goods purchases, which require resolution with OpenAI under the current commerce guidelines. See [OpenAI review preparation](https://github.com/bitrefill/agents/blob/main/docs/openai-review.md) for verified checks, review cases, and remaining materials. This package is not an approved directory listing.

### Claude Code / Cowork (plugin: skill + MCP)

```bash
/plugin marketplace add bitrefill/agents
/plugin install bitrefill@bitrefill-skills
/reload-plugins
```

Registers the **bitrefill** skill and eCommerce MCP ([`.mcp.json`](.mcp.json)); OAuth on first MCP call. Pin: `/plugin marketplace add bitrefill/agents#v4.0.0`.

Update from your shell, or in a session with `/plugin` → **Installed** → **bitrefill** → **Update now**, then `/reload-plugins`:

```bash
claude plugin update bitrefill@bitrefill-skills
```

**Cowork:** Customize → Plugins → add `bitrefill/agents` → install **bitrefill**. **claude.ai:** Connectors only → [claude-chat.md](skills/bitrefill/references/harnesses/claude-chat.md). Other hosts → [mcp.md](skills/bitrefill/references/touchpoints/mcp.md).

### Cursor / Grok Bot (plugin: skill + MCP)

Cursor: copy this repo to `~/.cursor/plugins/local/bitrefill` and run **Developer: Reload Window**; once Bitrefill is listed on Cursor Marketplace, **Customize** → **Bitrefill** → **Install**. Grok Bot installs it from that listing. Both get the skill and the connector in [`.mcp.json`](.mcp.json) (OAuth with your Bitrefill account). Host guide → [grok-bot.md](skills/bitrefill/references/harnesses/grok-bot.md).

### Hermes Agent (plugin: skill + MCP)

Hermes ≥ 0.22.3:

```bash
hermes plugins install bitrefill --enable
hermes mcp add bitrefill --url https://api.bitrefill.com/mcp --auth oauth --connect-timeout 300
hermes config set mcp_servers.bitrefill.trust untrusted
```

`bitrefill` is the Hermes plugin catalog entry. The plugin marks the server untrusted so Hermes asks before every order; `mcp add` resets that, so run the last line only after it prints `Saved 'bitrefill'`. Root [`plugin.json`](plugin.json) + [`mcp.json`](mcp.json) give Hermes the skill and the connector; `mcp add` signs in with your Bitrefill account (OAuth; Hermes stores the tokens per profile). Sign in on the Hermes machine, not in chat; SSH and Hermes Desktop → [mcp.md](skills/bitrefill/references/touchpoints/mcp.md) § Hermes Agent. Connector purchases spend real money: Hermes asks before every order, also under `/yolo`, each answer covers only that order, and the connector never buys in cron or other unattended runs. That prompt comes from the plugin, so run `hermes mcp remove bitrefill` before you disable or remove it. Every chat of a signed-in profile (Telegram, Discord…) shares its Bitrefill account, so the skill buys with it only in a local session (CLI, TUI, Desktop); in a chat app it only searches and quotes from your account (never balances, orders or codes) and checks out as a guest. On the gateway, allow only yourself: Hermes's session search lets any allowed user read earlier sessions, codes included. Without sign-in the skill checks out as a guest by running `npx -y @bitrefill/cli@0.3.0` in the terminal (needs Node.js; downloads the CLI and its dependencies from npm into the npm cache; sends your email to api.bitrefill.com; keeps a guest token in `~/.config/bitrefill-cli/`; no Hermes prompt, since it only opens invoices you pay by link or crypto). Until you sign in, Hermes logs at startup that the `bitrefill` connector returned 401; that is expected. Hermes keeps tool results in its local session history, including a guest invoice's access token, which unlocks the code: treat that history as private. If the agent has a crypto wallet (a wallet MCP or CLI), the skill pays crypto invoices from it after your yes; a wallet that only pays x402 (AgentCash) runs the whole order on Bitrefill's x402 checkout instead, signed in with the wallet's address. That wallet's own approvals and caps decide whether it asks again, and in a chat app the yes comes from whoever is in the chat. Hardening for `terminal` and `execute_code` → [safeguards.md](skills/bitrefill/references/safeguards.md) § Hermes. Tools and their instructions come from Bitrefill's server at runtime, not from the installed commit; without the skill loaded, those instructions point the model at `https://www.bitrefill.com/agents/SKILL.md`. Tool results reach your model provider. Feedback sends Bitrefill the note with your account id, IP, user agent and country, and only after Hermes asks. The skill's wallet sign-in scripts are for other hosts. Host guide → [hermes.md](skills/bitrefill/references/harnesses/hermes.md). Bitrefill [Terms](https://www.bitrefill.com/terms/) and [Privacy Policy](https://www.bitrefill.com/privacy/) apply.

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
openclaw mcp set bitrefill '{"url":"https://api.bitrefill.com/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login bitrefill
```

Connect with OAuth or configure `Authorization: Bearer $BITREFILL_API_KEY` using the host's supported secret/header settings. Keep credentials out of URLs.

Full setup, channel-aware scenarios, and hardening: [skills/bitrefill/references/harnesses/openclaw.md](skills/bitrefill/references/harnesses/openclaw.md).

## What the plugin uses

- **Connector:** `https://api.bitrefill.com/mcp` (HTTP, OAuth with your Bitrefill account, no API key): search, product details, buy, order updates, invoices, balances, saved cards, help articles.
- **Guest checkout** (no account): npm `@bitrefill/cli` from `registry.npmjs.org` and an email; else a `www.bitrefill.com` link.
- **Optional APIs:** `api.bitrefill.com/v2` (`BITREFILL_API_KEY`); `api.bitrefill.com/x402` through a wallet tool you already installed (e.g. Coinbase Wallet MCP, AgentCash), which pays any pay-per-call lookups, or direct HTTP. The skill never asks for private keys or seed phrases.
- **Bundled scripts:** `scripts/siwx_*.js` use Node built-ins only, accept sign-in challenges only from `https://api.bitrefill.com`, write an unsigned sign-in draft to `/tmp/siwx_payload.json` and send the signed one back to `api.bitrefill.com`.
- **Headless sign-in (optional):** an agent inbox such as AgentMail (`agentmail-cli` / `agentmail-mcp` from `registry.npmjs.org`, `AGENTMAIL_API_KEY`, `api.agentmail.to`); TOTP from the 1Password CLI (`op`, your own vault).

Each purchase is confirmed with you unless you opt into autonomous buying. Bitrefill [Terms](https://www.bitrefill.com/terms/) and [Privacy Policy](https://www.bitrefill.com/privacy/) apply.

## Skill

| Skill | Description |
|-------|-------------|
| `bitrefill` | Capability-driven routing: probe harness (exec, egress, MCP), pick touchpoint (Bitrefill MCP, x402 REST, CLI, API, browse), then wallet (balance, x402, send). Includes OpenClaw, Claude Chat, Grok Bot / Cursor, Hermes, ChatGPT + Coinbase Wallet MCP, and a matrix of agent wallets that can pay. |

### Structure

```
plugin.json                  # Agent Plugins 1.0 identity and OpenAI metadata
mcp.json                     # Portable Streamable HTTP MCP connection
.codex-plugin/plugin.json    # Codex compatibility manifest
assets/logo.png
.mcp.json                    # Claude / Cursor / older Codex MCP configuration
.claude-plugin/
├── plugin.json
└── marketplace.json
.cursor-plugin/
└── plugin.json
.github/workflows/
├── release.yml
└── check.yml
assets/
LICENSE
skills/bitrefill/
├── SKILL.md
├── scripts/
│   ├── siwx_build_message.js
│   └── siwx_send.js
└── references/
    ├── harnesses/
    │   ├── decision-engine.md
    │   ├── capability-matrix.md
    │   ├── openclaw.md
    │   ├── claude-chat.md
    │   ├── grok-bot.md
    │   └── hermes.md
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
    │   ├── kite-passport.md
    │   ├── bankr.md
    │   ├── alby.md
    │   ├── tether-wdk.md
    │   └── pay.md
    ├── safeguards.md
    └── troubleshooting.md
```

## Contributing

Build and validate with Python 3.13 or newer:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/package_plugin.py --tag v4.0.0
python scripts/package_plugin.py --validate dist/bitrefill.zip --tag v4.0.0
```

The release workflow validates tagged versions, packages the complete plugin as `bitrefill.zip`, and publishes it with `SHA256SUMS`. It excludes marketplace catalogs, development files and credentials. Keep versions synchronized across the portable, Codex, Claude and Cursor manifests, marketplace metadata and skill metadata.

To add a new skill:

1. Create a new directory under `skills/` (e.g., `skills/my-skill/`)
2. Add a `SKILL.md` file with valid YAML frontmatter (`name`, `description`) and agent instructions
3. Optionally add a `references/` subdirectory with supporting documentation
4. Bump the version fields → [CLAUDE.md § Releasing Updates](CLAUDE.md#releasing-updates) (skills are auto-discovered)

Skill names must be lowercase with hyphens and match the directory name exactly.

## Documentation

For the full Agent Skills specification, see [agentskills.io/specification](https://agentskills.io/specification).

## License

[MIT](LICENSE)
