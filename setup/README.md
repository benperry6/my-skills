# Cross-Tool AI Setup

How to make Claude Code, Codex CLI, Gemini CLI, and any future AI tool share the same rules, memory, local infrastructure, and browser-control behavior — so switching tools mid-day costs zero context.

## The problem this solves

Each AI coding tool has its own instruction file:

- Claude Code reads `CLAUDE.md`
- Codex CLI reads `AGENTS.md`
- Cursor reads `.cursorrules`
- Gemini CLI reads `GEMINI.md`

Without coordination, you end up with duplicated rules that diverge over time, memory that only one tool can see, and MCP servers configured three times in three different formats.

This setup eliminates all of that.

## Why this documentation lives in `~/.agents/skills`

This is machine-level infrastructure, not project-level documentation.

It belongs in the shared skills repo because this repo is:

- global instead of tied to a single business repo
- versioned in Git
- readable by humans from GitHub through the repo `README`s
- accessible from every project that already depends on this stack

The rules themselves still live in `~/.claude/CLAUDE.md`.

But the durable human documentation for how the stack is wired, reproduced, and debugged belongs here.

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
├── ~/.gemini/GEMINI.md          # Symlink → ~/.claude/CLAUDE.md
├── ~/.agents/skills/            # Shared skills (source of truth)
│   ├── ~/.claude/skills/*       # Symlinks → ~/.agents/skills/*
│   └── ~/.codex/skills/*        # Symlinks → ~/.agents/skills/*
│
├── ~/.gemini/antigravity/global_skills → ~/.agents/skills
├── ~/.codex/mcp/                # Shared MCP wrapper scripts
├── ~/.codex/brave-cdp-client/   # Brave native browser-control layer
├── ~/.codex/chrome-cdp-client/  # Chrome native browser-control layer
│
MCP server sync:
├── ~/.agents/skills/setup/mcp-servers.json   # Master MCP definitions (source of truth)
├── ~/.agents/skills/setup/sync-mcp.py        # Generates tool-native configs from master
│   writes to:
├── ~/.claude.json               → mcpServers   (JSON, Claude Code CLI)
├── ~/Library/.../claude_desktop_config.json   → mcpServers   (JSON, Desktop/Cowork)
├── ~/.codex/config.toml         → mcp_servers  (TOML, Codex CLI)
└── ~/.gemini/settings.json      → mcpServers   (JSON, Gemini CLI)
```

The shared skills repo is itself a versioned repo and should also follow the local `CLAUDE.md` + `AGENTS.md` convention.

## Setup from scratch on a new machine

### Prerequisites

- macOS (uses Keychain for secrets, AppleScript for browser automation)
- Python 3.11+ (for MCP sync script — ships with Xcode Command Line Tools)
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
ln -sf ../.claude/CLAUDE.md ~/.codex/AGENTS.md

# Global Gemini symlink → same rules
ln -sf ../.claude/CLAUDE.md ~/.gemini/GEMINI.md
```

**Why a symlink instead of a copy?** A copy diverges the moment either file is edited. A symlink guarantees all tools always read the exact same content.

### Step 3 — Symlink skills into the tools

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

# Gemini global skill source
mkdir -p ~/.gemini/antigravity
ln -sfn ~/.agents/skills ~/.gemini/antigravity/global_skills
```

**Why a different setup for Gemini?** Gemini discovers shared skills from `~/.gemini/antigravity/global_skills`. Do not duplicate the same shared skills into `~/.gemini/skills/` or Gemini will detect them twice.

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
set -eo pipefail
KEY=$(security find-generic-password -a "${USER:-$(whoami)}" -s KEY_NAME -w 2>/dev/null || true)
if [ -z "${KEY:-}" ]; then
  echo "KEY_NAME not found in Keychain." >&2
  exit 1
fi
export ENV_VAR_NAME="$KEY"
exec npx -y package-name "$@"
```

Avoid `set -u` in shared wrappers. Some tools launch MCP processes with a minimal environment, and `$USER` is not always populated.

Then `chmod +x ~/.codex/mcp/*.sh`.

**Register in each tool's config:**

| Tool | Config file | Format |
|------|-------------|--------|
| Claude Code | `~/.claude.json` → `mcpServers` | JSON: `"command": "/path/to/wrapper.sh"` |
| Claude Desktop / Cowork | `~/Library/Application Support/Claude/claude_desktop_config.json` | JSON |
| Codex | `~/.codex/config.toml` → `[mcp_servers.xxx]` | TOML: `command = "/path/to/wrapper.sh"` |
| Gemini | `~/.gemini/settings.json` → `mcpServers` | JSON |

**Why wrapper scripts?** API keys stay in the Keychain (not in config files that could leak). The same wrapper is referenced by all tools — change the wrapper once, all tools pick it up.

**Don't register servers manually.** Use the sync script instead (Step 4b below).

### Step 4b — Sync MCP server definitions across tools

Each tool has its own config file and format for MCP servers. Instead of maintaining these separately, a master file + sync script propagates definitions to all four tools automatically.

**Master file:** `~/.agents/skills/setup/mcp-servers.json` (versioned in this repo)

Defines all MCP servers in one place. Each server has a `command`, optional `args`, and optional `targets` (defaults to all tools). Use `${HOME}` in paths for portability.

```json
{
  "servers": {
    "haloscan": {
      "command": "${HOME}/.codex/mcp/haloscan-wrapper.sh"
    },
    "chrome-devtools": {
      "command": "${HOME}/.codex/mcp/chrome-devtools-wrapper.sh",
      "targets": ["claude-code", "codex"]
    }
  }
}
```

Servers without a `targets` field are deployed to all four tools: `claude-code`, `claude-desktop`, `codex`, `gemini`. Restrict targets for servers that need local resources (browsers, specific runtimes) unavailable in certain environments (e.g. Desktop/Cowork runs in a VM).

**Sync:**

```bash
# Preview changes
python3 ~/.agents/skills/setup/sync-mcp.py --dry-run

# Apply
python3 ~/.agents/skills/setup/sync-mcp.py

# Check if in sync (exit 1 if not — useful in CI or verify.sh)
python3 ~/.agents/skills/setup/sync-mcp.py --check
```

The sync script finds the master file relative to itself (`setup/mcp-servers.json`). No symlink or environment variable needed — as long as the repo is cloned at `~/.agents/skills/`, the script works.

The script:
- Reads `setup/mcp-servers.json`, resolves `${HOME}`
- Writes the `mcpServers` / `mcp_servers` section of each tool's native config
- Preserves all non-MCP sections (preferences, hooks, projects, features, etc.)
- Is idempotent — running twice produces no diff
- Verifies wrapper scripts exist before syncing (warns if missing)

**Adding a new MCP server:**
1. Add the entry to `~/.agents/skills/setup/mcp-servers.json`
2. Run `python3 ~/.agents/skills/setup/sync-mcp.py`
3. Done — all tools get the new server

**On a new machine:** after Step 1 (clone) and Step 4 (wrapper scripts), just run the sync script. It generates all four tool configs from the master file — no need to copy `~/.claude.json`, `config.toml`, or `settings.json` from the old machine.

### Step 4c — Set up native browser automation

This stack uses a browser policy that is intentionally stricter than the defaults of the tools:

- `Brave` is the default browser when the user does not specify one
- for Claude, prefer `Claude in Chrome` first when it reaches the correct live session
- otherwise, prefer `CDP/MCP-first` native browser control
- keep `AppleScript` only as fallback
- keep `Playwright` for public pages, isolated tests, or cases where a blank profile is acceptable

This policy is defined in `~/.claude/CLAUDE.md`. The implementation lives in shared local scripts under `~/.codex/`.

#### What is installed

| Purpose | File |
|--------|------|
| Brave CDP/MCP server | `~/.codex/brave-cdp-client/brave-devtools-server.mjs` |
| Brave launcher | `~/.codex/brave-cdp-client/launch-brave-ai-safe.sh` |
| Chrome launcher | `~/.codex/chrome-cdp-client/launch-chrome-ai-safe.sh` |
| Brave MCP wrapper | `~/.codex/mcp/brave-devtools-wrapper.sh` |
| Chrome MCP wrapper | `~/.codex/mcp/chrome-devtools-wrapper.sh` |

#### How it works today

- `Brave AI-safe` launches Brave with CDP on `127.0.0.1:9222` and restores the prior session.
- `Chrome AI-safe` launches Chrome with CDP on `127.0.0.1:9223`, using a cloned `user-data-dir` at `~/.codex/browser-profiles/chrome-ai-safe`, then restores the prior session.
- The Chrome clone exists because the native CDP path was unreliable on the real default profile. The cloned profile keeps the real profile as the source of truth while exposing a stable CDP endpoint.
- `Brave` stays on the custom local MCP server because the live Brave session needs a custom bootstrap and session-preserving behavior.
- `Chrome` uses the official `chrome-devtools-mcp` package, attached to the running `Chrome AI-safe` instance via `--browserUrl http://127.0.0.1:9223`.
- Brave and Chrome can run in parallel because they use separate ports and separate bootstrap logic.
- Today, the browser devtools wrappers are registered in Codex by default through `~/.codex/config.toml`. The scripts themselves are global local infrastructure and can be wired into other tools later if wanted.

#### Resource protection policy for Brave

- `Brave` is the default browser for short, targeted work in the existing live session.
- Do **not** use the live Brave session for heavy automation patterns: deep scraping, repeated DOM polling, repeated `Runtime.evaluate` loops, aggressive retries after navigation, or repeated creation of temporary CDP targets/tabs.
- If Brave shows signs of saturation — repeated timeouts, empty/incomplete snapshots, a page that does not visibly finish loading, or the browser becoming unresponsive — stop quickly, do not intensify retries, do not open extra temporary targets/tabs, and resume only with lighter, more targeted actions in the same Brave session.
- Do not automatically switch away from Brave just because automation becomes difficult or slow. Switch to Chrome or an isolated browser only if the user explicitly asks for it, or if the Brave session is genuinely unavailable.
- This is an operational rule, not just a project-specific workaround: large live Brave sessions can remain usable for manual work while becoming unstable under repeated automation pressure.

#### New-machine checklist for the browser layer

1. Copy `~/.codex/mcp/`, `~/.codex/brave-cdp-client/`, and `~/.codex/chrome-cdp-client/`
2. Copy `~/.codex/config.toml`
3. Ensure Homebrew `node` exists at the path expected by the wrappers, or update the wrapper paths
4. Ensure Brave and Chrome are installed in `/Applications/`
5. Verify `brave-devtools` and `chrome-devtools` entries exist in `~/.codex/config.toml`
6. Test the endpoints:
   - `curl -sf http://127.0.0.1:9222/json/version`
   - `curl -sf http://127.0.0.1:9223/json/version`
7. If a fresh tool session still reports stale MCP transport errors, restart the tool session itself — not just the browser

#### Fast debug checklist

```bash
# Is the CDP endpoint up?
curl -sf http://127.0.0.1:9222/json/version | jq .
curl -sf http://127.0.0.1:9223/json/version | jq .

# Which process owns the port?
lsof -nP -iTCP:9222 -sTCP:LISTEN
lsof -nP -iTCP:9223 -sTCP:LISTEN

# Are the browsers really running with remote debugging?
ps aux | rg 'Brave Browser|Google Chrome' | rg 'remote-debugging-port'
```

Useful logs:

- `/tmp/brave-devtools-stderr.log`
- `/tmp/chrome-devtools-stderr.log`
- `/tmp/chrome-devtools-mcp.log`
- `/tmp/brave-cdp.log`
- `/tmp/chrome-cdp.log`

#### Claude in Chrome — "No Chrome extension connected"

If `Claude in Chrome` shows `No Chrome extension connected`, the extension is usually still trying to talk to Claude Desktop instead of Claude Code.

Fast recovery:

1. Kill stale Desktop native hosts:
   ```bash
   ps aux | grep "Claude.app.*chrome-native-host" | grep -v grep | awk '{print $2}' | xargs kill 2>/dev/null
   ```
2. Force the bridge toward Claude Code:
   ```bash
   ~/.claude/scripts/chrome-connect.sh code
   ```
3. Reconnect the extension in Chrome:
   - open `https://clau.de/chrome/reconnect`
   - wait about 5 seconds
   - retest the Chrome-side tool path

Automatic cleanup:

- LaunchAgent: `com.anthropic.claude-chrome-cleanup`
- Script: `~/.claude/scripts/cleanup-chrome-zombies.sh`
- Purpose: kill zombie native hosts and orphaned MCP processes every 30 minutes

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
bash ~/.agents/skills/setup/verify.sh
```

## Auto-enforcement

The global `~/.claude/CLAUDE.md` contains short rules that make Claude Code verify and fix the setup automatically at the start of every session in any versioned repo that acts as source of truth for shared rules, skills, or memory.
That includes normal project repos and shared infrastructure repos like `~/.agents/skills`.

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
| This repo (skills + setup) | `~/.agents/skills/` | `git clone` (includes MCP master file) |
| Global Claude rules | `~/.claude/CLAUDE.md` | Copy file |
| Codex settings (non-MCP) | `~/.codex/config.toml` | Copy file (model, approval_policy, projects, features) |
| Gemini settings (non-MCP) | `~/.gemini/settings.json` | Copy file (hooks, security) |
| MCP wrappers | `~/.codex/mcp/*.sh` | Copy directory |
| Browser CDP clients | `~/.codex/brave-cdp-client/`, `~/.codex/chrome-cdp-client/` | Copy directories |
| API keys | macOS Keychain | Re-enter or export/import |
| Gmail tokens | `.gmail_tokens.json` per repo | Copy file |
| Shopify tokens | `.shopify_tokens.json` per repo | Copy file |
| Project repos | Google Drive | Automatic sync |
| Symlinks (global) | `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`, skills | Run Step 2-3 |
| Symlinks (per-project) | `AGENTS.md`, memory | Auto-enforced by Claude Code on first session |
| MCP servers (all tools) | `~/.claude.json`, Desktop config, `config.toml`, `settings.json` | `python3 ~/.agents/skills/setup/sync-mcp.py` |

**Key insight:** The real data (rules, memory, code) lives either in Google Drive (project repos) or in `~/.claude/` + `~/.codex/` + `~/.gemini/` (global config). Symlinks are the glue — they're lightweight and auto-recreated by the enforcement rules.

Tool-specific config files serve two purposes: non-MCP settings (model, hooks, features) that you copy manually, and MCP server definitions that the sync script generates from the master file. The sync script only touches the MCP section — it preserves everything else. Don't edit MCP servers directly in tool configs; edit `setup/mcp-servers.json` and re-sync.

## Full verification script

Run the maintained script in this repo:

```bash
bash ~/.agents/skills/setup/verify.sh
```

It checks the shared rules symlinks, the skill wiring, the project memory symlinks, the MCP wrapper layer, the Gemini global skill hook, and the local browser automation files.

## Design decisions and trade-offs

### Why CLAUDE.md is the source of truth (not AGENTS.md)

AGENTS.md is the emerging Linux Foundation standard with broader tool support. But Claude Code is our primary tool, and `CLAUDE.md` is its native format. The symlink makes this transparent — both tools read the same content regardless of which filename they look for.

### Why the browser runbook is documented here

The Brave/Chrome automation layer is not tied to any single product repo.

It is part of the local AI workstation itself:

- shared rules decide when to use it
- shared wrappers expose it
- multiple projects depend on it indirectly
- it must survive a machine migration without relying on memory or chat history

So the durable human documentation belongs here, next to the rest of the cross-tool infrastructure.

### Why not use Basic Memory (MCP-based cross-tool memory)

Basic Memory provides semantic search across a shared knowledge base. We evaluated it but our memory per project is small (1-10 KB) — reading the full file is fast enough. Basic Memory adds infrastructure (MCP server, database) that isn't justified at our current scale. If memory grows to hundreds of KB across dozens of projects, this decision should be revisited.

### Why not use the `sync-configs` or `agents-project-memory` skills

These skills are opinionated (specific frameworks, personas, conventions) and solve problems we've already solved with simpler filesystem primitives. Our approach uses only symlinks and naming conventions — no dependencies, no runtime, no configuration drift.

### Why not use `@agents-dev/cli`, `vsync`, or `mcpx-cli` for MCP sync

We evaluated these community tools (April 2026). None fits our setup:

- **`@agents-dev/cli`**: project-scoped (not global), no Claude Desktop/Cowork support, full-overwrites Codex config, solo maintainer at v0.8.
- **`vsync`**: picks one tool as source of truth and syncs to others — doesn't support a separate master file or Keychain-based wrapper scripts.
- **`mcpx-cli`**: similar limitations, and authored by the same person driving the (still-open) RFC for a standard config format.

All three add an npm dependency that could break or be abandoned. Our sync script is ~150 lines of stdlib Python, reads a JSON master file, and writes each tool's native format. If a tool changes its config format, one function in the script is updated — no upstream dependency to wait on.

The MCP specification (Linux Foundation / AAIF) does not define a config format. An RFC (#2219) exists but is not adopted. If a standard emerges, we can replace the script with a single config file.

### Why the memory file is called CLAUDE_MEMORY.md

Three files at the repo root, each immediately identifiable:
- `CLAUDE.md` — rules (what to do)
- `CLAUDE_MEMORY.md` — memory (what was learned)
- `AGENTS.md` — symlink for other tools

`MEMORY.md` alone wouldn't tell you where it comes from. The `CLAUDE_` prefix makes the origin explicit.
