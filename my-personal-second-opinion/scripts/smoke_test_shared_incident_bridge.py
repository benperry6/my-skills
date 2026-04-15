#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True

SCRIPT_DIR = Path(__file__).resolve().parent
RUNNER_PATH = SCRIPT_DIR / "second_opinion_runner.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("second_opinion_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load runner module from {RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    runner = load_runner_module()

    native_record = {
        "id": "smoke-test-native-record",
        "recorded_at": "2026-04-15T08:00:00+00:00",
        "current_engine": "codex",
        "target_engine": "gemini",
        "working_directory": "/tmp/shared-learning-smoke",
        "failed_command": "gemini -p broken",
        "failure_classification": "cli-surface-drift",
        "failure_signature": "unknown flag: -p",
        "repaired_command": "gemini -m gemini-2.5-pro -p fixed",
        "repair_strategy": "swap to verified invocation flags",
        "verified_models": {"gemini": "gemini-2.5-pro"},
        "response_preview": "OK",
    }

    incident = runner.to_shared_incident(native_record)
    schema = runner.load_shared_runtime_incident_schema()
    runner.validate_shared_incident(incident, schema)

    with tempfile.TemporaryDirectory(prefix="second-opinion-shared-smoke-") as tmpdir:
        tmpdir_path = Path(tmpdir)
        shared_json = tmpdir_path / "runtime-learning.shared.json"
        shared_md = tmpdir_path / "runtime-learning.shared.md"

        runner.SHARED_RUNTIME_LEARNING_JSON = shared_json
        runner.SHARED_RUNTIME_LEARNING_MD = shared_md

        first = runner.persist_shared_runtime_learning([native_record])
        if first.get("shared_added") != 1:
            raise SystemExit(f"Expected first shared_added=1, got {first}")

        stored = json.loads(shared_json.read_text(encoding="utf-8"))
        if not isinstance(stored, list) or len(stored) != 1:
            raise SystemExit(f"Expected one stored shared incident, got: {stored}")

        stored_incident = stored[0]
        if stored_incident["topic"] != "gemini-invocation-repair":
            raise SystemExit(f"Unexpected topic in stored incident: {stored_incident['topic']}")
        if stored_incident["extensions"]["native_record_id"] != native_record["id"]:
            raise SystemExit("native_record_id was not preserved in shared extensions.")

        markdown = shared_md.read_text(encoding="utf-8")
        if "gemini-invocation-repair" not in markdown:
            raise SystemExit("Shared markdown mirror did not render the expected topic.")

        second = runner.persist_shared_runtime_learning([native_record])
        if second.get("shared_added") != 0:
            raise SystemExit(f"Expected second shared_added=0 after dedup, got {second}")

    print("shared-incident-bridge-smoke-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
