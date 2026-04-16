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

source_count=$(ls -d ~/.agents/skills/my-personal-*/ 2>/dev/null | wc -l | tr -d ' ')
claude_count=$(ls -d ~/.claude/skills/my-personal-*/ 2>/dev/null | wc -l | tr -d ' ')
codex_count=$(ls -d ~/.codex/skills/my-personal-*/ 2>/dev/null | wc -l | tr -d ' ')

echo "  Source (~/.agents/skills):  $source_count"
echo "  Claude Code symlinks:       $claude_count"
echo "  Codex symlinks:             $codex_count"

if [ "$source_count" -eq 0 ]; then
    warn "No personal skills found in ~/.agents/skills/"
elif [ "$source_count" = "$claude_count" ] && [ "$source_count" = "$codex_count" ]; then
    ok "All $source_count skills synced to both tools"
else
    fail "DESYNC: source=$source_count, claude=$claude_count, codex=$codex_count"
    for skill in ~/.agents/skills/my-personal-*/; do
        name=$(basename "$skill")
        [ ! -L ~/.claude/skills/"$name" ] && echo "    Missing in Claude Code: $name"
        [ ! -L ~/.codex/skills/"$name" ] && echo "    Missing in Codex: $name"
    done
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

echo ""
echo "========================================="
echo "3. REPOS — CLAUDE.md ↔ AGENTS.md"
echo "========================================="

{
    find "/Users/$USER/My Drive" -maxdepth 6 \( -name "CLAUDE.md" -o -name "AGENTS.md" \) -print 2>/dev/null | \
        while IFS= read -r path; do
            dirname "$path"
        done

    if [ -e "$HOME/.agents/skills/CLAUDE.md" ] || [ -e "$HOME/.agents/skills/AGENTS.md" ]; then
        printf '%s\n' "$HOME/.agents/skills"
    fi
} | sort -u | while IFS= read -r dir; do

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
done

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

if rg -q 'BROWSER_LABEL="Chrome"' ~/.codex/mcp/chrome-devtools-wrapper.sh && rg -q 'brave-devtools-server.mjs' ~/.codex/mcp/chrome-devtools-wrapper.sh; then
    ok "chrome-devtools wrapper uses the explicit-identity local browser MCP server"
else
    warn "chrome-devtools wrapper does not appear to use the explicit-identity local browser MCP server"
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

if rg -q 'BROWSER_LABEL="Brave"' ~/.codex/mcp/brave-devtools-wrapper.sh && rg -q 'brave-devtools-server.mjs' ~/.codex/mcp/brave-devtools-wrapper.sh; then
    ok "brave-devtools wrapper uses the explicit-identity local browser MCP server"
else
    warn "brave-devtools wrapper does not appear to use the explicit-identity local browser MCP server"
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
else
    echo ""
    echo "  $FAIL issue(s) to fix."
fi
