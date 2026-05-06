# Positioning Charter

This document codifies the rules that protect `agentic-council`'s engineering positioning while allowing knowledge-work sibling councils (finance, people, revenue) to ship as additional slash commands inside the same plugin. It exists because v1.0.0's elevator pitch — *"Convene 20 agentic specialists on your hardest engineering problems"* — is the project's brand, and v1.1's expansion must not erode it.

**Architecture:** v1.1 ships one plugin (`agentic-council`) with multiple themed slash commands sharing one engine. Engineering remains the flagship command. Sibling councils are co-located in the same `commands/`, `agents/`, and `skills/` trees but are isolated by command, conductor, roster, and session directory.

## Frozen Surfaces (engineering plugin)

The following are immutable in v1.1 and any later release that does not explicitly bump the engineering plugin's major version:

1. **Roster.** `commands/council.md` agent table stays at 19 specialists + Steward. Net-new agents go to a sibling council, never `/council`.
2. **Conductor.** Steward (Platinum lens) remains the sole `/council` Maestro.
3. **Slash command.** `/council` and `/brainstorm` (its alias) keep their current behavior, modes, and theme variables.
4. **Elevator pitch.** The lead sentence of `.claude-plugin/plugin.json` and the `agentic-council` entry of `.claude-plugin/marketplace.json` stays verbatim: *"Convene 20 agentic specialists on your hardest engineering problems. Distinct perspectives, unified design, actionable plans, every decision tracked."* A trailing sentence may acknowledge sibling councils, but cannot replace or precede the engineering lead.
5. **README hierarchy.** README.md's first three sections (lead, "Why", agent overview) remain engineering-first. Sibling councils appear in a section that comes *after* this content, never before or interleaved.
6. **Engineering guardrails section.** `## Engineering guardrails` in README.md is preserved as-is.

## Sibling Council Rules

Every sibling council (`agentic-council-finance`, `agentic-council-people`, `agentic-council-revenue`, and any future siblings) must satisfy:

1. **Own slash command.** Never reuse `/council`. Use `/finance-council`, `/people-council`, `/revenue-council`, etc.
2. **Own conductor persona.** Distinct file, distinct color lens, distinct voice. Steward is reserved for engineering.
3. **Own session directory.** `.claude/<theme-id>/sessions/`. Never write into `.claude/council/`.
4. **Own roster.** Each council's themed command file declares its own `$ROSTER_TABLE`. The engine never assembles a session that mixes agents across rosters.
5. **Agent + skill prefixing.** Files in `agents/` and `skills/` use a council-specific prefix (`finance-`, `people-`, `revenue-`) so co-location in one plugin does not cause naming collisions with `council-` engineering files.
6. **Domain-noun-led command help.** Each themed command's help text leads with its domain ("finance", "people", "revenue") — never "engineering."
7. **Domain-internal modifier rules.** Anti-redundancy rules apply only between agents *within* the same council. No rules of the form "Finance Controller vs Architect."
8. **No engineering claims.** No copy in agent personas, skills, or commands implies the council handles engineering work.

## Cross-Council Interaction

Mixed-roster sessions are prohibited in v1.1. When a session surfaces a question outside its council's domain, the conductor emits a structured handoff block (see `references/cross-council-handoff.md`). The user runs the second council manually. This keeps the mental model clean and prevents agent fan-out from making any single council a generalist again.

## Marketplace-Level Copy

The marketplace top-level `description` field positions the suite as *"Multi-agent deliberation councils for knowledge work — engineering, finance, people, and revenue."* Engineering is named first, always. The umbrella description may evolve with later siblings, but engineering remains the lead noun.

## Charter Violations

A change violates this charter if it does any of:

- Adds a non-engineering agent to `/council`'s roster.
- Renames or rewords the engineering plugin's description.
- Promotes a sibling council above engineering content in README.md.
- Causes a sibling council's session to spawn agents from `/council`'s roster.
- Drops the domain-noun lead from a sibling description.

Charter violations require an explicit major-version bump and a documented decision in `CHANGELOG.md` justifying the repositioning.

## Review Cadence

This charter is reviewed at every minor-version release of `agentic-council` and at every new sibling-council launch. Reviewers: project maintainer + at least one user of each shipped council.
