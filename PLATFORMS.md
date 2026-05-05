# Platforms

## v1.0.0 — Claude Code only

The core deliberation engine relies on Claude Code's **agent teams** primitive (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) to spawn each council member as an isolated teammate with its own context window. As of this writing, no other coding agent ships an equivalent.

## Forward compatibility

We've made portability bets so that future support for other platforms is mostly a matter of writing a thin adapter:

- **SKILL.md frontmatter** uses only `name` and `description` — the same minimal set used by `anthropics/skills` and `anthropics/knowledge-work-plugins`. No platform-specific fields like `model:` or `allowed-tools:`.
- **Agent persona files** (`agents/council-*.md`) are plain markdown with a YAML header. The persona content is platform-neutral; only the spawning mechanism differs.
- **Engine prose** describes behaviors rather than calling tools by name where possible. References to Claude Code-only tools are isolated to a small set of integration points.

## Watch list

| Platform | Equivalent of agent teams | Status |
|---|---|---|
| OpenAI Codex | not yet | watching |
| Google Gemini CLI | not yet | watching |
| Cursor agents | partial (single-agent) | not enough for council |

When parity arrives we'll add adapter directories alongside `commands/` (e.g., `codex/`, `gemini/`) without disturbing the Claude Code layout. Open an issue or PR if you want to experiment.
