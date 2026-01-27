#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

curl -fsS "$BASE_URL/api/v1/health"
curl -fsS "$BASE_URL/api/v1/ready"
curl -fsS "$BASE_URL/api/v1/metrics" | grep -q "ai_native_requests_total"
