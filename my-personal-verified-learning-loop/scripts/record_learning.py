#!/usr/bin/env python3
"""Append a structured runtime or verified learning entry to a target skill."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def append_entry(target: Path, heading: str, lines: list[str]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    block = "\n".join([heading, "", *lines, ""])
    target.write_text(existing + block, encoding="utf-8")


def load_json_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit(f"{path} must contain a JSON array.")
    return payload


def save_json_records(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def stable_json(value):
    if isinstance(value, dict):
        return {key: stable_json(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [stable_json(item) for item in value]
    return value


def compute_runtime_record_id(record: dict) -> str:
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
            "agent": record.get("agent"),
            "target_files": sorted(record.get("target_files") or []),
            "canonical_change_candidate": record.get("canonical_change_candidate", False),
            "extensions": stable_json(extensions),
        }
    digest = hashlib.sha256(
        json.dumps(digest_source, sort_keys=True, ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    return digest[:16]


def render_runtime_markdown(records: list[dict]) -> str:
    lines = ["# Runtime Learning", ""]
    if not records:
        lines.extend(
            [
                "No runtime incidents have been recorded yet.",
                "",
            ]
        )
        return "\n".join(lines)

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a runtime or verified learning entry.")
    parser.add_argument("--skill-dir", required=True, help="Absolute path to the target skill directory.")
    parser.add_argument("--kind", choices=("runtime", "verified"), required=True)
    parser.add_argument("--topic", required=True, help="Short topic label for the entry heading.")
    parser.add_argument("--summary", required=True, help="One-line summary of the learning.")
    parser.add_argument(
        "--status",
        choices=("observed", "repaired", "unresolved", "promoted"),
        default="observed",
        help="Structured runtime status label.",
    )
    parser.add_argument(
        "--confidence",
        choices=("low", "medium", "high"),
        default="medium",
        help="Confidence tier for the learning record.",
    )
    parser.add_argument("--failed-path", help="Concrete failing path that was observed.")
    parser.add_argument("--repaired-path", help="Concrete repaired path that was validated.")
    parser.add_argument("--source-skill", help="Skill that generated the incident.")
    parser.add_argument("--source-session", help="Session identifier or transcript locator.")
    parser.add_argument("--agent", help="Agent or engine that observed the incident.")
    parser.add_argument("--target-file", action="append", default=[], help="File touched or implicated by this incident.")
    parser.add_argument(
        "--extensions-json",
        help="JSON object string containing skill-specific extension fields for runtime incidents.",
    )
    parser.add_argument(
        "--canonical-change-candidate",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether the incident suggests canonical guidance may need an update.",
    )
    parser.add_argument("--evidence", action="append", default=[], help="Concrete evidence line. Repeatable.")
    parser.add_argument("--notes", action="append", default=[], help="Extra note line. Repeatable.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    references_dir = skill_dir / "references"
    target = references_dir / ("runtime-learning.md" if args.kind == "runtime" else "verified-learning.md")
    runtime_json = references_dir / "runtime-learning.json"
    extensions = json.loads(args.extensions_json) if args.extensions_json else {}
    if not isinstance(extensions, dict):
        raise SystemExit("--extensions-json must decode to a JSON object.")

    heading = f"## {utc_now()} - {args.topic}"
    lines = [f"- Summary: {args.summary}"]
    lines.append(f"- Status: {args.status}")
    lines.append(f"- Confidence: {args.confidence}")
    if args.failed_path:
        lines.append(f"- Failed path: `{args.failed_path}`")
    if args.repaired_path:
        lines.append(f"- Repaired path: `{args.repaired_path}`")
    if args.source_skill:
        lines.append(f"- Source skill: `{args.source_skill}`")
    if args.source_session:
        lines.append(f"- Source session: `{args.source_session}`")
    if args.agent:
        lines.append(f"- Agent: `{args.agent}`")
    if args.target_file:
        lines.append("- Target files:")
        for item in args.target_file:
            lines.append(f"  - `{item}`")
    if extensions:
        lines.append(f"- Extensions JSON: `{json.dumps(extensions, sort_keys=True)}`")
    lines.append(f"- Canonical change candidate: `{str(args.canonical_change_candidate).lower()}`")
    for item in args.evidence:
        lines.append(f"- Evidence: {item}")
    for item in args.notes:
        lines.append(f"- Note: {item}")

    if args.kind == "runtime":
        records = load_json_records(runtime_json)
        for item in records:
            if "record_id" not in item or not item.get("record_id"):
                item["record_id"] = compute_runtime_record_id(item)
        record = {
            "timestamp": heading.removeprefix("## ").split(" - ", 1)[0],
            "kind": args.kind,
            "topic": args.topic,
            "summary": args.summary,
            "status": args.status,
            "confidence": args.confidence,
            "failed_path": args.failed_path,
            "repaired_path": args.repaired_path,
            "evidence": args.evidence,
            "notes": args.notes,
            "source_skill": args.source_skill,
            "source_session": args.source_session,
            "agent": args.agent,
            "target_files": args.target_file,
            "extensions": extensions,
            "canonical_change_candidate": args.canonical_change_candidate,
        }
        record["record_id"] = compute_runtime_record_id(record)
        existing_ids = {item["record_id"] for item in records}
        if record["record_id"] in existing_ids:
            save_json_records(runtime_json, records)
            target.write_text(render_runtime_markdown(records), encoding="utf-8")
            print(f"[OK] Skipped duplicate runtime learning for {target} and {runtime_json}")
            return 0
        records.append(record)
        save_json_records(runtime_json, records)
        target.write_text(render_runtime_markdown(records), encoding="utf-8")
    else:
        append_entry(target, heading, lines)

    if args.kind == "runtime":
        print(f"[OK] Appended runtime learning to {target} and {runtime_json}")
    else:
        print(f"[OK] Appended verified learning to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
