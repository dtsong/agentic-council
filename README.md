# agentic-council

A Claude Code plugin that turns any "big idea" into an actionable build plan through structured multi-agent deliberation.

`/council` interviews you, assembles a dynamic panel of 20 specialist agents (Architect, Skeptic, Strategist, Operator, Tuner, Guardian, …), runs them through three rounds of position → challenge → synthesis, and emits a design + implementation plan ready for execution.

## Install

```
/plugin marketplace add https://github.com/dtsong/agentic-council
/plugin install agentic-council
```

Then enable the agent-teams runtime that the council requires:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

See [INSTALL.md](./INSTALL.md) for the full setup including troubleshooting.

## Commands shipped

| Command | What it does |
|---|---|
| `/council "<idea>"` | Full workflow — interview, assembly, 3-round deliberation, design, plan |
| `/council --brainstorm "<idea>"` | 30-second gut check from 3 agents |
| `/council --quick "<idea>"` | Skip interview, single round |
| `/council --deep "<idea>"` | Full council + mandatory deep audit |
| `/council --meet "<question>"` | Discussion only — no action plan |
| `/council --audit "<area>"` | Direct codebase audit |
| `/brainstorm "<idea>"` | Top-level alias for `/council --brainstorm` |
| `/ship` | Post-council pipeline: implement → review → fix → PR |
| `/deepen` | Architecture review — find shallow modules |
| `/handover` | Save session knowledge to a handover doc |

Run `/council --help` for the complete reference, including `--resume`, `--list`, `--archive`, `--cleanup`.

## The Council (20 agents in v1.0.0)

**Engineering & systems**
- **Architect** — system design, data models, APIs
- **Craftsman** — testing strategy, code quality, patterns
- **Operator** — DevOps, deployment, infrastructure
- **Tuner** — performance, scalability, optimization
- **Alchemist** — data engineering, ML workflows
- **Sentinel** — IoT, embedded, edge protocols
- **Pathfinder** — mobile, cross-platform, native

**Product & design**
- **Strategist** — business value, scope, MVP
- **Advocate** — UX, product thinking, accessibility
- **Artisan** — visual design, design systems, motion
- **Herald** — growth, monetization, onboarding
- **Scout** — research, precedent, external knowledge
- **Chronicler** — documentation, knowledge architecture

**Risk & integrity**
- **Skeptic** — risk, devil's advocate, edge cases
- **Guardian** — compliance, governance, privacy
- **Cipher** — cryptographic engineering, protocol security
- **Warden** — OS kernel security, isolation
- **Prover** — formal methods, mathematical verification
- **Oracle** — AI/LLM integration, RAG, prompt engineering

**Maestro**
- **Steward** — facilitator, synthesizer (does not vote)

> **Held back for an `agentic-council-ee` spin-off:** Forge, Foundry, Accountant. Open an issue if you'd like that variant accelerated.

## How it works

1. **Phase 0 — Intake.** "What's the big idea?"
2. **Phase 1 — Interview.** Steward asks 3–7 questions to disambiguate scope, constraints, success.
3. **Phase 2 — Assembly.** Steward picks 5–9 council members based on the idea (Architect is always seated; Advocate, Skeptic, Guardian, Tuner get +2 mandatory bonuses for relevant domains).
4. **Phase 3 — Deliberation.** Three rounds: Position → Challenge → Synthesis. Tension pairs are surfaced organically (e.g., Skeptic vs Strategist, Operator vs Tuner).
5. **Phase 4 — Output.** Design doc, implementation plan, and an optional PRD ready to hand to `/ship` or `/looper`.

Session artifacts live in your workspace at `.claude/council/sessions/<slug>/` — never inside the plugin.

## Skills bundled (59)

Each council agent is paired with 2–4 first-class skills (e.g., `architect-schema-design`, `skeptic-threat-model`, `tuner-caching-strategy`, `guardian-compliance-review`). They're invokable directly as `/agentic-council:<skill-name>` or summoned by their parent agent during deliberation.

## License

Apache-2.0 — see [LICENSE](./LICENSE).

## Cross-platform note

v1.0.0 is Claude Code only — agent teams is currently a Claude Code primitive. SKILL.md and agent persona files use minimal, portable frontmatter to ease future Codex/Gemini support. See [PLATFORMS.md](./PLATFORMS.md).
