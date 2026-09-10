#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?set COURSE_DATA}" "${COURSE_OUT:?set COURSE_OUT}"

# STEP: 자료의 출처와 시각 확인
grep -Fx 'source_type=synthetic' "$COURSE_DATA/provenance.txt"
grep -Fx 'source_timezone=Asia/Seoul' "$COURSE_DATA/provenance.txt"
grep -Fx 'audit_coverage=partial' "$COURSE_DATA/provenance.txt"

# STEP: 원본과 작업 사본 구분
umask 077
cp "$COURSE_DATA/provenance.txt" "$COURSE_OUT/working-copy.txt"
cmp "$COURSE_DATA/provenance.txt" "$COURSE_OUT/working-copy.txt"
printf 'copy_matches=yes\n'

# STEP: 결과를 별도 파일에 기록
printf 'case_id=COURSE-IR-002\nanalysis_status=needs_more_evidence\n' > "$COURSE_OUT/analysis.txt"
test "$(wc -l < "$COURSE_OUT/analysis.txt")" -eq 2
printf 'original_and_analysis=separate\n'

# STEP: 누락을 정상 결과로 바꾸지 않기
if test -r "$COURSE_DATA/not-collected.txt"; then
    printf 'unexpected fixture\n' >&2
    exit 1
else
    printf 'not-collected=unavailable, not zero events\n'
fi
