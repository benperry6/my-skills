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


def run_once(skill_dir: Path) -> None:
    command = [
        sys.executable,
        str(RECORD_LEARNING),
        "--skill-dir",
        str(skill_dir),
        "--kind",
        "runtime",
        "--topic",
        "shared-dedup-smoke",
        "--summary",
        "Shared helper de-duplicates the same runtime incident.",
        "--status",
        "repaired",
        "--failed-path",
        "vendor-cli --broken",
        "--repaired-path",
        "vendor-cli --fixed",
        "--source-skill",
        "my-personal-verified-learning-loop",
        "--agent",
        "codex",
        "--target-file",
        "references/runtime-learning.md",
        "--extensions-json",
        json.dumps(
            {
                "vendor": "SmokeVendor",
                "operation": "bootstrap",
            },
            sort_keys=True,
        ),
        "--evidence",
        "exit code 0 on repaired path",
    ]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    completed = subprocess.run(command, check=False, capture_output=True, text=True, env=env)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "record_learning.py failed")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="verified-learning-dedup-") as tmpdir:
        skill_dir = Path(tmpdir) / "test-skill"
        references = skill_dir / "references"
        references.mkdir(parents=True, exist_ok=True)

        run_once(skill_dir)
        run_once(skill_dir)

        runtime_json = references / "runtime-learning.json"
        runtime_md = references / "runtime-learning.md"

        records = json.loads(runtime_json.read_text(encoding="utf-8"))
        if not isinstance(records, list) or len(records) != 1:
            raise SystemExit(f"Expected exactly one runtime record after dedup, got: {records}")

        record = records[0]
        if not record.get("record_id"):
            raise SystemExit("Expected generated record_id in runtime incident.")

        markdown = runtime_md.read_text(encoding="utf-8")
        if markdown.count("shared-dedup-smoke") != 1:
            raise SystemExit("Runtime markdown mirror contains duplicated heading entries.")

    print("record-learning-dedup-smoke-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
