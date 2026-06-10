# Contributing to agentic-council

## Local development

Clone the repo and load the plugin in a throwaway workspace:

```bash
git clone https://github.com/dtsong/agentic-council
cd /tmp && mkdir test-council && cd test-council
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1   # optional — only for --meet steering / Path A teams
claude --plugin-dir /path/to/agentic-council
```

Inside Claude:

```
/agentic-council:council --brainstorm "Should we migrate to Bun?"
```

## Validating before committing

Two layers of checks run in CI; run them locally first.

**1. Structural integrity (Python)**

```bash
pip install pyyaml
python3 scripts/validate.py
```

This checks:

- Both `.claude-plugin/*.json` manifests parse and use the right names
- Every `skills/<name>/SKILL.md` has `name` + `description` frontmatter
- Every `agents/council-*.md` has frontmatter and matches the roster table in `commands/council.md`
- Agent `model` frontmatter is a tier alias (`inherit`, `sonnet`, `opus`, `haiku`, `fable`) or omitted — pinned `claude-*` IDs are rejected (they go stale)
- Workflow templates referenced by the engine exist under `references/workflows/` and carry an `export const meta` block
- `references/department-index.md` is in sync with the actual `skills/` tree
- No held-back agents (`forge`, `foundry`, `accountant`) leak into the v1.0.0 bundle
- No hardcoded user paths (`/Users/...`, `/home/...`)
- No stale `.claude/skills/council/` or `DEPARTMENT.md` references in plugin assets

**2. Claude Code's own validator**

```bash
claude plugin validate .
```

This checks the marketplace manifest schema against Anthropic's published schema.

## Adding a new skill

1. Create `skills/<dept>-<skill>/SKILL.md` with `name` + `description` frontmatter.
2. Add a bullet for it under the matching `## <dept>` section in `references/department-index.md`.
3. Run `python3 scripts/validate.py`. It will fail if the index is out of sync.
4. Commit and open a PR.

## Adding or modifying an agent

1. Edit/add `agents/council-<dept>.md` with `name`, `description`, and `model` frontmatter. `model` must be `inherit` (preferred — the engine routes the actual tier per cost profile at spawn time) or a tier alias (`sonnet`, `opus`, `haiku`, `fable`). Never pin a `claude-*` model ID; the validator rejects it.
2. Update the **Agent Roster** table in `commands/council.md` (file column = `council-<dept>`, subagent type column = the YAML `name`).
3. Update `references/department-index.md` to add a `## <dept>` section listing that agent's skills.
4. Run validation.

## Promoting a held-back agent (forge / foundry / accountant)

These were excluded from v1.0.0 to keep the plugin software-focused. To bring one back:

1. Copy the relevant files from the source dotfiles repo (`my-claude-setup/agents/`, `my-claude-setup/skills/council/<dept>/`).
2. Remove the dept name from `HELD_BACK_DEPTS` and add it to `EXPECTED_DEPTS` in `scripts/validate.py`.
3. Add the dept to `commands/council.md` roster + `references/department-index.md`.
4. Run validation, commit, tag a new version (`vX.Y.Z`).

## Releasing

```bash
# Bump version in CHANGELOG.md and commit.
# Then:
git tag vX.Y.Z
git push origin main vX.Y.Z
```

The Anthropic marketplace pulls by tag (or commit SHA when no tag). Submitted plugins update automatically when a new tag is pushed.
