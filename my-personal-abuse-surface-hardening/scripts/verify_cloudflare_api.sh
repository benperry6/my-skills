#!/bin/bash
set -eo pipefail

WRAPPER="${HOME}/.codex/mcp/cloudflare-wrapper.sh"
ZONE_NAME="${1:-}"

if [ ! -x "$WRAPPER" ]; then
  echo "Cloudflare wrapper not found or not executable: $WRAPPER" >&2
  exit 1
fi

TOKEN_JSON="$("$WRAPPER" GET /user/tokens/verify)"
echo "$TOKEN_JSON"

echo "$TOKEN_JSON" | grep -q '"success":true' || {
  echo "Cloudflare token verification failed." >&2
  exit 1
}

if [ -n "$ZONE_NAME" ]; then
  ZONE_JSON="$("$WRAPPER" GET "/zones?name=${ZONE_NAME}")"
else
  ZONE_JSON="$("$WRAPPER" GET "/zones?per_page=20")"
fi

echo "$ZONE_JSON"

echo "$ZONE_JSON" | grep -q '"success":true' || {
  echo "Cloudflare zone listing failed." >&2
  exit 1
}

echo "[OK] Cloudflare API path is working."
