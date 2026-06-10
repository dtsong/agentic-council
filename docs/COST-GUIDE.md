[Docs home](./index.md) · [Usage](./USAGE.md) · [Councils](./COUNCILS.md) · **Cost guide** · [Orchestration](./ORCHESTRATION.md) · [Architecture eval](./ARCHITECTURE-EVAL.md)

# Cost Guide

The council spawns real agents, so sessions have real token costs. Two levers control spend:

1. **`--profile lean|balanced|max`** — which model tier each *spawned agent* runs on.
2. **`/model`** — which model *you* (the conductor) run on. The interview, synthesis, design doc, and PRD are conductor work; the engine never overrides your choice.

The engine shows a token estimate at the Assembly approval gate — before anything spawns — and echoes your current conductor model so a mismatch is visible.

## What each profile does

Models are routed by **spawn site** (an agent's model is fixed when it spawns):

| Spawn site | `lean` | `balanced` (default) | `max` |
|---|---|---|---|
| Positions & converge (Rounds 1/3) | Sonnet | Opus | Opus |
| Challenge round (Round 2) | **Opus** one-shots | persistent agents | **Fable** one-shots |
| Audit agents | Sonnet | Sonnet | Opus |
| Brainstorm | Sonnet | Sonnet | Sonnet |
| Conductor | your `/model` | your `/model` | your `/model` |

Why Round 2 gets special treatment: the challenge round is where positions actually move — it's the highest-leverage spot for extra intelligence. In `lean`, fresh Opus one-shots read both Round 1 positions from disk and write the rebuttals, so you pay Opus prices only for the debate itself. In `max`, the same mechanism upgrades to Fable.

## Estimated token usage

Total tokens, 5-agent baseline — scale roughly by `selected agents ÷ 5`:

| Mode | lean | balanced | max |
|---|---|---|---|
| brainstorm | 10–15K | 10–15K | 10–15K |
| quick | 20–35K | 30–50K | 45–75K |
| standard | 80–120K | 120–180K | 180–270K |
| deep | + 50–80K audit | + 50–100K audit | + 80–150K audit |

Estimates are deliberately coarse — the engine is prompt logic and can't meter tokens. The hard ceiling, where one exists, is the deliberation/audit workflow's token budget (see [Orchestration](./ORCHESTRATION.md)).

## If you're API-billed (enterprise agreement, token-conscious)

Run **`--profile lean`**. Positions and convergence run on Sonnet 4.6, and Opus is spent only on the challenge round. A Sonnet conductor is acceptable; expect a flatter design doc — if one phase deserves `/model opus`, it's a standard session's synthesis.

Indicative API pricing (June 2026, per MTok in/out — verify current pricing before budgeting):

| Model | Input | Output |
|---|---|---|
| Sonnet 4.6 | $3.00 | $15.00 |
| Opus 4.8 | $5.00 | $25.00 |
| Fable 5 | $10.00 | $50.00 |

Back-of-envelope: a 5-agent standard session at `lean` lands roughly in the $0.50–1.50 range; `balanced` roughly $1.50–4.00, output-heavy sessions trending higher.

Other levers:

- Trim the roster at the Assembly gate — cost scales linearly with agent count.
- Prefer `--quick` for well-understood changes; save standard/deep for genuinely contested designs.
- `--auto --profile lean` is the cheapest unattended full session.

## If you're on a Claude Max plan ($100–200/mo)

There is no per-token dollar cost — sessions draw on your plan's rate limits. The question becomes *where to spend quality*, not money:

- **`--profile max`** puts Opus on every seat and Fable on the challenge round.
- **`/model opus` (or fable) before standard/deep sessions** — conductor synthesis is the single highest-leverage model choice in the whole session.
- `balanced` remains the sane daily default; deep + max burns rate limits fastest, so save it for the decisions that warrant a one-hour deliberation.
- Workflow-backed deliberation also runs in the background, so a max-profile deep session doesn't block your interactive work.

## Profile mechanics

- Resolution order: `--profile` flag → the council's `DEFAULT_PROFILE` theme variable → `balanced`.
- The resolved profile persists in `session.md`/`index.json` and survives `--resume`. Pre-v1.2 sessions resume as `balanced`.
- Composable with every mode: `/council --deep --profile lean "Redesign auth"`.
- If a Fable spawn errors (availability, plan access), the engine retries the spawn with Opus.
- Agent files declare `model: inherit`; the engine passes the routed tier explicitly on every spawn. Pinned `claude-*` IDs are rejected by the validator — they go stale.

---

Next: [Orchestration](./ORCHESTRATION.md) — the backends behind a session and how they degrade.
