# agentic-council

> A 20-agent council that interviews, debates, and produces an actionable build plan for your hardest engineering decisions.

Single-agent coding assistants give one perspective. Real engineering decisions need many: an architect reasoning about boundaries, a skeptic naming what could break, a tuner asking about cost at scale, a guardian flagging the privacy footprint. **agentic-council** stages that conversation. Twenty specialist personas convene around your prompt, post positions, debate, and converge on a build plan you can ship.

## Install

```
/plugin marketplace add https://github.com/dtsong/agentic-council
/plugin install agentic-council
```

Then enable the agent-teams runtime that the council requires:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

See [INSTALL.md](./INSTALL.md) for the full setup including troubleshooting. The `/council` engine has a preflight check that prints this instruction if the flag is missing.

## Quick start

```bash
/council --brainstorm "Should we migrate from Node to Bun?"
/council --quick      "Add a tournament coach feature"
/council --meet       "Re-architect the billing stack"
/council --audit      "Audit our authentication stack"
```

Each mode scales differently:

| Mode | Agents | Rounds | Use when |
|---|---|---|---|
| `--brainstorm` | 3 | 1 | Gut check, pre-decision ideation |
| `--quick` | 5 | 1 | You know roughly what you want |
| (default) | 5 to 9 | 3 | Ambitious feature, full deliberation |
| `--deep` | 5 to 9 | 3 + audit | Max rigor, ~1 hour |
| `--meet` | 5 to 9 | 3 | Discussion only, no plan |
| `--audit` | 4 to 6 | 1 | Adversarial codebase review |

## How it works

1. **Intake.** "What's the big idea?"
2. **Interview.** Steward asks 3 to 7 questions to disambiguate scope, constraints, and success.
3. **Assembly.** Steward picks 5 to 9 council members based on the topic. Architect is always seated; Advocate, Skeptic, Guardian, and Tuner get bonus weight for relevant domains.
4. **Deliberation.** Three rounds: Position, Challenge, Synthesis. Tension pairs surface organically (Skeptic vs Strategist, Operator vs Tuner).
5. **Output.** Design doc, implementation plan, and an optional PRD ready to hand to `/ship`.

## Persistence and context handoff

Every session writes to `.claude/council/sessions/<slug>/` in your workspace, capturing each phase as a discrete artifact:

```
.claude/council/sessions/<slug>/
├── interview.md         # Phase 1 questions and answers
├── assembly.md          # Phase 2 roster and rationale
├── deliberation/
│   ├── round-1.md       # Each agent's opening position
│   ├── round-2.md       # Cross-examination and rebuttals
│   └── round-3.md       # Synthesis
├── design.md            # Phase 4 design doc
└── plan.md              # Phase 4 build plan
```

This is the key to the council pattern. Subsequent agents read prior rounds from disk so context flows agent-to-agent without bloating the parent context window. A 9-agent, 3-round deliberation that would blow past any single context window stays lean because each agent only loads what it needs.

Session lifecycle commands:

| Command | Purpose |
|---|---|
| `/council --resume` | Resume the most recent active session |
| `/council --resume <slug>` | Resume a specific session |
| `/council --list [--all]` | List sessions in this workspace (or all) |
| `/council --status` | Quick workspace summary |
| `/council --archive <slug>` | Export a session to a GitHub issue |
| `/council --cleanup` | Review and remove stale sessions |

A cross-workspace registry at `~/.claude/council/` tracks usage across projects, and `/handover` exports session knowledge for the next Claude conversation to pick up cold.

Plugin assets are read-only at `${CLAUDE_PLUGIN_ROOT}`. Session and registry data always lives in your workspace and home directory.

## Commands shipped

| Command | What it does |
|---|---|
| `/council "<idea>"` | Full workflow: interview, assembly, 3-round deliberation, design, plan |
| `/council --brainstorm "<idea>"` | 30-second gut check from 3 agents |
| `/council --quick "<idea>"` | Skip interview, single round |
| `/council --deep "<idea>"` | Full council plus mandatory deep audit |
| `/council --meet "<question>"` | Discussion only, no action plan |
| `/council --audit "<area>"` | Direct codebase audit |
| `/brainstorm "<idea>"` | Top-level alias for `/council --brainstorm` |
| `/ship` | Post-council pipeline: implement, review, fix, PR |
| `/deepen` | Architecture review, find shallow modules |
| `/handover` | Save session knowledge to a handover doc |

Run `/council --help` for the complete reference.

## The council

**Engineering and systems**
- **Architect** for system design, data models, APIs
- **Craftsman** for testing strategy, code quality, patterns
- **Operator** for DevOps, deployment, infrastructure
- **Tuner** for performance, scalability, optimization
- **Alchemist** for data engineering, ML workflows
- **Sentinel** for IoT, embedded, edge protocols
- **Pathfinder** for mobile, cross-platform, native

**Product and design**
- **Strategist** for business value, scope, MVP
- **Advocate** for UX, product thinking, accessibility
- **Artisan** for visual design, design systems, motion
- **Herald** for growth, monetization, onboarding
- **Scout** for research, precedent, external knowledge
- **Chronicler** for documentation, knowledge architecture

**Risk and integrity**
- **Skeptic** for risk, devil's advocate, edge cases
- **Guardian** for compliance, governance, privacy
- **Cipher** for cryptographic engineering, protocol security
- **Warden** for OS kernel security, isolation
- **Prover** for formal methods, mathematical verification
- **Oracle** for AI/LLM integration, RAG, prompt engineering

**Maestro**
- **Steward** facilitator and synthesizer (does not vote)

## Skills bundled (59)

Each council agent is paired with 2 to 4 first-class skills (e.g., `architect-schema-design`, `skeptic-threat-model`, `tuner-caching-strategy`, `guardian-compliance-review`). They load on demand during deliberation, or you can invoke them directly as `/agentic-council:<skill-name>`.

## Engineering guardrails

- `scripts/validate.py` runs 7 structural checks (manifest parsing, frontmatter completeness, roster cross-references, no hardcoded user paths, no held-back-dept leakage).
- GitHub Actions CI runs the validator and `claude plugin validate` on every push and PR.
- No telemetry, no network calls outside the agent runtime itself.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full local dev workflow.

## License

Apache-2.0. See [LICENSE](./LICENSE).

## Cross-platform note

v1.0.0 is Claude Code only because agent teams is currently a Claude Code primitive. SKILL.md and agent persona files use minimal, portable frontmatter to ease future Codex and Gemini support. See [PLATFORMS.md](./PLATFORMS.md).
