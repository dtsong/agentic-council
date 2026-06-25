# Changelog

All notable changes to agentic-council are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Slash commands now register.** `plugin.json` declares a `commands` array (`council`, `brainstorm`, `deepen`, `handover`, `ship`, `finance-council`, `people-council`, `revenue-council`). Claude Code 2.1.x only registers a plugin's `commands/*.md` as invokable slash commands when `plugin.json` lists them; without it every command file was absorbed as a skill, so bare `/council` failed with "Unknown command" and only `/agentic-council:council` existed. `_council-engine.md` is an include (no frontmatter) and is intentionally excluded.

## [1.2.0] - 2026-06-10

### Added
- **Cost profiles** — `--profile lean|balanced|max` on every council command, with a per-theme `DEFAULT_PROFILE` variable. Models are routed by spawn site: lean runs positions/converge on Sonnet with fresh Opus one-shots for Round 2 challenges; max upgrades challenges to Fable. Profile persists in `session.md`/`index.json` and survives `--resume`.
- **Cost transparency** — the roster-approval gate now shows an estimated token range (mode × profile, scaled by agent count) and echoes the conductor's current `/model`. Quick/auto modes print a non-blocking one-liner.
- **Workflow-backed deliberation** — standard/auto/deep/guided deliberation runs as a background dynamic workflow (`references/workflows/council-deliberation.template.js`): parallel positions, a tension-pairing judge, paired challenges, convergence, and synthesis, with round texts kept out of the conductor's context and only the structured Decision Log/Tension Resolutions returned. Guided mode splits into two invocations at the positions gate.
- **Workflow-backed deep audit** — Phase 5D/`--audit` runs as `references/workflows/council-audit.template.js`: zone waves, gap-detection judge between passes, loop-until-convergence with a hard token budget; replaces the conductor checkpoint/respawn machinery on this path. On-disk audit artifacts unchanged.
- **`docs/ARCHITECTURE-EVAL.md`** — the design record: v1.1 strengths/gaps, the enterprise vs Max cost personas, and the per-phase workflows-vs-teams rationale.
- **README Cost guide** — profile table, token estimates, and persona guidance (API-billed lean vs Max-plan max).
- `scripts/validate.py`: agent `model` frontmatter must be a tier alias or `inherit` (pinned `claude-*` IDs are errors); workflow templates referenced by the engine must exist and carry `export const meta`.

### Changed
- **The experimental agent-teams flag is no longer required.** The engine's hard-exit preflight is replaced by an orchestration capability check that resolves a backend per mode (workflow → teams → sequential) and never exits. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is now optional, unlocking `--meet` live steering and Path A team execution; both degrade gracefully without it.
- All 38 agent files: `model: "claude-opus-4-6"` (two generations stale) → `model: inherit`. The engine passes an explicit tier alias on every spawn per the routing table, so agents track the latest models and respect the session profile.
- Quick mode runs as inline parallel Task calls (no team, no workflow). Brainstorm's hardcoded sonnet now references the routing table (same value).
- Mode table gains Backend and Budget columns; INSTALL.md requirements lead with Claude Code ≥ 2.1.154 + dynamic workflows; README fixes the 5–9 vs 3–7 agent-count inconsistency.
- Cleanup only sends teammate shutdown/`TeamDelete` on the teams backend.

### Unchanged (per positioning charter)
- `/council`'s 19 specialists + Steward roster, all agent personas, all skills.
- Session directory layout, index/registry schemas, resume slugs, archive format. Pre-v1.2 sessions resume as `balanced` profile with backend re-detected.

## [1.1.1] - 2026-05-06

### Changed
- `plugin.json` and `marketplace.json` now carry an explicit `version` field. Without it, every commit on `main` would register as a new "version" for installed users. With explicit versioning, updates land only when this field bumps. Required ahead of an Anthropic plugin directory submission.
- `scripts/validate.py` extended to recognize `finance-`, `people-`, and `revenue-` prefixes for skills and agents shipped under sibling councils. Engineering-only roster checks remain in place for `/council`. v1.1.0's CI broke against the v1.0.x validator; this restores green CI.
- `scripts/validate.py` now enforces that `plugin.json` and `marketplace.json` carry matching, semver-shaped `version` fields. Catches the gap that prompted this patch from regressing.

### Removed
- Empty placeholder directory `skills/people-job-description/` (scaffolded in v1.1.0 but no SKILL.md was ever shipped — actual people skills are tracked for v1.2).

## [1.1.0] - 2026-05-06

### Added
- **Sibling councils** for non-engineering knowledge work, each with its own slash command, conductor, roster, and session directory:
  - `/finance-council` — Comptroller conducting Controller, Tax, FP&A, Treasurer, Auditor, Capital, RegRep (7 specialists).
  - `/people-council` — Chair conducting Talent, PeoplePartner, TotalRewards, LearnDev, DEI, PeopleOps (6 specialists).
  - `/revenue-council` — Quartermaster conducting AE and SDR (2 specialists; 5 more tracked for v1.2).
- **6 finance skills:** `finance-reconciliation`, `finance-journal-entries`, `finance-close-checklist`, `finance-tax-research`, `finance-controls-audit`, `finance-variance-analysis`. People and revenue skills tracked for v1.2.
- **`references/positioning-charter.md`** codifying frozen surfaces (engineering elevator pitch, `/council` roster, Steward as sole Maestro) and sibling-council isolation rules.
- **`references/cross-council-handoff.md`** defining the structured handoff protocol when a session surfaces a question outside its council's domain. Mixed-roster sessions remain prohibited.
- Engine variable `$ACTION_PATHS` so themes can declare non-engineering Phase 5 outputs (memos, JE packages, account plans) without disturbing Path A team execution.
- Finance council departments added to `references/department-index.md`.

### Changed
- `plugin.json` and `marketplace.json` descriptions append a sibling-council acknowledgment after the unchanged engineering elevator pitch.

### Unchanged (per positioning charter)
- `/council`'s 19 specialists + Steward roster.
- `/council` and `/brainstorm` behavior, modes, and theme variables.
- README hierarchy (engineering-first lead, "Why", agent overview).

## [1.0.1] - 2026-05-05

### Added
- `scout-enterprise-search-strategy` skill for structured internal-knowledge searches across wikis, ADRs, postmortems, ticket systems, and chat archives. Brings Scout to 4 skills (60 total bundled skills).
- `PRIVACY.md` documenting the no-telemetry, no-network-egress posture.
- GitHub repo topics, homepage, and description aligned with the canonical hook.

### Changed
- `plugin.json` and `marketplace.json` descriptions standardized on the marketplace-ready hook: "Convene 20 agentic specialists on your hardest engineering problems. Distinct perspectives, unified design, actionable plans, every decision tracked."
- README rewritten to lead with the hook and surface persistence as a top-level value prop. Added "Example sessions" with three concrete walkthroughs.
- Em-dashes swept from all user-facing docs for consistent prose.
- `PLATFORMS.md` clarified that v1 is Claude Code only, with an honest assessment of why a Cowork port is not a clean adapter.

## [1.0.0] - 2026-05-04

### Added
- Initial release of agentic-council as a standalone Claude Code plugin.
- 20 council agents (`council-*`) covering systems, product, design, risk, and security perspectives.
- 59 department-bundled skills (4 architect, 3 skeptic, 4 advocate, 3 craftsman, 3 scout, 3 strategist, 4 operator, 3 chronicler, 3 guardian, 3 tuner, 3 alchemist, 3 pathfinder, 3 artisan, 3 herald, 3 sentinel, 3 oracle, 3 cipher, 3 warden, 2 prover).
- 6 slash commands: `/council`, `/brainstorm`, `/ship`, `/deepen`, `/handover`, plus the shared `_council-engine`.
- Self-hosted single-plugin marketplace at `.claude-plugin/marketplace.json`.
- Apache-2.0 licensed.
- GitHub Actions CI running `scripts/validate.py` and `claude plugin validate` on every push and pull request.
- Preflight check in the deliberation engine that detects missing `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and exits with a friendly install message.

### Held back from v1.0.0
- **Forge** for microarchitecture, RTL security, physical-design security
- **Foundry** for chip design flow, verification methodology, SoC integration
- **Accountant** for accounting, tax, audit

These will ship in a future `agentic-council-ee` spin-off plugin.

[Unreleased]: https://github.com/dtsong/agentic-council/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/dtsong/agentic-council/releases/tag/v1.1.1
[1.1.0]: https://github.com/dtsong/agentic-council/releases/tag/v1.1.0
[1.0.1]: https://github.com/dtsong/agentic-council/releases/tag/v1.0.1
[1.0.0]: https://github.com/dtsong/agentic-council/releases/tag/v1.0.0
