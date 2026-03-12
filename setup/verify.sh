#!/bin/bash
# Cross-tool AI setup — full verification
# Run from anywhere. Checks global config, skills, all repos, and memory symlinks.

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

echo ""
echo "========================================="
echo "3. REPOS — CLAUDE.md ↔ AGENTS.md"
echo "========================================="

find "/Users/$USER/My Drive" -maxdepth 6 \( -name "CLAUDE.md" -o -name "AGENTS.md" \) 2>/dev/null | \
    xargs -I{} dirname {} | sort -u | while read dir; do

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
