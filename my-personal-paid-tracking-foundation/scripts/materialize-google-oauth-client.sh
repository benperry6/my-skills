#!/bin/bash
set -eo pipefail

TARGET_PATH="${1:-$HOME/.config/gcloud/paid-media-vendor-m2m-api-access-oauth-client.json}"
OP_REF="${GOOGLE_TRACKING_OAUTH_OP_REF:-op://Employee/Google Paid Media Vendor M2M OAuth Client/client_json}"
OP_READ_HELPER="${OP_READ_HELPER:-$HOME/.codex/mcp/op-read.sh}"

mkdir -p "$(dirname "$TARGET_PATH")"

if [ ! -x "$OP_READ_HELPER" ]; then
  echo "Helper 1Password introuvable ou non executable: $OP_READ_HELPER" >&2
  exit 1
fi

if ! JSON_VALUE="$("$OP_READ_HELPER" "$OP_REF")" || [ -z "${JSON_VALUE:-}" ]; then
  echo "1Password item '$OP_REF' introuvable. Vérifie que 'op' est signé." >&2
  exit 1
fi

printf '%s' "$JSON_VALUE" | base64 -d > "$TARGET_PATH"
chmod 600 "$TARGET_PATH"

echo "$TARGET_PATH"
