#!/usr/bin/env bash
# Hermes VPS setup — targeted verification
# This intentionally excludes macOS-only checks from setup/verify.sh
# such as LaunchAgents, AppleScript, Keychain, and live Brave/Chrome CDP.

set -u

PASS=0
FAIL=0
WARN=0

ok()   { echo "  ✅ $1"; ((PASS++)); }
fail() { echo "  ❌ $1"; ((FAIL++)); }
warn() { echo "  ⚠️  $1"; ((WARN++)); }
section() { echo ""; echo "========================================="; echo "$1"; echo "========================================="; }

HOME_DIR="${HOME:-/home/hermes}"
SKILLS_ROOT="$HOME_DIR/.agents/skills"

section "1. VPS BASELINE"

if [ "$(uname -s 2>/dev/null)" = "Linux" ]; then
  ok "Running on Linux"
else
  fail "This verifier is for Hermes/Linux VPS only; got: $(uname -s 2>/dev/null || echo unknown)"
fi

if [ "$HOME_DIR" = "/home/hermes" ]; then
  ok "HOME is /home/hermes"
else
  warn "HOME is $HOME_DIR, expected /home/hermes for Ben's Hermes VPS"
fi

if [ -d "$SKILLS_ROOT/.git" ]; then
  ok "Skills repo present at $SKILLS_ROOT"
else
  fail "Skills repo missing at $SKILLS_ROOT"
fi

section "2. GLOBAL RULES"

if [ -f "$HOME_DIR/.claude/CLAUDE.md" ] && [ ! -L "$HOME_DIR/.claude/CLAUDE.md" ]; then
  ok "~/.claude/CLAUDE.md exists as real file"
else
  fail "~/.claude/CLAUDE.md missing or not a real file"
fi

if [ -L "$HOME_DIR/.codex/AGENTS.md" ] && [ "$(readlink "$HOME_DIR/.codex/AGENTS.md")" = "../.claude/CLAUDE.md" ] && [ -f "$HOME_DIR/.codex/AGENTS.md" ]; then
  ok "~/.codex/AGENTS.md -> ../.claude/CLAUDE.md"
else
  fail "~/.codex/AGENTS.md is not the expected symlink"
fi

if [ -L "$HOME_DIR/.gemini/GEMINI.md" ] && [ "$(readlink "$HOME_DIR/.gemini/GEMINI.md")" = "../.claude/CLAUDE.md" ] && [ -f "$HOME_DIR/.gemini/GEMINI.md" ]; then
  ok "~/.gemini/GEMINI.md -> ../.claude/CLAUDE.md"
else
  fail "~/.gemini/GEMINI.md is not the expected symlink"
fi

if grep -q 'Hermes on the VPS is the primary executor' "$HOME_DIR/.claude/CLAUDE.md" 2>/dev/null && \
   grep -q 'GitHub/Git is the source of truth' "$HOME_DIR/.claude/CLAUDE.md" 2>/dev/null && \
   grep -q 'Google Drive is the human workspace' "$HOME_DIR/.claude/CLAUDE.md" 2>/dev/null; then
  ok "Global rules contain Hermes/GitHub/Drive operating model"
else
  warn "Global rules do not clearly contain the Hermes/GitHub/Drive operating model"
fi

section "3. HERMES SKILL DISCOVERY"

if grep -q -- '- /home/hermes/.agents/skills' "$HOME_DIR/.hermes/config.yaml" 2>/dev/null; then
  ok "Hermes config includes /home/hermes/.agents/skills as external skill dir"
else
  fail "Hermes config does not include /home/hermes/.agents/skills"
fi

if [ -f "$SKILLS_ROOT/setup/sync-skills.py" ]; then
  sync_output="$(python3 "$SKILLS_ROOT/setup/sync-skills.py" --check 2>&1)"
  sync_status=$?
  if [ "$sync_status" -eq 0 ]; then
    ok "Claude/Codex/Gemini personal-skill symlinks are synced"
  else
    fail "Claude/Codex/Gemini personal-skill symlinks are desynced"
    printf '%s\n' "$sync_output" | sed 's/^/    /'
  fi
else
  fail "sync-skills.py missing"
fi

if [ -L "$HOME_DIR/.gemini/antigravity/global_skills" ] && [ "$(readlink "$HOME_DIR/.gemini/antigravity/global_skills")" = "$SKILLS_ROOT" ]; then
  ok "Gemini Antigravity global_skills points to shared skills repo"
else
  fail "Gemini Antigravity global_skills is not pointed at shared skills repo"
fi

section "4. LINUX SKILL SYNC GUARD"

if [ -x "$HOME_DIR/.local/bin/sync-hermes-skills" ]; then
  ok "Linux sync script installed at ~/.local/bin/sync-hermes-skills"
else
  fail "Linux sync script missing or not executable"
fi

if grep -q 'sync-skills.py' "$HOME_DIR/.local/bin/sync-hermes-skills" 2>/dev/null && \
   grep -q -- '--ff-only' "$HOME_DIR/.local/bin/sync-hermes-skills" 2>/dev/null; then
  ok "Linux sync script pulls ff-only and repairs skill symlinks"
else
  fail "Linux sync script does not include expected ff-only + sync-skills behavior"
fi

if command -v systemctl >/dev/null 2>&1; then
  if systemctl --user is-active hermes-skills-sync.timer >/dev/null 2>&1; then
    ok "systemd user timer hermes-skills-sync.timer is active"
  else
    fail "systemd user timer hermes-skills-sync.timer is not active"
  fi
else
  fail "systemctl not available"
fi

section "5. VPS-SAFE MCP CONFIG"

mcp_output="$(python3 - <<'PY'
import json, sys
from pathlib import Path
home = Path.home()
expected = {"context7", "playwright-vps"}
failed = False
warned = False

def emit(level, msg):
    print(f"{level}\t{msg}")

for path in [home / ".claude.json", home / ".gemini/settings.json"]:
    try:
        data = json.loads(path.read_text())
    except Exception as exc:
        emit("fail", f"{path} is not readable JSON: {exc}")
        failed = True
        continue
    servers = data.get("mcpServers") or {}
    names = set(servers)
    if names == expected:
        emit("ok", f"{path} active MCP set is exactly {sorted(expected)}")
    else:
        emit("warn", f"{path} active MCP set is {sorted(names)}; recommended default is {sorted(expected)}")
        warned = True
    mac_paths = [str(v.get("command", "")) for v in servers.values() if isinstance(v, dict) and str(v.get("command", "")).startswith("/Users/")]
    if mac_paths:
        emit("fail", f"{path} contains macOS /Users MCP command paths")
        failed = True
    else:
        emit("ok", f"{path} has no macOS /Users MCP command paths")

codex = home / ".codex/config.toml"
text = codex.read_text() if codex.exists() else ""
if '[mcp_servers.context7]' in text and '[mcp_servers.playwright-vps]' in text:
    emit("ok", "~/.codex/config.toml registers context7 and playwright-vps")
else:
    emit("fail", "~/.codex/config.toml missing context7 or playwright-vps MCP registration")
    failed = True
if "/Users/" in text:
    emit("fail", "~/.codex/config.toml contains macOS /Users paths")
    failed = True
else:
    emit("ok", "~/.codex/config.toml has no macOS /Users paths")

sys.exit(2 if failed else (1 if warned else 0))
PY
)"
mcp_status=$?
while IFS=$'\t' read -r level msg; do
  [ -n "${level:-}" ] || continue
  case "$level" in
    ok) ok "$msg" ;;
    warn) warn "$msg" ;;
    fail) fail "$msg" ;;
    *) warn "$level $msg" ;;
  esac
done <<< "$mcp_output"
if [ "$mcp_status" -eq 0 ]; then
  ok "MCP config matches recommended minimal VPS default"
elif [ "$mcp_status" -eq 1 ]; then
  warn "MCP config is usable but differs from recommended minimal VPS default"
else
  fail "MCP config has VPS safety issues"
fi

for wrapper in "$HOME_DIR/.codex/mcp/context7-wrapper.sh" "$HOME_DIR/.codex/mcp/playwright-vps-wrapper.sh"; do
  if [ -x "$wrapper" ]; then
    if "$wrapper" --help >/tmp/verify-vps-wrapper-help.$$ 2>&1; then
      ok "$(basename "$wrapper") smoke test exits successfully"
    else
      warn "$(basename "$wrapper") --help did not exit successfully"
    fi
    rm -f /tmp/verify-vps-wrapper-help.$$
  else
    fail "$(basename "$wrapper") missing or not executable"
  fi
done

section "6. INTENTIONALLY EXCLUDED MAC-ONLY LAYERS"

ok "LaunchAgents/launchctl are intentionally excluded on Hermes VPS; systemd timer is used instead"
ok "macOS Keychain wrappers are intentionally excluded; use op/env/Hermes-native tools on VPS"
ok "Live Mac Brave/Chrome CDP and AppleScript are intentionally excluded; use isolated/headless VPS browser automation"

section "SUMMARY"
echo "  ✅ Pass: $PASS"
echo "  ❌ Fail: $FAIL"
echo "  ⚠️  Warn: $WARN"

if [ "$FAIL" -eq 0 ]; then
  echo ""
  echo "  Hermes VPS checks passed."
  exit 0
else
  echo ""
  echo "  $FAIL issue(s) to fix."
  exit 1
fi
