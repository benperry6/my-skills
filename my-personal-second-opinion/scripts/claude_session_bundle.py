#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


CLAUDE_PROJECTS_ROOT = Path.home() / ".claude" / "projects"
CLAUDE_LOCAL_AGENT_ROOT = Path.home() / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions"

PATH_CLEANUP_CHARS = "\"'`()[]{}<>.,;:"
GENERATED_SESSION_MARKERS = (
    "Context: We are running a post-implementation audit",
    "Context: We are extending the personal skill `my-personal-second-opinion`",
)


def existing_search_roots() -> list[Path]:
    roots: list[Path] = []
    if CLAUDE_PROJECTS_ROOT.exists():
        roots.append(CLAUDE_PROJECTS_ROOT)
    if CLAUDE_LOCAL_AGENT_ROOT.exists():
        roots.append(CLAUDE_LOCAL_AGENT_ROOT)
    return roots


def sanitize_path(raw: str) -> str:
    return raw.strip().strip(PATH_CLEANUP_CHARS)


def text_fragments_from_jsonl(path: Path) -> Iterable[str]:
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue

            message = payload.get("message")
            if isinstance(message, dict):
                content = message.get("content")
                yield from content_fragments(content)

            prompt = payload.get("prompt")
            if isinstance(prompt, str):
                yield prompt

            data = payload.get("data")
            if isinstance(data, dict):
                nested_message = data.get("message")
                if isinstance(nested_message, dict):
                    nested_payload = nested_message.get("message")
                    if isinstance(nested_payload, dict):
                        yield from content_fragments(nested_payload.get("content"))


def looks_like_generated_second_opinion_session(path: Path) -> bool:
    for index, fragment in enumerate(text_fragments_from_jsonl(path)):
        if any(marker in fragment for marker in GENERATED_SESSION_MARKERS):
            return True
        if index >= 5:
            break
    return False


def content_fragments(content: object) -> Iterable[str]:
    if isinstance(content, str):
        yield content
        return
    if not isinstance(content, list):
        return
    for item in content:
        if isinstance(item, str):
            yield item
            continue
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str):
            yield text
        item_content = item.get("content")
        if isinstance(item_content, str):
            yield item_content


def extract_transcript_links(text: str) -> list[Path]:
    links: list[Path] = []
    pattern = re.compile(r"read the full transcript at:\s*(/.*?\.jsonl)", re.IGNORECASE)
    for match in pattern.finditer(text):
        candidate = Path(sanitize_path(match.group(1)))
        if candidate.exists():
            links.append(candidate)
    return links


def is_plan_like(path: Path) -> bool:
    lowered = str(path).lower()
    return (
        "/plans/" in lowered
        or lowered.endswith("-plan.md")
        or lowered.endswith("-design.md")
        or "/.claude/plans/" in lowered
    )


def extract_plan_links(text: str) -> list[Path]:
    plans: list[Path] = []
    pattern = re.compile(r"(/.*?\.md)")
    for match in pattern.finditer(text):
        candidate = Path(sanitize_path(match.group(1)))
        if candidate.exists() and is_plan_like(candidate):
            plans.append(candidate)
    return plans


def dedupe_paths(paths: Iterable[Path]) -> list[Path]:
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        ordered.append(path.resolve())
    return ordered


def follow_transcript_chain(session_file: Path) -> list[Path]:
    ordered: list[Path] = []
    visited: set[str] = set()

    def visit(path: Path) -> None:
        resolved = path.resolve()
        key = str(resolved)
        if key in visited or not resolved.exists():
            return
        visited.add(key)
        fragments = list(text_fragments_from_jsonl(resolved))
        previous_links: list[Path] = []
        for fragment in fragments:
            previous_links.extend(extract_transcript_links(fragment))
        for previous in dedupe_paths(previous_links):
            visit(previous)
        ordered.append(resolved)

    visit(session_file)
    return ordered


def discover_plan_files(transcript_files: list[Path]) -> list[Path]:
    plans: list[Path] = []
    for transcript in transcript_files:
        for fragment in text_fragments_from_jsonl(transcript):
            plans.extend(extract_plan_links(fragment))
    return dedupe_paths(plans)


def candidate_sessions_for_cwd(cwd: Path) -> list[Path]:
    roots = existing_search_roots()
    if not roots:
        return []

    needles = [f'"cwd":"{cwd}"', f'"cwd": "{cwd}"']
    matches: list[Path] = []
    if shutil_which("rg"):
        for needle in needles:
            command = ["rg", "-l", "--fixed-strings", needle, *[str(root) for root in roots]]
            completed = subprocess.run(command, check=False, capture_output=True, text=True)
            if completed.returncode not in (0, 1):
                continue
            for line in completed.stdout.splitlines():
                candidate = Path(line.strip())
                if candidate.exists():
                    matches.append(candidate)
    else:
        for root in roots:
            for candidate in root.rglob("*.jsonl"):
                try:
                    payload = candidate.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if any(needle in payload for needle in needles):
                    matches.append(candidate)
    ordered = sorted(
        [
            path
            for path in dedupe_paths(matches)
            if "/subagents/" not in str(path)
        ],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    filtered = [path for path in ordered if not looks_like_generated_second_opinion_session(path)]
    return filtered or ordered


def shutil_which(binary: str) -> str | None:
    completed = subprocess.run(["/usr/bin/env", "which", binary], check=False, capture_output=True, text=True)
    return completed.stdout.strip() or None


def build_bundle(session_file: Path) -> dict[str, object]:
    transcript_files = follow_transcript_chain(session_file)
    plan_files = discover_plan_files(transcript_files)
    return {
        "session_file": str(session_file.resolve()),
        "transcript_files": [str(path) for path in transcript_files],
        "plan_files": [str(path) for path in plan_files],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve a Claude Code transcript chain and related plan files.")
    parser.add_argument("--session-file")
    parser.add_argument("--cwd")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--format", choices=["json", "paths"], default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if bool(args.session_file) == bool(args.cwd):
        raise SystemExit("Pass exactly one of --session-file or --cwd.")
    if args.cwd and not args.latest:
        raise SystemExit("When using --cwd, pass --latest to select the latest matching Claude session.")

    if args.session_file:
        session_file = Path(args.session_file).expanduser().resolve()
        if not session_file.exists():
            raise SystemExit(f"Session file not found: {session_file}")
    else:
        cwd = Path(args.cwd).expanduser().resolve()
        candidates = candidate_sessions_for_cwd(cwd)
        if not candidates:
            raise SystemExit(f"No Claude sessions found for cwd: {cwd}")
        session_file = candidates[0]

    bundle = build_bundle(session_file)
    if args.format == "paths":
        for path in bundle["transcript_files"]:
            print(path)
        for path in bundle["plan_files"]:
            print(path)
        return 0

    print(json.dumps(bundle, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
