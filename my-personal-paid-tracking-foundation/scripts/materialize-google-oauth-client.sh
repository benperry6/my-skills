#!/bin/bash
set -eo pipefail

TARGET_PATH="${1:-$HOME/.config/gcloud/paid-media-vendor-m2m-api-access-oauth-client.json}"
OP_REF="${GOOGLE_TRACKING_OAUTH_OP_REF:-op://Employee/Google Paid Media Vendor M2M OAuth Client/client_json}"

mkdir -p "$(dirname "$TARGET_PATH")"

JSON_VALUE="$(op read "$OP_REF" 2>/dev/null || true)"

if [ -z "${JSON_VALUE:-}" ]; then
  echo "1Password item '$OP_REF' introuvable. Vérifie que 'op' est signé." >&2
  exit 1
fi

printf '%s' "$JSON_VALUE" | base64 -d > "$TARGET_PATH"
chmod 600 "$TARGET_PATH"

echo "$TARGET_PATH"
