#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


SIMPLE_PLACEHOLDER_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
HTML_TAG_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)\b[^>]*>")
ICU_TYPES = {"plural", "select", "selectordinal", "number", "date", "time"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def classify_type(value: Any) -> str:
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, bool):
        return "boolean"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return "number"
    return type(value).__name__


def walk_schema(value: Any, prefix: str = "", schema: dict[str, str] | None = None) -> dict[str, str]:
    if schema is None:
        schema = {}

    if prefix:
        schema[prefix] = classify_type(value)

    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            walk_schema(child, child_prefix, schema)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_prefix = f"{prefix}[{index}]" if prefix else f"[{index}]"
            walk_schema(child, child_prefix, schema)

    return schema


def collect_string_leaves(value: Any, prefix: str = "", leaves: dict[str, str] | None = None) -> dict[str, str]:
    if leaves is None:
        leaves = {}

    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            collect_string_leaves(child, child_prefix, leaves)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_prefix = f"{prefix}[{index}]" if prefix else f"[{index}]"
            collect_string_leaves(child, child_prefix, leaves)
    elif isinstance(value, str):
        leaves[prefix] = value

    return leaves


def split_top_level(text: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    brace_depth = 0
    bracket_depth = 0
    paren_depth = 0
    in_quote: str | None = None
    escape = False

    for char in text:
        if in_quote:
            current.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == in_quote:
                in_quote = None
            continue

        if char == '"':
            in_quote = char
            current.append(char)
            continue

        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth = max(0, brace_depth - 1)
        elif char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth = max(0, bracket_depth - 1)
        elif char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth = max(0, paren_depth - 1)

        if (
            char == delimiter
            and brace_depth == 0
            and bracket_depth == 0
            and paren_depth == 0
        ):
            parts.append("".join(current).strip())
            current = []
            continue

        current.append(char)

    parts.append("".join(current).strip())
    return parts


def extract_top_level_brace_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    start: int | None = None
    depth = 0

    for index, char in enumerate(text):
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                tokens.append(text[start : index + 1])
                start = None

    return tokens


def extract_icu_options(text: str) -> list[str]:
    options: list[str] = []
    index = 0
    while index < len(text):
        while index < len(text) and text[index] in " \n\t,":
            index += 1
        if index >= len(text):
            break

        key_start = index
        while index < len(text) and text[index] not in " \n\t{":
            index += 1
        key = text[key_start:index].strip()

        while index < len(text) and text[index] in " \n\t":
            index += 1

        if not key:
            index += 1
            continue

        if key.startswith("offset:"):
            continue

        if index >= len(text) or text[index] != "{":
            continue

        depth = 0
        while index < len(text):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    index += 1
                    break
            index += 1

        options.append(key)

    return sorted(options)


def describe_brace_token(token: str) -> tuple[str, tuple[str, ...]]:
    inner = token[1:-1].strip()
    parts = split_top_level(inner)

    if len(parts) >= 2 and parts[1] in ICU_TYPES:
        variable = parts[0]
        icu_type = parts[1]
        option_keys = tuple(extract_icu_options(parts[2]) if len(parts) >= 3 else [])
        return (f"icu:{variable}:{icu_type}", option_keys)

    if SIMPLE_PLACEHOLDER_RE.fullmatch(inner):
        return (f"placeholder:{inner}", ())

    return (f"complex:{inner}", ())


def extract_string_signature(text: str) -> dict[str, Counter[Any]]:
    signature: dict[str, Counter[Any]] = {
        "placeholders": Counter(),
        "icu_heads": Counter(),
        "markup_tags": Counter(),
    }

    for token in extract_top_level_brace_tokens(text):
        kind, payload = describe_brace_token(token)
        if kind.startswith("placeholder:"):
            signature["placeholders"][kind.split(":", 1)[1]] += 1
        elif kind.startswith("icu:"):
            signature["icu_heads"][(kind, payload)] += 1

    for match in HTML_TAG_RE.finditer(text):
        signature["markup_tags"][match.group(1)] += 1

    return signature


def normalize_placeholders_for_hybrid_icu(signature: dict[str, Counter[Any]]) -> Counter[str]:
    """Ignore duplicate simple placeholders when the same variable also drives ICU.

    Source catalogs sometimes render a variable and then use a plural helper only
    for the suffix, for example:

    `Voir les {count} résultat{count, plural, one {} other {s}}`

    A native target translation may correctly collapse that into one ICU message:

    `View {count, plural, one {# result} other {# results}}`

    Both messages use the same runtime variable. Treating the source's extra
    simple `{count}` token as a hard mismatch creates false positives.
    """
    normalized = Counter(signature["placeholders"])
    icu_variables = {
        str(head).split(":", 2)[1]
        for head, _payload in signature["icu_heads"]
        if str(head).startswith("icu:")
    }
    for variable in icu_variables:
        if normalized[variable] > 0:
            normalized[variable] = 0
            del normalized[variable]
    return normalized


def compare_catalogs(source_path: Path, target_path: Path) -> dict[str, Any]:
    source_data = load_json(source_path)
    target_data = load_json(target_path)

    source_schema = walk_schema(source_data)
    target_schema = walk_schema(target_data)
    source_leaves = collect_string_leaves(source_data)
    target_leaves = collect_string_leaves(target_data)

    source_leaf_paths = set(source_leaves)
    target_leaf_paths = set(target_leaves)

    findings: dict[str, Any] = {
        "source": str(source_path),
        "target": str(target_path),
        "missing_keys": sorted(source_leaf_paths - target_leaf_paths),
        "extra_keys": sorted(target_leaf_paths - source_leaf_paths),
        "type_mismatches": [],
        "placeholder_mismatches": [],
        "icu_mismatches": [],
        "markup_mismatches": [],
    }

    for path in sorted(set(source_schema) & set(target_schema)):
        if source_schema[path] != target_schema[path]:
            findings["type_mismatches"].append(
                {
                    "path": path,
                    "source_type": source_schema[path],
                    "target_type": target_schema[path],
                }
            )

    for path in sorted(source_leaf_paths & target_leaf_paths):
        source_signature = extract_string_signature(source_leaves[path])
        target_signature = extract_string_signature(target_leaves[path])
        source_placeholders = normalize_placeholders_for_hybrid_icu(source_signature)
        target_placeholders = normalize_placeholders_for_hybrid_icu(target_signature)

        if source_placeholders != target_placeholders:
            findings["placeholder_mismatches"].append(
                {
                    "path": path,
                    "source": dict(source_placeholders),
                    "target": dict(target_placeholders),
                }
            )

        if source_signature["icu_heads"] != target_signature["icu_heads"]:
            findings["icu_mismatches"].append(
                {
                    "path": path,
                    "source": [
                        {"head": head, "count": count}
                        for head, count in sorted(source_signature["icu_heads"].items())
                    ],
                    "target": [
                        {"head": head, "count": count}
                        for head, count in sorted(target_signature["icu_heads"].items())
                    ],
                }
            )

        if source_signature["markup_tags"] != target_signature["markup_tags"]:
            findings["markup_mismatches"].append(
                {
                    "path": path,
                    "source": dict(source_signature["markup_tags"]),
                    "target": dict(target_signature["markup_tags"]),
                }
            )

    findings["has_findings"] = any(
        findings[key]
        for key in (
            "missing_keys",
            "extra_keys",
            "type_mismatches",
            "placeholder_mismatches",
            "icu_mismatches",
            "markup_mismatches",
        )
    )
    return findings
