#!/bin/bash
# Cross-tool AI setup — full verification
# Run from anywhere. Checks global config, skills, repos, memory symlinks,
# MCP wrappers, Gemini wiring, and the local browser automation layer.

PASS=0
FAIL=0
WARN=0

ok()   { echo "  ✅ $1"; ((PASS++)); }
fail() { echo "  ❌ $1"; ((FAIL++)); }
warn() { echo "  ⚠️  $1"; ((WARN++)); }

echo "========================================="
echo "1. GLOBAL CONFIG"
echo "========================================="

# Global rules
if [ -f ~/.claude/CLAUDE.md ]; then
    ok "~/.claude/CLAUDE.md exists ($(wc -c < ~/.claude/CLAUDE.md | tr -d ' ') bytes)"
else
    fail "~/.claude/CLAUDE.md MISSING"
fi

# Codex global symlink
if [ -L ~/.codex/AGENTS.md ]; then
    target=$(readlink ~/.codex/AGENTS.md)
    if [ -f ~/.codex/AGENTS.md ]; then
        ok "~/.codex/AGENTS.md → $target (target exists)"
    else
        fail "~/.codex/AGENTS.md → $target (BROKEN — target missing)"
    fi
else
    fail "~/.codex/AGENTS.md is NOT a symlink"
fi

# Gemini global symlink
if [ -L ~/.gemini/GEMINI.md ]; then
    target=$(readlink ~/.gemini/GEMINI.md)
    if [ -f ~/.gemini/GEMINI.md ]; then
        ok "~/.gemini/GEMINI.md → $target (target exists)"
    else
        fail "~/.gemini/GEMINI.md → $target (BROKEN — target missing)"
    fi
else
    fail "~/.gemini/GEMINI.md is NOT a symlink"
fi

echo ""
echo "========================================="
echo "2. SKILLS"
echo "========================================="

if [ -f ~/.agents/skills/setup/sync-skills.py ]; then
    sync_output="$(python3 ~/.agents/skills/setup/sync-skills.py --check 2>&1)"
    sync_status=$?
    if [ "$sync_status" -eq 0 ]; then
        ok "Shared personal skills synced across Claude Code, Codex, and Gemini"
    else
        fail "Shared personal skills DESYNC"
        printf '%s\n' "$sync_output" | sed 's/^/    /'
    fi
else
    fail "~/.agents/skills/setup/sync-skills.py missing"
fi

if [ -L ~/.gemini/antigravity/global_skills ]; then
    target=$(readlink ~/.gemini/antigravity/global_skills)
    if [ -d "$target" ]; then
        ok "~/.gemini/antigravity/global_skills → $target"
    else
        fail "~/.gemini/antigravity/global_skills → $target (BROKEN — target missing)"
    fi
else
    fail "~/.gemini/antigravity/global_skills is NOT a symlink"
fi

if [ -f ~/Library/LaunchAgents/com.codex.skill-sync-guard.plist ]; then
    ok "LaunchAgent plist installed for skill sync guard"
else
    fail "LaunchAgent plist missing for skill sync guard"
fi

if launchctl print "gui/$(id -u)/com.codex.skill-sync-guard" >/dev/null 2>&1; then
    ok "LaunchAgent com.codex.skill-sync-guard loaded"
else
    fail "LaunchAgent com.codex.skill-sync-guard not loaded"
fi

echo ""
echo "========================================="
echo "3. REPOS — CLAUDE.md ↔ AGENTS.md"
echo "========================================="

while IFS= read -r dir; do

    echo ""
    echo "  --- $(basename "$dir") ---"

    if [ -f "$dir/CLAUDE.md" ] && [ ! -L "$dir/CLAUDE.md" ]; then
        ok "CLAUDE.md — real file ($(wc -c < "$dir/CLAUDE.md" | tr -d ' ') bytes)"
    elif [ -L "$dir/CLAUDE.md" ]; then
        warn "CLAUDE.md is a symlink (should be the real file)"
    elif [ ! -f "$dir/CLAUDE.md" ] && [ -f "$dir/AGENTS.md" ]; then
        fail "CLAUDE.md MISSING (only AGENTS.md exists — should rename)"
    fi

    if [ -L "$dir/AGENTS.md" ]; then
        target=$(readlink "$dir/AGENTS.md")
        if [ "$target" = "CLAUDE.md" ]; then
            ok "AGENTS.md → CLAUDE.md"
        else
            warn "AGENTS.md → $target (expected: CLAUDE.md)"
        fi
    elif [ -f "$dir/AGENTS.md" ] && [ -f "$dir/CLAUDE.md" ]; then
        fail "AGENTS.md is a REAL FILE (should be symlink → CLAUDE.md)"
    elif [ ! -f "$dir/AGENTS.md" ] && [ -f "$dir/CLAUDE.md" ]; then
        fail "AGENTS.md MISSING (CLAUDE.md exists but no symlink)"
    fi

    if [ -f "$dir/CLAUDE_MEMORY.md" ]; then
        ok "CLAUDE_MEMORY.md exists ($(wc -c < "$dir/CLAUDE_MEMORY.md" | tr -d ' ') bytes)"
    fi
done < <({
    find "/Users/$USER/My Drive" -maxdepth 6 \( -name "CLAUDE.md" -o -name "AGENTS.md" \) -print 2>/dev/null | \
        while IFS= read -r path; do
            dirname "$path"
        done

    if [ -e "$HOME/.agents/skills/CLAUDE.md" ] || [ -e "$HOME/.agents/skills/AGENTS.md" ]; then
        printf '%s\n' "$HOME/.agents/skills"
    fi
} | sort -u)

echo ""
echo "========================================="
echo "4. MEMORY SYMLINKS (native → repo)"
echo "========================================="

for memdir in ~/.claude/projects/*/memory/; do
    [ -d "$memdir" ] || continue
    encoded=$(basename "$(dirname "$memdir")")

    if [ -L "$memdir/MEMORY.md" ]; then
        target=$(readlink "$memdir/MEMORY.md")
        if [ -f "$target" ]; then
            ok "$encoded → $(basename "$target")"
        else
            fail "BROKEN SYMLINK: $encoded → $target"
        fi
    elif [ -f "$memdir/MEMORY.md" ]; then
        size=$(wc -c < "$memdir/MEMORY.md" | tr -d ' ')
        if [ "$size" -gt 10 ]; then
            fail "NOT MIGRATED ($size bytes): $encoded"
        fi
    fi
done

echo ""
echo "========================================="
echo "5. MCP WRAPPERS"
echo "========================================="

wrapper_count=$(ls ~/.codex/mcp/*.sh 2>/dev/null | wc -l | tr -d ' ')
if [ "$wrapper_count" -gt 0 ]; then
    ok "$wrapper_count MCP wrapper scripts found"
    for w in ~/.codex/mcp/*.sh; do
        if [ -x "$w" ]; then
            ok "$(basename "$w") — executable"
        else
            fail "$(basename "$w") — NOT executable (run: chmod +x $w)"
        fi
    done
else
    warn "No MCP wrapper scripts in ~/.codex/mcp/"
fi

if [ -f ~/.codex/config.toml ]; then
    if rg -q '\[mcp_servers\."brave-devtools"\]' ~/.codex/config.toml; then
        ok "Codex config registers brave-devtools"
    else
        fail "Codex config missing brave-devtools registration"
    fi

    if rg -q '\[mcp_servers\."chrome-devtools"\]' ~/.codex/config.toml; then
        ok "Codex config registers chrome-devtools"
    else
        fail "Codex config missing chrome-devtools registration"
    fi
else
    fail "~/.codex/config.toml MISSING"
fi

if [ -f ~/.claude.json ]; then
    if rg -q '"brave-devtools"' ~/.claude.json; then
        ok "Claude Code config registers brave-devtools"
    else
        fail "Claude Code config missing brave-devtools registration"
    fi

    if rg -q '"chrome-devtools"' ~/.claude.json; then
        ok "Claude Code config registers chrome-devtools"
    else
        fail "Claude Code config missing chrome-devtools registration"
    fi
else
    fail "~/.claude.json MISSING"
fi

if [ -x ~/.codex/browser-control/cleanup-browser-parasites.sh ]; then
    ok "Persistent browser parasite guard script installed"
else
    fail "Persistent browser parasite guard script missing at ~/.codex/browser-control/cleanup-browser-parasites.sh"
fi

if [ -f ~/Library/LaunchAgents/com.codex.browser-parasite-guard.plist ]; then
    ok "LaunchAgent plist installed for browser parasite guard"
else
    fail "LaunchAgent plist missing for browser parasite guard"
fi

if launchctl print "gui/$(id -u)/com.codex.browser-parasite-guard" >/dev/null 2>&1; then
    ok "LaunchAgent com.codex.browser-parasite-guard loaded"
else
    warn "LaunchAgent com.codex.browser-parasite-guard not currently loaded"
fi

if rg -q -- '--watch' ~/Library/LaunchAgents/com.codex.browser-parasite-guard.plist && \
   rg -q 'KeepAlive' ~/Library/LaunchAgents/com.codex.browser-parasite-guard.plist && \
   rg -q -- '--watch' ~/.codex/browser-control/cleanup-browser-parasites.sh; then
    ok "Browser parasite guard runs in continuous lightweight watch mode"
else
    warn "Browser parasite guard is not configured for continuous watch mode"
fi

if rg -q 'BROWSER_LABEL="Chrome"' ~/.codex/mcp/chrome-devtools-wrapper.sh && rg -q 'brave-devtools-server.mjs' ~/.codex/mcp/chrome-devtools-wrapper.sh; then
    ok "chrome-devtools wrapper uses the explicit-identity local browser MCP server"
else
    warn "chrome-devtools wrapper does not appear to use the explicit-identity local browser MCP server"
fi

if [ -x ~/.agents/skills/setup/browser-control/configure-antigravity-browser.sh ]; then
    ok "Antigravity browser isolation script installed"
else
    warn "Antigravity browser isolation script missing"
fi

antigravity_browser_check="$(python3 - <<'PY' 2>/dev/null
import base64, sqlite3, sys
from pathlib import Path

db_path = Path.home() / "Library/Application Support/Antigravity/User/globalStorage/state.vscdb"
if not db_path.exists():
    print("missing-db")
    sys.exit(0)

def read_varint(data, idx):
    shift = 0
    value = 0
    while True:
        byte = data[idx]
        idx += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, idx
        shift += 7

def parse_msg(data):
    fields = {}
    idx = 0
    while idx < len(data):
        tag, idx = read_varint(data, idx)
        field = tag >> 3
        wire = tag & 7
        if wire == 2:
            length, idx = read_varint(data, idx)
            fields.setdefault(field, []).append(data[idx:idx + length])
            idx += length
        elif wire == 0:
            value, idx = read_varint(data, idx)
            fields.setdefault(field, []).append(value)
        else:
            raise ValueError(wire)
    return fields

def setting_value(row_msg):
    row = parse_msg(row_msg)
    return base64.b64decode(row[1][0])

with sqlite3.connect(db_path) as db:
    row = db.execute("select value from ItemTable where key='antigravityUnifiedStateSync.browserPreferences'").fetchone()
if not row:
    print("missing-topic")
    sys.exit(0)

topic = parse_msg(base64.b64decode(row[0]))
values = {}
wanted = {
    "browser_cdp_port_sentinel_key",
    "browser_user_profile_path_sentinel_key",
    "browser_chrome_binary_path_sentinel_key",
}
for entry_msg in topic.get(1, []):
    entry = parse_msg(entry_msg)
    key = entry[1][0].decode()
    if key in wanted and 2 in entry:
        values[key] = setting_value(entry[2][0])

def int_field(data):
    msg = parse_msg(data)
    return msg.get(1, [0])[0]

def str_field(data):
    msg = parse_msg(data)
    return msg.get(1, [b""])[0].decode()

port = int_field(values.get("browser_cdp_port_sentinel_key", b""))
profile = str_field(values.get("browser_user_profile_path_sentinel_key", b""))
binary = str_field(values.get("browser_chrome_binary_path_sentinel_key", b""))
print(f"{port}|{profile}|{binary}")
PY
)"

if [ "$antigravity_browser_check" = "9322|$HOME/.gemini/antigravity-browser-profile|/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    ok "Antigravity browser launcher is isolated from Brave/Chrome live sessions"
else
    warn "Antigravity browser launcher isolation not verified ($antigravity_browser_check)"
fi

if rg -q "Sessions/\\*\\*\\*" ~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh && \
   rg -q "Last Session" ~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh && \
   rg -q "Current Session" ~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh; then
    ok "Chrome AI-safe launcher excludes source session restore files from sync"
else
    warn "Chrome AI-safe launcher may still sync source session restore files"
fi

if rg -q 'profile.exit_type = "Normal"' ~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh; then
    ok "Chrome AI-safe launcher normalizes cloned profile exit state"
else
    warn "Chrome AI-safe launcher does not appear to normalize cloned profile exit state"
fi

if rg -q 'mirror-chrome-ai-safe-session.sh' ~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh && \
   [ -x ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh ]; then
    ok "Chrome AI-safe launcher starts the background session mirror"
else
    warn "Chrome AI-safe launcher does not appear to start the background session mirror"
fi

if rg -Fq '"$clone_profile/Sessions/" "$source_profile/Sessions/"' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh; then
    ok "Chrome AI-safe session mirror syncs clone session artifacts back to the real profile"
else
    warn "Chrome AI-safe session mirror does not appear to sync session artifacts back to the real profile"
fi

if rg -q 'sync_durable_profile_once' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh && \
   rg -q 'rsync -a --delete' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh && \
   rg -q 'sync_sqlite_files_once' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh && \
   rg -q 'SQLite format 3' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh && \
   rg -q 'sync_root_durable_artifacts_once' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh; then
    ok "Chrome AI-safe mirror syncs the full durable active profile with SQLite-safe copies"
else
    warn "Chrome AI-safe mirror does not appear to sync the full durable active profile safely"
fi

if rg -q 'ANTIGRAVITY_PROFILE_DIR' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh && \
   rg -q -- '--remote-debugging-port=9322' ~/.codex/chrome-cdp-client/mirror-chrome-ai-safe-session.sh; then
    ok "Chrome AI-safe mirror ignores the isolated Antigravity browser when detecting real Chrome"
else
    warn "Chrome AI-safe mirror may confuse isolated Antigravity Chrome with real Chrome"
fi

if rg -q 'BROWSER_LABEL="Brave"' ~/.codex/mcp/brave-devtools-wrapper.sh && rg -q 'brave-devtools-server.mjs' ~/.codex/mcp/brave-devtools-wrapper.sh; then
    ok "brave-devtools wrapper uses the explicit-identity local browser MCP server"
else
    warn "brave-devtools wrapper does not appear to use the explicit-identity local browser MCP server"
fi

if rg -q 'cleanup-browser-parasites.sh' ~/.codex/mcp/brave-devtools-wrapper.sh && \
   rg -q 'cleanup-browser-parasites.sh' ~/.codex/mcp/chrome-devtools-wrapper.sh && \
   rg -q 'cleanup-browser-parasites.sh' ~/.codex/brave-cdp-client/launch-brave-ai-safe.sh && \
   rg -q 'cleanup-browser-parasites.sh' ~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh; then
    ok "Browser wrappers and AI-safe launchers run the parasite guard before starting work"
else
    warn "Browser wrappers and launchers do not all appear to run the parasite guard"
fi

if rg -q 'executable-path /Applications/Brave Browser.app/Contents/MacOS/Brave Browser' ~/.codex/browser-control/cleanup-browser-parasites.sh && \
   rg -q 'executable-path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome' ~/.codex/browser-control/cleanup-browser-parasites.sh && \
   rg -q 'chrome-headless-shell' ~/.codex/browser-control/cleanup-browser-parasites.sh && \
   rg -q 'is_playwright_launched_real_browser' ~/.codex/browser-control/cleanup-browser-parasites.sh; then
    ok "Browser parasite guard targets attached-browser Playwright, direct real-browser Playwright children, and stale temporary headless browsers"
else
    warn "Browser parasite guard does not appear to target the expected parasite browser patterns"
fi

echo ""
echo "========================================="
echo "6. BROWSER AUTOMATION LAYER"
echo "========================================="

browser_files=(
    ~/.codex/mcp/brave-devtools-wrapper.sh
    ~/.codex/mcp/chrome-devtools-wrapper.sh
    ~/.codex/brave-cdp-client/brave-devtools-server.mjs
    ~/.codex/brave-cdp-client/launch-brave-ai-safe.sh
    ~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh
)

for file in "${browser_files[@]}"; do
    if [ -e "$file" ]; then
        if [ -x "$file" ] || [[ "$file" == *.mjs ]]; then
            ok "$(basename "$file") present"
        else
            fail "$(basename "$file") present but NOT executable"
        fi
    else
        fail "$(basename "$file") MISSING"
    fi
done

if curl -sf http://127.0.0.1:9222/json/version >/dev/null 2>&1; then
    ok "Brave CDP endpoint responding on 127.0.0.1:9222"
else
    if pgrep -x "Brave Browser" >/dev/null 2>&1; then
        if pgrep -fal "Brave Browser" | rg -q -- '--remote-debugging-port=9222'; then
            fail "Brave appears to be running with remote debugging args but 127.0.0.1:9222 is not responding"
        else
            warn "Brave is running without CDP on 127.0.0.1:9222 (expected if not launched via Brave AI-safe)"
        fi
    else
        ok "Brave is not currently running; 127.0.0.1:9222 is expected to be absent until Brave AI-safe is launched"
    fi
fi

if curl -sf http://127.0.0.1:9223/json/version >/dev/null 2>&1; then
    ok "Chrome CDP endpoint responding on 127.0.0.1:9223"
else
    warn "Chrome CDP endpoint not responding on 127.0.0.1:9223"
fi

twitter_scraper_root="/Users/benjaminperry/My Drive/ProStrike Holdings/TOOLS/Twitter:X Scraper"
if [ -d "$twitter_scraper_root" ]; then
    browser_control_file="$twitter_scraper_root/src/lib/browser-control.js"
    grok_browser_file="$twitter_scraper_root/src/lib/grok-browser.js"
    browser_search_file="$twitter_scraper_root/src/lib/browser-search.js"

    if [ -f "$browser_control_file" ] && \
       rg -q 'assertBrowserIdentity' "$grok_browser_file" && \
       rg -q 'ensureResponsiveTarget' "$grok_browser_file" && \
       rg -q 'assertBrowserIdentity' "$browser_search_file" && \
       rg -q 'ensureResponsiveTarget' "$browser_search_file"; then
        ok "Twitter:X Scraper mirrors the shared browser guardrails in grok-browser/browser-search"
    else
        warn "Twitter:X Scraper exists but does not appear aligned with the shared browser guardrails"
    fi
fi

echo ""
echo "========================================="
echo "SUMMARY"
echo "========================================="
echo "  ✅ Pass: $PASS"
echo "  ❌ Fail: $FAIL"
echo "  ⚠️  Warn: $WARN"
if [ "$FAIL" -eq 0 ]; then
    echo ""
    echo "  All checks passed."
    exit 0
else
    echo ""
    echo "  $FAIL issue(s) to fix."
    exit 1
fi
