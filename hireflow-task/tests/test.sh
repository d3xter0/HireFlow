#!/usr/bin/env bash
set -euo pipefail

mkdir -p /logs/verifier
BASE_URL="http://localhost:5000"

AUTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer USER1_TOKEN" "${BASE_URL}/resume/1/download")

IDOR_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer USER1_TOKEN" "${BASE_URL}/resume/2/download")

if [ "$AUTH_STATUS" -eq 200 ] && [ "$IDOR_STATUS" -eq 403 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
