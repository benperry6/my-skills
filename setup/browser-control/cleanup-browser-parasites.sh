#!/bin/bash
set -uo pipefail

LOCK_ROOT="$HOME/.codex/browser-locks"
LOCK_DIR="$LOCK_ROOT/browser-parasite-guard.lock"
LOG_PATH="$HOME/.codex/browser-control/cleanup.log"
HEADLESS_TTL_SECONDS="${HEADLESS_TTL_SECONDS:-900}"
LOCK_HELD=0
HANDLED_FILE=""

mkdir -p "$LOCK_ROOT" "$(dirname "$LOG_PATH")"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "$LOG_PATH"
}

trim_log() {
  if [ -f "$LOG_PATH" ] && [ "$(wc -l < "$LOG_PATH")" -gt 200 ]; then
    tail -100 "$LOG_PATH" > "${LOG_PATH}.tmp" && mv "${LOG_PATH}.tmp" "$LOG_PATH"
  fi
}

cleanup() {
  if [ -n "$HANDLED_FILE" ] && [ -f "$HANDLED_FILE" ]; then
    rm -f "$HANDLED_FILE"
  fi

  if [ "$LOCK_HELD" -eq 1 ] && [ -d "$LOCK_DIR" ] && [ -f "$LOCK_DIR/pid" ] && [ "$(cat "$LOCK_DIR/pid" 2>/dev/null || true)" = "$$" ]; then
    rm -rf "$LOCK_DIR"
    LOCK_HELD=0
  fi
}

trap cleanup EXIT INT TERM

lock_is_stale() {
  if [ ! -d "$LOCK_DIR" ]; then
    return 1
  fi

  local lock_pid=""
  local started_at=""
  lock_pid="$(cat "$LOCK_DIR/pid" 2>/dev/null || true)"
  started_at="$(cat "$LOCK_DIR/started_at" 2>/dev/null || true)"

  if [ -n "$lock_pid" ] && kill -0 "$lock_pid" >/dev/null 2>&1; then
    if [ -n "$started_at" ]; then
      local now age
      now="$(date +%s)"
      age=$((now - started_at))
      if [ "$age" -lt 300 ]; then
        return 1
      fi
    else
      return 1
    fi
  fi

  return 0
}

acquire_lock() {
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    printf '%s\n' "$$" > "$LOCK_DIR/pid"
    date +%s > "$LOCK_DIR/started_at"
    LOCK_HELD=1
    return 0
  fi

  if lock_is_stale; then
    log "removing stale parasite-guard lock"
    rm -rf "$LOCK_DIR"
    if mkdir "$LOCK_DIR" 2>/dev/null; then
      printf '%s\n' "$$" > "$LOCK_DIR/pid"
      date +%s > "$LOCK_DIR/started_at"
      LOCK_HELD=1
      return 0
    fi
  fi

  return 1
}

cmd_for_pid() {
  ps -p "$1" -o command= 2>/dev/null | head -n 1
}

elapsed_to_seconds() {
  local raw="$1"
  local days=0
  local hours=0
  local minutes=0
  local seconds=0
  local time_part="$raw"

  if [[ "$raw" == *-* ]]; then
    days="${raw%%-*}"
    time_part="${raw#*-}"
  fi

  IFS=':' read -r first second third <<< "$time_part"
  if [ -n "${third:-}" ]; then
    hours="$first"
    minutes="$second"
    seconds="$third"
  elif [ -n "${second:-}" ]; then
    minutes="$first"
    seconds="$second"
  else
    seconds="$first"
  fi

  printf '%s\n' $((10#$seconds + 60 * 10#$minutes + 3600 * 10#$hours + 86400 * 10#$days))
}

is_attached_browser_playwright() {
  local cmd="$1"
  [[ "$cmd" == *"playwright-mcp"* || "$cmd" == *"@playwright/mcp"* ]] || return 1
  [[ "$cmd" == *"--executable-path /Applications/Brave Browser.app/Contents/MacOS/Brave Browser"* \
    || "$cmd" == *"--executable-path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome"* ]]
}

is_stale_temp_headless() {
  local elapsed_seconds="$1"
  local cmd="$2"
  [ "$elapsed_seconds" -ge "$HEADLESS_TTL_SECONDS" ] || return 1
  [[ "$cmd" == *"chrome-headless-shell"* ]] || return 1
  [[ "$cmd" == *"/ms-playwright/"* || "$cmd" == *"mcp-chrome-for-testing"* ]]
}

is_handled() {
  local pid="$1"
  [ -n "$HANDLED_FILE" ] && grep -qx "$pid" "$HANDLED_FILE" 2>/dev/null
}

mark_handled() {
  local pid="$1"
  printf '%s\n' "$pid" >> "$HANDLED_FILE"
}

kill_tree() {
  local pid="$1"
  local child
  while IFS= read -r child; do
    [ -n "$child" ] || continue
    kill_tree "$child"
  done < <(pgrep -P "$pid" 2>/dev/null || true)

  kill "$pid" 2>/dev/null || true
}

if ! acquire_lock; then
  exit 0
fi

HANDLED_FILE="$(mktemp "${TMPDIR:-/tmp}/browser-parasite-guard.XXXXXX")"

while IFS= read -r line; do
  [ -n "$line" ] || continue

  local_pid=""
  local_ppid=""
  local_etime=""
  local_cmd=""
  read -r local_pid local_ppid local_etime local_cmd <<< "$line"
  [ -n "$local_pid" ] || continue

  if is_attached_browser_playwright "$local_cmd"; then
    root_pid="$local_pid"
    parent_cmd="$(cmd_for_pid "$local_ppid")"
    if [ -n "$parent_cmd" ] && is_attached_browser_playwright "$parent_cmd"; then
      root_pid="$local_ppid"
    fi

    if ! is_handled "$root_pid"; then
      log "killing attached-browser Playwright stack pid=$root_pid cmd=$(cmd_for_pid "$root_pid")"
      kill_tree "$root_pid"
      mark_handled "$root_pid"
    fi
    continue
  fi

  local_elapsed_seconds="$(elapsed_to_seconds "$local_etime")"

  if is_stale_temp_headless "$local_elapsed_seconds" "$local_cmd"; then
    if ! is_handled "$local_pid"; then
      log "killing stale temporary headless browser pid=$local_pid elapsed=${local_elapsed_seconds}s cmd=$local_cmd"
      kill_tree "$local_pid"
      mark_handled "$local_pid"
    fi
  fi
done < <(ps -Ao pid=,ppid=,etime=,command=)

trim_log
exit 0
