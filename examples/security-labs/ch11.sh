#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: 인용된 요청과 상태 분리
awk -F '"' '{split($3, status, " "); print $2 "|" status[1]}' "$COURSE_DATA/access.log" > "$COURSE_OUT/requests.psv"
test "$(wc -l < "$COURSE_OUT/requests.psv")" -eq 6
grep -Fx 'GET /uploads/report.txt HTTP/1.1|200' "$COURSE_OUT/requests.psv"

# STEP: 상태 분포와 요청 경로 해석
awk -F '|' '{print $2}' "$COURSE_OUT/requests.psv" | LC_ALL=C sort | uniq -c > "$COURSE_OUT/status-counts.txt"
grep -Eq '^[[:space:]]*3 401$' "$COURSE_OUT/status-counts.txt"
grep -Eq '^[[:space:]]*2 200$' "$COURSE_OUT/status-counts.txt"
grep -Eq '^[[:space:]]*1 404$' "$COURSE_OUT/status-counts.txt"
cat "$COURSE_OUT/status-counts.txt"

# STEP: 두 로컬 작업의 종료 상태 회수
wc -l < "$COURSE_DATA/auth.log" > "$COURSE_OUT/01.count" &
first_pid=$!
wc -l < "$COURSE_DATA/access.log" > "$COURSE_OUT/02.count" &
second_pid=$!
wait "$first_pid"
wait "$second_pid"
test "$(cat "$COURSE_OUT/01.count")" -eq 5
test "$(cat "$COURSE_OUT/02.count")" -eq 6
printf 'auth_rows=5 access_rows=6 order=fixed\n'
