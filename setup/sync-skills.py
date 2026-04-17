#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


HOME = Path.home()
SOURCE_ROOT = HOME / ".agents" / "skills"
SKILL_GLOB = "my-personal-*"
TARGETS = {
    "claude": HOME / ".claude" / "skills",
    "codex": HOME / ".codex" / "skills",
}
GEMINI_LINK = HOME / ".gemini" / "antigravity" / "global_skills"


@dataclass
class Finding:
    level: str
    message: str


def now_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def source_skills() -> list[Path]:
    return sorted(path for path in SOURCE_ROOT.glob(SKILL_GLOB) if path.is_dir())


def ensure_dir(path: Path, apply: bool, findings: list[Finding]) -> None:
    if path.is_dir():
        return
    if apply:
        path.mkdir(parents=True, exist_ok=True)
        findings.append(Finding("fix", f"Created directory: {path}"))
    else:
        findings.append(Finding("drift", f"Missing directory: {path}"))


def relative_target(destination_dir: Path, source: Path) -> str:
    return os.path.relpath(source, destination_dir)


def move_as_backup(path: Path, apply: bool, findings: list[Finding]) -> bool:
    backup = path.with_name(f"{path.name}.backup-{now_slug()}")
    if apply:
        shutil.move(str(path), str(backup))
        findings.append(Finding("fix", f"Moved unexpected real path to backup: {path} -> {backup}"))
        return True
    findings.append(Finding("drift", f"Unexpected real path blocks required symlink: {path}"))
    return False


def ensure_symlink(link_path: Path, source: Path, apply: bool, findings: list[Finding]) -> None:
    expected = relative_target(link_path.parent, source)

    if link_path.is_symlink():
        current = os.readlink(link_path)
        if current == expected:
            findings.append(Finding("ok", f"Symlink OK: {link_path} -> {current}"))
            return
        if apply:
            link_path.unlink()
            link_path.symlink_to(expected)
            findings.append(Finding("fix", f"Replaced wrong symlink: {link_path} -> {expected}"))
        else:
            findings.append(Finding("drift", f"Wrong symlink: {link_path} -> {current} (expected {expected})"))
        return

    if link_path.exists():
        if not move_as_backup(link_path, apply, findings):
            return

    if apply:
        link_path.symlink_to(expected)
        findings.append(Finding("fix", f"Created symlink: {link_path} -> {expected}"))
    else:
        findings.append(Finding("drift", f"Missing symlink: {link_path} -> {expected}"))


def clean_stale_symlinks(target_dir: Path, valid_names: set[str], apply: bool, findings: list[Finding]) -> None:
    if not target_dir.exists():
        return
    for path in sorted(target_dir.glob(SKILL_GLOB)):
        if path.name in valid_names:
            continue
        if path.is_symlink():
            current = os.readlink(path)
            if apply:
                path.unlink()
                findings.append(Finding("fix", f"Removed stale symlink: {path} -> {current}"))
            else:
                findings.append(Finding("drift", f"Stale symlink present: {path} -> {current}"))
        else:
            findings.append(Finding("warn", f"Unmanaged real path kept in place: {path}"))


def ensure_gemini_link(apply: bool, findings: list[Finding]) -> None:
    parent = GEMINI_LINK.parent
    ensure_dir(parent, apply, findings)
    expected = str(SOURCE_ROOT)

    if GEMINI_LINK.is_symlink():
        current = os.readlink(GEMINI_LINK)
        if current == expected:
            findings.append(Finding("ok", f"Gemini global_skills OK: {GEMINI_LINK} -> {current}"))
            return
        if apply:
            GEMINI_LINK.unlink()
            GEMINI_LINK.symlink_to(expected)
            findings.append(Finding("fix", f"Replaced wrong Gemini global_skills link: {GEMINI_LINK} -> {expected}"))
        else:
            findings.append(Finding("drift", f"Wrong Gemini global_skills link: {GEMINI_LINK} -> {current} (expected {expected})"))
        return

    if GEMINI_LINK.exists():
        if not move_as_backup(GEMINI_LINK, apply, findings):
            return

    if apply:
        GEMINI_LINK.symlink_to(expected)
        findings.append(Finding("fix", f"Created Gemini global_skills link: {GEMINI_LINK} -> {expected}"))
    else:
        findings.append(Finding("drift", f"Missing Gemini global_skills link: {GEMINI_LINK} -> {expected}"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync shared personal skills into Claude Code, Codex, and Gemini.")
    parser.add_argument("--dry-run", action="store_true", help="Preview fixes without writing")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if any drift is detected")
    args = parser.parse_args()

    if args.dry_run and args.check:
        parser.error("--dry-run and --check are mutually exclusive")

    apply = not args.check and not args.dry_run
    findings: list[Finding] = []

    if not SOURCE_ROOT.is_dir():
        print(f"Source skills root missing: {SOURCE_ROOT}")
        return 1

    skills = source_skills()
    valid_names = {path.name for path in skills}
    if not skills:
        print(f"No source skills found matching {SKILL_GLOB} in {SOURCE_ROOT}")
        return 1

    for target_dir in TARGETS.values():
        ensure_dir(target_dir, apply, findings)

    for target_dir in TARGETS.values():
        for skill_path in skills:
            ensure_symlink(target_dir / skill_path.name, skill_path, apply, findings)
        clean_stale_symlinks(target_dir, valid_names, apply, findings)

    ensure_gemini_link(apply, findings)

    drift = [item for item in findings if item.level == "drift"]
    fixes = [item for item in findings if item.level == "fix"]
    warnings = [item for item in findings if item.level == "warn"]

    mode = "apply"
    if args.dry_run:
        mode = "dry-run"
    elif args.check:
        mode = "check"

    print(f"Skill sync mode: {mode}")
    print(f"Source skills: {len(skills)}")
    print(f"Drift: {len(drift)}")
    print(f"Fixes applied: {len(fixes)}")
    print(f"Warnings: {len(warnings)}")

    for group_name, items in (("drift", drift), ("fix", fixes), ("warn", warnings)):
        if not items:
            continue
        print(f"\n{group_name.upper()}:")
        for item in items:
            print(f"- {item.message}")

    if args.check and drift:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
