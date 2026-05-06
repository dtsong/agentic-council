# Installing agentic-council

## 1. Add the marketplace and install the plugin

```
/plugin marketplace add https://github.com/dtsong/agentic-council
/plugin install agentic-council
```

## 2. Enable the agent-teams runtime

The council spawns each member as a separate teammate with its own context window. This requires the experimental agent-teams flag:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Add this to your shell profile (`~/.zshrc`, `~/.bash_profile`, etc.) so it persists across sessions.

> Plugins cannot set process-level environment variables, so this step is unavoidable until the flag is no longer experimental.

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

**"Agent teams not enabled" preflight error**
Confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is exported in the shell that launched Claude Code. Restart Claude Code after exporting.

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
