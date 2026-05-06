# Platforms

## v1.0.0: Claude Code only

The core deliberation engine relies on Claude Code's **agent teams** primitive (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) to spawn each council member as an isolated teammate with its own context window. As of this writing, no other coding agent ships an equivalent.

## Forward compatibility

We've made portability bets so that future support for other platforms is mostly a matter of writing a thin adapter:

- **SKILL.md frontmatter** uses only `name` and `description`, the same minimal set used by `anthropics/skills` and `anthropics/knowledge-work-plugins`. No platform-specific fields like `model:` or `allowed-tools:`.
- **Agent persona files** (`agents/council-*.md`) are plain markdown with a YAML header. The persona content is platform-neutral; only the spawning mechanism differs.
- **Engine prose** describes behaviors rather than calling tools by name where possible. References to Claude Code-only tools are isolated to a small set of integration points.

## Watch list

| Platform | Equivalent of agent teams | Status |
|---|---|---|
| Claude Cowork | partial (general-purpose Task tool, no named subagent types) | adapter plausible, see below |
| OpenAI Codex | not yet | watching |
| Google Gemini CLI | not yet | watching |
| Cursor agents | partial (single-agent) | not enough for council |

When parity arrives we'll add adapter directories alongside `commands/` (e.g., `codex/`, `gemini/`) without disturbing the Claude Code layout. Open an issue or PR if you want to experiment.

## Claude Cowork: why not yet

Cowork doesn't expose Claude Code's agent-teams primitive, so the registered-subagent-type pattern (`subagent_type: "Architect"`) doesn't work there. Forgoing agent teams trades away most of what makes the council valuable.

What agent teams gives us:

- **Isolated context window per council member.** A 9-agent, 3-round deliberation produces tens of thousands of tokens of accumulated debate. With agent teams, no single context has to hold all of it. Without isolation, the synthesizer has to read every position, every challenge, and every rebuttal in one window.
- **Persistent persona identity across rounds.** When the Architect responds in round 2, it's still the Architect. The persona is registered by name and survives the round boundary.
- **Parallel spawning.** Round 1 positions run concurrently across all seated agents.
- **Failure isolation.** If one agent's reasoning derails, it doesn't poison the parent context.

A Cowork port using the general-purpose Task tool would preserve context isolation and parallel spawning, but it loses the named-persona registry and the persistent-identity-across-rounds ergonomics. Every "Architect" call becomes a fresh general-purpose subagent that has to be re-briefed on its persona, the topic, and prior-round context every time. That's workable for a single round but gets brittle and expensive across three rounds with cross-references between rounds.

Sequential persona-switching in one context (no subagents) was considered and rejected: the parent context bloats after a few rounds and you lose the deliberation's main win.

**Decision:** v1 stays Claude Code only. We'd rather ship a tool that's powerful where it lives than a diluted version that runs everywhere. A Cowork variant gets revisited if and when Cowork ships a comparable agent-teams primitive, or if we find a structurally clean way to express persistent named personas through the Task tool. Open an issue if you want to drive that work.
