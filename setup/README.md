# Cross-Tool AI Setup

How to make Claude Code, Codex CLI, and any future AI coding tool share the same rules, memory, and configuration — so switching tools mid-day costs zero context.

## The problem this solves

Each AI coding tool has its own instruction file:

- Claude Code reads `CLAUDE.md`
- Codex CLI reads `AGENTS.md`
- Cursor reads `.cursorrules`
- Gemini CLI reads `GEMINI.md`

Without coordination, you end up with duplicated rules that diverge over time, memory that only one tool can see, and MCP servers configured three times in three different formats.

This setup eliminates all of that.

## Architecture overview

```
Each repo root:
├── CLAUDE.md            # Real file — project rules (source of truth)
├── AGENTS.md            # Symlink → CLAUDE.md (so Codex reads the same rules)
└── CLAUDE_MEMORY.md     # Real file — accumulated memory from Claude Code sessions

~/.claude/projects/<encoded-project>/memory/
└── MEMORY.md            # Symlink → <repo>/CLAUDE_MEMORY.md

Global config:
├── ~/.claude/CLAUDE.md          # Real file — global rules for all projects
├── ~/.codex/AGENTS.md           # Symlink → ~/.claude/CLAUDE.md
├── ~/.agents/skills/            # Shared skills (symlinked into both tools)
│   ├── ~/.claude/skills/*       # Symlinks → ~/.agents/skills/*
│   └── ~/.codex/skills/*        # Symlinks → ~/.agents/skills/*
└── ~/.codex/mcp/                # MCP wrapper scripts (shared via macOS Keychain)
```

## Setup from scratch on a new machine

### Prerequisites

- macOS (uses Keychain for secrets, AppleScript for browser automation)
- Node.js 18+
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- Codex CLI installed (`npm install -g @openai/codex`)
- Git configured with SSH key for GitHub

### Step 1 — Clone this repo

```bash
git clone git@github.com:benperry6/my-skills.git ~/.agents/skills
```

This gives you all personal skills and this setup guide.

### Step 2 — Transfer global config files

Copy these from the old machine (or from Google Drive backup):

```bash
# Global rules (Claude Code reads this at every session start)
cp <source>/.claude/CLAUDE.md ~/.claude/CLAUDE.md

# Global Codex symlink → same rules
ln -sf ~/.claude/CLAUDE.md ~/.codex/AGENTS.md
```

**Why a symlink instead of a copy?** A copy diverges the moment either file is edited. A symlink guarantees both tools always read the exact same content. We tested that both Claude Code and Codex follow symlinks correctly for both reading and writing.

### Step 3 — Symlink skills into both tools

```bash
# Claude Code skills
for skill in ~/.agents/skills/my-personal-*/; do
    name=$(basename "$skill")
    ln -sf "../../.agents/skills/$name" ~/.claude/skills/"$name"
done

# Codex skills
for skill in ~/.agents/skills/my-personal-*/; do
    name=$(basename "$skill")
    ln -sf "../../.agents/skills/$name" ~/.codex/skills/"$name"
done
```

**Why symlinks from a shared source?** Skills are edited in `~/.agents/skills/` (this git repo). Both tools see the same version without manual syncing. The `my-personal-*` prefix convention identifies personal skills.

### Step 4 — Set up MCP wrapper scripts

MCP servers need API keys. Instead of hardcoding them, we use macOS Keychain + wrapper scripts.

**Add API keys to Keychain:**

```bash
security add-generic-password -a "$USER" -s HALOSCAN_API_KEY -w "your-key"
security add-generic-password -a "$USER" -s FIRECRAWL_API_KEY -w "your-key"
security add-generic-password -a "$USER" -s PAGESPEED_API_KEY -w "your-key"
security add-generic-password -a "$USER" -s DATAFORSEO_USERNAME -w "your-username"
security add-generic-password -a "$USER" -s DATAFORSEO_PASSWORD -w "your-password"
security add-generic-password -a "$USER" -s GEMINI_DESIGN_API_KEY -w "your-key"
```

**Create wrapper scripts in `~/.codex/mcp/`:**

Each wrapper follows this pattern:

```bash
#!/bin/bash
set -euo pipefail
KEY=$(security find-generic-password -a "$USER" -s KEY_NAME -w 2>/dev/null || true)
if [ -z "${KEY:-}" ]; then
  echo "KEY_NAME not found in Keychain." >&2
  exit 1
fi
export ENV_VAR_NAME="$KEY"
exec npx -y package-name "$@"
```

Then `chmod +x ~/.codex/mcp/*.sh`.

**Register in each tool's config:**

| Tool | Config file | Format |
|------|-------------|--------|
| Claude Code | `~/.claude.json` → `mcpServers` | JSON: `"command": "/path/to/wrapper.sh"` |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | JSON |
| Codex | `~/.codex/config.toml` → `[mcp_servers.xxx]` | TOML: `command = "/path/to/wrapper.sh"` |

**Why wrapper scripts?** API keys stay in the Keychain (not in config files that could leak). The same wrapper is referenced by all three tools — change the wrapper once, all tools pick it up.

### Step 5 — Set up project-level symlinks

For each project repo, create the symlinks that share rules and memory:

```bash
cd /path/to/your/repo

# Rules: AGENTS.md → CLAUDE.md (if CLAUDE.md exists)
ln -sf CLAUDE.md AGENTS.md

# Memory: if Claude Code has already created memory for this project,
# move it to the repo and symlink back
ENCODED=$(echo "$PWD" | sed 's|/|-|g')
NATIVE="$HOME/.claude/projects/$ENCODED/memory"
if [ -f "$NATIVE/MEMORY.md" ] && [ ! -L "$NATIVE/MEMORY.md" ]; then
    cp "$NATIVE/MEMORY.md" ./CLAUDE_MEMORY.md
    rm "$NATIVE/MEMORY.md"
    ln -sf "$PWD/CLAUDE_MEMORY.md" "$NATIVE/MEMORY.md"
    echo "Memory migrated: $NATIVE/MEMORY.md → ./CLAUDE_MEMORY.md"
fi
```

**Why does the real memory file live in the repo (not in `~/.claude/`)?**

Three reasons, all tested empirically:

1. **Google Drive syncs real files but not symlinks.** The repo is on Google Drive. If the real file is in `~/.claude/` and the symlink is in the repo, Google Drive won't sync the symlink to another machine. With the real file in the repo, Drive syncs the content automatically.

2. **Claude Code follows symlinks transparently.** We tested Read, Write, and Edit tools through symlinks pointing from the local filesystem to Google Drive. All three follow the symlink without replacing it (they use `writeFileSync` internally, not atomic `rename()`).

3. **Codex reads the file directly at the repo root.** No symlink to follow, no special instruction needed beyond "read CLAUDE_MEMORY.md at startup" (added to CLAUDE.md).

### Step 6 — Verify

```bash
# Check global setup
echo "=== Global rules ==="
ls -la ~/.claude/CLAUDE.md ~/.codex/AGENTS.md

echo "=== Skills ==="
ls ~/.claude/skills/my-personal-* 2>/dev/null | wc -l
ls ~/.codex/skills/my-personal-* 2>/dev/null | wc -l

echo "=== MCP wrappers ==="
ls ~/.codex/mcp/*.sh | wc -l

# Check each project
for repo in /path/to/repo1 /path/to/repo2; do
    echo "=== $repo ==="
    ls -la "$repo/CLAUDE.md" "$repo/AGENTS.md" "$repo/CLAUDE_MEMORY.md" 2>/dev/null
done
```

## Auto-enforcement

The global `~/.claude/CLAUDE.md` contains rules that make Claude Code verify and fix the setup automatically at the start of every session:

- If `AGENTS.md` is missing → creates the symlink
- If `AGENTS.md` and `CLAUDE.md` both exist as real files → merges into `CLAUDE.md`, replaces `AGENTS.md` with symlink
- If `CLAUDE_MEMORY.md` doesn't exist at repo root but native memory exists → migrates it
- If native memory path isn't symlinked → creates the symlink

This means the setup is self-healing: even on a new repo where only `CLAUDE.md` exists, the next Claude Code session will create `AGENTS.md` and set up memory correctly.

## Gmail setup

Two Gmail accounts are used for e-commerce operations:

- `paenma2021@gmail.com` — client communication (with boutique aliases)
- `paenma.va1@gmail.com` — supplier/carrier notifications

**OAuth credentials:**

```bash
security add-generic-password -a "$USER" -s GMAIL_CLIENT_ID -w "your-client-id"
security add-generic-password -a "$USER" -s GMAIL_CLIENT_SECRET -w "your-client-secret"
```

**Token authorization (once per account):**

```bash
cd /path/to/ShopifyMCP_Codex
node gmail-auth.cjs
# Opens browser → authorize → token saved to .gmail_tokens.json
```

Tokens are stored in `.gmail_tokens.json` (gitignored). Must be transferred manually or re-authorized on a new machine.

## Shopify setup

Tokens for each boutique are stored in `.shopify_tokens.json` (gitignored). Must be transferred manually to a new machine.

Connected boutiques:

| Short name | myshopify.com domain |
|------------|---------------------|
| BDR | berceau-des-reves.myshopify.com |
| MPL | ma-petite-licorne-8210.myshopify.com |
| MG | fleurs-sechees-gaya.myshopify.com |
| MLL | paenma5.myshopify.com |

## What to transfer manually when changing machines

| What | Where | How |
|------|-------|-----|
| This repo (skills + setup) | `~/.agents/skills/` | `git clone` |
| Global Claude rules | `~/.claude/CLAUDE.md` | Copy file |
| Claude Code settings | `~/.claude.json` | Copy file |
| Codex config | `~/.codex/config.toml` | Copy file |
| MCP wrappers | `~/.codex/mcp/*.sh` | Copy directory |
| API keys | macOS Keychain | Re-enter or export/import |
| Gmail tokens | `.gmail_tokens.json` per repo | Copy file |
| Shopify tokens | `.shopify_tokens.json` per repo | Copy file |
| Project repos | Google Drive | Automatic sync |
| Symlinks (global) | `~/.codex/AGENTS.md`, skills | Run Step 2-3 |
| Symlinks (per-project) | `AGENTS.md`, memory | Auto-enforced by Claude Code on first session |

**Key insight:** The real data (rules, memory, code) lives either in Google Drive (project repos) or in `~/.claude/` + `~/.codex/` (global config). Symlinks are the glue — they're lightweight and auto-recreated by the enforcement rules.

## Design decisions and trade-offs

### Why CLAUDE.md is the source of truth (not AGENTS.md)

AGENTS.md is the emerging Linux Foundation standard with broader tool support. But Claude Code is our primary tool, and `CLAUDE.md` is its native format. The symlink makes this transparent — both tools read the same content regardless of which filename they look for.

### Why not use Basic Memory (MCP-based cross-tool memory)

Basic Memory provides semantic search across a shared knowledge base. We evaluated it but our memory per project is small (1-10 KB) — reading the full file is fast enough. Basic Memory adds infrastructure (MCP server, database) that isn't justified at our current scale. If memory grows to hundreds of KB across dozens of projects, this decision should be revisited.

### Why not use the `sync-configs` or `agents-project-memory` skills

These skills are opinionated (specific frameworks, personas, conventions) and solve problems we've already solved with simpler filesystem primitives. Our approach uses only symlinks and naming conventions — no dependencies, no runtime, no configuration drift.

### Why the memory file is called CLAUDE_MEMORY.md

Three files at the repo root, each immediately identifiable:
- `CLAUDE.md` — rules (what to do)
- `CLAUDE_MEMORY.md` — memory (what was learned)
- `AGENTS.md` — symlink for other tools

`MEMORY.md` alone wouldn't tell you where it comes from. The `CLAUDE_` prefix makes the origin explicit.
