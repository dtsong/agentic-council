# Department Index

Routing table that maps each council department to its bundled skills. The shared deliberation engine reads this once per session during Phase 2.5 ("Skill Loading") to learn which skill keys belong to which department.

Each entry: `<department>` — list of `<dept>-<skill>` keys that resolve to `${CLAUDE_PLUGIN_ROOT}/skills/<dept>-<skill>/SKILL.md`.

> **NOTE:** This file is populated in Phase 4 of plugin migration alongside the actual `skills/` flatten. Below is the v1.0.0 target shape.

## architect

- `architect-codebase-context` — "Tech chief": infrastructure analysis + context briefing for downstream agents
- `architect-schema-design` — Database schema design with normalization trade-offs
- `architect-api-design` — REST/RPC endpoint contracts, versioning, error shapes
- `architect-distributed-patterns` — Event-driven, request/response, message queues

## skeptic

- `skeptic-threat-model` — STRIDE-based threat analysis
- `skeptic-failure-mode-analysis` — Failure scenarios + mitigations
- `skeptic-edge-case-enumeration` — Systematic edge case discovery

## advocate

- `advocate-journey-mapping` — User journey with states + emotions
- `advocate-interaction-design` — Component specs with all states
- `advocate-i18n-review` — Internationalization readiness review
- `advocate-a11y-audit` — WCAG 2.2 AA accessibility audit

## craftsman

- `craftsman-testing-strategy` — Test plan with coverage targets
- `craftsman-pattern-analysis` — Codebase pattern audit + conventions
- `craftsman-e2e-testing` — E2E test design + visual regression

## scout

- `scout-library-evaluation` — Structured library scoring + comparison
- `scout-competitive-analysis` — Feature comparison matrix
- `scout-technology-radar` — Technology maturity assessment

## strategist

- `strategist-mvp-scoping` — MoSCoW prioritization + value-effort matrix
- `strategist-impact-estimation` — RICE scoring for feature prioritization
- `strategist-analytics-design` — Telemetry events + A/B test instrumentation

## operator

- `operator-deployment-plan` — Deployment strategy + rollback procedures
- `operator-observability-design` — Monitoring, alerting, logging strategy
- `operator-cost-analysis` — Infrastructure cost modeling
- `operator-finops-analysis` — Cloud cost attribution + unit economics

## chronicler

- `chronicler-documentation-plan` — Documentation architecture + audiences
- `chronicler-adr-template` — Architecture Decision Record creation
- `chronicler-changelog-design` — Changelog + migration guide design

## guardian

- `guardian-compliance-review` — GDPR/privacy compliance review
- `guardian-data-classification` — Data sensitivity classification
- `guardian-audit-trail-design` — Audit logging design

## tuner

- `tuner-performance-audit` — Bottleneck identification + profiling
- `tuner-caching-strategy` — Cache hierarchy design
- `tuner-load-modeling` — Capacity planning + benchmarks

## alchemist

- `alchemist-schema-evaluation` — Data warehouse schema design
- `alchemist-pipeline-design` — ETL/ELT pipeline architecture
- `alchemist-ml-workflow` — ML workflow + experiment tracking

## pathfinder

- `pathfinder-platform-audit` — Platform guideline compliance
- `pathfinder-navigation-design` — Mobile navigation + deep linking
- `pathfinder-device-integration` — Hardware APIs, sensors, biometrics

## artisan

- `artisan-visual-audit` — Structured visual design critique
- `artisan-design-system-architecture` — Token hierarchy + theming
- `artisan-motion-design` — Animation principles + reduced-motion

## herald

- `herald-growth-engineering` — Onboarding funnels + referral systems
- `herald-monetization-design` — Pricing tiers + paywall architecture
- `herald-messaging-strategy` — Product copy + value propositions

## sentinel

- `sentinel-embedded-architecture` — Firmware design + RTOS patterns
- `sentinel-protocol-design` — BLE/MQTT/Matter protocol selection
- `sentinel-fleet-management` — Device provisioning + OTA updates

## oracle

- `oracle-prompt-engineering` — System prompts + structured output
- `oracle-rag-architecture` — Chunking + embeddings + vector DB
- `oracle-ai-evaluation` — Golden datasets + hallucination detection

## cipher

- `cipher-crypto-review` — Cryptographic implementation review
- `cipher-protocol-analysis` — Protocol state machine security analysis
- `cipher-pqc-readiness` — Post-quantum cryptography readiness

## warden

- `warden-isolation-review` — Isolation boundary analysis + bypass testing
- `warden-kernel-hardening` — Kernel security configuration audit
- `warden-hw-sw-boundary` — HW/SW security interface review

## prover

- `prover-formal-spec` — TLA+ specification + model checking
- `prover-invariant-analysis` — Security invariant identification

## Held back from v1.0.0

The following departments are parked for an `agentic-council-ee` spin-off plugin and are NOT bundled. The engine should ignore selections targeting these:

- **forge** — microarchitecture, RTL security, physical design security, hw-security signoff
- **foundry** — chip design flow, verification methodology, SoC integration
- **accountant** — accounting, tax, audit (no skills implemented yet)

If the conductor's agent assembly targets one of the held-back agents, log a note and substitute the closest available perspective (e.g., Cipher for hardware-security-leaning topics).
