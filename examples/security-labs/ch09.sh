#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: 사건 수와 아티팩트 행 수 구분
awk -F '|' 'NR>1 && $2=="analyst" {print $1 "|" $4 "|" $5}' "$COURSE_DATA/login-review.psv" > "$COURSE_OUT/login-context.psv"
test "$(wc -l < "$COURSE_OUT/login-context.psv")" -eq 4
printf 'artifact_rows=4 not four independent successful logins\n'

# STEP: 인증 방식과 세션 기록 교차 확인
grep -F 'Accepted publickey for analyst' "$COURSE_DATA/auth.log" > "$COURSE_OUT/auth-success.txt"
test "$(wc -l < "$COURSE_OUT/auth-success.txt")" -eq 1
awk -F '|' 'NR>1 && $1=="wtmp-summary" {print $4}' "$COURSE_DATA/login-review.psv" > "$COURSE_OUT/session-time.txt"
grep -Fx '2026-09-10T09:02:00+09:00' "$COURSE_OUT/session-time.txt"

# STEP: 변형된 입력을 조용히 무시하지 않기
printf 'artifact|user|source|time_kst|meaning\nbroken|record\n' > "$COURSE_OUT/malformed.psv"
status=0
awk -F '|' 'NR>1 && NF!=5 {bad=1} END {exit bad}' "$COURSE_OUT/malformed.psv" || status=$?
test "$status" -eq 1
printf 'malformed_detected=yes coverage=selected_records\n'
