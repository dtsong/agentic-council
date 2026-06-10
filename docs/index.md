# agentic-council Documentation

> Convene agentic specialists on your hardest problems. Distinct perspectives, unified design, actionable plans, every decision tracked.

Hosted docs: **https://dtsong.github.io/agentic-council/** · Source: [github.com/dtsong/agentic-council](https://github.com/dtsong/agentic-council)

## Start here

```
/plugin marketplace add https://github.com/dtsong/agentic-council
/plugin install agentic-council
/council --brainstorm "Should we migrate from Node to Bun?"
```

Full setup (requirements, optional agent-teams flag, troubleshooting): [Install guide](https://github.com/dtsong/agentic-council/blob/main/INSTALL.md).

## Guides

| Guide | What's in it |
|---|---|
| **[Usage](./USAGE.md)** | Session anatomy, all 8 modes, flags, action paths, session lifecycle, artifacts on disk, practical tips |
| **[Councils](./COUNCILS.md)** | The four councils — engineering, finance, people, revenue — rosters, conductors, theme outputs, cross-council handoffs |
| **[Cost guide](./COST-GUIDE.md)** | `--profile lean\|balanced\|max`, token estimates, and playbooks for API-billed vs Claude Max users |
| **[Orchestration](./ORCHESTRATION.md)** | The workflow / teams / sequential backends, what degrades when, troubleshooting |
| **[Architecture eval](./ARCHITECTURE-EVAL.md)** | The design record: v1.1 strengths and gaps, the workflows-vs-teams rationale, deferred work |

## Quick answers

- **What does a session cost?** ~10–15K tokens for a brainstorm, ~120–180K for a full standard session at the default profile. The engine shows an estimate before anything spawns. → [Cost guide](./COST-GUIDE.md)
- **Do I need the experimental agent-teams flag?** No (since v1.2). It's optional — it unlocks live panel steering in `--meet` and team-based execution. → [Orchestration](./ORCHESTRATION.md)
- **Where do my sessions live?** `.claude/<council>/sessions/<slug>/` in your workspace, one artifact per phase, committed to git. → [Usage § Artifacts](./USAGE.md#artifacts-on-disk)
- **Can I resume a session from last week?** Yes — `/council --resume` (or `--list` to find it). Profile and backend survive resume. → [Usage § Session lifecycle](./USAGE.md#session-lifecycle)
- **Which council do I want?** Engineering for anything you'd build; finance/people/revenue for those domains' decisions. They never mix. → [Councils](./COUNCILS.md)

## Reference

- [Install](https://github.com/dtsong/agentic-council/blob/main/INSTALL.md) · [Contributing](https://github.com/dtsong/agentic-council/blob/main/CONTRIBUTING.md) · [Changelog](https://github.com/dtsong/agentic-council/blob/main/CHANGELOG.md) · [Platforms](https://github.com/dtsong/agentic-council/blob/main/PLATFORMS.md)
- Engine internals: [`commands/_council-engine.md`](https://github.com/dtsong/agentic-council/blob/main/commands/_council-engine.md) — every phase, gate, and fallback is specified there
