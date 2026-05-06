# Cross-Council Handoff Protocol

When a council session surfaces a question outside its domain, the conductor emits a **handoff block** in the design document. The user runs the receiving council manually — there is no automatic spawn — and the receiving council reads the carry-forward artifacts during its Phase 1 context scan.

This protocol exists to keep councils focused. Mixed-roster sessions are prohibited (`references/positioning-charter.md` §"Cross-Council Interaction"). Handoffs replace them.

## When to Emit a Handoff

A conductor (any Maestro: Steward, Comptroller, Chair, Quartermaster, etc.) emits a handoff when, during synthesis (Phase 3 → design.md or Phase 4 → prd.md), at least one of the following holds:

- A decision in the design depends on a quantifiable answer the current roster cannot produce (e.g., engineering proposes a $40K/mo infra ceiling — finance owns the unit-economics validation).
- A risk identified during deliberation falls squarely in another council's domain (e.g., `/people-council` notes that a comp band change may trigger securities-law disclosure — punt to `/finance-council`'s RegRep).
- The user's idea contains tightly-coupled sub-questions that span councils, and splitting them produces sharper artifacts than forcing one council to generalize.

A handoff is **not** emitted for tangential mentions. Threshold: would a separate council session change a meaningful decision in this design?

## Handoff Block Format

The conductor appends one block per handoff to the design document under a top-level `## Cross-Council Handoffs` section:

```markdown
## Cross-Council Handoffs

### Handoff 1
- **From:** /council (engineering)
- **To:** /finance-council
- **Question:** "Validate the unit-economics model behind the $40K/mo infra ceiling for US-007."
- **Why we can't answer it:** Engineering council lacks tax + capital-allocation perspective; the ceiling assumes a 30% gross-margin floor we did not derive.
- **Carry-forward artifacts:**
  - `.claude/council/sessions/<slug>/design.md` § "Cost Model"
  - `.claude/council/sessions/<slug>/prd.md` US-007 acceptance criteria
- **Recommended trigger:** `/finance-council "Validate the $40K/mo infra ceiling for <feature> against our 30% gross-margin floor."`
```

## Receiving Council — Phase 1 Consumption

When a sibling council's `/x-council` is invoked with carry-forward context (either via the `--from-handoff <path>` flag or by user paste of the handoff block), the conductor:

1. **Reads carry-forward artifacts** during Phase 1's context scan, in addition to the standard project scan.
2. **Surfaces the originating handoff** at the top of the interview summary so receiving agents can see the chain of reasoning.
3. **Constrains scope to the handoff question.** The receiving council does not re-litigate decisions made by the originating council unless the user explicitly opens them.
4. **Emits a return handoff** if its synthesis changes assumptions in the originating council's design (e.g., finance concludes $40K/mo is too generous; recommends $28K). The originating council's session can be resumed (`/<original> --resume <slug>`) to incorporate the return.

## Anti-Patterns

- **Auto-spawn:** never automatically invoke a sibling council. The user controls whether to spend the time.
- **Handoff chains > 2 deep:** if Council A hands off to B which wants to hand off to C, escalate to the user with all three open questions in one place. Three-deep chains usually mean the original idea was ambiguous, not that the system is working.
- **Handoff for trivial cross-domain mentions:** the threshold is *"would change a meaningful decision."* Lower bar = noise.

## Telemetry

Each handoff block written or consumed is logged to the workspace index (`.claude/<theme-id>/index.json`) under the session entry:

```json
{
  "handoffs_out": [
    { "to": "/finance-council", "question": "...", "emitted_at": "<ISO 8601>" }
  ],
  "handoffs_in": [
    { "from": "/council", "question": "...", "received_at": "<ISO 8601>" }
  ]
}
```

This data lets us evaluate, after a few months of usage, whether sibling councils are actually being chained productively or whether certain handoffs recur often enough to suggest a built-in mechanism.
