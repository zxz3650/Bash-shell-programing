#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: 문자열과 정규식 비교
grep -F 'indicator.example' "$COURSE_DATA/ioc.log" > "$COURSE_OUT/literal.txt"
grep 'indicator.example' "$COURSE_DATA/ioc.log" > "$COURSE_OUT/regex.txt"
test "$(wc -l < "$COURSE_OUT/literal.txt")" -eq 1
test "$(wc -l < "$COURSE_OUT/regex.txt")" -eq 2
printf 'literal=1 regex=2\n'

# STEP: 부분 문자열과 필드의 정확한 값 구분
grep -F '192.0.2.10' "$COURSE_DATA/ioc.log" > "$COURSE_OUT/substring.txt"
awk '$2 == "src=192.0.2.10" {print}' "$COURSE_DATA/ioc.log" > "$COURSE_OUT/exact-field.txt"
test "$(wc -l < "$COURSE_OUT/substring.txt")" -eq 2
test "$(wc -l < "$COURSE_OUT/exact-field.txt")" -eq 1
printf 'substring=2 exact_field=1\n'

# STEP: 검색 결과 없음과 오류 구분
status=0
grep -F -- 'absent-marker' "$COURSE_DATA/ioc.log" > "$COURSE_OUT/no-match.txt" || status=$?
test "$status" -eq 1
test ! -s "$COURSE_OUT/no-match.txt"
printf 'no_match_status=1\n'

# STEP: 반복 입력을 코드로 실행하지 않기
printf '%s\n' 'indicator.example' 'absent-marker' > "$COURSE_OUT/indicators.txt"
while IFS= read -r indicator; do
    status=0
    grep -F -- "$indicator" "$COURSE_DATA/ioc.log" > /dev/null || status=$?
    case $status in
        0) printf 'found=%s\n' "$indicator" ;;
        1) printf 'not_found=%s\n' "$indicator" ;;
        *) exit "$status" ;;
    esac
done < "$COURSE_OUT/indicators.txt"

# STEP: getopts로 입력을 받는 검색 도구 확인
bash "$COURSE_TOOLS/ioc-search.sh" -f "$COURSE_DATA/ioc.log" -i 'indicator.example' > "$COURSE_OUT/cli.txt"
test "$(wc -l < "$COURSE_OUT/cli.txt")" -eq 1
grep -q '^3:' "$COURSE_OUT/cli.txt"
printf 'cli_literal_match=1\n'
