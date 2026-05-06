#!/usr/bin/env python3
"""Plugin integrity validator for agentic-council.

Runs structural checks that aren't covered by `claude plugin validate`:
manifest parsing, frontmatter completeness, cross-reference integrity
between roster/agents/skills/index, no leakage of held-back agents or
hardcoded user paths.

Exit code 0 on success, 1 on any failure. Designed to run in CI.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

HELD_BACK_DEPTS = {"forge", "foundry", "accountant"}
ENGINEERING_DEPTS = {
    "architect", "skeptic", "advocate", "craftsman", "scout",
    "strategist", "operator", "chronicler", "guardian", "tuner",
    "alchemist", "pathfinder", "artisan", "herald", "sentinel",
    "oracle", "cipher", "warden", "prover",
}
SIBLING_PREFIXES = {"finance", "people", "revenue"}
VALID_SKILL_PREFIXES = ENGINEERING_DEPTS | SIBLING_PREFIXES
VALID_AGENT_PREFIXES = {"council"} | SIBLING_PREFIXES
EXPECTED_DEPTS = ENGINEERING_DEPTS
USER_PATH_PATTERNS = [
    re.compile(r"/Users/[a-zA-Z][a-zA-Z0-9_-]*"),
    re.compile(r"/home/[a-zA-Z][a-zA-Z0-9_-]*"),
]
STALE_PATH_PATTERNS = [
    re.compile(r"\.claude/skills/council/"),
    re.compile(r"DEPARTMENT\.md"),
]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    body = text[3:end].strip()
    return yaml.safe_load(body) or {}


def check_manifests(report: Report) -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    market_path = ROOT / ".claude-plugin" / "marketplace.json"

    for p in (plugin_path, market_path):
        if not p.exists():
            report.err(f"Missing manifest: {p.relative_to(ROOT)}")
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            report.err(f"Invalid JSON in {p.relative_to(ROOT)}: {e}")

    if plugin_path.exists() and market_path.exists():
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        market = json.loads(market_path.read_text(encoding="utf-8"))
        if plugin.get("name") != "agentic-council":
            report.err(f"plugin.json name must be 'agentic-council', got {plugin.get('name')!r}")
        plugin_version = plugin.get("version")
        if not plugin_version:
            report.err("plugin.json missing required 'version' field (without it, every commit becomes a new version for users)")
        elif not re.fullmatch(r"\d+\.\d+\.\d+", plugin_version):
            report.err(f"plugin.json version must be semver MAJOR.MINOR.PATCH, got {plugin_version!r}")
        plugin_entries = market.get("plugins", [])
        market_entry = next((p for p in plugin_entries if p.get("name") == "agentic-council"), None)
        if market_entry is None:
            report.err("marketplace.json must list 'agentic-council' in plugins[]")
        else:
            market_version = market_entry.get("version")
            if not market_version:
                report.err("marketplace.json plugin entry missing 'version' field")
            elif plugin_version and market_version != plugin_version:
                report.err(f"plugin.json version {plugin_version!r} disagrees with marketplace.json version {market_version!r}")


def check_skills(report: Report) -> set[str]:
    skills_dir = ROOT / "skills"
    found: set[str] = set()
    if not skills_dir.is_dir():
        report.err("skills/ directory missing")
        return found

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            report.err(f"skills/{name}/ has no SKILL.md")
            continue

        dept = name.split("-", 1)[0]
        if dept in HELD_BACK_DEPTS:
            report.err(f"Held-back department leak: skills/{name}/ should not be shipped")
            continue
        if dept not in VALID_SKILL_PREFIXES:
            report.err(f"Unknown department prefix in skills/{name}/")

        fm = parse_frontmatter(skill_md)
        if fm is None:
            report.err(f"skills/{name}/SKILL.md missing YAML frontmatter")
            continue
        for required in ("name", "description"):
            if not fm.get(required):
                report.err(f"skills/{name}/SKILL.md missing frontmatter field: {required}")

        found.add(name)

    if len(found) < 50:
        report.err(f"Only {len(found)} skills found — expected ~59 in v1.0.0")

    return found


def check_agents(report: Report) -> set[str]:
    agents_dir = ROOT / "agents"
    found: set[str] = set()
    if not agents_dir.is_dir():
        report.err("agents/ directory missing")
        return found

    for agent_md in sorted(agents_dir.glob("*.md")):
        stem = agent_md.stem
        prefix = stem.split("-", 1)[0]
        if prefix not in VALID_AGENT_PREFIXES:
            continue
        if prefix == "council":
            dept = stem.removeprefix("council-")
            if dept in HELD_BACK_DEPTS:
                report.err(f"Held-back agent leak: agents/{agent_md.name} should not be shipped")
                continue
        fm = parse_frontmatter(agent_md)
        if fm is None:
            report.err(f"agents/{agent_md.name} missing YAML frontmatter")
            continue
        for required in ("name", "description"):
            if not fm.get(required):
                report.err(f"agents/{agent_md.name} missing frontmatter field: {required}")
        found.add(stem)

    expected_engineering = {f"council-{d}" for d in ENGINEERING_DEPTS} | {"council-steward"}
    missing_engineering = expected_engineering - found
    if missing_engineering:
        report.err(f"Missing expected engineering agent files: {sorted(missing_engineering)}")

    return found


def check_department_index(report: Report, skill_names: set[str]) -> None:
    index_path = ROOT / "references" / "department-index.md"
    if not index_path.exists():
        report.err("references/department-index.md missing")
        return
    text = index_path.read_text(encoding="utf-8")

    all_known_prefixes = VALID_SKILL_PREFIXES | HELD_BACK_DEPTS
    referenced: set[str] = set()
    planned: set[str] = set()
    for match in re.finditer(r"`([a-z]+-[a-z0-9-]+)`(?:\s*\*?\(planned[^)]*\)\*?)?", text):
        token = match.group(1)
        if not token.startswith(tuple(f"{d}-" for d in all_known_prefixes)):
            continue
        # Tokens marked as "planned" in the text don't have to exist on disk yet.
        match_end = match.end()
        trailing = text[match_end:match_end + 80]
        if "planned" in trailing.split("\n", 1)[0].lower():
            planned.add(token)
        else:
            referenced.add(token)

    for name in referenced:
        dept = name.split("-", 1)[0]
        if dept in HELD_BACK_DEPTS:
            continue
        if name not in skill_names:
            report.err(f"department-index.md references missing skill: {name}")

    for dept_header in re.finditer(r"^##\s+([a-z-]+)\s*$", text, re.MULTILINE):
        section = dept_header.group(1)
        if section in HELD_BACK_DEPTS or section == "held back from v1.0.0":
            continue
        if section in ENGINEERING_DEPTS:
            section_skills = {n for n in referenced if n.startswith(f"{section}-")}
            actual = {n for n in skill_names if n.startswith(f"{section}-")}
            if section_skills != actual:
                report.err(
                    f"department-index.md '{section}' section out of sync with skills/: "
                    f"index has {sorted(section_skills - actual)} extra, missing {sorted(actual - section_skills)}"
                )


def check_council_roster(report: Report, agents: set[str]) -> None:
    council_md = ROOT / "commands" / "council.md"
    if not council_md.exists():
        report.err("commands/council.md missing")
        return
    text = council_md.read_text(encoding="utf-8")

    roster_files = set(re.findall(r"`(council-[a-z]+)`", text))
    held_back_in_roster = roster_files & {f"council-{d}" for d in HELD_BACK_DEPTS}
    if held_back_in_roster:
        report.err(f"commands/council.md still lists held-back agents: {sorted(held_back_in_roster)}")

    expected_in_roster = {f"council-{d}" for d in EXPECTED_DEPTS} | {"council-steward"}
    missing = expected_in_roster - roster_files
    if missing:
        report.err(f"commands/council.md roster missing: {sorted(missing)}")

    referenced_but_no_file = roster_files - agents
    if referenced_but_no_file:
        report.err(f"commands/council.md references nonexistent agents: {sorted(referenced_but_no_file)}")


def check_no_user_paths(report: Report) -> None:
    for path in ROOT.rglob("*"):
        if path.is_file() and any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        if not path.is_file() or path.suffix not in {".md", ".json", ".yaml", ".yml", ".sh", ".py"}:
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in {".git", "scripts"} and path.name == "validate.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in USER_PATH_PATTERNS:
            for m in pattern.finditer(text):
                report.err(f"{rel}: hardcoded user path: {m.group(0)!r}")


def check_no_stale_skill_paths(report: Report) -> None:
    plugin_assets = list((ROOT / "commands").glob("*.md")) + \
                    list((ROOT / "agents").glob("*.md")) + \
                    list((ROOT / "references").glob("*.md")) + \
                    list((ROOT / "skills").rglob("SKILL.md"))
    for path in plugin_assets:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        for pattern in STALE_PATH_PATTERNS:
            for m in pattern.finditer(text):
                report.err(f"{rel}: stale path reference {m.group(0)!r} (use ${{CLAUDE_PLUGIN_ROOT}} or department-index.md)")


def main() -> int:
    report = Report()
    print(f"Validating plugin at {ROOT}\n")

    check_manifests(report)
    skills = check_skills(report)
    agents = check_agents(report)
    check_department_index(report, skills)
    check_council_roster(report, agents)
    check_no_user_paths(report)
    check_no_stale_skill_paths(report)

    if report.warnings:
        print(f"⚠  {len(report.warnings)} warnings:")
        for w in report.warnings:
            print(f"   {w}")
        print()

    if report.errors:
        print(f"✘ {len(report.errors)} errors:")
        for e in report.errors:
            print(f"   {e}")
        print()
        print("✘ Validation failed")
        return 1

    print(f"✓ {len(skills)} skills, {len(agents)} agents — validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
