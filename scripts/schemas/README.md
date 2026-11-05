# Package schemas

Unmodified Agent Plugins 1.0.0 schemas retrieved on 2026-11-04 from:

- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json

OpenAI's [packaging documentation](https://developers.openai.com/plugins/build/plugins)
identifies these schema URLs. The release validator uses these local copies so
an upstream network failure or schema change cannot silently change a release.
OpenAI-specific listing and archive checks supplement the portable schemas.

The retrieved MCP schema does not accept per-server `extensions`, although
OpenAI documents that extension for optional authentication overrides. This
package uses the existing endpoint without overrides; OAuth must be verified
through the host connection flow. No client IDs, scopes or secrets are guessed.
