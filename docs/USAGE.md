[Docs home](./index.md) · **Usage** · [Councils](./COUNCILS.md) · [Cost guide](./COST-GUIDE.md) · [Orchestration](./ORCHESTRATION.md) · [Architecture eval](./ARCHITECTURE-EVAL.md)

# Usage Guide

Everything `/council` (and its sibling councils) can do, end to end. New here? Run `/council --brainstorm "your idea"` first — 30 seconds, no files, no setup.

## Anatomy of a session

A full (default) session moves through six phases. You are in the loop at every gate marked 👤:

| Phase | What happens | Your touchpoint |
|---|---|---|
| 0 — Intake | Capture the idea | 👤 provide the idea |
| 1 — Interview | Conductor scans your codebase, asks 2–3 rounds of context-aware questions | 👤 answer 3–9 questions |
| 2 — Assembly | All roster agents scored for relevance; top 3–7 proposed | 👤 approve/adjust the roster — **token estimate shown here** |
| 3 — Deliberation | Round 1 positions → tension pairs → Round 2 challenges → Round 3 converge → synthesis. Runs as a background workflow; round texts stay on disk | 👤 approve the design (Decision Log + Tension Resolutions) |
| 4 — Planning | PRD, acceptance contract with BDD test stubs, task decomposition | 👤 scope review, then pick an action path |
| 5 — Action | Ship, export issues, team execution, handoff, or deep audit | depends on path |

Every phase writes artifacts to `.claude/council/sessions/<slug>-<timestamp>/` in your workspace — nothing lives only in a context window.

## Modes

| Command | Time | What you get |
|---|---|---|
| `/council --brainstorm "<idea>"` | ~30s | 3 perspectives + synthesis, inline only. Also available as top-level `/brainstorm` |
| `/council --quick "<idea>"` | ~3m | Skip interview; 3 agents, 1 round; `design-sketch.md` + task list |
| `/council "<idea>"` | ~30m | Full deliberation: design doc, PRD, acceptance contract, action paths |
| `/council --deep "<idea>"` | ~1h | Standard + mandatory multi-pass audit (Phase 5D) |
| `/council --auto "<idea>"` | ~10m | Full session, zero touchpoints, auto-approve everything. Idea must be in the arguments |
| `/council --guided "<idea>"` | ~30m+ | Approval gate at every phase, including a positions gate before agents debate |
| `/council --meet "<question>"` | ~15m | Discussion only — cross-examination protocol, `meeting-notes.md`, no plan |
| `/council --audit "<focus>"` | ~20m | Straight to the multi-pass codebase audit |

## Flags

- `--profile lean|balanced|max` — model spend per spawned agent (composable with any mode). See the [Cost guide](./COST-GUIDE.md) for which profile fits your billing model. Default: `balanced`.
- `--help` — full reference.

## Choosing a mode

- **Deciding whether to build at all** → `--brainstorm`, then `--meet` if it deserves a real debate.
- **You know what you want, need a sanity pass** → `--quick`.
- **Ambitious feature, multiple competing concerns** → default mode.
- **Security-, money-, or migration-critical** → `--deep` (or `--audit` on the existing system first).
- **Trust the council, hate clicking approve** → `--auto` (pair with `--profile lean` for cheap unattended runs).
- **Don't trust anyone, including the council** → `--guided`.

## Action paths (Phase 5)

After the PRD, the conductor offers:

| Path | What it does |
|---|---|
| **Ship** (recommended) | Export GitHub issues, then `/ship` implements, reviews, fixes, and merges PRs in dependency order |
| Export to GitHub Issues | One issue per user story with acceptance criteria, milestone, and dependency links |
| Team execution | Agents implement tasks directly (agent-teams flag preferred; degrades to sequential) |
| Ralf / Launch handoff | Hand the PRD to `/ralf` or `/launch` in a separate worktree |
| Deep audit | Multi-pass audit before committing to the plan |
| Review first | Read `design.md` / `prd.md` before deciding |

Sibling councils replace the engineering paths with their own outputs — see [COUNCILS.md](./COUNCILS.md).

## Session lifecycle

```
/council --resume               # resume the most recent active session
/council --resume <slug>        # fuzzy-match a specific session
/council --resume --pick        # interactive picker
/council --list [--all]        # sessions in this workspace (or every workspace)
/council --status               # quick workspace summary
/council --archive <slug>       # export the full deliberation to a GitHub issue
/council --lock <slug>          # re-create the acceptance-contract issue
/council --cleanup [--all]      # review and clear stale sessions
```

Sessions resume from the last completed phase — including mid-audit. The cost profile and orchestration backend are recorded in `session.md` and survive resume. Sessions go stale after 7 days (active) / 14 days (completed); `--cleanup` walks you through archiving or deleting them.

## Artifacts on disk

```
.claude/council/sessions/<slug>-<timestamp>/
├── session.md                  # metadata: phase, profile, backend, loaded skills
├── interview-summary.md        # + interview-transcript.md
├── assembly.md                 # roster scores and rationale
├── deliberation/round{1,2,3}/  # one file per agent per round
├── design.md                   # the synthesized design (or design-sketch.md in quick mode)
├── prd.md                      # + acceptance-contract.md, test-stubs/
├── plan.md                     # + issues.md after a GitHub export
└── audit/                      # deep-audit state, findings, and report
```

Design docs and plans are committed to git as they're produced, so the "why did we do it this way?" trail survives in history. `--archive` packages the entire deliberation — every position, every rebuttal — into a single GitHub issue.

## Skills

Each agent owns 2–4 department skills (e.g. `skeptic-threat-model`, `tuner-caching-strategy`). The conductor loads the 1–2 most relevant per agent during Assembly and inlines them into deliberation prompts, so positions follow a structured methodology instead of freestyling. You can also invoke any skill directly: `/agentic-council:<skill-name>`.

## Practical tips

- **Set your conductor model before a big session.** Interview, synthesis, and the PRD run on *your* `/model`. `/model opus` (or fable) before a standard/deep session is the single highest-leverage quality knob.
- **Watch the estimate at the Assembly gate.** It scales with roster size — trimming a marginal agent is the easiest cost cut.
- **Deliberation runs in the background.** Your session stays responsive; ask for progress or check `/workflows` while rounds run.
- **Use `--archive` before deleting anything.** The GitHub issue holds the full deliberation, so local cleanup is safe.

---

Next: [Councils](./COUNCILS.md) — the four rosters and when to convene each.
