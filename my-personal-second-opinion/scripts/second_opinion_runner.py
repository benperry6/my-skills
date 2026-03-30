#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCES_DIR = SKILL_DIR / "references"
RUNTIME_LEARNING_JSON = REFERENCES_DIR / "runtime-learning.json"
RUNTIME_LEARNING_MD = REFERENCES_DIR / "runtime-learning.md"
CLAUDE_SESSION_BUNDLE_SCRIPT = SKILL_DIR / "scripts" / "claude_session_bundle.py"

TARGETS_BY_ENGINE = {
    "claude": ["codex", "gemini"],
    "codex": ["claude", "gemini"],
    "gemini": ["claude", "codex"],
}

POST_IMPLEMENTATION_RUBRIC = [
    {
        "name": "Plan coverage",
        "description": "Did the delivered implementation actually cover what the transcript or validated plan said should be shipped?",
    },
    {
        "name": "Scope drift",
        "description": "Did the implementation add, remove, or change material behavior that was not justified by the stated goal?",
    },
    {
        "name": "Correctness risk",
        "description": "Based on the code and local evidence, what defects, regressions, or edge-case failures are most plausible?",
    },
    {
        "name": "Runtime confidence",
        "description": "What is already verified by evidence, and what still needs real runtime confirmation before trusting the change?",
    },
    {
        "name": "Test adequacy",
        "description": "Do the current tests or proposed tests meaningfully cover the risky behavior, or is there still a verification gap?",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def slugify(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in value.strip())
    collapsed = "-".join(part for part in cleaned.split("-") if part)
    return collapsed or "audit"


def detect_current_engine() -> str | None:
    if os.environ.get("CLAUDECODE") == "1":
        return "claude"
    if os.environ.get("CODEX_CI") == "1":
        return "codex"
    if os.environ.get("GEMINI_CLI") == "1":
        return "gemini"
    return None


def default_targets_for(current_engine: str | None) -> list[str]:
    if current_engine in TARGETS_BY_ENGINE:
        return TARGETS_BY_ENGINE[current_engine]
    return ["claude", "codex", "gemini"]


def load_prompt(args: argparse.Namespace) -> str:
    if args.smoke_test:
        return "Reply with exactly: OK"
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    raise SystemExit("Provide --prompt, --prompt-file, or --smoke-test.")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def run_json_command(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip()
        raise SystemExit(stderr or f"Command failed: {shlex.join(command)}")
    payload = json.loads(completed.stdout)
    if not isinstance(payload, dict):
        raise SystemExit(f"Expected JSON object from command: {shlex.join(command)}")
    return payload


def git_output(workdir: Path, arguments: list[str], pathspecs: list[str] | None = None) -> str:
    command = ["git", "-C", str(workdir), *arguments]
    if pathspecs:
        command.extend(["--", *pathspecs])
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def collect_git_evidence(workdir: Path, pathspecs: list[str] | None = None) -> dict[str, Any]:
    repo_root = git_output(workdir, ["rev-parse", "--show-toplevel"])
    if not repo_root:
        return {
            "repo_root": "",
            "status_short": "",
            "diff_stat": "",
            "cached_diff_stat": "",
            "changed_files": [],
            "audit_paths": pathspecs or [],
        }

    changed_files = sorted(
        {
            *[
                line
                for line in git_output(workdir, ["diff", "--name-only"], pathspecs=pathspecs).splitlines()
                if line
            ],
            *[
                line
                for line in git_output(workdir, ["diff", "--cached", "--name-only"], pathspecs=pathspecs).splitlines()
                if line
            ],
        }
    )

    return {
        "repo_root": repo_root,
        "status_short": git_output(workdir, ["status", "--short"], pathspecs=pathspecs),
        "diff_stat": git_output(workdir, ["diff", "--stat"], pathspecs=pathspecs),
        "cached_diff_stat": git_output(workdir, ["diff", "--cached", "--stat"], pathspecs=pathspecs),
        "changed_files": changed_files,
        "audit_paths": pathspecs or [],
    }


def resolve_post_impl_manifest(args: argparse.Namespace, workdir: Path) -> dict[str, Any]:
    if args.transcript_file:
        return {
            "session_file": args.session_file or "",
            "transcript_files": [str(Path(path).expanduser().resolve()) for path in args.transcript_file],
            "plan_files": [str(Path(path).expanduser().resolve()) for path in (args.plan_file or [])],
        }

    if args.session_manifest_json:
        payload = json.loads(Path(args.session_manifest_json).expanduser().read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise SystemExit("--session-manifest-json must contain a JSON object.")
        return payload

    command = ["python3", str(CLAUDE_SESSION_BUNDLE_SCRIPT), "--format", "json"]
    if args.session_file:
        command.extend(["--session-file", args.session_file])
    elif args.session_cwd:
        command.extend(["--cwd", args.session_cwd, "--latest"])
    else:
        command.extend(["--cwd", str(workdir), "--latest"])
    return run_json_command(command)


def build_post_implementation_prompt(args: argparse.Namespace, workdir: Path) -> tuple[str, dict[str, Any]]:
    manifest = resolve_post_impl_manifest(args, workdir)
    transcript_files = manifest.get("transcript_files") or []
    if not isinstance(transcript_files, list) or not transcript_files:
        raise SystemExit("Post-implementation audit requires at least one transcript file.")
    plan_files = manifest.get("plan_files") or []
    if not isinstance(plan_files, list):
        raise SystemExit("Invalid plan_files in manifest.")

    audit_paths = args.audit_path or []
    git_evidence = collect_git_evidence(workdir, pathspecs=audit_paths)
    transcript_block = "\n".join(f"- {path}" for path in transcript_files)
    plan_block = "\n".join(f"- {path}" for path in plan_files) if plan_files else "- None discovered automatically."
    changed_files = "\n".join(f"- {path}" for path in git_evidence["changed_files"]) if git_evidence["changed_files"] else "- No unstaged or staged changed files detected."
    status_short = git_evidence["status_short"] or "(clean working tree or not inside a git repo)"
    diff_stat = git_evidence["diff_stat"] or "(no unstaged diff detected)"
    cached_diff_stat = git_evidence["cached_diff_stat"] or "(no staged diff detected)"
    extra_focus = args.audit_focus.strip() if args.audit_focus else ""
    audit_scope_block = (
        "\n".join(f"- {path}" for path in audit_paths)
        if audit_paths
        else "- Whole working tree."
    )
    rubric_block = "\n".join(
        f"- {criterion['name']}: {criterion['description']}"
        for criterion in POST_IMPLEMENTATION_RUBRIC
    )

    prompt = (
        "Context: We are running a post-implementation audit for a completed Claude Code implementation.\n"
        f"Working directory: {workdir}\n"
        f"Repository root: {git_evidence['repo_root'] or 'Not detected'}\n"
        "Audit scope:\n"
        f"{audit_scope_block}\n"
        "Claude transcript files to read fully in chronological order:\n"
        f"{transcript_block}\n"
        "Validated plan files to read fully:\n"
        f"{plan_block}\n"
        "Current git working-tree status:\n"
        f"{status_short}\n"
        "Unstaged diff stat:\n"
        f"{diff_stat}\n"
        "Staged diff stat:\n"
        f"{cached_diff_stat}\n"
        "Currently changed files:\n"
        f"{changed_files}\n"
        "Evaluation rubric:\n"
        f"{rubric_block}\n"
    )
    if extra_focus:
        prompt += f"Additional audit focus from the orchestrator:\n{extra_focus}\n"
    prompt += (
        "Task:\n"
        "1. Read the transcript files fully, oldest to newest.\n"
        "2. Read the validated plan files fully.\n"
        "3. Inspect the current code in the working directory.\n"
        "4. Determine whether everything that was planned was actually implemented, or whether there were omissions, mistakes, or regressions.\n"
        "5. Determine whether the implementation is plausibly correct in real behavior, and say explicitly what still requires real testing.\n"
        "6. If you find issues, recommend the smallest complete fix set and the most relevant real tests.\n"
        "Please return:\n"
        "(1) Findings first, ordered by severity\n"
        "(2) Rubric scorecard: for each rubric criterion, mark PASS / CONCERN / FAIL with a brief reason\n"
        "(3) Completeness verdict vs the validated plan\n"
        "(4) Behavior-confidence verdict: what is verified vs what still needs real testing\n"
        "(5) Exact fixes / next tests\n"
        "(6) Open questions\n"
        "Be concrete. Cite file paths when possible.\n"
    )

    return prompt, {**manifest, "audit_paths": audit_paths, "rubric": POST_IMPLEMENTATION_RUBRIC}


def build_audit_artifact_payload(summary: dict[str, Any], prompt: str) -> dict[str, Any]:
    return {
        "generated_at": utc_now(),
        "mode": summary.get("mode"),
        "current_engine": summary.get("current_engine"),
        "working_directory": summary.get("working_directory"),
        "audit_manifest": summary.get("audit_manifest", {}),
        "targets": summary.get("targets", []),
        "prompt": prompt,
        "results": summary.get("results", []),
    }


def render_audit_artifact_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Second Opinion Audit",
        "",
        f"- Generated at: `{payload.get('generated_at', '')}`",
        f"- Mode: `{payload.get('mode', '')}`",
        f"- Current engine: `{payload.get('current_engine', '')}`",
        f"- Working directory: `{payload.get('working_directory', '')}`",
        "",
    ]

    manifest = payload.get("audit_manifest", {})
    if isinstance(manifest, dict) and manifest:
        lines.extend(["## Audit Context", ""])
        session_file = manifest.get("session_file")
        if session_file:
            lines.append(f"- Session file: `{session_file}`")
        transcript_files = manifest.get("transcript_files") or []
        if transcript_files:
            lines.append("- Transcript files:")
            for item in transcript_files:
                lines.append(f"  - `{item}`")
        plan_files = manifest.get("plan_files") or []
        if plan_files:
            lines.append("- Plan files:")
            for item in plan_files:
                lines.append(f"  - `{item}`")
        audit_paths = manifest.get("audit_paths") or []
        if audit_paths:
            lines.append("- Audit scope:")
            for item in audit_paths:
                lines.append(f"  - `{item}`")
        rubric = manifest.get("rubric") or []
        if rubric:
            lines.extend(["", "## Rubric", ""])
            for criterion in rubric:
                if isinstance(criterion, dict):
                    lines.append(f"- **{criterion.get('name', 'Criterion')}**: {criterion.get('description', '')}")
        lines.append("")

    lines.extend(["## Prompt", "", "```text", payload.get("prompt", "").rstrip(), "```", ""])

    results = payload.get("results") or []
    for result in results:
        if not isinstance(result, dict):
            continue
        lines.extend([f"## Result — {result.get('engine', 'unknown')}", ""])
        lines.append(f"- Success: `{result.get('success', False)}`")
        if result.get("repaired"):
            lines.append("- Repaired path: `true`")
        if result.get("needs_web_research"):
            lines.append("- Needs web research: `true`")
        models = result.get("models") or {}
        if models:
            lines.append(f"- Models: `{json.dumps(models, sort_keys=True)}`")
        lines.extend(["", payload_result_block(result), ""])

    return "\n".join(lines).rstrip() + "\n"


def payload_result_block(result: dict[str, Any]) -> str:
    response = (result.get("response") or "").rstrip()
    if not response:
        return "_No response captured._"
    return "```text\n" + response + "\n```"


def write_audit_artifacts(
    summary: dict[str, Any],
    prompt: str,
    report_dir: Path,
    report_prefix: str,
) -> dict[str, Any]:
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{timestamp_slug()}-{slugify(report_prefix)}"
    json_path = report_dir / f"{stem}.json"
    md_path = report_dir / f"{stem}.md"
    payload = build_audit_artifact_payload(summary, prompt)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    md_path.write_text(render_audit_artifact_markdown(payload), encoding="utf-8")
    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
    }


def extract_json(text: str) -> Any | None:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "[{":
            continue
        try:
            payload, _ = decoder.raw_decode(text[index:])
            return payload
        except json.JSONDecodeError:
            continue
    return None


def extract_response_text(payload: Any) -> str:
    if isinstance(payload, dict):
        for key in ("response", "result", "message", "content", "text"):
            value = payload.get(key)
            if isinstance(value, str):
                return value.strip()
        if isinstance(payload.get("messages"), list):
            chunks: list[str] = []
            for item in payload["messages"]:
                if isinstance(item, str):
                    chunks.append(item)
                elif isinstance(item, dict):
                    for key in ("text", "content", "message"):
                        value = item.get(key)
                        if isinstance(value, str):
                            chunks.append(value)
            if chunks:
                return "\n".join(chunks).strip()
    if isinstance(payload, list):
        chunks = [item for item in payload if isinstance(item, str)]
        if chunks:
            return "\n".join(chunks).strip()
    return ""


def classify_failure(text: str, returncode: int) -> str:
    lowered = text.lower()
    if returncode == 124:
        return "timeout"
    if "model_capacity_exhausted" in lowered or "no capacity available for model" in lowered:
        return "capacity"
    if "modelnotfounderror" in lowered or "requested entity was not found" in lowered:
        return "model-unavailable"
    if "not a git repository" in lowered or "git repo check" in lowered:
        return "git-topology"
    if "authentication" in lowered or "authenticate" in lowered or "signed in" in lowered and returncode != 0:
        return "auth"
    if "unknown option" in lowered or "unknown argument" in lowered or "invalid option" in lowered:
        return "cli-surface-drift"
    if "command not found" in lowered or "no such file or directory" in lowered:
        return "cli-missing"
    return "unknown"


def failure_signature(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    interesting = (
        "resource_exhausted",
        "model_capacity_exhausted",
        "modelnotfounderror",
        "requested entity was not found",
        "not a git repository",
        "authentication",
        "unknown option",
        "unknown argument",
    )
    for line in lines:
        lowered = line.lower()
        if any(token in lowered for token in interesting):
            return line[:300]
    return lines[-1][:300] if lines else "No failure output captured."


def prompt_models(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        stats = payload.get("stats")
        if isinstance(stats, dict):
            models = stats.get("models")
            if isinstance(models, dict):
                return models
    return {}


def gemini_auth_mode() -> str:
    settings_path = Path.home() / ".gemini" / "settings.json"
    try:
        payload = json.loads(settings_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return "unknown"
    return (
        payload.get("security", {})
        .get("auth", {})
        .get("selectedType", "unknown")
    )


def ensure_runtime_learning_files() -> None:
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    if not RUNTIME_LEARNING_JSON.exists():
        RUNTIME_LEARNING_JSON.write_text('{"records":[]}\n', encoding="utf-8")
    if not RUNTIME_LEARNING_MD.exists():
        RUNTIME_LEARNING_MD.write_text(
            "# Runtime Learning — my-personal-second-opinion\n\n"
            "Auto-managed by `scripts/second_opinion_runner.py`.\n\n"
            "No runtime-learned repair incidents recorded yet.\n",
            encoding="utf-8",
        )


def load_runtime_records() -> dict[str, Any]:
    ensure_runtime_learning_files()
    payload = json.loads(RUNTIME_LEARNING_JSON.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        return {"records": []}
    return payload


def render_runtime_learning(records: list[dict[str, Any]]) -> str:
    lines = [
        "# Runtime Learning — my-personal-second-opinion",
        "",
        "Auto-managed by `scripts/second_opinion_runner.py`.",
        "",
    ]
    if not records:
        lines.append("No runtime-learned repair incidents recorded yet.")
        lines.append("")
        return "\n".join(lines)

    for record in sorted(records, key=lambda item: item["recorded_at"], reverse=True):
        lines.extend(
            [
                f"## {record['recorded_at']} — {record['target_engine']}",
                "",
                f"- Current engine: `{record['current_engine']}`",
                f"- Working directory: `{record['working_directory']}`",
                f"- Failed path: `{record['failed_command']}`",
                f"- Failure classification: `{record['failure_classification']}`",
                f"- Failure signature: `{record['failure_signature']}`",
                f"- Repaired path: `{record['repaired_command']}`",
                f"- Repair strategy: `{record['repair_strategy']}`",
            ]
        )
        models = record.get("verified_models") or {}
        if models:
            lines.append(f"- Verified models: `{json.dumps(models, sort_keys=True)}`")
        response_preview = record.get("response_preview", "")
        if response_preview:
            lines.append(f"- Response preview: `{response_preview}`")
        lines.extend(["", ""])
    return "\n".join(lines).rstrip() + "\n"


def persist_runtime_learning(records: list[dict[str, Any]], enable_git_persist: bool) -> dict[str, Any]:
    payload = load_runtime_records()
    existing = payload["records"]
    existing_ids = {item.get("id") for item in existing}
    added: list[dict[str, Any]] = []
    for record in records:
        digest_source = json.dumps(
            {
                "target_engine": record["target_engine"],
                "failed_command": record["failed_command"],
                "failure_signature": record["failure_signature"],
                "repaired_command": record["repaired_command"],
            },
            sort_keys=True,
        )
        record_id = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:16]
        if record_id in existing_ids:
            continue
        stored = {"id": record_id, **record}
        existing.append(stored)
        existing_ids.add(record_id)
        added.append(stored)

    if not added:
        return {"added": 0, "committed": False, "pushed": False}

    RUNTIME_LEARNING_JSON.write_text(
        json.dumps({"records": existing}, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    RUNTIME_LEARNING_MD.write_text(render_runtime_learning(existing), encoding="utf-8")

    git_result = {"committed": False, "pushed": False}
    if enable_git_persist:
        git_result = git_persist_learning_files()

    return {"added": len(added), **git_result}


def git_persist_learning_files() -> dict[str, Any]:
    repo_root = subprocess.run(
        ["git", "-C", str(SKILL_DIR), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if repo_root.returncode != 0:
        return {"committed": False, "pushed": False, "git_error": repo_root.stderr.strip()}
    root = repo_root.stdout.strip()

    subprocess.run(
        ["git", "-C", root, "add", str(RUNTIME_LEARNING_JSON), str(RUNTIME_LEARNING_MD)],
        check=False,
        capture_output=True,
        text=True,
    )
    staged = subprocess.run(
        ["git", "-C", root, "diff", "--cached", "--quiet"],
        check=False,
        capture_output=True,
        text=True,
    )
    if staged.returncode == 0:
        return {"committed": False, "pushed": False}

    commit = subprocess.run(
        ["git", "-C", root, "commit", "-m", "Auto-learn second-opinion runtime repair"],
        check=False,
        capture_output=True,
        text=True,
    )
    if commit.returncode != 0:
        return {
            "committed": False,
            "pushed": False,
            "git_error": commit.stderr.strip() or commit.stdout.strip(),
        }

    push = subprocess.run(
        ["git", "-C", root, "push", "origin", "main"],
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "committed": True,
        "pushed": push.returncode == 0,
        "git_error": "" if push.returncode == 0 else (push.stderr.strip() or push.stdout.strip()),
    }


def codex_attempts(prompt: str, workdir: Path, attempt_dir: Path) -> list[dict[str, Any]]:
    answer_file = attempt_dir / "codex-last-message.txt"
    return [
        {
            "name": "codex-exec",
            "command": [
                "codex",
                "exec",
                "--dangerously-bypass-approvals-and-sandbox",
                "--skip-git-repo-check",
                "--output-last-message",
                str(answer_file),
                prompt,
            ],
            "answer_file": answer_file,
        }
    ]


def claude_attempts(prompt: str, _: Path, __: Path) -> list[dict[str, Any]]:
    return [
        {
            "name": "claude-json",
            "command": ["claude", "-p", prompt, "--output-format", "json"],
            "parse_json": True,
        },
        {
            "name": "claude-text",
            "command": ["claude", "-p", prompt, "--output-format", "text"],
            "parse_json": False,
        },
    ]


def gemini_attempts(prompt: str, _: Path, __: Path) -> list[dict[str, Any]]:
    auth_mode = gemini_auth_mode()
    attempts = [
        {
            "name": "gemini-pro",
            "command": ["gemini", "-m", "pro", "-p", prompt, "--output-format", "json"],
            "parse_json": True,
        },
        {
            "name": "gemini-auto",
            "command": ["gemini", "-m", "auto", "-p", prompt, "--output-format", "json"],
            "parse_json": True,
        },
    ]

    if auth_mode == "oauth-personal":
        attempts.extend(
            [
                {
                    "name": "gemini-3-flash-preview",
                    "command": [
                        "gemini",
                        "-m",
                        "gemini-3-flash-preview",
                        "-p",
                        prompt,
                        "--output-format",
                        "json",
                    ],
                    "parse_json": True,
                },
                {
                    "name": "gemini-2.5-flash",
                    "command": ["gemini", "-m", "gemini-2.5-flash", "-p", prompt, "--output-format", "json"],
                    "parse_json": True,
                },
                {
                    "name": "gemini-2.5-pro",
                    "command": ["gemini", "-m", "gemini-2.5-pro", "-p", prompt, "--output-format", "json"],
                    "parse_json": True,
                },
            ]
        )
    else:
        attempts.extend(
            [
                {
                    "name": "gemini-3.1-pro-preview",
                    "command": [
                        "gemini",
                        "-m",
                        "gemini-3.1-pro-preview",
                        "-p",
                        prompt,
                        "--output-format",
                        "json",
                    ],
                    "parse_json": True,
                },
                {
                    "name": "gemini-3-flash-preview",
                    "command": [
                        "gemini",
                        "-m",
                        "gemini-3-flash-preview",
                        "-p",
                        prompt,
                        "--output-format",
                        "json",
                    ],
                    "parse_json": True,
                },
            ]
        )
    return attempts


def build_attempts(engine: str, prompt: str, workdir: Path, attempt_dir: Path) -> list[dict[str, Any]]:
    if engine == "codex":
        return codex_attempts(prompt, workdir, attempt_dir)
    if engine == "claude":
        return claude_attempts(prompt, workdir, attempt_dir)
    if engine == "gemini":
        return gemini_attempts(prompt, workdir, attempt_dir)
    raise ValueError(f"Unsupported engine: {engine}")


def execute_attempt(
    engine: str,
    strategy: dict[str, Any],
    workdir: Path,
    attempt_dir: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    attempt_dir.mkdir(parents=True, exist_ok=True)
    started_at = time.time()
    command = strategy["command"]
    if shutil.which(command[0]) is None:
        return {
            "strategy": strategy["name"],
            "command": shlex.join(command),
            "success": False,
            "returncode": 127,
            "classification": "cli-missing",
            "failure_signature": f"{command[0]} not found in PATH",
            "duration_ms": 0,
            "stdout_path": "",
            "stderr_path": "",
        }

    if engine == "codex":
        log_path = attempt_dir / "combined.log"
        try:
            with log_path.open("w", encoding="utf-8") as log_file:
                completed = subprocess.run(
                    command,
                    cwd=str(workdir),
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                    timeout=timeout_seconds,
                )
        except subprocess.TimeoutExpired:
            return {
                "strategy": strategy["name"],
                "command": shlex.join(command),
                "success": False,
                "returncode": 124,
                "classification": "timeout",
                "failure_signature": "Timed out while waiting for command completion.",
                "duration_ms": int((time.time() - started_at) * 1000),
                "stdout_path": str(log_path),
                "stderr_path": "",
                "models": {},
            }
        answer_text = read_text(strategy["answer_file"]).strip()
        success = completed.returncode == 0 and bool(answer_text)
        output_text = read_text(log_path)
        return {
            "strategy": strategy["name"],
            "command": shlex.join(command),
            "success": success,
            "returncode": completed.returncode,
            "response": answer_text,
            "duration_ms": int((time.time() - started_at) * 1000),
            "stdout_path": str(log_path),
            "stderr_path": "",
            "models": {},
            "classification": "" if success else classify_failure(output_text, completed.returncode),
            "failure_signature": "" if success else failure_signature(output_text),
        }

    stdout_path = attempt_dir / "stdout.log"
    stderr_path = attempt_dir / "stderr.log"
    try:
        with stdout_path.open("w", encoding="utf-8") as stdout_file, stderr_path.open(
            "w", encoding="utf-8"
        ) as stderr_file:
            completed = subprocess.run(
                command,
                cwd=str(workdir),
                stdout=stdout_file,
                stderr=stderr_file,
                text=True,
                check=False,
                timeout=timeout_seconds,
            )
    except subprocess.TimeoutExpired:
        return {
            "strategy": strategy["name"],
            "command": shlex.join(command),
            "success": False,
            "returncode": 124,
            "classification": "timeout",
            "failure_signature": "Timed out while waiting for command completion.",
            "duration_ms": int((time.time() - started_at) * 1000),
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "models": {},
        }

    stdout_text = read_text(stdout_path)
    stderr_text = read_text(stderr_path)
    combined = "\n".join(part for part in (stdout_text, stderr_text) if part).strip()
    payload = extract_json(stdout_text if strategy.get("parse_json", False) else "")
    response = extract_response_text(payload) if payload is not None else stdout_text.strip()
    models = prompt_models(payload) if payload is not None else {}
    success = completed.returncode == 0 and bool(response)

    return {
        "strategy": strategy["name"],
        "command": shlex.join(command),
        "success": success,
        "returncode": completed.returncode,
        "response": response,
        "duration_ms": int((time.time() - started_at) * 1000),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "models": models,
        "classification": "" if success else classify_failure(combined, completed.returncode),
        "failure_signature": "" if success else failure_signature(combined),
    }


def run_engine(
    current_engine: str,
    target_engine: str,
    prompt: str,
    workdir: Path,
    logs_root: Path,
    timeout_seconds: int,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    target_dir = logs_root / target_engine
    target_dir.mkdir(parents=True, exist_ok=True)
    attempts: list[dict[str, Any]] = []
    strategies = build_attempts(target_engine, prompt, workdir, target_dir)
    first_failure: dict[str, Any] | None = None

    for index, strategy in enumerate(strategies, start=1):
        attempt_dir = target_dir / f"attempt-{index:02d}"
        result = execute_attempt(target_engine, strategy, workdir, attempt_dir, timeout_seconds)
        attempts.append(result)
        if result["success"]:
            summary = {
                "engine": target_engine,
                "success": True,
                "response": result.get("response", ""),
                "models": result.get("models", {}),
                "attempts": attempts,
                "repaired": first_failure is not None,
            }
            learning_record = None
            if first_failure is not None:
                learning_record = {
                    "recorded_at": utc_now(),
                    "current_engine": current_engine,
                    "target_engine": target_engine,
                    "working_directory": str(workdir),
                    "failed_command": first_failure["command"],
                    "failure_classification": first_failure["classification"],
                    "failure_signature": first_failure["failure_signature"],
                    "repaired_command": result["command"],
                    "repair_strategy": result["strategy"],
                    "verified_models": result.get("models", {}),
                    "response_preview": (result.get("response", "") or "").strip()[:120],
                }
            return summary, learning_record

        if first_failure is None:
            first_failure = result
        # Stop early if the failure is a local CLI problem unlikely to be fixed by the next attempt.
        if result["classification"] in {"cli-missing", "auth", "git-topology", "timeout"} and target_engine != "gemini":
            break

    last_failure = attempts[-1] if attempts else {
        "classification": "unknown",
        "failure_signature": "No attempts executed.",
    }
    return (
        {
            "engine": target_engine,
            "success": False,
            "response": "",
            "models": {},
            "attempts": attempts,
            "repaired": False,
            "needs_web_research": True,
            "final_failure_classification": last_failure["classification"],
            "final_failure_signature": last_failure["failure_signature"],
        },
        None,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Self-healing second-opinion runner.")
    parser.add_argument(
        "--mode",
        choices=["standard", "post-implementation-audit"],
        default="standard",
        help="Standard prompt relay or post-implementation audit mode.",
    )
    parser.add_argument("--current-engine", choices=["claude", "codex", "gemini"])
    parser.add_argument("--targets", nargs="+", choices=["claude", "codex", "gemini"])
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--session-file", help="Explicit Claude session file for post-implementation audit.")
    parser.add_argument(
        "--session-cwd",
        help="Resolve the latest Claude session whose recorded cwd matches this path.",
    )
    parser.add_argument(
        "--session-manifest-json",
        help="Precomputed JSON manifest containing transcript_files and optional plan_files.",
    )
    parser.add_argument(
        "--transcript-file",
        nargs="+",
        help="Explicit transcript file list for post-implementation audit, oldest to newest.",
    )
    parser.add_argument(
        "--plan-file",
        nargs="+",
        help="Optional validated plan files to include in post-implementation audit mode.",
    )
    parser.add_argument(
        "--audit-focus",
        help="Extra audit instructions appended to the post-implementation prompt.",
    )
    parser.add_argument(
        "--audit-path",
        nargs="+",
        help="Optional git pathspec(s) limiting the post-implementation audit to the relevant files/directories.",
    )
    parser.add_argument(
        "--audit-report-dir",
        help="Optional directory where a durable post-implementation audit artifact should be written.",
    )
    parser.add_argument(
        "--audit-report-prefix",
        default="second-opinion-audit",
        help="Filename prefix used when writing durable post-implementation audit artifacts.",
    )
    parser.add_argument("--working-directory", default=os.getcwd())
    parser.add_argument("--output-json")
    parser.add_argument("--logs-dir")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--smoke-test", action="store_true")
    parser.add_argument("--persist-learning", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--git-persist", action=argparse.BooleanOptionalAction, default=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    current_engine = args.current_engine or detect_current_engine()
    if args.smoke_test:
        current_engine = current_engine or "orchestrator"
        targets = args.targets or default_targets_for(None if current_engine == "orchestrator" else current_engine)
    else:
        if current_engine is None:
            raise SystemExit("Unable to detect the current engine. Pass --current-engine explicitly.")
        targets = args.targets or default_targets_for(current_engine)

    workdir = Path(args.working_directory).resolve()
    prompt_manifest: dict[str, Any] = {}
    if args.mode == "post-implementation-audit":
        prompt, prompt_manifest = build_post_implementation_prompt(args, workdir)
    else:
        prompt = load_prompt(args)

    logs_root = (
        Path(args.logs_dir).resolve()
        if args.logs_dir
        else Path(tempfile.mkdtemp(prefix="second-opinion-run-"))
    )
    logs_root.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "run_at": utc_now(),
        "mode": args.mode,
        "current_engine": current_engine,
        "targets": targets,
        "working_directory": str(workdir),
        "logs_root": str(logs_root),
        "results": [],
        "persisted_learning": {"added": 0, "committed": False, "pushed": False},
    }
    if prompt_manifest:
        summary["audit_manifest"] = prompt_manifest
    learning_records: list[dict[str, Any]] = []

    for target in targets:
        result, learning_record = run_engine(
            current_engine=current_engine,
            target_engine=target,
            prompt=prompt,
            workdir=workdir,
            logs_root=logs_root,
            timeout_seconds=args.timeout_seconds,
        )
        summary["results"].append(result)
        if learning_record is not None and args.persist_learning:
            learning_records.append(learning_record)

    if learning_records and args.persist_learning:
        summary["persisted_learning"] = persist_runtime_learning(
            learning_records, enable_git_persist=args.git_persist
        )

    if args.mode == "post-implementation-audit" and args.audit_report_dir:
        summary["audit_artifact"] = write_audit_artifacts(
            summary=summary,
            prompt=prompt,
            report_dir=Path(args.audit_report_dir).expanduser().resolve(),
            report_prefix=args.audit_report_prefix,
        )

    if args.output_json:
        Path(args.output_json).write_text(
            json.dumps(summary, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(summary, indent=2, ensure_ascii=True))
    return 0 if all(result["success"] for result in summary["results"]) else 1


if __name__ == "__main__":
    sys.exit(main())
