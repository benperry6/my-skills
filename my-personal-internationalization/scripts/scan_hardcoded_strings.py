#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALLOWED_EXTENSIONS = {
    ".astro",
    ".go",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".mdx",
    ".php",
    ".py",
    ".rb",
    ".svelte",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
}
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".next",
    ".nuxt",
    "build",
    "coverage",
    "dist",
    "i18n",
    "lang",
    "languages",
    "locales",
    "messages",
    "node_modules",
    "storybook-static",
    "test",
    "tests",
    "__snapshots__",
    "__tests__",
    "vendor",
}
STRING_LITERAL_RE = re.compile(
    r'(?P<quote>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`)'
)
JSX_TEXT_RE = re.compile(r">([^<>{][^<>]*[A-Za-z][^<>]*)<")
NON_USER_FACING_ATTRIBUTE_MARKERS = (
    "class=",
    "className=",
    "d=",
    "fill=",
    "height=",
    "stroke=",
    "strokeLinecap=",
    "strokeLinejoin=",
    "strokeWidth=",
    "viewBox=",
    "width=",
    "xmlns=",
)


def should_skip_file(path: Path, root: Path, exclude_dirs: set[str]) -> bool:
    if path.suffix not in ALLOWED_EXTENSIONS:
        return True

    relative_parts = path.relative_to(root).parts[:-1]
    return any(part in exclude_dirs for part in relative_parts)


def looks_non_user_facing(candidate: str) -> bool:
    text = candidate.strip()
    if len(text) < 4:
        return True
    if not re.search(r"[A-Za-zÀ-ÿ]", text):
        return True
    if text.startswith(("http://", "https://", "/", "./", "../", "@/")):
        return True
    if "*" in text and " " not in text:
        return True
    if text.startswith(("data:image/", "linear-gradient(")):
        return True
    if text in {"noopener noreferrer"}:
        return True
    if any(operator in text for operator in ("&&", "||", "===", "!==")):
        return True
    if text.startswith("[") and "data-" in text:
        return True
    if re.fullmatch(r"[MmLlHhVvCcSsQqTtAaZz0-9 ,.\-]+", text) and any(char.isdigit() for char in text):
        return True
    if re.fullmatch(r"[a-z]+(?:[A-Z][a-z0-9]+)+", text):
        return True
    if text.startswith("#${") or text.startswith("${"):
        return True
    if text.startswith("faq.") and re.fullmatch(r"[A-Za-z0-9_.-]+", text):
        return True
    if re.fullmatch(r"[A-Za-z0-9_.:/#?=&%+-]+", text):
        if any(marker in text for marker in ("/", ".", "_", "::", "=>", "://")):
            return True
        if text.isupper():
            return True
        if text.lower() == text and " " not in text:
            return True
    if text.count(",") >= 2 and all(re.fullmatch(r"[A-Za-z0-9_ ]+", part.strip()) for part in text.split(",")):
        return True
    tokens = text.split()
    if tokens and any(any(char in token for char in "-:/[]().%") or any(char.isdigit() for char in token) for token in tokens):
        if all(re.fullmatch(r"[!@A-Za-z0-9_:[\]()/%.+-]+", token) for token in tokens):
            return True
    if re.fullmatch(r"[A-Za-z0-9-]+", text) and text.lower() == text:
        return True
    if text in {"use client", "use strict"}:
        return True
    if re.fullmatch(r"[A-Za-z]+(?:\.[A-Za-z]+)+", text):
        return True
    return False


def normalize_literal(raw: str) -> str:
    if raw.startswith(("'", '"', "`")) and raw.endswith(raw[0]):
        return raw[1:-1]
    return raw


def line_is_probably_code_only(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith(("//", "#", "*", "/*", "*/")):
        return True
    if re.match(r"^(import|export)\b", stripped):
        return True
    if " from " in stripped and re.match(r"^(import|export)\b", stripped):
        return True
    if "require(" in stripped:
        return True
    return False


def should_skip_literal_for_line(line: str, literal: str) -> bool:
    if any(marker in line for marker in NON_USER_FACING_ATTRIBUTE_MARKERS):
        if "${" in literal:
            return True
        tokens = literal.split()
        if len(tokens) >= 1 and (
            len(tokens) == 1
            or all(re.fullmatch(r"[!@A-Za-z0-9_:[\]()/%.+-]+", token) for token in tokens)
        ):
            return True
    return False


def collect_findings(root: Path, exclude_dirs: set[str], limit: int) -> list[dict[str, str | int]]:
    findings: list[dict[str, str | int]] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip_file(path, root, exclude_dirs):
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        relative_path = str(path.relative_to(root))

        for line_number, line in enumerate(lines, start=1):
            if line_is_probably_code_only(line):
                continue

            for match in STRING_LITERAL_RE.finditer(line):
                literal = normalize_literal(match.group("quote")).strip()
                if should_skip_literal_for_line(line, literal):
                    continue
                if looks_non_user_facing(literal):
                    continue
                findings.append(
                    {
                        "path": relative_path,
                        "line": line_number,
                        "kind": "string-literal",
                        "text": literal,
                    }
                )
                if len(findings) >= limit:
                    return findings

            for match in JSX_TEXT_RE.finditer(line):
                text = " ".join(match.group(1).split())
                if looks_non_user_facing(text):
                    continue
                findings.append(
                    {
                        "path": relative_path,
                        "line": line_number,
                        "kind": "jsx-text",
                        "text": text,
                    }
                )
                if len(findings) >= limit:
                    return findings

    return findings


def render_text(findings: list[dict[str, str | int]], root: Path) -> str:
    lines = [f"Root: {root}"]
    if not findings:
        lines.append("Result: OK - no obvious hardcoded user-facing string candidates found.")
        return "\n".join(lines)

    lines.append("Result: REVIEW - hardcoded user-facing string candidates found.")
    lines.append("These are heuristic findings and require confirmation.")
    for item in findings:
        lines.append(
            f"- {item['path']}:{item['line']} [{item['kind']}] {item['text']}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan a codebase for likely hardcoded user-facing strings outside locale catalogs."
    )
    parser.add_argument("--root", required=True, type=Path, help="Root directory to scan.")
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Directory name to exclude. Can be passed multiple times.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Maximum findings to print. Defaults to 200.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit with code 1 when any candidate is found.",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    exclude_dirs = DEFAULT_EXCLUDE_DIRS | set(args.exclude_dir)
    findings = collect_findings(root, exclude_dirs, max(1, args.limit))

    if args.format == "json":
        print(json.dumps({"root": str(root), "findings": findings}, indent=2, ensure_ascii=False))
    else:
        print(render_text(findings, root))

    should_fail = bool(findings) and args.fail_on_findings
    raise SystemExit(1 if should_fail else 0)


if __name__ == "__main__":
    main()
