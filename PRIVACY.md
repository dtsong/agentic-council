# Privacy Policy

**Last updated:** 2026-05-05

## Summary

agentic-council is a Claude Code plugin. It does not collect, transmit, or share any user data. Everything stays on your machine.

## What the plugin does

agentic-council is a set of markdown files (commands, agent personas, skills) and one Python validator script. It has no runtime of its own. When you invoke `/council` (or any other command), the plugin's markdown is interpreted by Claude Code, which spawns subagents that talk to Anthropic's Claude API on your behalf using your existing Claude Code authentication.

## What data is created

When you run a council session, Claude Code writes session artifacts to your local filesystem:

- **Per-workspace session data:** `<workspace>/.claude/council/sessions/<slug>/` containing the interview, assembly notes, deliberation rounds, design doc, and build plan.
- **Per-workspace session index:** `<workspace>/.claude/council/index.json`.
- **Per-user registry:** `~/.claude/council/registry.json` tracking skill usage across workspaces, and `~/.claude/council/global-registry.json` for cross-workspace session metadata.

These files live entirely on your machine. The plugin never reads them back to a remote server.

## What the plugin does not do

- No telemetry. No analytics. No usage pings.
- No network calls of its own. The plugin ships zero executable code that opens a network socket. The only Python in the repo is `scripts/validate.py`, which is a CI-only structural checker that never runs at plugin invocation time.
- No data sharing with third parties. The plugin has no third parties.
- No tracking across machines. The cross-workspace registry described above stays in `~/.claude/`. It never leaves your home directory.

## Third-party data flows

Running the plugin causes Claude Code to send your prompts and session content to **Anthropic's Claude API** as part of normal Claude Code operation. That data flow is governed by Anthropic's own privacy policy at <https://www.anthropic.com/legal/privacy>, not by this plugin.

If your council session reads files from your codebase (via `/council --audit`, for example), those file contents are sent to the Claude API the same way any Claude Code session would send them. The plugin does not introduce any additional data egress beyond what Claude Code already does.

## Your rights

You own all session artifacts. To delete them, remove the directories listed in **What data is created** above. The plugin will recreate the registry on next use; existing session data is gone permanently.

## Contact

Open an issue at <https://github.com/dtsong/agentic-council/issues> for privacy-related questions or concerns.

## Changes

This policy may be updated as the plugin evolves. Material changes will be noted in [CHANGELOG.md](./CHANGELOG.md).
