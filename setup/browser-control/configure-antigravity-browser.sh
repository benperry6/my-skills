#!/bin/bash
set -euo pipefail

DB_PATH="${ANTIGRAVITY_STATE_DB:-$HOME/Library/Application Support/Antigravity/User/globalStorage/state.vscdb}"
CDP_PORT="${ANTIGRAVITY_BROWSER_CDP_PORT:-9322}"
PROFILE_PATH="${ANTIGRAVITY_BROWSER_PROFILE:-$HOME/.gemini/antigravity-browser-profile}"
CHROME_BINARY="${ANTIGRAVITY_CHROME_BINARY:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

if [ ! -f "$DB_PATH" ]; then
  echo "Antigravity state DB not found: $DB_PATH" >&2
  exit 1
fi

if pgrep -x "Antigravity" >/dev/null 2>&1 || pgrep -f "/Antigravity.app/" >/dev/null 2>&1; then
  echo "Antigravity is running. Quit it before editing browser launcher preferences." >&2
  exit 2
fi

mkdir -p "$PROFILE_PATH"
backup_path="${DB_PATH}.backup.$(date +%Y%m%d%H%M%S)"
cp -p "$DB_PATH" "$backup_path"

python3 - "$DB_PATH" "$CDP_PORT" "$PROFILE_PATH" "$CHROME_BINARY" <<'PY'
import base64
import sqlite3
import sys
import time

db_path, port_raw, profile_path, chrome_binary = sys.argv[1:]
port = int(port_raw)
topic_key = "antigravityUnifiedStateSync.browserPreferences"


def read_varint(data, idx):
    shift = 0
    value = 0
    while True:
        if idx >= len(data):
            raise ValueError("truncated varint")
        byte = data[idx]
        idx += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, idx
        shift += 7


def write_varint(value):
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def len_field(field_number, value):
    return write_varint((field_number << 3) | 2) + write_varint(len(value)) + value


def varint_field(field_number, value):
    return write_varint((field_number << 3) | 0) + write_varint(value)


def parse_entry_key(entry):
    idx = 0
    while idx < len(entry):
        field_tag, idx = read_varint(entry, idx)
        field_number = field_tag >> 3
        wire_type = field_tag & 7
        if wire_type == 2:
            length, idx = read_varint(entry, idx)
            value = entry[idx : idx + length]
            idx += length
            if field_number == 1:
                return value.decode("utf-8")
        elif wire_type == 0:
            _, idx = read_varint(entry, idx)
        else:
            raise ValueError(f"unsupported entry wire type: {wire_type}")
    return None


def parse_topic(data):
    entries = []
    trailing = []
    idx = 0
    while idx < len(data):
        start = idx
        field_tag, idx = read_varint(data, idx)
        field_number = field_tag >> 3
        wire_type = field_tag & 7
        if wire_type == 2:
            length, idx = read_varint(data, idx)
            value = data[idx : idx + length]
            idx += length
            raw = data[start:idx]
            if field_number == 1:
                key = parse_entry_key(value)
                entries.append((key, raw))
            else:
                trailing.append(raw)
        elif wire_type == 0:
            _, idx = read_varint(data, idx)
            trailing.append(data[start:idx])
        else:
            raise ValueError(f"unsupported topic wire type: {wire_type}")
    return entries, trailing


def setting_value_int(value):
    return base64.b64encode(varint_field(1, value)).decode("ascii")


def setting_value_string(value):
    encoded = value.encode("utf-8")
    return base64.b64encode(len_field(1, encoded)).decode("ascii")


def make_entry(key, setting_value_b64):
    # Entry format matches Antigravity's persisted USS topic state:
    # field 1 = sentinel key, field 2 = row { field 1 = base64 protobuf value, field 2 = eTag }.
    row = len_field(1, setting_value_b64.encode("ascii")) + varint_field(2, int(time.time() * 1000))
    entry = len_field(1, key.encode("utf-8")) + len_field(2, row)
    return len_field(1, entry)


required = {
    "browser_cdp_port_sentinel_key": setting_value_int(port),
    "browser_user_profile_path_sentinel_key": setting_value_string(profile_path),
    "browser_chrome_binary_path_sentinel_key": setting_value_string(chrome_binary),
}

with sqlite3.connect(db_path) as db:
    row = db.execute("select value from ItemTable where key=?", (topic_key,)).fetchone()
    if row is None:
        current = b""
    else:
        current = base64.b64decode(row[0])

    entries, trailing = parse_topic(current)
    seen = set()
    rebuilt = bytearray()

    for key, raw in entries:
        if key in required:
            rebuilt.extend(make_entry(key, required[key]))
            seen.add(key)
        else:
            rebuilt.extend(raw)

    for key, value in required.items():
        if key not in seen:
            rebuilt.extend(make_entry(key, value))

    for raw in trailing:
        rebuilt.extend(raw)

    encoded = base64.b64encode(bytes(rebuilt)).decode("ascii")
    db.execute(
        "insert into ItemTable(key, value) values(?, ?) "
        "on conflict(key) do update set value=excluded.value",
        (topic_key, encoded),
    )
    db.commit()

print(f"Antigravity browser launcher isolated on CDP port {port}")
print(f"Antigravity browser profile: {profile_path}")
print(f"Antigravity Chrome binary: {chrome_binary}")
PY

echo "Backup: $backup_path"
