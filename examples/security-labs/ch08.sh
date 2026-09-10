#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: 자동 시작 위치의 승인 상태 확인
awk -F '|' 'NR>1 && $4=="unknown" {print $1 "|" $2}' "$COURSE_DATA/persistence.psv" > "$COURSE_OUT/unapproved.psv"
test "$(wc -l < "$COURSE_OUT/unapproved.psv")" -eq 1
cat "$COURSE_OUT/unapproved.psv"

# STEP: 서비스 실행 주체와 경로 읽기
grep -E '^(User|ExecStart|DropInPaths|change_ticket)=' "$COURSE_DATA/service-review.txt" > "$COURSE_OUT/service-context.txt"
grep -Fx 'User=collector' "$COURSE_OUT/service-context.txt"
grep -Fx 'DropInPaths=not_collected' "$COURSE_OUT/service-context.txt"

# STEP: 정상 기준선도 함께 남기기
awk -F '|' 'NR>1 && $4!="unknown" {print $1 "|" $4}' "$COURSE_DATA/persistence.psv" > "$COURSE_OUT/known.psv"
test "$(wc -l < "$COURSE_OUT/known.psv")" -eq 3
printf 'unknown_approval=1 known_records=3 installed_by_lab=0\n'
