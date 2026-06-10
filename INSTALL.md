# Installing agentic-council

## 1. Add the marketplace and install the plugin

```
/plugin marketplace add https://github.com/dtsong/agentic-council
/plugin install agentic-council
```

## 2. Requirements

**Claude Code ≥ 2.1.154 with dynamic workflows available.** Deliberation runs as a background workflow — available by default on Max, Team, and Enterprise plans; on Pro, turn on **Dynamic workflows** in `/config`. If your org disables workflows (`disableWorkflows` in managed settings), the engine degrades to agent teams (if enabled below) or sequential agent calls.

Check your version with `claude --version`. See the [Cost guide](./README.md#cost-guide) for choosing a `--profile` before your first full session.

## 2b. Optional: enable the agent-teams runtime

Agent teams are **experimental** and no longer required for the core `/council` flow. Enabling them unlocks:

- `--meet` live steering — message individual panelists mid-discussion (Shift+Down)
- Path A team execution — shared task list with dependency unblocking and per-task plan approval

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Add this to your shell profile (`~/.zshrc`, `~/.bash_profile`, etc.) so it persists across sessions. Known teams limitations apply (no `/resume` of in-process teammates, slow shutdown, one team at a time) — these now only affect the features above, not the whole plugin.

## 3. Verify

In a workspace, run:

```
/council --help
```

You should see the full command reference. Then try:

```
/council --brainstorm "Should we migrate from Express to Fastify?"
```

Three agents should post positions and the Steward should synthesize a recommendation.

## Troubleshooting

**"Orchestration: sequential" notice on every session**
Neither workflows nor agent teams are available. Update Claude Code to ≥ 2.1.154, check that Dynamic workflows isn't disabled in `/config` (or by `CLAUDE_CODE_DISABLE_WORKFLOWS` / org managed settings), or export `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Sequential mode still works — it's just slower.

**`--meet` says live steering is unavailable**
Live panel steering requires the agent-teams flag (step 2b). Confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is exported in the shell that launched Claude Code, then restart Claude Code.

**Skills not discovered**
Each skill directory must contain a `SKILL.md`. Run `/plugin reload agentic-council` if you've upgraded.

**Session artifacts in unexpected locations**
Session state lives in your *workspace* `.claude/council/`, not the plugin root. If you don't see `.claude/council/sessions/<slug>/` after a run, the engine may have failed early. Check the transcript output.

**Slash commands missing**
Run `/plugin list` to confirm `agentic-council` is installed and active. If it shows but commands don't appear, the plugin namespace is `agentic-council:` and `/council` is exposed as a top-level alias.

## Uninstall

```
/plugin uninstall agentic-council
/plugin marketplace remove https://github.com/dtsong/agentic-council
```

Workspace session data under `.claude/council/` is preserved. Delete it manually if you want a clean slate.
