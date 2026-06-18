[Docs home](./index.md) · [Usage](./USAGE.md) · [Councils](./COUNCILS.md) · [Cost guide](./COST-GUIDE.md) · **Orchestration** · [Architecture eval](./ARCHITECTURE-EVAL.md)

# Orchestration Backends

The council never requires a single runtime. At session start, a capability check resolves a **backend** per mode and degrades gracefully — it never hard-exits.

## The three backends

| Backend | What it is | Needs |
|---|---|---|
| **workflow** | Deliberation/audit runs as a background [dynamic workflow](https://code.claude.com/docs/en/workflows) — a script orchestrating subagents, with round texts kept on disk and out of your session's context | Claude Code ≥ 2.1.154, workflows enabled (default on Max/Team/Enterprise; `/config` toggle on Pro) |
| **teams** | Each council member is a live [agent-teams](https://code.claude.com/docs/en/agent-teams) teammate you can message directly | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (experimental) |
| **sequential** | The conductor drives the same rounds with plain agent calls | nothing |

All three produce identical on-disk artifacts. Sequential is slower and chattier; it exists so the plugin works everywhere.

## Which backend runs what

| Mode / phase | Preferred | Degrades to | Why |
|---|---|---|---|
| brainstorm, quick | inline agent calls | — | 3 one-shots; orchestration runtime is overhead |
| standard / auto / deep / guided deliberation | **workflow** | teams → sequential | The 3-round structure is deterministic — script-shaped. Background execution, in-session resume, hard token budget |
| `--meet` cross-examination | **teams** | workflow-style fixed phases → sequential | Direct agent-to-agent Q&A and live steering are what teams are for |
| Path A team execution | **teams** | sequential over the task dependency list | Shared task list, dependency unblocking, per-task plan approval |
| Deep audit (5D) / `--audit` | **workflow** | conductor-driven waves | Loop-until-convergence with a budget ceiling; replaces checkpoint/respawn machinery |

The resolved backend is printed when it differs from the preferred one, and recorded in `session.md` so `--resume` continues on the same path.

## Why deliberation moved to workflows (v1.2)

Anthropic's framing for choosing between primitives is *who holds the plan*: with subagents and teams, Claude decides turn by turn; with a workflow, the script decides. The council's deliberation — survey the codebase once for everyone, positions in parallel, pick tension pairs, paired rebuttals, converge, synthesize — is a fixed structure. Encoding it as a script bought:

- **No experimental flag** for the core flow — workflows are available on all paid plans.
- **Context hygiene** — a 7-agent, 3-round deliberation's full text never enters your session; only the structured Decision Log and Tension Resolutions come back.
- **Background execution** — your session stays responsive while rounds run; watch progress via `/workflows`.
- **Resumability** — completed agents return cached results if a run is interrupted.
- **A hard token budget** — the mode's budget (e.g. ~750K standard, ~2M audit) is a ceiling, not a suggestion.

The scripts ship in the plugin at `references/workflows/council-deliberation.template.js` and `council-audit.template.js`. The conductor writes a per-session copy with one marked line rewritten to a literal `INPUT` object (roster, idea, skill content, model routing) and runs that copy via the Workflow tool's `scriptPath`; the logic below the INPUT line is byte-for-byte identical, so the same scripts serve all four councils. Injecting literals replaced an earlier attempt to pass everything through the runtime `args` global, which proved unreliable for large nested payloads — a failed run now degrades to teams/sequential rather than improvising a substitute script.

What teams still do better — and why `--meet` and Path A prefer them: teammates are persistent (they remember their own Round 1 reasoning), they message *each other* directly, and you can jump into any teammate's session mid-flight (Shift+Down). Workflow agents compensate by re-reading their own prior round files from disk ("it is YOUR prior work"), which works because every round has always been persisted.

## Degradation matrix

| Mode | WF ✓ Teams ✓ | WF ✓ Teams ✗ | WF ✗ Teams ✓ | Neither |
|---|---|---|---|---|
| brainstorm / quick | inline | inline | inline | inline |
| standard / auto / deep / guided | workflow | workflow | teams | sequential |
| meeting | **teams** | workflow phases, no live steering | teams | sequential |
| Path A execution | **teams** | sequential | teams | sequential |
| audit / 5D | workflow | workflow | conductor waves | conductor waves |

## Troubleshooting

**`Orchestration: sequential` notice on every session** — neither runtime is available. Update Claude Code to ≥ 2.1.154; check Dynamic workflows isn't off in `/config` (or disabled by `CLAUDE_CODE_DISABLE_WORKFLOWS` / org managed settings); or export the teams flag. Sequential still works.

**`--meet` says live steering is unavailable** — that specific feature needs `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` exported in the shell that launched Claude Code (then restart).

**Deliberation workflow fails to launch** — the engine treats the failure as detection and re-runs on teams (if enabled) or sequential. If it keeps happening on a plan that should support workflows, check `claude --version` and `/config`.

**Teams quirks** (only relevant when the flag is on): `/resume` doesn't restore in-process teammates, shutdown can be slow, one team at a time. These now affect only `--meet` steering and Path A — not the core flow.

---

Next: [Architecture eval](./ARCHITECTURE-EVAL.md) — the design record behind these choices.
