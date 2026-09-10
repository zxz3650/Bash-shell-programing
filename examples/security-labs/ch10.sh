#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: Journal 요약에서 서비스와 부팅 문맥 선택
awk -F '|' 'NR>1 && $3=="report-helper.service" {print $1 "|" $2 "|" $5}' \
 "$COURSE_DATA/journal-review.psv" > "$COURSE_OUT/service-events.psv"
test "$(wc -l < "$COURSE_OUT/service-events.psv")" -eq 2
cat "$COURSE_OUT/service-events.psv"

# STEP: Audit 레코드와 이벤트 수 구분
sed -n 's/.*msg=audit(\([^)]*\)).*/\1/p' "$COURSE_DATA/audit.log" | LC_ALL=C sort -u > "$COURSE_OUT/event-ids.txt"
test "$(wc -l < "$COURSE_DATA/audit.log")" -eq 6
test "$(wc -l < "$COURSE_OUT/event-ids.txt")" -eq 1
grep -Fx '1788998580.000:900' "$COURSE_OUT/event-ids.txt"
printf 'audit_records=6 audit_events=1\n'

# STEP: 원래 로그인 ID와 실행 권한 구분
grep -F 'type=SYSCALL ' "$COURSE_DATA/audit.log" > "$COURSE_OUT/syscall.txt"
grep -qF 'auid=1000 uid=0 gid=0 euid=0' "$COURSE_OUT/syscall.txt"
grep -qF 'exe="/usr/bin/id"' "$COURSE_OUT/syscall.txt"
printf 'auid=1000 euid=0 command=id approval=not_in_audit_record\n'
