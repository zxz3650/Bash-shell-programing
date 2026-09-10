#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: UID 0 계정과 로그인 셸 구분
awk -F: '$3==0 {print $1 "|" $7}' "$COURSE_DATA/passwd.sample" > "$COURSE_OUT/uid0.psv"
test "$(wc -l < "$COURSE_OUT/uid0.psv")" -eq 2
grep -Fx 'legacy-admin|/usr/sbin/nologin' "$COURSE_OUT/uid0.psv"

# STEP: 비트와 승인 기준선 함께 읽기
awk -F '|' 'NR>1 && $4 ~ /^[4567]/ {print $1 "|" $4 "|" $6}' \
 "$COURSE_DATA/permissions.psv" > "$COURSE_OUT/suid-review.psv"
grep -Fx '/usr/bin/passwd|4755|baseline' "$COURSE_OUT/suid-review.psv"

# STEP: 검토 대상과 취약점 확정 구분
awk -F '|' 'NR>1 && $6=="review" {print $1 "|" $3 "|" $4}' \
 "$COURSE_DATA/permissions.psv" > "$COURSE_OUT/review.psv"
grep -Fx '/opt/collector/bin/report|collector|0775' "$COURSE_OUT/review.psv"
printf 'review_items=1 exploitation_proven=no\n'
