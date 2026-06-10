[Docs home](./index.md) · [Usage](./USAGE.md) · **Councils** · [Cost guide](./COST-GUIDE.md) · [Orchestration](./ORCHESTRATION.md) · [Architecture eval](./ARCHITECTURE-EVAL.md)

# The Four Councils

One deliberation engine, four domains. Each council has its own slash command, conductor persona, specialist roster, and session directory — and they never mix (mixed-roster sessions are prohibited by the [positioning charter](https://github.com/dtsong/agentic-council/blob/main/references/positioning-charter.md)).

| Council | Command | Conductor | Specialists | Cap | Decisions it's for |
|---|---|---|---|---|---|
| Engineering | `/council` | **Steward** (Platinum) | 19 | 7 | Features, architecture, migrations, audits |
| Finance | `/finance-council` | **Comptroller** (Verdigris) | 7 | 5 | Close, tax, treasury, capital, disclosure |
| People | `/people-council` | **Chair** (Linen) | 6 | 5 | Hiring, comp, ER, org design, compliance |
| Revenue | `/revenue-council` | **Quartermaster** (Cobalt) | 7 | 5 | Deals, expansion, churn, pipeline, partners |

All four share the same session flow (interview → assembly → 3-round deliberation → synthesis → planning), the same `--profile` cost controls, and the same session-management commands (`--list`, `--resume`, `--archive`, …). The conductor is a persona the main session adopts — it facilitates and synthesizes but never votes.

## Engineering — `/council`

The flagship. 19 specialists; the Architect is always seated, and Advocate, Skeptic, Guardian, and Tuner get bonus weight in scoring.

**Engineering & systems:** Architect (Blue — systems, APIs, data models) · Craftsman (Purple — testing, code quality) · Operator (Orange — DevOps, infra) · Tuner (Amber — performance, scale) · Alchemist (Indigo — data/ML) · Sentinel (Titanium — IoT, embedded) · Pathfinder (Coral — mobile, cross-platform)

**Product & design:** Strategist (Gold — scope, MVP) · Advocate (Green — UX, accessibility) · Artisan (Rose — visual design) · Herald (Bronze — growth, monetization) · Scout (Cyan — research, precedent) · Chronicler (Ivory — documentation)

**Risk & integrity:** Skeptic (Red — devil's advocate) · Guardian (Silver — compliance, privacy) · Cipher (Obsidian — cryptography, PQC) · Warden (Slate — kernel security, isolation) · Prover (Pearl — formal methods) · Oracle (Violet — AI/LLM integration, RAG)

Each specialist owns 2–4 department skills (59 engineering skills total — `architect-schema-design`, `skeptic-threat-model`, `oracle-rag-architecture`, …). Action paths: Ship, GitHub issues export, team execution, Ralf/Launch handoff, deep audit.

## Finance — `/finance-council`

Intake: *"What's the financial decision?"*

| Specialist | Color | Lens |
|---|---|---|
| Controller | Forest | GAAP/IFRS, journals, reconciliation, monthly close |
| Tax | Mustard | Federal/state/international tax, transfer pricing |
| FP&A | Sky | Forecasting, variance analysis, scenario modeling |
| Treasurer | Bronze | Cash, liquidity, working capital, FX |
| Auditor | Onyx | Internal controls, SOX, audit evidence |
| Capital | Indigo | Capital allocation, M&A, investor relations |
| RegRep | Slate | SEC filings, regulatory reporting, disclosures |

Theme action paths: **Path G** — finance memo + draft journal-entries worksheet ready for GL import; **Path H** — FP&A handoff package (forecast revisions + variance commentary). Six skills shipped (`finance-reconciliation`, `finance-journal-entries`, `finance-close-checklist`, `finance-variance-analysis`, `finance-tax-research`, `finance-controls-audit`); eight more tracked.

## People — `/people-council`

Intake: *"What's the people decision?"*

| Specialist | Color | Lens |
|---|---|---|
| Talent | Coral | Recruiting, interview-loop design, offer mechanics |
| PeoplePartner | Sage | Employee relations, performance, manager coaching |
| TotalRewards | Gold | Comp bands, equity, benefits, geo differentials |
| LearnDev | Teal | L&D, career frameworks, skills development |
| DEI | Plum | Belonging, accessibility, equitable practice design |
| PeopleOps | Slate | HRIS, payroll, employment-law compliance, leave |

Theme action paths: **Path I** — job-description package (role spec, success criteria, comp band reference, interview rubric); **Path J** — employment-decision memo with jurisdiction-specific considerations (flags external legal/finance sign-off rather than assuming facilitation closes it). One skill shipped (`people-job-description`); twelve more tracked.

## Revenue — `/revenue-council`

Intake: *"What's the revenue decision?"*

| Specialist | Color | Lens |
|---|---|---|
| AE | Crimson | Deal mechanics, MEDDPICC, negotiation |
| SDR | Amber | Outbound prospecting, qualification |
| SE | Blue | Technical sales, demos, POC design |
| CSM | Green | Adoption, expansion, churn signals, renewals |
| Support | Cyan | Ticket triage, escalation, SLA |
| RevOps | Indigo | Pipeline, forecast methodology, territory design |
| Partnerships | Bronze | Channel, alliances, ecosystem co-sell |

The seven cleave into pre-sale / post-sale / system tracks — rarely do all need to speak, hence the 5-agent cap. Theme action paths: **Path K** — account-plan package; **Path L** — deal-room brief for executive engagement (MEDDPICC scoring, asks, risks); **Path M** — QBR deck for joint CSM/AE presentation. One skill shipped (`revenue-account-plan`); thirteen more tracked.

## Cross-council handoffs

When a session surfaces a question outside its council's domain — an engineering design with a revenue-recognition implication, a hiring plan with a budget question — the conductor does **not** seat a foreign specialist. It emits a structured handoff block naming the receiving council, the question, and the context to carry over; you then open a session there. See [`references/cross-council-handoff.md`](https://github.com/dtsong/agentic-council/blob/main/references/cross-council-handoff.md) for the block format.

Session data is isolated per council: `.claude/council/`, `.claude/finance-council/`, `.claude/people-council/`, `.claude/revenue-council/`.

---

Next: [Cost guide](./COST-GUIDE.md) — profiles, token estimates, and which to pick for your billing model.
