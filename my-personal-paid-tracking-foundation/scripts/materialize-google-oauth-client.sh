#!/bin/bash
set -eo pipefail

TARGET_PATH="${1:-$HOME/.config/gcloud/tracking-skills-access-oauth-client.json}"
KEYCHAIN_ITEM="${GOOGLE_TRACKING_OAUTH_KEYCHAIN_ITEM:-Google Tracking Skills OAuth Client JSON}"

mkdir -p "$(dirname "$TARGET_PATH")"

JSON_VALUE="$(security find-generic-password -a "${USER:-$(whoami)}" -s "$KEYCHAIN_ITEM" -w 2>/dev/null || true)"

if [ -z "${JSON_VALUE:-}" ]; then
  echo "Keychain item '$KEYCHAIN_ITEM' introuvable." >&2
  exit 1
fi

printf '%s' "$JSON_VALUE" | base64 -d > "$TARGET_PATH"
chmod 600 "$TARGET_PATH"

echo "$TARGET_PATH"
