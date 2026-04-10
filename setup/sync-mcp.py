#!/usr/bin/env python3
"""
Synchronize MCP server definitions from a single master file
to all AI tool configs (Claude Code, Claude Desktop/Cowork, Codex, Gemini).

Usage:
    python3 ~/.agents/skills/setup/sync-mcp.py          # sync all targets
    python3 ~/.agents/skills/setup/sync-mcp.py --dry-run # preview changes
    python3 ~/.agents/skills/setup/sync-mcp.py --check   # exit 1 if out of sync

Master file: ~/.agents/mcp-servers.json
"""

import json
import os
import re
import sys
from pathlib import Path

HOME = Path.home()
SCRIPT_DIR = Path(__file__).resolve().parent
MASTER = SCRIPT_DIR / "mcp-servers.json"

TARGETS = {
    "claude-code":    HOME / ".claude.json",
    "claude-desktop": HOME / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
    "codex":          HOME / ".codex" / "config.toml",
    "gemini":         HOME / ".gemini" / "settings.json",
}

ALL_TARGETS = list(TARGETS.keys())


# --- Master file ---

def load_master():
    with open(MASTER) as f:
        raw = json.load(f)
    servers = {}
    for name, defn in raw["servers"].items():
        command = defn["command"].replace("${HOME}", str(HOME))
        args = [a.replace("${HOME}", str(HOME)) for a in defn.get("args", [])]
        targets = defn.get("targets", ALL_TARGETS)
        servers[name] = {"command": command, "args": args, "targets": targets}
    return servers


def servers_for(servers, target):
    return {n: s for n, s in sorted(servers.items()) if target in s["targets"]}


# --- Claude Code CLI (~/.claude.json) ---

def build_claude_code(servers):
    return {
        name: {"command": s["command"], "args": s["args"], "env": {}, "type": "stdio"}
        for name, s in servers.items()
    }


def read_claude_code():
    path = TARGETS["claude-code"]
    with open(path) as f:
        data = json.load(f)
    return data, data.get("mcpServers", {})


def write_claude_code(data, mcp):
    data["mcpServers"] = mcp
    with open(TARGETS["claude-code"], "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# --- Claude Desktop / Cowork ---

def build_claude_desktop(servers):
    return {
        name: {"command": s["command"], "args": s["args"]}
        for name, s in servers.items()
    }


def read_claude_desktop():
    path = TARGETS["claude-desktop"]
    if not path.exists():
        return {}, {}
    with open(path) as f:
        data = json.load(f)
    return data, data.get("mcpServers", {})


def write_claude_desktop(data, mcp):
    data["mcpServers"] = mcp
    path = TARGETS["claude-desktop"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# --- Gemini CLI (~/.gemini/settings.json) ---

def build_gemini(servers):
    return {
        name: {"command": s["command"], "args": s["args"], "env": {}, "timeout": 60000}
        for name, s in servers.items()
    }


def read_gemini():
    path = TARGETS["gemini"]
    with open(path) as f:
        data = json.load(f)
    return data, data.get("mcpServers", {})


def write_gemini(data, mcp):
    data["mcpServers"] = mcp
    with open(TARGETS["gemini"], "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# --- Codex CLI (~/.codex/config.toml) ---

def build_codex_toml(servers):
    """Generate TOML text for mcp_servers sections."""
    lines = []
    for name, s in servers.items():
        needs_quote = bool(re.search(r"[^a-zA-Z0-9_]", name))
        header = f'[mcp_servers."{name}"]' if needs_quote else f"[mcp_servers.{name}]"
        lines.append(header)
        lines.append('type = "stdio"')
        lines.append(f'command = "{s["command"]}"')
        if s["args"]:
            args_str = ", ".join(f'"{a}"' for a in s["args"])
            lines.append(f"args = [{args_str}]")
        lines.append("")
    return "\n".join(lines)


def read_codex_non_mcp():
    """Read config.toml and return everything EXCEPT mcp_servers sections."""
    path = TARGETS["codex"]
    with open(path) as f:
        text = f.read()

    result_lines = []
    in_mcp = False
    for line in text.splitlines():
        if re.match(r"\[mcp_servers[\.\]]", line):
            in_mcp = True
            continue
        if line.startswith("[") and not line.startswith("[mcp_servers"):
            in_mcp = False
        if not in_mcp:
            result_lines.append(line)

    # Strip trailing blank lines
    while result_lines and result_lines[-1].strip() == "":
        result_lines.pop()

    return "\n".join(result_lines)


def read_codex_mcp_names():
    """Read current mcp_servers names from config.toml."""
    path = TARGETS["codex"]
    with open(path) as f:
        text = f.read()
    return set(re.findall(r'\[mcp_servers[.]"?([^]"]+)"?\]', text))


def write_codex(non_mcp_text, mcp_toml):
    with open(TARGETS["codex"], "w") as f:
        f.write(non_mcp_text)
        f.write("\n\n")
        f.write(mcp_toml)


# --- Diff reporting ---

def diff_names(old_mcp, new_mcp):
    old = set(old_mcp.keys()) if isinstance(old_mcp, dict) else old_mcp
    new = set(new_mcp.keys()) if isinstance(new_mcp, dict) else new_mcp
    return sorted(new - old), sorted(old - new)


def report(label, path, count, added, removed):
    status = "="
    if added or removed:
        status = "~"
    print(f"  {status} {label:20s} {count:2d} servers  {path}")
    if added:
        print(f"    + {', '.join(added)}")
    if removed:
        print(f"    - {', '.join(removed)}")


# --- Main ---

def main():
    dry_run = "--dry-run" in sys.argv
    check = "--check" in sys.argv

    if not MASTER.exists():
        print(f"Master file not found: {MASTER}")
        sys.exit(1)

    # Verify wrapper scripts exist
    servers = load_master()
    missing = []
    for name, s in servers.items():
        cmd = s["command"]
        if cmd.startswith("/") and not Path(cmd).exists():
            missing.append(f"  {name}: {cmd}")
    if missing:
        print("Warning: wrapper scripts not found:")
        print("\n".join(missing))
        print()

    print(f"Master: {len(servers)} servers from {MASTER}")
    if dry_run:
        print("(dry run — no files written)\n")
    elif check:
        print("(check mode — exit 1 if out of sync)\n")
    else:
        print()

    out_of_sync = False

    # Claude Code
    cc = servers_for(servers, "claude-code")
    cc_mcp = build_claude_code(cc)
    cc_data, cc_old = read_claude_code()
    added, removed = diff_names(cc_old, cc_mcp)
    if added or removed:
        out_of_sync = True
    report("Claude Code CLI", TARGETS["claude-code"], len(cc_mcp), added, removed)
    if not dry_run and not check:
        write_claude_code(cc_data, cc_mcp)

    # Claude Desktop / Cowork
    cd = servers_for(servers, "claude-desktop")
    cd_mcp = build_claude_desktop(cd)
    cd_data, cd_old = read_claude_desktop()
    added, removed = diff_names(cd_old, cd_mcp)
    if added or removed:
        out_of_sync = True
    report("Claude Desktop", TARGETS["claude-desktop"], len(cd_mcp), added, removed)
    if not dry_run and not check:
        write_claude_desktop(cd_data, cd_mcp)

    # Codex
    cx = servers_for(servers, "codex")
    cx_mcp_toml = build_codex_toml(cx)
    cx_non_mcp = read_codex_non_mcp()
    cx_old_names = read_codex_mcp_names()
    cx_new_names = set(cx.keys())
    added, removed = diff_names(cx_old_names, cx_new_names)
    if added or removed:
        out_of_sync = True
    report("Codex CLI", TARGETS["codex"], len(cx), added, removed)
    if not dry_run and not check:
        write_codex(cx_non_mcp, cx_mcp_toml)

    # Gemini
    gm = servers_for(servers, "gemini")
    gm_mcp = build_gemini(gm)
    gm_data, gm_old = read_gemini()
    added, removed = diff_names(gm_old, gm_mcp)
    if added or removed:
        out_of_sync = True
    report("Gemini CLI", TARGETS["gemini"], len(gm_mcp), added, removed)
    if not dry_run and not check:
        write_gemini(gm_data, gm_mcp)

    print()
    if check:
        if out_of_sync:
            print("Out of sync. Run without --check to fix.")
            sys.exit(1)
        else:
            print("All targets in sync.")
    elif dry_run:
        if out_of_sync:
            print("Changes pending. Run without --dry-run to apply.")
        else:
            print("Already in sync. Nothing to do.")
    else:
        print("Sync complete.")


if __name__ == "__main__":
    main()
