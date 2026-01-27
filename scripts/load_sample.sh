#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

for i in $(seq 1 25); do
  curl -fsS -X POST "$BASE_URL/api/v1/documents/process" \
    -H "content-type: application/json" \
    -d "{\"content\":\"sample document $i\",\"priority\":\"balanced\"}" >/dev/null
done

echo "submitted 25 sample document requests"
