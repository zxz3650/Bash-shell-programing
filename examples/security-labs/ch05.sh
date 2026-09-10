#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: 원본에서 실패 행 선택
grep -F 'Failed password' "$COURSE_DATA/auth.log" > "$COURSE_OUT/failed.txt"
test "$(wc -l < "$COURSE_OUT/failed.txt")" -eq 3
printf 'failed_rows=3\n'

# STEP: from 표식 뒤의 주소 추출
awk '{for (i=1; i<NF; i++) if ($i=="from") {print $(i+1); break}}' \
    "$COURSE_OUT/failed.txt" > "$COURSE_OUT/addresses.txt"
test "$(wc -l < "$COURSE_OUT/addresses.txt")" -eq 3
cat "$COURSE_OUT/addresses.txt"

# STEP: 정렬과 중복 집계
LC_ALL=C sort "$COURSE_OUT/addresses.txt" | uniq -c | LC_ALL=C sort -nr > "$COURSE_OUT/counts.txt"
grep -Eq '^[[:space:]]*2 192\.0\.2\.10$' "$COURSE_OUT/counts.txt"
grep -Eq '^[[:space:]]*1 198\.51\.100\.8$' "$COURSE_OUT/counts.txt"
cat "$COURSE_OUT/counts.txt"

# STEP: 성공과 실패를 별도로 읽기
grep -F 'Accepted publickey' "$COURSE_DATA/auth.log" > "$COURSE_OUT/accepted.txt"
test "$(wc -l < "$COURSE_OUT/accepted.txt")" -eq 1
grep -F 'sudo:' "$COURSE_DATA/auth.log" > "$COURSE_OUT/sudo.txt"
test "$(wc -l < "$COURSE_OUT/sudo.txt")" -eq 1
printf 'accepted_publickey=1 sudo_records=1\n'
