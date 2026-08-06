# Session Budget Guard

> Internal mechanics — never voiced. Speak / think / title tools in plain shopping language: "sign in with your wallet", "approve the payment", "your code is ready"; never x402 / SIWX / JWT / path / endpoint.

**Mandatory agent-policy preflight.** Read and apply this file for every budget request (`set`, `status`, `change`, or `reset`), before every ledger read or mutation, before processing payment/refund/reversal evidence, and, with [safeguards.md](safeguards.md), before every operation that can create, submit, auto-pay, pay, or settle a Bitrefill purchase. This includes post-processing after a read-only status call. A budget is a ceiling, not permission to spend; confirmation and host approval remain separate.

## Enforcement boundary

This guard is instruction-layer enforcement. It depends on the agent retaining valid session state, following these rules, and serializing purchase attempts. It does not intercept tools, bind other agents or sessions, or provide host-, wallet-, cryptographic-, or Bitrefill-side enforcement. Keep host approvals enabled and use a dedicated low-balance account or wallet cap as independent controls.

If the host cannot retain and atomically update session state, or another actor could spend against the same ledger concurrently, stop. Never describe this guard as unbypassable.

## Canonical session state

Keep one ledger in host-provided session-local structured state; otherwise keep it in current-conversation working memory. Do not intentionally copy it to a profile, new chat, disk, logs, or shared memory. Host state may have provider retention: if its session scope cannot be verified, block purchases. A new session starts with no budget.

All minor-unit values are canonical base-10 integer **strings**, not JSON numbers:

```yaml
session_id: <opaque current-session identifier>
ledger_revision: "7"
budget_currency: EUR
budget_scale: 2
budget_limit_minor: "10000"
alias_index:
  alias_1: {kind: invoice, value: inv_123, attempt: purchase_a91e/attempt_1}
  alias_2: {kind: order, value: ord_456, attempt: purchase_a91e/attempt_1}
financial_event_index:
  event_1:
    identity: [wallet, debit, "eip155:8453", USDC_BASE, 0xtx]
    charge: purchase_a91e/attempt_1/charge_principal_1
  event_2:
    identity: [wallet, fee-debit, "eip155:8453", ETH_BASE, 0xtx]
    charge: purchase_a91e/attempt_1/charge_fee_1
purchases:
  purchase_a91e:
    product: <slug or safe description>
    created_at: <session-local timestamp>
    active_attempt_id: attempt_1
    attempts:
      attempt_1:
        idempotency_key: <unique key for this provider attempt>
        cart_binding: <hash/reference of canonical product/package/quantity/region/recipient terms>
        payment_method: usdc_base
        payer_reference: <safe non-secret account or wallet binding/hash>
        aliases:
          invoice_id: inv_123
          order_ids: [ord_456]
        lifecycle: active
        checkout_status: payment_confirmed
        checkout_version: <monotonic version or authoritative timestamp>
        charges:
          charge_principal_1:
            kind: principal
            accounting:
              debit_authority: wallet
              refund_authority: bitrefill
            payable:
              asset: USDC_BASE
              network: eip155:8453
              destination_binding: <normalized recipient or provider-bound destination hash>
              payment_terms_reference: <invoice/challenge/authorization ID or hash>
              scale: 6
              authorized_minor: "33000000"
              debited_minor: "30000000"
              refunded_minor: "0"
            budget_impact:
              currency: EUR
              scale: 2
              authorized_minor: "3100"
              settled_minor: "2820"
              refunded_minor: "0"
              conversion_reference: <authoritative quote or response ID>
            financial_status: paid
            evidence:
              bitrefill: <status plus version/timestamp>
              wallet: <status plus version/timestamp>
          charge_fee_1:
            kind: network_fee
            accounting:
              debit_authority: wallet
              refund_authority: wallet
            payable:
              asset: ETH_BASE
              network: eip155:8453
              destination_binding: <fee quote or transaction-intent binding>
              payment_terms_reference: <authoritative fee quote ID or hash>
              scale: 18
              authorized_minor: <integer string>
              debited_minor: <integer string>
              refunded_minor: "0"
            budget_impact:
              currency: EUR
              scale: 2
              authorized_minor: <integer string>
              settled_minor: <integer string>
              refunded_minor: "0"
              conversion_reference: <authoritative fee quote ID>
            financial_status: paid
            evidence:
              wallet: <status plus version/timestamp>
```

An immutable logical purchase owns one or more provider attempts. Each attempt records its own payment method and safe payer binding because a replacement may route differently. Each attempt owns immutable, unique charge IDs for principal, network fee, wallet/service fee, or paid lookup. A component's `payable` records the asset that can leave the account plus the network, destination binding, and authoritative terms reference; its `budget_impact` records what it commits against the budget. Never aggregate different assets into one payable field. Authorization is a cap and settlement is the authoritative actual debit; they must never share one field.

Derived values, recomputed after every transition:

- `reserved = sum(charge.budget_impact.authorized_minor)` for every charge whose `financial_status` is `reserved` or `debit_unresolved` on every attempt; inactive attempts remain committed until authoritative no-debit evidence releases them.
- `settled = sum(charge.budget_impact.settled_minor - charge.budget_impact.refunded_minor)` for all `paid`, `partially_refunded`, `refunded`, or `reversed` charges, including frozen attempts.
- `committed_headroom = budget_limit_minor - reserved - settled`.
- `verified_remaining = committed_headroom` only when no charge is `debit_unresolved` and the guard is not breached; otherwise it is unknown. `available = max(0, verified_remaining)` when known and `0` otherwise.

An unexpected authoritative debit may make `committed_headroom` negative. Record the truth, mark the guard breached, report the exact overage, and block all further purchase-capable calls. Never clamp or rewrite settled spend to make the ledger appear valid.

## Exact money rules

Use arbitrary-precision integer arithmetic. Full-match decimal input against `(?:0|[1-9][0-9]*)(?:\.[0-9]+)?`; reject signs, exponent notation, whitespace, separators, `NaN`, infinity, or trailing text. Use an authoritative integer scale from 0 through 18, pad missing fractional digits, and reject rather than round excess precision. The budget limit and every created charge authorization must be positive; zero is valid only where the state rules below allow it.

Declare and enforce `MAX_MINOR = 2^256 - 1` for every stored minor-unit amount and the numeric ledger revision. Perform multiplication and division at arbitrary precision, then range-check the result. Never use IEEE-754 `Number` for ledger arithmetic or comparisons. If an external tool accepts only a JSON number, render the already-validated decimal lexeme at that boundary without recomputing it, and block if the host cannot preserve the lexeme safely.

Before every read or mutation, validate:

- `session_id` matches the current session; missing or mismatched state is lost state. `ledger_revision` is a canonical bounded unsigned integer string and every mutation uses compare-and-swap against it.
- The budget limit is positive; scales, assets, currencies, integer strings, bounds, and derived totals are valid.
- For each charge, `0 <= payable.refunded_minor <= payable.debited_minor` and `0 <= budget_impact.refunded_minor <= budget_impact.settled_minor`. A normal settlement is no greater than its authorization; retain an authoritative over-cap debit as a breach.
- Every charge's budget-impact currency and scale equal the ledger currency and scale. Its payable asset may differ only when an authoritative quote binds that component's exact budget impact.
- Every purchase has one immutable session-scoped logical key. Every attempt has a distinct immutable idempotency key, cart binding, payment method, safe payer reference, aliases, checkout evidence, and lifecycle `active` or `frozen`. Build `cart_binding` deterministically from every purchase-relevant product/package/value, quantity, region, and recipient/delivery field; store only safe normalized fields or a one-way session-bound hash for sensitive values. `active_attempt_id` is either `null` when no call is eligible or points to the exactly one `active` attempt; every other attempt is `frozen`. Attempt identity and route fields never change after the first provider write. Freeze + new proposed attempt + pointer swap is one revision-CAS transition; reservation is a later CAS before payment. A CAS conflict fails closed and reconciles before another call.
- Charge IDs are immutable and unique within an attempt. A payment-capable attempt has exactly one `kind: principal` charge by reservation time; every fee/lookup component has its own charge ID. Each charge selects one immutable canonical accounting authority/stream for debit amounts and one for refunds before reservation. Financial state lives only on charges.
- A `proposed` charge is absent or all-zero and may omit payment terms. Each `reserved` charge has non-empty payable asset, network, destination binding, and payment-terms reference; positive payable/budget authorizations; and zero debit, settlement, and refund. `debit_unresolved` has the same non-empty bindings, positive authorization and authoritative payable debit, zero budget settlement/refund, and any exact payable refund within the debit bound; keep its full budget authorization reserved and block new writes. Each `paid` charge has the same bindings plus positive authoritative debit/settlement and zero refunds. `partially_refunded` retains the paid predicates and has a positive authoritative refund that is below the relevant gross amount; budget rounding may leave its budget refund at zero. `refunded` and `reversed` have budget refund equal to gross budget settlement; when original-payable-asset evidence is used, payable refund also equals gross payable debit. A `released` charge has zero debit, settlement, and refund; it may retain historical authorization and bindings for audit but contributes nothing to totals. Any debit under `proposed`, `reserved`, or `released` is inconsistent state and fails closed.
- Each charge stores financial evidence separately per authority (for example Bitrefill, wallet, network, or service) with that authority's own status and monotonic version/timestamp. Never order unrelated authorities by comparing their clocks.
- Each non-empty external identifier, including every ID in a multi-order list, is indexed exactly once as the structured tuple `(kind, exact value)` to one attempt. Two attempts claiming the same tuple, or one response resolving to different attempts, is an ambiguous collision and fails closed. Never merge by product, amount, or time.
- Each authoritative debit, fee, refund, or reversal event is indexed exactly once as the structured tuple `(authority, event kind, network-or-na, asset, exact event ID)` to one charge. Compare structured fields directly or use a canonical length-prefixed encoding; never concatenate unescaped delimiters. Repeated evidence updates that charge; the same event on two charges is an ambiguous collision and fails closed. Only the charge's selected canonical stream changes accounting amounts. Evidence from another authority is corroboration/conflict, never an additional debit/refund; link it explicitly to the same economic event or exclude it from totals until reconciled.

Missing, inconsistent, ambiguous, or unsupported state blocks creating or paying an order. Reconcile unresolved transactions; never reconstruct spend by guessing from chat history.

## Budget lifecycle

- **Set:** require an explicit positive amount and currency for this session. Clarify ambiguous symbols such as `$`. Creating a budget is not purchase approval.
- **Status:** report the exact limit, net paid amount, pending authorization, and remainder or overage only when verified. With any `debit_unresolved` charge, report the known settled amount and committed cap but say the remainder cannot be verified; make no new purchase. Do not expose internal fields or sensitive responses.
- **Change:** increasing, decreasing, replacing, or changing currency requires a separate explicit confirmation after restating the change. A decrease cannot go below net settled plus reserved. Change currency only while `purchases` is empty; otherwise reconcile, explicitly reset, then set a new ledger. Removing a budget follows Reset, never Change.
- **Reset/remove:** require explicit confirmation. Never remove the limit or delete ledger records while any charge is `reserved`/`debit_unresolved`, any attempt is ambiguous, or any financial outcome is pending/unknown. Resolve all exposure first; only then may the confirmed reset remove the ledger. Purchases remain blocked until a new explicit budget is set.
- **Autonomy:** never infer a cap from a purchase request. A valid budget also never substitutes for manual confirmation unless safeguards record a current-session autonomous opt-in.

## Preflight, reservation, and repricing

Run this sequence immediately before every purchase-capable call:

1. Reconcile pending attempts through non-paying status tools. An unknown outcome remains committed and cannot be retried through a replacement attempt.
2. Establish every payable authorization and budget impact from the most authoritative current quote, invoice, payment challenge, and fee quote. Persist the normalized asset, network, destination binding, and terms reference for each component. Model principal and each differently denominated network/wallet/service fee as separate charge components; face value is insufficient.
3. When a charge's payable asset differs from the budget currency, require an authoritative conversion bound to that component and store its reference. Show the total exact budget impact under normal confirmation rules. Never use a market quote, inferred rate, or silent conversion.
4. Create one random session-scoped logical purchase key before the first write and one distinct attempt/idempotency key before each provider create attempt. Pass the attempt key to the provider when supported. Add later request, invoice, order, transaction, and payment IDs as typed aliases of that exact attempt after uniqueness checks; index every financial event to exactly one charge.
5. In one serialized update, validate the ledger and add or replace only the new `reserved` charge authorizations before any money-moving call. Accept the transition only when its recomputed post-update `reserved + settled <= budget_limit_minor`; equality is allowed. For a new purchase this is equivalent to `sum(new_authorized_budget_impacts) <= available`. Already-paid ancillary charges remain counted only in `settled`, never reserved again.
6. Immediately before invocation, reconstruct the actual request and require exact equality with the active attempt's idempotency key, cart/product terms, payer, payment method, and every reserved charge's asset, network, destination, payable amount/cap, budget impact, and fee cap. For the first expressly non-paying create call, match its proposed cart/route/idempotency fields and prove it cannot pay; separately reserve any paid-call fee. A mismatch blocks without invoking.
7. Invoke the operation once. A create/quote response must resolve uniquely to that attempt and match its cart/method; validate its newly returned terms before attaching aliases or exposing anything. Quarantine a mismatched/ambiguous response, freeze the attempt, clear its active pointer atomically, retain all exposure, and reconcile. A money-moving response instead records its uniquely indexed actual debit—even when below its cap—and treats any over-cap debit as a breach. A duplicate or already-paid response updates the indexed attempt/charge, never triggers another purchase.
8. On payment confirmation, retain each charge's historical authorization cap, record its authoritative actual debit and budget settlement, and move its financial status out of `reserved`. The derived totals then release only that component's unused authorization without erasing the audit cap. One charge may settle even if another fails or remains unknown.

Before the first provider write, a `proposed` attempt may replace its proposed cart/route fields. After that write, its cart, method, payer, exact payable amount, asset, network, destination, and payment-terms references are immutable. A same-attempt authorization-cap adjustment is allowed only for reserved charges with no debit when the underlying server-bound payable terms and fee references are byte-for-byte unchanged. Compute `available_for_active_attempt = limit - net_settled_all - reserved_all_except_active_attempt_charge_set`; this includes every frozen attempt, including those under the same logical purchase. Atomically replace, rather than add to, the active attempt's complete reserved authorization set when `sum(new_authorized_impacts) <= available_for_active_attempt`, then renew confirmation. Any changed cart, method, payer, price, fee terms, asset, network, destination, terms reference, or budget impact requires the no-debit freeze/replacement procedure. Never reprice a debited attempt or use replacement to evade a failed check.

Recreate only after every principal/payment charge has authoritative no-debit proof and is released, while every ancillary lookup/create/fee charge is authoritatively settled or released. A settled ancillary fee stays counted. In one revision-CAS transition freeze the old attempt, create the new proposed attempt with a new idempotency key, and switch `active_attempt_id`; reserve its returned terms in a later CAS before payment. A response may mutate only the attempt selected through its typed alias. Late financial evidence may strengthen only the frozen attempt's indexed charge; it can never release, reprice, or settle the active attempt. Any recommitment or debit of a frozen principal/payment charge locks all new writes until that old exposure is authoritatively resolved, even when current headroom is positive.

An expressly non-paying quote or invoice call may obtain the exact total after a coarse estimate passes. That estimate must itself be positive, cover the complete cart and known fees, have the budget currency or an authoritative conversion, and be no greater than `available`; it is a screening check, not a reservation or authorization. If those facts are unavailable, block even the create call. Reserve the returned exact amount before exposing a payment link or making any payment call. If it exceeds `verified_remaining`, leave it unpaid. For `balance` or any auto-paying create call, the exact total and reservation must exist before creation; otherwise disable auto-pay, use a non-paying flow, or block.

For each charge, store an exact provider-reported budget-currency debit when available. Otherwise, when an authoritative locked conversion supplied authorization pairs `P_auth` payable and `B_auth` budget minor units, derive its smaller actual impact conservatively as `ceil(B_auth * P_debit / P_auth)`. Do not fetch a new FX rate. If neither method is possible, retain that component's full authorization as `debit_unresolved`, preserve the exact payable debit, and block further writes.

Any network fee, wallet/service fee, paid lookup, invoice-creation fee, or paid status call is its own charge component with its own asset, authorization, debit, conversion reference, and refund state. Reserve all components atomically. Do not use a client that can pay before exposing the exact amount, fee cap, and stable identifier.

## Provider-state reconciliation

Financial evidence is monotonic per charge and authority: a later or stale delivery/status observation cannot erase a confirmed debit or refund. Within one authority prefer sequence/version, then authoritative event time; never compare clocks across authorities. Combine evidence conservatively—the strongest financial fact wins—and fail closed on conflict. Interpret Bitrefill's documented [invoice and order statuses](https://docs.bitrefill.com/docs/core-concepts) as follows:

| Authoritative observation | Ledger action |
| --- | --- |
| Invoice `unpaid` | Keep reserved. Release only with authoritative expiry/cancellation **and** proof of no debit. |
| Invoice `payment_detected` | Keep reserved unless an authoritative wallet/provider response gives the exact debit. Record it; settle only with a safe budget impact, otherwise use `debit_unresolved`. Never release. |
| Invoice `payment_confirmed`, `pending`, or `complete` | Record the exact actual debit and settle its safe budget impact. If either value is unavailable, keep the full authorization committed as unresolved and block further writes. |
| Invoice `denied` from `unpaid` | Release only when the same attempt authoritatively shows no payment detection or debit. |
| Invoice `blocked` or `payment_error` | Ambiguous financial outcome: keep reserved/settled. Release only after authoritative no-debit proof; apply a confirmed refund separately. |
| Touchpoint `expired` or `cancelled` | Release only when authoritative status also proves unpaid/no debit. Local timeout is insufficient. |
| Order `created`, `payment_detected`, `processing`, `delivered`, or `failed` | Do not release funds. Reconcile any payment indication separately; delivery failure after payment remains paid until a refund is confirmed. |
| Order/payment `refunded` or provider reversal | Apply only its authoritative cumulative refund; never infer a refund from delivery failure. |
| Unknown, missing, contradictory, or older status | Preserve the strongest committed amount, block retries, and reconcile. |

A lost create/payment response keeps the attempt's reservations. Discover the result by its idempotency key, typed aliases, or authoritative history; attach a unique match to that attempt. No match is not proof of failure, and multiple matches are an ambiguity. Never repeat a money-moving call solely because its response was lost. An older `unpaid` response cannot downgrade `payment_detected`, a confirmed debit, or a refund, and an old attempt can never mutate its replacement.

## Deterministic refunds

For each refunded charge, keep gross settlement unchanged and increase only canonical cumulative refund fields from the charge's single selected refund-accounting stream. Accept an authoritative cumulative total directly. If that stream supplies increments, require a unique event ID for each, index each once to this charge, and sum only those increments into the canonical cumulative total. Cross-authority observations never add a second amount. Prefer the canonical total already expressed in the budget currency. If only an exact cumulative refund in the charge's original payable asset is authoritative, reuse its original settlement allocation—never current FX:

`target_budget_refund = floor(gross_budget_settlement * cumulative_payable_refund / gross_payable_debit)`

On a confirmed full refund of that charge, set the target to its full gross budget settlement to remove rounding residue. Apply only the positive delta from its previously stored cumulative refund, never more than its gross settlement. For a refund paid in a different asset, restore budget only when the selected refund authority supplies an exact cumulative budget-currency returned impact tied uniquely to this charge; otherwise restore nothing and keep reconciliation blocked. The same zero-restore rule applies when any refund lacks an exact cumulative amount or unique charge binding. Never prorate a principal refund across separate fee charges; a fee returns only when its own authoritative refund confirms it.

## Privacy and user-facing copy

Store only typed transaction identifiers, a safe product description or slug, the cart binding/hash, money allocation fields, payment method, normalized network, safe payer/destination bindings or hashes, timestamps/versions, authoritative terms/conversion references, and status. Never store redemption codes, eSIM QR data, seed phrases, private keys, API keys, auth tokens, full invoices, or full tool responses.

Keep messages short, localized, and free of internal terms:

- Allowed: “€30 is within your €100 session budget. €70 will remain after purchase.”
- Blocked: “This €80 purchase would exceed your remaining €70 budget. I haven’t placed the order.”
- Status: “Your session budget is €100. You’ve spent €20, €10 is pending, and €70 remains.”
- Unresolved debit: “Your session budget is €100. €20 is confirmed and up to €15 is still being verified, so I can’t confirm the remaining amount or place another order yet.”
- State unavailable: “I can’t verify the session budget, so I haven’t placed the order. Set the budget again before continuing.”

Do not expose terms such as state machine, ledger, MCP, endpoint, x402, harness, or idempotency key.

## Acceptance scenarios

| Scenario | Required result |
| --- | --- |
| €100 budget; authorize €30; debit €30 | Reserve then settle €30; €70 remains. |
| Authorize €31 cap; actual debit €28.20 | Settle €28.20 and release €2.80; never count the cap as paid. |
| €30 paid; next request €80 | Block before purchase; €70 remains. |
| Pre-write proposed attempt changes €30 → €35 | Replace the proposal before its first provider write; after a write, changed payment terms require a replacement attempt. |
| €30 USDC principal plus ETH network fee | Reserve and settle two charge components with separate assets and budget impacts; never combine their minor units. |
| Invoice A expires unpaid; replacement invoice B is created | Freeze A, create a new attempt under the same purchase, and let late A responses mutate only A. |
| Retry a paid invoice or lose its response | Reconcile the same record; never issue a second money-moving call. |
| Stale `unpaid` arrives after `payment_confirmed` | Preserve the confirmed debit. |
| `payment_error` after `payment_detected` | Keep funds committed until exact debit/no-debit/refund evidence arrives. |
| Delivery fails after €30 payment | Keep €30 settled; restore only an authoritative refund. |
| Unpaid invoice authoritatively expires with no debit | Release its reservation; settled spend is unchanged. |
| USD 30.00 payable settles as authoritative €28.20 impact; USD 15 refunded | Restore €14.10 using the original allocation, without new FX. |
| Concurrent €60 + €60 against €100 | Serialize; only one reserves. |
| Duplicate invoice alias appears on two records | Treat as collision, block, and reconcile; never merge heuristically. |
| Same wallet debit/refund event appears on two charges | Treat as collision; update neither total until it maps uniquely to one charge. |
| Frozen attempt recommits while its replacement is active | Count both exposures and block all new writes until the old principal resolves. |
| EUR budget; total known only in USD | Block unless an authoritative conversion binds the exact EUR impact. |
| State lost after restart/context loss | Block and never reconstruct spend by guessing. |
| User increases, replaces, or resets the cap | Restate the change and require explicit confirmation. |
| Autonomous buy without a cap | Ask for an amount and currency; infer no unlimited budget. |
| User asks for status | Report limit, net paid, reserved, and remaining without sensitive data. |
| A debit has no safe budget-currency impact | Report known spend and committed cap, say remainder is unverified, and block new writes. |
| Purchase exactly equals remainder | Allow; remainder becomes zero. |
| Negative, zero, `NaN`, infinity, `1e2`, over-precision, >`2^256-1`, or float-coerced purchase amount | Reject before every purchase-capable call. |
