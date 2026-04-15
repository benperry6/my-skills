#!/usr/bin/env python3
"""Append runtime or verified learning entries to a target skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SHARED_SKILL_DIR = Path(__file__).resolve().parents[1]
SHARED_RUNTIME_INCIDENT_SCHEMA = SHARED_SKILL_DIR / "references" / "runtime-incident.schema.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def append_entry(target: Path, heading: str, lines: list[str]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    block = "\n".join([heading, "", *lines, ""])
    target.write_text(existing + block, encoding="utf-8")


def append_entries(target: Path, blocks: list[str]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    payload = existing + "\n".join(blocks)
    if payload and not payload.endswith("\n"):
        payload += "\n"
    target.write_text(payload, encoding="utf-8")


def load_json_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        payload = payload["records"]
    if not isinstance(payload, list):
        raise SystemExit(f"{path} must contain a JSON array or an object with a `records` array.")
    return payload


def save_json_records(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def stable_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: stable_json(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [stable_json(item) for item in value]
    return value


def compute_runtime_record_id(record: dict[str, Any]) -> str:
    extensions = dict(record.get("extensions") or {})
    fingerprint_override = extensions.get("learning_fingerprint")
    if isinstance(fingerprint_override, str) and fingerprint_override.strip():
        digest_source = {"learning_fingerprint": fingerprint_override.strip()}
    else:
        digest_source = {
            "kind": record.get("kind"),
            "topic": record.get("topic"),
            "summary": record.get("summary"),
            "status": record.get("status"),
            "confidence": record.get("confidence"),
            "failed_path": record.get("failed_path"),
            "repaired_path": record.get("repaired_path"),
            "source_skill": record.get("source_skill"),
            "source_session": record.get("source_session"),
            "agent": record.get("agent"),
            "target_files": sorted(record.get("target_files") or []),
            "canonical_change_candidate": record.get("canonical_change_candidate", False),
            "extensions": stable_json(extensions),
        }
    digest = hashlib.sha256(
        json.dumps(digest_source, sort_keys=True, ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    return digest[:16]


def default_runtime_preamble() -> str:
    return "# Runtime Learning\n\n"


def extract_runtime_preamble(target: Path) -> str:
    if not target.exists():
        return default_runtime_preamble()
    existing = target.read_text(encoding="utf-8")
    lines = existing.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("## "):
            preamble = "\n".join(lines[:index]).rstrip()
            return f"{preamble}\n\n" if preamble else default_runtime_preamble()
    stripped = existing.rstrip()
    return f"{stripped}\n\n" if stripped else default_runtime_preamble()


def render_runtime_markdown(records: list[dict[str, Any]], preamble: str) -> str:
    lines = [preamble.rstrip(), ""]
    if not records:
        lines.extend(["No runtime incidents have been recorded yet.", ""])
        return "\n".join(lines).rstrip() + "\n"

    for record in sorted(records, key=lambda item: item["timestamp"], reverse=True):
        lines.extend(
            [
                f"## {record['timestamp']} - {record['topic']}",
                "",
                f"- Summary: {record['summary']}",
                f"- Status: {record['status']}",
                f"- Confidence: {record['confidence']}",
                f"- Record ID: `{record['record_id']}`",
            ]
        )
        if record.get("failed_path"):
            lines.append(f"- Failed path: `{record['failed_path']}`")
        if record.get("repaired_path"):
            lines.append(f"- Repaired path: `{record['repaired_path']}`")
        if record.get("source_skill"):
            lines.append(f"- Source skill: `{record['source_skill']}`")
        if record.get("source_session"):
            lines.append(f"- Source session: `{record['source_session']}`")
        if record.get("agent"):
            lines.append(f"- Agent: `{record['agent']}`")
        target_files = record.get("target_files") or []
        if target_files:
            lines.append("- Target files:")
            for item in target_files:
                lines.append(f"  - `{item}`")
        extensions = record.get("extensions") or {}
        if extensions:
            lines.append(f"- Extensions JSON: `{json.dumps(extensions, sort_keys=True)}`")
        lines.append(
            f"- Canonical change candidate: `{str(record.get('canonical_change_candidate', False)).lower()}`"
        )
        for item in record.get("evidence") or []:
            lines.append(f"- Evidence: {item}")
        for item in record.get("notes") or []:
            lines.append(f"- Note: {item}")
        lines.extend(["", ""])
    return "\n".join(lines).rstrip() + "\n"


def load_schema(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing schema file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"{path} must contain a JSON object schema.")
    return payload


def load_shared_runtime_schema() -> dict[str, Any]:
    return load_schema(SHARED_RUNTIME_INCIDENT_SCHEMA)


def load_skill_extension_schema(skill_dir: Path) -> dict[str, Any] | None:
    schema_path = skill_dir / "references" / "runtime-extensions.schema.json"
    if not schema_path.exists():
        return None
    return load_schema(schema_path)


def matches_type(value: Any, expected_type: str) -> bool:
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    return True


def validate_schema_value(value: Any, schema: dict[str, Any], pointer: str) -> None:
    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(matches_type(value, item_type) for item_type in expected_type):
            raise SystemExit(f"{pointer} does not match expected types {expected_type}.")
    elif isinstance(expected_type, str):
        if not matches_type(value, expected_type):
            raise SystemExit(f"{pointer} does not match expected type `{expected_type}`.")

    if "const" in schema and value != schema["const"]:
        raise SystemExit(f"{pointer} must equal `{schema['const']}`.")
    if "enum" in schema and value not in schema["enum"]:
        raise SystemExit(f"{pointer} has unsupported value `{value}`.")
    if isinstance(value, str) and "minLength" in schema and len(value) < schema["minLength"]:
        raise SystemExit(f"{pointer} is shorter than minLength={schema['minLength']}.")

    if isinstance(value, dict):
        required = schema.get("required", [])
        properties = schema.get("properties", {})
        for key in required:
            if key not in value:
                raise SystemExit(f"{pointer} is missing required field `{key}`.")
        if schema.get("additionalProperties", True) is False:
            extra = sorted(set(value.keys()) - set(properties.keys()))
            if extra:
                raise SystemExit(f"{pointer} has unsupported field(s): {', '.join(extra)}.")
        for key, child_schema in properties.items():
            if key in value:
                validate_schema_value(value[key], child_schema, f"{pointer}.{key}")

    if isinstance(value, list) and "items" in schema:
        item_schema = schema["items"]
        for index, item in enumerate(value):
            validate_schema_value(item, item_schema, f"{pointer}[{index}]")


def normalize_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SystemExit("Expected a list of strings.")
    return value


def runtime_record_from_entry(
    entry: dict[str, Any],
    shared_schema: dict[str, Any],
    extension_schema: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise SystemExit("Each runtime batch entry must be a JSON object.")
    extensions = entry.get("extensions") or {}
    if not isinstance(extensions, dict):
        raise SystemExit("Runtime incident `extensions` must be a JSON object.")
    if extension_schema is not None:
        validate_schema_value(extensions, extension_schema, "extensions")

    record: dict[str, Any] = {
        "record_id": entry.get("record_id"),
        "timestamp": entry.get("timestamp") or utc_now(),
        "kind": "runtime",
        "topic": entry.get("topic"),
        "summary": entry.get("summary"),
        "status": entry.get("status", "observed"),
        "confidence": entry.get("confidence", "medium"),
        "failed_path": entry.get("failed_path"),
        "repaired_path": entry.get("repaired_path"),
        "evidence": normalize_string_list(entry.get("evidence")),
        "notes": normalize_string_list(entry.get("notes")),
        "source_skill": entry.get("source_skill"),
        "source_session": entry.get("source_session"),
        "agent": entry.get("agent"),
        "target_files": normalize_string_list(entry.get("target_files")),
        "extensions": extensions,
        "canonical_change_candidate": bool(entry.get("canonical_change_candidate", False)),
    }
    record["record_id"] = record.get("record_id") or compute_runtime_record_id(record)
    validate_schema_value(record, shared_schema, "runtime_incident")
    return record


def verified_block_from_entry(entry: dict[str, Any]) -> str:
    if not isinstance(entry, dict):
        raise SystemExit("Each verified batch entry must be a JSON object.")
    topic = entry.get("topic")
    summary = entry.get("summary")
    if not isinstance(topic, str) or not topic.strip():
        raise SystemExit("Verified learning entry is missing `topic`.")
    if not isinstance(summary, str) or not summary.strip():
        raise SystemExit("Verified learning entry is missing `summary`.")

    heading = f"## {entry.get('timestamp') or utc_now()} - {topic}"
    lines = [f"- Summary: {summary}"]
    if entry.get("failed_path"):
        lines.append(f"- Failed path: `{entry['failed_path']}`")
    if entry.get("repaired_path"):
        lines.append(f"- Repaired path: `{entry['repaired_path']}`")
    if entry.get("source_skill"):
        lines.append(f"- Source skill: `{entry['source_skill']}`")
    if entry.get("source_session"):
        lines.append(f"- Source session: `{entry['source_session']}`")
    if entry.get("agent"):
        lines.append(f"- Agent: `{entry['agent']}`")
    for item in normalize_string_list(entry.get("target_files")):
        lines.append(f"- Target file: `{item}`")
    for item in normalize_string_list(entry.get("evidence")):
        lines.append(f"- Evidence: {item}")
    for item in normalize_string_list(entry.get("notes")):
        lines.append(f"- Note: {item}")
    return "\n".join([heading, "", *lines, ""])


def build_single_entry_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if not args.topic or not args.summary:
        raise SystemExit("Provide --topic and --summary when batch mode is not used.")
    extensions = json.loads(args.extensions_json) if args.extensions_json else {}
    if not isinstance(extensions, dict):
        raise SystemExit("--extensions-json must decode to a JSON object.")
    return {
        "topic": args.topic,
        "summary": args.summary,
        "status": args.status,
        "confidence": args.confidence,
        "failed_path": args.failed_path,
        "repaired_path": args.repaired_path,
        "source_skill": args.source_skill,
        "source_session": args.source_session,
        "agent": args.agent,
        "target_files": args.target_file,
        "extensions": extensions,
        "canonical_change_candidate": args.canonical_change_candidate,
        "evidence": args.evidence,
        "notes": args.notes,
    }


def load_batch_entries(args: argparse.Namespace) -> list[dict[str, Any]]:
    payload: Any
    if args.batch_json:
        payload = json.loads(args.batch_json)
    elif args.batch_json_file:
        payload = json.loads(Path(args.batch_json_file).expanduser().read_text(encoding="utf-8"))
    else:
        return [build_single_entry_from_args(args)]

    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        payload = payload["records"]
    if not isinstance(payload, list):
        raise SystemExit("Batch payload must be a JSON array or an object with a `records` array.")
    return payload


def persist_runtime_records(
    runtime_json: Path,
    runtime_md: Path,
    entries: list[dict[str, Any]],
    shared_schema: dict[str, Any],
    extension_schema: dict[str, Any] | None,
) -> dict[str, Any]:
    preamble = extract_runtime_preamble(runtime_md)
    records = load_json_records(runtime_json)
    for item in records:
        if "record_id" not in item or not item.get("record_id"):
            item["record_id"] = compute_runtime_record_id(item)
        validate_schema_value(item, shared_schema, "runtime_incident")

    existing_ids = {item["record_id"] for item in records}
    added = 0
    skipped = 0
    for entry in entries:
        record = runtime_record_from_entry(entry, shared_schema, extension_schema)
        if record["record_id"] in existing_ids:
            skipped += 1
            continue
        records.append(record)
        existing_ids.add(record["record_id"])
        added += 1

    save_json_records(runtime_json, records)
    runtime_md.write_text(render_runtime_markdown(records, preamble), encoding="utf-8")
    return {"added": added, "skipped": skipped}


def persist_verified_entries(target: Path, entries: list[dict[str, Any]]) -> dict[str, Any]:
    blocks = [verified_block_from_entry(entry) for entry in entries]
    append_entries(target, blocks)
    return {"added": len(blocks)}


def git_persist_files(skill_dir: Path, paths: list[Path], commit_message: str) -> dict[str, Any]:
    repo_root_result = subprocess.run(
        ["git", "-C", str(skill_dir), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if repo_root_result.returncode != 0:
        raise SystemExit(repo_root_result.stderr.strip() or "Unable to resolve git repo root for --git-persist.")
    repo_root = repo_root_result.stdout.strip()

    add_result = subprocess.run(
        ["git", "-C", repo_root, "add", *[str(path) for path in paths]],
        check=False,
        capture_output=True,
        text=True,
    )
    if add_result.returncode != 0:
        raise SystemExit(add_result.stderr.strip() or "git add failed for learning artifacts.")

    staged_result = subprocess.run(
        ["git", "-C", repo_root, "diff", "--cached", "--quiet"],
        check=False,
        capture_output=True,
        text=True,
    )
    if staged_result.returncode == 0:
        return {"committed": False, "pushed": False}

    commit_result = subprocess.run(
        ["git", "-C", repo_root, "commit", "-m", commit_message],
        check=False,
        capture_output=True,
        text=True,
    )
    if commit_result.returncode != 0:
        raise SystemExit(commit_result.stderr.strip() or commit_result.stdout.strip() or "git commit failed.")

    push_result = subprocess.run(
        ["git", "-C", repo_root, "push"],
        check=False,
        capture_output=True,
        text=True,
    )
    if push_result.returncode != 0:
        raise SystemExit(push_result.stderr.strip() or push_result.stdout.strip() or "git push failed.")

    return {"committed": True, "pushed": True}


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a runtime or verified learning entry.")
    parser.add_argument("--skill-dir", required=True, help="Absolute path to the target skill directory.")
    parser.add_argument("--kind", choices=("runtime", "verified"), required=True)
    parser.add_argument("--topic", help="Short topic label for a single entry.")
    parser.add_argument("--summary", help="One-line summary for a single entry.")
    parser.add_argument(
        "--status",
        choices=("observed", "repaired", "unresolved", "promoted"),
        default="observed",
        help="Structured runtime status label for single-entry mode.",
    )
    parser.add_argument(
        "--confidence",
        choices=("low", "medium", "high"),
        default="medium",
        help="Confidence tier for the learning record in single-entry mode.",
    )
    parser.add_argument("--failed-path", help="Concrete failing path observed in single-entry mode.")
    parser.add_argument("--repaired-path", help="Concrete repaired path validated in single-entry mode.")
    parser.add_argument("--source-skill", help="Skill that generated the incident.")
    parser.add_argument("--source-session", help="Session identifier or transcript locator.")
    parser.add_argument("--agent", help="Agent or engine that observed the incident.")
    parser.add_argument("--target-file", action="append", default=[], help="File touched or implicated by this incident.")
    parser.add_argument(
        "--extensions-json",
        help="JSON object string containing skill-specific extension fields for single-entry mode.",
    )
    parser.add_argument(
        "--canonical-change-candidate",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether the incident suggests canonical guidance may need an update.",
    )
    parser.add_argument("--evidence", action="append", default=[], help="Concrete evidence line. Repeatable.")
    parser.add_argument("--notes", action="append", default=[], help="Extra note line. Repeatable.")
    parser.add_argument("--batch-json", help="JSON array or object-with-records payload for batch append.")
    parser.add_argument("--batch-json-file", help="Path to a JSON batch payload.")
    parser.add_argument(
        "--git-persist",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Commit and push the learning artifacts after writing them.",
    )
    parser.add_argument(
        "--git-commit-message",
        help="Commit message to use with --git-persist.",
    )
    args = parser.parse_args()

    if args.batch_json and args.batch_json_file:
        raise SystemExit("Use only one of --batch-json or --batch-json-file.")

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    references_dir = skill_dir / "references"
    target = references_dir / ("runtime-learning.md" if args.kind == "runtime" else "verified-learning.md")
    runtime_json = references_dir / "runtime-learning.json"

    entries = load_batch_entries(args)

    touched_paths: list[Path] = []
    if args.kind == "runtime":
        shared_schema = load_shared_runtime_schema()
        extension_schema = load_skill_extension_schema(skill_dir)
        result = persist_runtime_records(
            runtime_json=runtime_json,
            runtime_md=target,
            entries=entries,
            shared_schema=shared_schema,
            extension_schema=extension_schema,
        )
        touched_paths = [runtime_json, target]
        message = (
            f"[OK] Runtime learning write complete for {target} and {runtime_json}"
            f" (added={result['added']}, skipped={result['skipped']})"
        )
    else:
        result = persist_verified_entries(target, entries)
        touched_paths = [target]
        message = f"[OK] Verified learning write complete for {target} (added={result['added']})"

    git_result = {"committed": False, "pushed": False}
    if args.git_persist:
        commit_message = args.git_commit_message or f"Auto-learn {args.kind} entries"
        git_result = git_persist_files(skill_dir, touched_paths, commit_message)
        message += f" [git committed={git_result['committed']} pushed={git_result['pushed']}]"

    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
