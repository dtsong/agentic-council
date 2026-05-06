# Changelog

All notable changes to agentic-council are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Roadmap notes

- **v1.1 candidate:** expand the council with non-technical departments for product decisions where finance, HR, customer-success, and sales lenses matter. Dynamic assembly keeps engineering-only sessions unaffected. Design pass scheduled before implementation.

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

[Unreleased]: https://github.com/dtsong/agentic-council/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/dtsong/agentic-council/releases/tag/v1.0.1
[1.0.0]: https://github.com/dtsong/agentic-council/releases/tag/v1.0.0
