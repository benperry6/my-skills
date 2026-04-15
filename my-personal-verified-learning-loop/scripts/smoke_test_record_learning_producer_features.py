#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RECORD_LEARNING = SCRIPT_DIR / "record_learning.py"


def run(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def git(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return run(["git", *command], cwd=cwd)


def main() -> int:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

    with tempfile.TemporaryDirectory(prefix="verified-learning-producer-") as tmpdir:
        root = Path(tmpdir)
        remote = root / "remote.git"
        repo = root / "repo"
        skill_dir = repo / "test-skill"
        references = skill_dir / "references"
        references.mkdir(parents=True, exist_ok=True)

        git(["init", "--bare", str(remote)], cwd=root)
        git(["init", "-b", "main", str(repo)], cwd=root)
        git(["config", "user.name", "Codex Smoke"], cwd=repo)
        git(["config", "user.email", "codex-smoke@example.com"], cwd=repo)
        git(["remote", "add", "origin", str(remote)], cwd=repo)

        (references / "runtime-learning.md").write_text(
            "# Runtime Learning — test-skill\n\nCustom preamble preserved.\n",
            encoding="utf-8",
        )
        (references / "runtime-extensions.schema.json").write_text(
            json.dumps(
                {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "vendor": {"type": "string", "minLength": 1},
                        "phase": {"type": "string", "minLength": 1},
                        "operation": {"type": "string", "minLength": 1},
                        "browser_fallback_used": {"type": "boolean"},
                        "learning_fingerprint": {"type": "string", "minLength": 1},
                    },
                },
                indent=2,
                ensure_ascii=True,
            )
            + "\n",
            encoding="utf-8",
        )

        git(["add", "."], cwd=repo)
        initial_commit = git(["commit", "-m", "Initial smoke repo"], cwd=repo)
        if initial_commit.returncode != 0:
            raise SystemExit(initial_commit.stderr.strip() or initial_commit.stdout.strip() or "initial git commit failed")
        initial_push = git(["push", "-u", "origin", "main"], cwd=repo)
        if initial_push.returncode != 0:
            raise SystemExit(initial_push.stderr.strip() or initial_push.stdout.strip() or "initial git push failed")

        valid_batch = [
            {
                "topic": "batch-runtime-a",
                "summary": "Producer batch append keeps one canonical runtime incident for bootstrap A.",
                "status": "repaired",
                "failed_path": "vendor-a --broken",
                "repaired_path": "vendor-a --fixed",
                "source_skill": "test-skill",
                "agent": "codex",
                "target_files": ["references/runtime-learning.md"],
                "extensions": {
                    "vendor": "VendorA",
                    "phase": "phase-2",
                    "operation": "bootstrap",
                    "browser_fallback_used": False,
                    "learning_fingerprint": "vendor-a-phase-2-bootstrap",
                },
                "evidence": ["exit code 0 on repaired path"],
            },
            {
                "topic": "batch-runtime-a-duplicate",
                "summary": "Duplicate fingerprint should not create a second record.",
                "status": "repaired",
                "failed_path": "vendor-a --broken-again",
                "repaired_path": "vendor-a --fixed-again",
                "source_skill": "test-skill",
                "agent": "codex",
                "target_files": ["references/runtime-learning.md"],
                "extensions": {
                    "vendor": "VendorA",
                    "phase": "phase-2",
                    "operation": "bootstrap",
                    "browser_fallback_used": False,
                    "learning_fingerprint": "vendor-a-phase-2-bootstrap",
                },
                "evidence": ["same learning, second observation"],
            },
            {
                "topic": "batch-runtime-b",
                "summary": "Second unique incident should be persisted.",
                "status": "observed",
                "failed_path": "vendor-b --timeout",
                "source_skill": "test-skill",
                "agent": "codex",
                "target_files": ["references/runtime-learning.md"],
                "extensions": {
                    "vendor": "VendorB",
                    "phase": "phase-4",
                    "operation": "ingestion-check",
                    "browser_fallback_used": True,
                    "learning_fingerprint": "vendor-b-phase-4-ingestion",
                },
                "evidence": ["timeout reproduced twice"],
            },
        ]

        valid_batch_path = root / "valid-batch.json"
        valid_batch_path.write_text(json.dumps(valid_batch, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

        valid_run = run(
            [
                sys.executable,
                str(RECORD_LEARNING),
                "--skill-dir",
                str(skill_dir),
                "--kind",
                "runtime",
                "--batch-json-file",
                str(valid_batch_path),
                "--git-persist",
                "--git-commit-message",
                "Auto-learn producer smoke batch",
            ],
            cwd=repo,
            env=env,
        )
        if valid_run.returncode != 0:
            raise SystemExit(valid_run.stderr.strip() or valid_run.stdout.strip() or "producer feature smoke write failed")

        records = json.loads((references / "runtime-learning.json").read_text(encoding="utf-8"))
        if not isinstance(records, list) or len(records) != 2:
            raise SystemExit(f"Expected exactly two deduplicated runtime records, got: {records}")
        if any(not record.get("record_id") for record in records):
            raise SystemExit("Expected generated record_id values on all runtime records.")

        markdown = (references / "runtime-learning.md").read_text(encoding="utf-8")
        if "Custom preamble preserved." not in markdown:
            raise SystemExit("Runtime markdown preamble was not preserved.")
        if markdown.count("## ") != 2:
            raise SystemExit("Expected exactly two runtime headings after batch append.")

        log_output = git(["log", "--oneline", "-1"], cwd=repo)
        if "Auto-learn producer smoke batch" not in log_output.stdout:
            raise SystemExit("Expected git-persist commit message was not found in local git log.")

        remote_head = git(["--git-dir", str(remote), "log", "--oneline", "-1", "refs/heads/main"], cwd=root)
        if "Auto-learn producer smoke batch" not in remote_head.stdout:
            raise SystemExit("Expected git-persist commit message was not found on the pushed remote.")

        invalid_batch = [
            {
                "topic": "invalid-extension",
                "summary": "This should fail schema validation.",
                "extensions": {
                    "vendor": "VendorC",
                    "unknown_field": "nope",
                },
            }
        ]
        invalid_batch_path = root / "invalid-batch.json"
        invalid_batch_path.write_text(json.dumps(invalid_batch, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

        invalid_run = run(
            [
                sys.executable,
                str(RECORD_LEARNING),
                "--skill-dir",
                str(skill_dir),
                "--kind",
                "runtime",
                "--batch-json-file",
                str(invalid_batch_path),
            ],
            cwd=repo,
            env=env,
        )
        if invalid_run.returncode == 0:
            raise SystemExit("Expected invalid extension schema smoke to fail.")
        stderr = invalid_run.stderr.strip() or invalid_run.stdout.strip()
        if "unsupported field" not in stderr:
            raise SystemExit(f"Unexpected invalid-extension failure output: {stderr}")

    print("record-learning-producer-features-smoke-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
