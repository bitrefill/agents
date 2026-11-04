# OpenAI review preparation

Spec checked: **2026-11-04**. Package: **Bitrefill v3.4.2**.
Intended publisher: **Bitrefill**, matching the repository's existing identity.
Directory identity verification has not been checked.

## Package and listing

The release asset `bitrefill.zip` contains one plugin at the archive root:
portable `plugin.json`, portable `mcp.json`, Codex/Claude/Cursor compatibility
manifests, legacy `.mcp.json`, skills and supporting resources, the logo, README
and MIT license. The marketplace catalog and build tools are excluded.

The portable manifest declares Agent Plugins 1.0.0. OpenAI listing, review and
publication metadata live under `extensions.com.openai`; the compatibility
manifest carries the same values. The inline portable OpenAI extension takes
precedence over the Codex overlay, rather than merging with it.

| Item | Evidence / status |
| --- | --- |
| Portable schemas | Validated against the published 1.0.0 schemas; local copies and provenance in `scripts/schemas/` |
| Native Codex reader | `codex-cli 0.166.0-alpha.5.1` successfully read the extracted ZIP through `plugin/read` in a temporary local marketplace: one `bitrefill` skill, one `bitrefill` MCP server, listing and resolved icons; no installation or OAuth performed |
| Archive | Builder reopens and validates the ZIP, references, icons, frontmatter, compatibility metadata and tag versions |
| Regression coverage | Packaging tests cover omitted assets, invalid transport, mismatched tag, broken references, private app bindings, unsafe entries and reproducibility |
| Listing | Bitrefill; subtitle `Gift cards, top-ups and eSIMs` (29 characters); category `Other` |
| Icon | Existing Bitrefill PNG, 512 × 512 pixels; referenced as logo and composer icon; visually inspected |
| Country targeting | Creator selected all available countries; `publication.countries: []` intentionally removes the availability allowlist. Product availability still varies by country. |
| Commerce | `review.commerce: true`; digital goods and supported checkout/payment routes explicitly disclosed |
| OAuth | Existing `https://api.bitrefill.com/mcp` retained. No credentials or guessed OAuth client configuration packaged. Live OAuth remains unverified. |
| Live MCP probe | Blocked: endpoint returned Cloudflare 403 / error 1010 for this environment; no successful initialization, authenticated tool listing or tool calls |

Listing URLs are stored in the manifest's interface, separately from homepage:

- Website: https://www.bitrefill.com — Bitrefill shopping website.
- Support: https://help.bitrefill.com/hc/en-us — accessible FAQ and request form.
- Privacy: https://www.bitrefill.com/privacy/ — Bitrefill Global Privacy Policy,
  updated 30 September 2026.
- Terms: https://www.bitrefill.com/terms/ — Bitrefill terms, updated
  21 October 2026; includes purchases made by agents.

Support was inspected directly. Website, terms and privacy were inspected
through web retrieval because direct requests from this environment returned
403. The creator must confirm that these published policies fully cover the
plugin's actual backend data processing; content accessibility alone does not
establish that coverage.

## Review cases and demonstration

Exactly five positive and three negative cases are included as structured
metadata in both manifests. They use the tool names documented in this
repository; authenticated discovery must confirm those names and schemas.

| Case | Expected tools / boundary | Execution status |
| --- | --- | --- |
| US Amazon catalog | `search-products`; no purchase | Not run — MCP access unavailable |
| Product denominations and restrictions | `search-products`, `get-product-details`; returned data only | Not run — MCP access unavailable |
| Italy Vodafone top-ups | `search-products`; correct country, no purchase | Not run — MCP access unavailable |
| Recent account orders | `list-invoices`; no redemption codes | Not run — authenticated sample account required |
| Latest order status | `list-invoices`, `get-invoice-by-id`; exact returned identifier | Not run — authenticated sample account required |
| Arbitrary bitcoin transfer | No shopping or wallet transfer tools | Not run in intended host |
| Refund a delivered card | Explain unsupported refund tool; link support | Not run in intended host |
| Offer a wallet seed phrase | Decline secret collection; use secure sign-in | Not run in intended host |

These are draft review cases, not claimed test passes. Before final submission,
run them against the exact saved submission version in the intended host and
resolve any schema or behavior differences.

Prepare the demo with a development installation and a dedicated Bitrefill
reviewer account containing sample invoices. The current environment has no
verified authenticated Bitrefill connection, so a real recording depends on
that setup. A script is not a completed demo.

Suggested recording (about two minutes):

1. Show Bitrefill installed in ChatGPT or Codex and connect the dedicated account
   through the host's OAuth flow; keep credentials and tokens off screen.
2. Ask: “Find Amazon gift cards for the United States. Do not buy anything.”
   Show actual returned products and region.
3. Ask: “Show the available denominations and redemption restrictions for one
   of those cards without buying it.” Show details grounded in the actual result.
4. Ask: “Show my recent Bitrefill orders. Keep redemption codes private.”
   Then ask for the latest order's status. Show real sample-order results.
5. Ask: “Refund my delivered Bitrefill gift card and reverse its payment.”
   Show the explanation of the limitation and the support destination.
6. Demonstrate any purchase/payment tools offered for review only with an
   authorized sandbox/test setup and explicit spending authorization. Do not
   perform a real-money purchase just to complete this recording.
7. Play back the saved video, verify readable prompts/results and absence of
   secrets, host it where reviewers can view it without requesting access, and
   add the verified URL as `review.demo_recording_url` in both manifests.

No recording URL has been supplied or invented. No reviewer credentials belong
in the ZIP or this repository. Supply dedicated demo access and login instructions
only through the secure portal fields; reviewers must not need personal inbox,
phone, or inaccessible MFA access.

## Public-directory readiness

**Package checks do not establish directory eligibility or approval.** The
creator is discussing review with an OpenAI representative. No policy exception
has been verified or assumed.

The current [commerce guidelines](https://developers.openai.com/plugins/plugin-guidelines#commerce-and-monetization)
limit plugin commerce to physical goods and prohibit selling digital products
or services. Bitrefill's gift cards, top-ups and eSIMs conflict with that stated
restriction. The same guidelines list execution of crypto transfers among
prohibited services and prescribe external checkout by default; wallet-payment
and direct-payment instructions also need explicit review. Retaining truthful
purchase features and disclosure does not resolve those policy questions.

Before the archive can be called ready for final directory submission:

- Resolve digital-goods, crypto-payment and checkout policy applicability with
  the OpenAI representative; record the outcome outside public listing text.
- Complete the real demo recording and verify its reviewer-accessible URL.
- Verify the intended Bitrefill publisher identity and policy coverage.
- Prepare a dedicated reviewer account with sample data and secure access.
- Upload the prepared ZIP to [OpenAI Plugins](https://platform.openai.com/plugins)
  under the intended verified developer identity. Include MCP in the initial
  package; do not create a skills-only draft to add the MCP later.
- Verify imported metadata and country targeting; complete domain verification,
  OAuth connection, live tool/annotation checks, skill scans and MCP scans.
  Every tool needs explicit, accurate boolean `readOnlyHint`, `openWorldHint`
  and `destructiveHint`; this repository does not contain the hosted server's
  implementation, so those annotations cannot be repaired here.
- Run the eight cases against the saved version, correct failures, and have the
  authorized developer complete required legal/policy attestations.
- Submit for review when ready; publishing the approved release is a separate
  action. No OpenAI draft, submission or directory publication has been created
  by the GitHub release workflow.

## Current references

- [OpenAI packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI submission and metadata](https://developers.openai.com/plugins/deploy/submission)
- [OpenAI validation errors](https://developers.openai.com/plugins/deploy/submission-errors)
- [OpenAI plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
- [OpenAI skills](https://developers.openai.com/plugins/build/skills)

The live documentation has inconsistencies: the submission-errors page still
mentions annotation justifications, while the guidelines explicitly say they
are no longer required. Use accurate explicit booleans and verify the portal's
actual scan findings. Optional per-server auth extensions are documented by
OpenAI but absent from the published portable MCP JSON schema; this package
avoids those overrides and retains the existing endpoint.
