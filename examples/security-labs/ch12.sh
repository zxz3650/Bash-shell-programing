#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}" "${COURSE_TOOLS:?}"

# STEP: dry-run으로 필수 입력과 출력 경계 확인
bash "$COURSE_TOOLS/triage-offline.sh" -d "$COURSE_DATA" -o "$COURSE_OUT/report" -n
test ! -e "$COURSE_OUT/report"

# STEP: 기능별 사본 수집과 상태 기록
bash "$COURSE_TOOLS/triage-offline.sh" -d "$COURSE_DATA" -o "$COURSE_OUT/report"
grep -Fx 'collection_status=complete' "$COURSE_OUT/report/context.txt"
test "$(wc -l < "$COURSE_OUT/report/manifest.tsv")" -eq 13
test -s "$COURSE_OUT/report/SHA256SUMS"
test "$(cat "$COURSE_OUT/report/COLLECTION_FINISHED")" = complete

# STEP: 기존 결과 덮어쓰기 거부
status=0
bash "$COURSE_TOOLS/triage-offline.sh" -d "$COURSE_DATA" -o "$COURSE_OUT/report" \
 > "$COURSE_OUT/retry-out.txt" 2> "$COURSE_OUT/retry-err.txt" || status=$?
test "$status" -eq 2
test ! -s "$COURSE_OUT/retry-out.txt"
printf 'existing_report_preserved=yes\n'

# STEP: 사실과 가설을 분리한 인계 기록
printf 'fact=failed SSH records: 3\nfact=publickey success records: 1\nhypothesis=account access needs review\nunknown=service approval and audit completeness\n' > "$COURSE_OUT/handoff.txt"
test "$(wc -l < "$COURSE_OUT/handoff.txt")" -eq 4
printf 'handoff=2 facts, 1 hypothesis, 1 unknown\n'
