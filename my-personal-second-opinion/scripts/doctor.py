#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
RUNNER = SKILL_DIR / "scripts" / "second_opinion_runner.py"
HOME = Path.home()
SOURCE_SKILL = HOME / ".agents" / "skills" / "my-personal-second-opinion"
CLAUDE_LINK = HOME / ".claude" / "skills" / "my-personal-second-opinion"
CODEX_LINK = HOME / ".codex" / "skills" / "my-personal-second-opinion"
GEMINI_GLOBAL = HOME / ".gemini" / "antigravity" / "global_skills"


def readlink_if_symlink(path: Path) -> str | None:
    if not path.is_symlink():
        return None
    return os.readlink(path)


def check_link(path: Path, expected: Path) -> dict[str, Any]:
    exists = path.exists() or path.is_symlink()
    resolved = path.resolve() if exists else None
    return {
        "path": str(path),
        "exists": exists,
        "is_symlink": path.is_symlink(),
        "target": readlink_if_symlink(path),
        "resolved": str(resolved) if resolved else None,
        "points_to_expected": bool(resolved == expected.resolve()) if exists else False,
    }


def count_lines(path: Path) -> int | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def run_help() -> dict[str, Any]:
    completed = subprocess.run(
        ["python3", str(RUNNER), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout_preview": completed.stdout[:400],
        "stderr_preview": completed.stderr[:400],
    }


def run_smoke(current_engine: str, working_directory: Path, timeout_seconds: int) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="second-opinion-doctor-") as tmpdir:
        tmp = Path(tmpdir)
        output_json = tmp / "result.json"
        logs_dir = tmp / "logs"
        command = [
            "python3",
            str(RUNNER),
            "--current-engine",
            current_engine,
            "--working-directory",
            str(working_directory),
            "--smoke-test",
            "--timeout-seconds",
            str(timeout_seconds),
            "--output-json",
            str(output_json),
            "--logs-dir",
            str(logs_dir),
            "--no-persist-learning",
            "--no-git-persist",
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        payload: dict[str, Any] | None = None
        if output_json.exists():
            payload = json.loads(output_json.read_text(encoding="utf-8"))
        return {
            "ok": completed.returncode == 0 and isinstance(payload, dict),
            "returncode": completed.returncode,
            "command": command,
            "stdout_preview": completed.stdout[:400],
            "stderr_preview": completed.stderr[:400],
            "result": payload,
        }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    skill_md = SOURCE_SKILL / "SKILL.md"
    report: dict[str, Any] = {
        "source_skill": {
            "path": str(SOURCE_SKILL),
            "exists": SOURCE_SKILL.is_dir(),
        },
        "skill_md": {
            "path": str(skill_md),
            "exists": skill_md.exists(),
            "line_count": count_lines(skill_md),
        },
        "runner": {
            "path": str(RUNNER),
            "exists": RUNNER.exists(),
        },
        "surfaces": {
            "claude": check_link(CLAUDE_LINK, SOURCE_SKILL),
            "codex": check_link(CODEX_LINK, SOURCE_SKILL),
            "gemini_global_skills": check_link(GEMINI_GLOBAL, HOME / ".agents" / "skills"),
        },
        "runner_help": run_help(),
    }
    line_count = report["skill_md"]["line_count"]
    report["skill_md"]["within_500_line_budget"] = bool(line_count is not None and line_count <= 500)
    if not args.skip_smoke:
        report["smoke"] = run_smoke(
            current_engine=args.current_engine,
            working_directory=Path(args.working_directory).resolve(),
            timeout_seconds=args.timeout_seconds,
        )
    return report


def text_report(report: dict[str, Any]) -> str:
    lines = [
        "second-opinion doctor",
        f"- source skill exists: {report['source_skill']['exists']}",
        f"- SKILL.md lines: {report['skill_md']['line_count']}",
        f"- within 500-line budget: {report['skill_md']['within_500_line_budget']}",
        f"- runner exists: {report['runner']['exists']}",
        f"- claude surface OK: {report['surfaces']['claude']['points_to_expected']}",
        f"- codex surface OK: {report['surfaces']['codex']['points_to_expected']}",
        f"- gemini global_skills OK: {report['surfaces']['gemini_global_skills']['points_to_expected']}",
        f"- runner --help OK: {report['runner_help']['ok']}",
    ]
    smoke = report.get("smoke")
    if isinstance(smoke, dict):
        lines.append(f"- smoke OK: {smoke['ok']}")
        result = smoke.get("result") or {}
        if isinstance(result, dict):
            for engine_result in result.get("results", []):
                lines.append(
                    f"  - {engine_result.get('engine')}: success={engine_result.get('success')}"
                )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose second-opinion surfacing and runner health.")
    parser.add_argument("--current-engine", default="codex", choices=["claude", "codex", "gemini"])
    parser.add_argument("--working-directory", default=os.getcwd())
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--skip-smoke", action="store_true")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args)

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(text_report(report))

    smoke = report.get("smoke")
    ok = (
        report["source_skill"]["exists"]
        and report["skill_md"]["within_500_line_budget"]
        and report["runner"]["exists"]
        and report["surfaces"]["claude"]["points_to_expected"]
        and report["surfaces"]["codex"]["points_to_expected"]
        and report["surfaces"]["gemini_global_skills"]["points_to_expected"]
        and report["runner_help"]["ok"]
        and (smoke is None or smoke["ok"])
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
