---
name: bitrefill
description: "Buy or browse Bitrefill — 1,500+ gift cards, mobile top-ups, and eSIMs across 180+ countries, payable in crypto, Lightning, USDC via x402, or pre-funded account balance. Routes the host agent to its highest-fidelity channel (residential browser, MCP server, npm CLI, or REST API) based on detected runtime capabilities, with a dedicated OpenClaw integration guide for chat-channel scenarios. Triggers when the user mentions Bitrefill, gift cards, mobile top-up, eSIM data plan, refilling a phone, or asks to pay or check out with crypto, Lightning, USDC, or x402."
compatibility: "Detects host capabilities at runtime. Paths require: browse — residential-IP browser; MCP — MCP-capable client + Bitrefill OAuth/API key; CLI — Node.js >=18 + shell + npm; API — outbound HTTP + Bitrefill API key (Personal) or API ID/Secret (Business/Affiliate). OpenClaw host gets a dedicated guide."
metadata:
  author: bitrefill
  version: "2.0.0"
  homepage: "https://www.bitrefill.com"
  docs: "https://docs.bitrefill.com"
  repository: "https://github.com/bitrefill/cli"
---

# Bitrefill

Bitrefill sells digital goods (gift cards, mobile top-ups, eSIMs) across 180+ countries and 1,500+ brands. Pay with crypto, Lightning, USDC via x402, or pre-funded account balance. Codes deliver instantly after payment confirms.

This skill **routes by capability, not by use case**. Same intent ("buy a Steam card") plays out differently across hosts. Pick a path below based on what your runtime can do.

## Pick a path

Walk these checks **in order**. First match wins.

1. **Inside OpenClaw?** Check for `~/.openclaw/openclaw.json`, `~/.openclaw/skills/`, or `openclaw` on PATH. If yes → read [host-openclaw.md](references/host-openclaw.md) first. OpenClaw is a superset host: it can run all four paths plus chat-channel scenarios (Telegram purchase, cron top-up, mobile camera). After setup, return here and pick MCP/CLI/API for the actual task.

2. **Browse-only intent (no purchase)?** If the user only wants to explore, compare prices, or learn how products work:
   - Have a residential-IP browser (ChatGPT Atlas, Cursor browser tool, Claude/Playwright Chrome extension, OpenClaw on user host)? → [browse.md](references/browse.md).
   - Datacenter egress only (ChatGPT web/Agent, Gemini consumer, Jules)? `www.bitrefill.com` returns **403 Cloudflare** to datacenter IPs. Use [mcp.md](references/mcp.md) `search-products` / `product-details` instead — they return the same catalog without scraping.

3. **MCP supported?** Bitrefill ships a remote HTTP/SSE MCP at `https://api.bitrefill.com/mcp`. Works on Claude.ai (Pro+), Cowork, Claude Desktop, Claude Code, ChatGPT (Plus+), Atlas, Codex CLI, Gemini CLI, Cursor, OpenCode, OpenClaw. **Highest-fidelity purchase channel — typed tool calls, OAuth or API key, no shell needed.** → [mcp.md](references/mcp.md).

4. **Shell + `npm install` available?** Claude Code, Codex CLI, Cursor, Gemini CLI, OpenCode, OpenClaw, Jules (ephemeral VM), ChatGPT Agent (sandbox). → [cli.md](references/cli.md).

5. **Outbound HTTP from agent loop?** Anywhere shell exists, plus Claude Code `WebFetch`. Last resort — verbose, no typed validation. → [api.md](references/api.md).

6. **None of the above** (e.g. Gemini consumer free tier): give the user a `bitrefill.com` link and stop.

Don't know which host you're in? Read [capability-matrix.md](references/capability-matrix.md) — per-client cheat sheet maps every leading agent product to its viable paths.

## Top spending safeguards (read full list before any purchase)

This skill enables **real-money transactions**. Codes deliver instantly and digital goods are non-refundable per EU consumer rights.

- **Confirm before buying.** Present product, denomination, price, payment method. Wait for explicit user approval. Autonomous purchasing only when user opts in for the current session.
- **Treat codes as cash.** Never paste in group chats or public channels. Prefer in-memory storage over plain-text logs. Advise user to redeem ASAP.
- **Use a dedicated, low-balance account.** Never give the agent access to high-balance accounts or crypto wallet seeds. This skill is **not a wallet**.
- **Log every purchase.** `invoice_id`, product, amount, payment method.

Full safeguards + per-host hardening (OpenClaw exec-approvals, Cursor auto-approve, Codex sandbox, Claude Code allowlist) → [safeguards.md](references/safeguards.md).

## References

| File | Use when |
|------|----------|
| [browse.md](references/browse.md) | Agent has residential-IP browser; user wants to explore |
| [mcp.md](references/mcp.md) | MCP-capable host; preferred purchase path |
| [cli.md](references/cli.md) | Shell + npm available; headless scripting |
| [api.md](references/api.md) | HTTP-only runtime; Personal / Business / Affiliate REST tiers |
| [host-openclaw.md](references/host-openclaw.md) | Running inside OpenClaw Gateway |
| [capability-matrix.md](references/capability-matrix.md) | Per-client viable paths cheat sheet |
| [safeguards.md](references/safeguards.md) | Spending policy + per-host hardening |
| [troubleshooting.md](references/troubleshooting.md) | Common errors across all paths |

## Source of truth

Skill summarizes and routes. For exhaustive enums (countries, payment methods, full endpoint list), follow link-outs to <https://docs.bitrefill.com>.
