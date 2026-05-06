#!/bin/bash
set -uo pipefail

PROFILE_DIR="${CHROME_SESSION_GUARDIAN_PROFILE_DIR:-$HOME/Library/Application Support/Google/Chrome/Profile 3}"
SESSIONS_DIR="$PROFILE_DIR/Sessions"
SNAP_ROOT="${CHROME_SESSION_GUARDIAN_SNAPSHOT_ROOT:-$HOME/.codex/browser-session-snapshots/chrome-profile3}"
LOG_PATH="${CHROME_SESSION_GUARDIAN_LOG:-$HOME/.codex/browser-control/chrome-session-guardian.log}"
LOCK_ROOT="$HOME/.codex/browser-locks"
LOCK_DIR="$LOCK_ROOT/chrome-session-guardian.lock"
WATCH_INTERVAL_SECONDS="${WATCH_INTERVAL_SECONDS:-2}"
MAX_SNAPSHOTS="${MAX_SNAPSHOTS:-120}"
APP_BINARY="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ANTIGRAVITY_PROFILE_DIR="${ANTIGRAVITY_BROWSER_PROFILE_DIR:-$HOME/.gemini/antigravity-browser-profile}"

mkdir -p "$SNAP_ROOT/snapshots" "$SNAP_ROOT/pre-restore" "$(dirname "$LOG_PATH")" "$LOCK_ROOT"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG_PATH"
}

trim_log() {
  if [ -f "$LOG_PATH" ] && [ "$(wc -l < "$LOG_PATH")" -gt 400 ]; then
    tail -200 "$LOG_PATH" > "${LOG_PATH}.tmp" && mv "${LOG_PATH}.tmp" "$LOG_PATH"
  fi
}

chrome_running() {
  if [ "${CHROME_SESSION_GUARDIAN_ASSUME_STOPPED:-0}" = "1" ]; then
    return 1
  fi

  local cmd
  while IFS= read -r cmd; do
    if [[ "$cmd" == "$APP_BINARY"* ]] \
      && [[ "$cmd" != *"--user-data-dir=$HOME/.codex/browser-profiles/"* ]] \
      && [[ "$cmd" != *"--user-data-dir=$ANTIGRAVITY_PROFILE_DIR"* ]] \
      && [[ "$cmd" != *"--remote-debugging-port=9322"* ]]; then
      return 0
    fi
  done < <(ps -axo command=)

  return 1
}

session_signature() {
  local dir="$1"
  [ -d "$dir" ] || return 1

  find "$dir" -maxdepth 1 -type f \( -name 'Session_*' -o -name 'Tabs_*' \) -print0 2>/dev/null \
    | while IFS= read -r -d '' path; do
        stat -f '%N|%z|%m' "$path" 2>/dev/null | sed "s#^$dir/##"
      done \
    | LC_ALL=C sort
}

valid_session_pair() {
  local dir="$1"
  local session_count tabs_count
  [ -d "$dir" ] || return 1
  session_count="$(find "$dir" -maxdepth 1 -type f -name 'Session_*' -size +1024c -print 2>/dev/null | wc -l | tr -d ' ')"
  tabs_count="$(find "$dir" -maxdepth 1 -type f -name 'Tabs_*' -size +1024c -print 2>/dev/null | wc -l | tr -d ' ')"
  [ "$session_count" -gt 0 ] && [ "$tabs_count" -gt 0 ]
}

profile_exit_clean() {
  [ -f "$PROFILE_DIR/Preferences" ] || return 1
  command -v jq >/dev/null 2>&1 || return 1

  jq -e '
    (.profile.exit_type // "") == "Normal"
    and ((.profile.exited_cleanly // true) == true)
  ' "$PROFILE_DIR/Preferences" >/dev/null 2>&1
}

latest_snapshot_dir() {
  if [ -L "$SNAP_ROOT/latest" ]; then
    readlink "$SNAP_ROOT/latest"
  elif [ -f "$SNAP_ROOT/latest" ]; then
    cat "$SNAP_ROOT/latest"
  fi
}

snapshot_current_sessions() {
  if ! valid_session_pair "$SESSIONS_DIR"; then
    log "skipped snapshot: no valid Chrome session pair in $SESSIONS_DIR"
    return 0
  fi

  local sig_before sig_after last_sig snapshot_dir created_at
  sig_before="$(session_signature "$SESSIONS_DIR" || true)"
  sleep 0.4
  sig_after="$(session_signature "$SESSIONS_DIR" || true)"

  if [ "$sig_before" != "$sig_after" ] || [ -z "$sig_after" ]; then
    log "skipped snapshot: session files are still changing"
    return 0
  fi

  last_sig="$(cat "$SNAP_ROOT/latest.signature" 2>/dev/null || true)"
  if [ "$sig_after" = "$last_sig" ]; then
    return 0
  fi

  created_at="$(date '+%Y%m%d-%H%M%S')"
  snapshot_dir="$SNAP_ROOT/snapshots/$created_at"
  mkdir -p "$snapshot_dir/Sessions"
  rsync -a --delete "$SESSIONS_DIR/" "$snapshot_dir/Sessions/" || return 1

  if [ -f "$PROFILE_DIR/Preferences" ]; then
    cp -p "$PROFILE_DIR/Preferences" "$snapshot_dir/Preferences.json" || return 1
  fi

  printf '%s\n' "$sig_after" > "$snapshot_dir/signature.txt"
  printf 'created_at=%s\nprofile_dir=%s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')" "$PROFILE_DIR" > "$snapshot_dir/manifest.txt"
  ln -sfn "$snapshot_dir" "$SNAP_ROOT/latest"
  printf '%s\n' "$sig_after" > "$SNAP_ROOT/latest.signature"
  rm -f "$SNAP_ROOT/last-skipped-at" "$SNAP_ROOT/last-skipped-signature"
  log "snapshotted Chrome session state into $snapshot_dir"
}

restore_latest_snapshot_if_needed() {
  local latest current_sig latest_sig backup_dir
  latest="$(latest_snapshot_dir)"

  if [ -z "$latest" ] || [ ! -d "$latest/Sessions" ] || ! valid_session_pair "$latest/Sessions"; then
    if valid_session_pair "$SESSIONS_DIR"; then
      snapshot_current_sessions
    fi
    return 0
  fi

  current_sig="$(session_signature "$SESSIONS_DIR" 2>/dev/null || true)"
  latest_sig="$(session_signature "$latest/Sessions" 2>/dev/null || true)"

  if [ -n "$current_sig" ] && [ "$current_sig" = "$latest_sig" ]; then
    return 0
  fi

  if valid_session_pair "$SESSIONS_DIR" && profile_exit_clean; then
    snapshot_current_sessions
    log "accepted cleanly closed Chrome session as latest known-good state"
    return 0
  fi

  backup_dir="$SNAP_ROOT/pre-restore/$(date '+%Y%m%d-%H%M%S')"
  mkdir -p "$backup_dir"
  if [ -d "$SESSIONS_DIR" ]; then
    rsync -a "$SESSIONS_DIR/" "$backup_dir/Sessions-before-restore/" || return 1
  fi
  if [ -f "$PROFILE_DIR/Preferences" ]; then
    cp -p "$PROFILE_DIR/Preferences" "$backup_dir/Preferences-before-restore.json" || return 1
  fi

  rm -rf "$SESSIONS_DIR"
  mkdir -p "$SESSIONS_DIR"
  rsync -a "$latest/Sessions/" "$SESSIONS_DIR/" || return 1

  if [ -f "$PROFILE_DIR/Preferences" ] && command -v jq >/dev/null 2>&1; then
    local tmp_path
    tmp_path="$(mktemp "$PROFILE_DIR/Preferences.XXXXXX")" || return 1
    if jq '.profile.exit_type = "Crashed" | .profile.exited_cleanly = false' "$PROFILE_DIR/Preferences" > "$tmp_path"; then
      mv -f "$tmp_path" "$PROFILE_DIR/Preferences"
    else
      rm -f "$tmp_path"
    fi
  fi

  log "restored Chrome session snapshot $latest into profile; previous state saved to $backup_dir"
  rm -f "$SNAP_ROOT/last-skipped-at" "$SNAP_ROOT/last-skipped-signature"
}

prune_snapshots() {
  find "$SNAP_ROOT/snapshots" -mindepth 1 -maxdepth 1 -type d -print 2>/dev/null \
    | LC_ALL=C sort -r \
    | awk -v max="$MAX_SNAPSHOTS" 'NR > max { print }' \
    | while IFS= read -r old_snapshot; do
        rm -rf "$old_snapshot"
      done
}

run_once() {
  if chrome_running; then
    local current_sig latest_sig
    current_sig="$(session_signature "$SESSIONS_DIR" 2>/dev/null || true)"
    latest_sig="$(cat "$SNAP_ROOT/latest.signature" 2>/dev/null || true)"

    if profile_exit_clean || [ -z "$latest_sig" ] || [ "$current_sig" = "$latest_sig" ]; then
      snapshot_current_sessions
    else
      local last_skip_at now
      now="$(date '+%s')"
      last_skip_at="$(cat "$SNAP_ROOT/last-skipped-at" 2>/dev/null || echo 0)"
      if [ $((now - last_skip_at)) -gt 300 ]; then
        log "skipped snapshot: Chrome profile is not cleanly exited, preserving latest known-good snapshot"
        printf '%s\n' "$now" > "$SNAP_ROOT/last-skipped-at"
      fi
    fi
  else
    restore_latest_snapshot_if_needed
  fi
  prune_snapshots
  trim_log
}

with_lock() {
  if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    local lock_pid
    lock_pid="$(cat "$LOCK_DIR/pid" 2>/dev/null || true)"
    if [ -n "$lock_pid" ] && kill -0 "$lock_pid" >/dev/null 2>&1; then
      return 0
    fi
    rm -rf "$LOCK_DIR"
    mkdir "$LOCK_DIR" 2>/dev/null || return 0
  fi

  printf '%s\n' "$$" > "$LOCK_DIR/pid"
  trap 'rm -rf "$LOCK_DIR"' EXIT INT TERM
  run_once
  rm -rf "$LOCK_DIR"
}

case "${1:---once}" in
  --watch)
    while true; do
      with_lock
      sleep "$WATCH_INTERVAL_SECONDS"
    done
    ;;
  --snapshot)
    snapshot_current_sessions
    ;;
  --restore-if-needed)
    restore_latest_snapshot_if_needed
    ;;
  --once)
    with_lock
    ;;
  *)
    echo "usage: $0 [--watch|--once|--snapshot|--restore-if-needed]" >&2
    exit 64
    ;;
esac
