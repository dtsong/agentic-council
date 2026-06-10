# Architecture Evaluation — v1.1 → v1.2

*June 2026. The design record behind the v1.2.0 changes: cost profiles, model un-pinning, and workflow-first orchestration.*

## What v1.1 got right

- **One engine, four themes.** `commands/_council-engine.md` holds all orchestration; each council supplies ~50 lines of theme variables. Adding the finance/people/revenue councils cost ~0% duplication. This is the architecture's load-bearing wall — keep it.
- **Disk-mediated context flow.** Every round writes to `$SESSION_DIR/deliberation/`; later agents read from disk instead of inheriting a bloated context. A 7-agent, 3-round deliberation that would overflow any single context window stays lean. This convention is also what made the v1.2 workflow migration cheap — fresh-context workflow agents pick up exactly where persistent teammates left off, because the state was never in a context window to begin with.
- **Organic tension pairing.** Round 2 pairs emerge from reading Round 1 positions rather than hardcoded rules. Real disagreements surface; fake ones don't.
- **The skill system as methodology capture.** 60+ skills are structured prompts (Process + Quality Checks + Evolution Notes), not libraries. They make agent output consistent and defensible (STRIDE, WCAG 2.2 AA, etc.).

## What v1.1 got wrong

### 1. Stale, undifferentiated model pinning

All 38 agent files pinned `model: "claude-opus-4-6"` — two model generations stale by June 2026, with a 38-file maintenance burden on every release. Worse, the pin was *undifferentiated*: a position statement, an adversarial rebuttal, and an audit sweep have very different intelligence requirements, and every user — regardless of billing model — paid Opus prices for all of them.

**v1.2 fix:** agents declare `model: inherit`; the engine passes an explicit tier alias (`sonnet`/`opus`/`fable`) on every spawn, routed by a **spawn-site × profile table**. `scripts/validate.py` now rejects any pinned `claude-*` ID, making the stale-pin failure mode unrepeatable.

### 2. No cost model for either kind of user

Two personas, neither served:

- **Enterprise / API-billed (token-conscious, Sonnet 4.6 default).** Wants Sonnet everywhere except where extra intelligence demonstrably pays. The highest-leverage spot in a deliberation is the **Round 2 challenge** — it's where positions actually move. `--profile lean` runs R1/R3 on Sonnet and spawns fresh Opus one-shots per tension pair (they read both Round 1 files from disk). Roughly 40% cheaper than balanced with most of the debate quality retained.
- **Claude Max subscriber ($100–200/mo, rate-limit-bound, not dollar-bound).** Wants maximum value, deliberately. `--profile max` keeps Opus everywhere and upgrades challenges to Fable one-shots; pairing it with `/model opus|fable` for the conductor covers synthesis — the single highest-leverage model choice in the whole session, since the conductor writes the design doc and PRD.

Cost transparency was also zero: a standard session burned 120–180K tokens with no warning. v1.2 prints a mode × profile estimate at the roster-approval gate, before anything spawns.

### 3. Orchestration bet entirely on an experimental primitive

The engine hard-exited without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — even for brainstorm and audit modes that never used teams. Meanwhile Anthropic shipped **dynamic workflows** (GA on all paid plans): script-driven orchestration, background execution, in-session resume, and intermediate results that never touch the main context.

## Workflows vs agent teams — the per-phase decision

Anthropic's own framing is "who holds the plan": with teams, the lead decides turn by turn; with a workflow, the script decides. Applying that per phase:

| Phase / mode | Plan-holder | v1.2 primitive | Why |
|---|---|---|---|
| Intake, interview, approvals | the user | **main loop** | Workflows can't take mid-run input; gates belong in conversation |
| brainstorm, quick | nobody (one fan-out) | **inline Task** | 3 one-shots; any orchestration runtime is overhead |
| standard/auto/deep/guided deliberation | **fixed** (R1 → pair → R2 → R3 → synthesize) | **workflow** | Deterministic round structure is exactly script-shaped; round texts stay out of the conductor's context; resumable; no experimental flag |
| `--meet` cross-examination | emergent (who asks whom, follow-ups, user steering) | **teams** (degrades) | Direct agent-to-agent messaging and Shift+Down steering are teams' core value |
| Path A execution | shared task list w/ dependencies | **teams** (degrades) | File locking, dependency unblocking, per-task plan approval are team features |
| Deep audit (5D) | fixed loop-until-converged | **workflow** | Replaces the hand-rolled checkpoint/respawn machinery; `budget` gives a hard token ceiling |

Degradation order everywhere: preferred backend → the other → sequential Task calls. The engine never hard-exits on a missing runtime again. The teams flag is now an optional enhancement (two features), not a gate on the whole plugin.

**Primary quality risk accepted:** workflow agents are fresh contexts, so a member doesn't "remember" its Round 1 reasoning the way a persistent teammate does. Mitigation: every R2/R3 prompt instructs the agent to read its own prior round file first ("it is YOUR prior work"). The teams deliberation path is retained verbatim as a fallback, which also makes A/B comparison possible if deliberation depth regresses.

**Why not ship the scripts as saved workflows?** Plugins can't ship a `workflows/` component (verified against the plugin spec, June 2026 — recognized dirs are skills/commands/agents/hooks/mcp/lsp/monitors/bin). The templates live in `references/workflows/*.template.js`; the conductor invokes them verbatim via the Workflow tool with all session specifics in `args`. If plugin workflow distribution lands later, promote them to first-class saved workflows.

## Cost-profile design notes

- **Routing is keyed by spawn site, not round**, because a teammate's model is fixed at spawn. The lean/max R2 upgrade therefore uses *fresh one-shot spawns* per tension pair rather than a mid-flight model swap — possible only because round state lives on disk.
- **Brainstorm stays Sonnet in every profile.** It's the mode new users try first; don't make it slower or dumber to save pennies, and don't let `max` make a 30-second gut check expensive.
- **The conductor is documented, not controlled.** It's the main session; the plugin can't set its model. The roster-approval estimate echoes the current `/model` so a mismatch (max profile + haiku conductor) is visible before spending.
- **Estimates are coarse by design.** Prompt logic can't meter tokens; ranges are honest about that. The hard ceiling, where it matters, is the workflow `budget`.

## Fallback / compatibility matrix

| Mode | WF ✓ Teams ✓ | WF ✓ Teams ✗ | WF ✗ Teams ✓ | Neither |
|---|---|---|---|---|
| brainstorm / quick | inline | inline | inline | inline |
| standard / auto / deep / guided | workflow | workflow | teams (v1.1 behavior) | sequential |
| meeting | **teams** | workflow, no live steering (notice printed) | teams | sequential |
| Path A execution | **teams** | sequential over the TaskCreate dependency list | teams | sequential |
| audit / 5D | workflow | workflow | conductor waves (v1.1) | conductor waves |

Session layout, index/registry schemas, resume slugs, and archive format are unchanged. `session.md` gains `Profile:` and `Backend:`; both default sensibly when absent, so pre-v1.2 sessions resume cleanly.

## Deferred (v1.3 candidates)

- **Worktree-isolated workflow execution for Path A** — `agent(…, {isolation: 'worktree'})` could replace teams for parallel implementation without file conflicts.
- **Post-session token actuals** — currently approximated (artifact word count); a harness-level usage surface would make it real.
- **First-class saved workflows** — if/when plugins can ship a `workflows/` component.
- **Meeting mode on workflows with steering** — would need mid-run user input, which workflows deliberately don't support; revisit if that changes.
