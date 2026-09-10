#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: 실행하지 않을 교육용 파일 만들기
mkdir "$COURSE_OUT/tree"
printf 'plain evidence\n' > "$COURSE_OUT/tree/file with spaces.txt"
printf 'hidden note\n' > "$COURSE_OUT/tree/.note"
printf 'option-like filename\n' > "$COURSE_OUT/tree/-n"
printf 'new line filename\n' > "$COURSE_OUT/tree/line"$'\n'"break.txt"
printf 'created_files=4\n'

# STEP: NUL 구분 목록으로 파일 경계 보존
find "$COURSE_OUT/tree" -type f -print0 > "$COURSE_OUT/files.nul"
count=0
while IFS= read -r -d '' path; do
    test -f "$path"
    count=$((count + 1))
done < "$COURSE_OUT/files.nul"
test "$count" -eq 4
printf 'nul_records=%s\n' "$count"

# STEP: 줄 수와 파일 수의 차이 확인
find "$COURSE_OUT/tree" -type f -print > "$COURSE_OUT/files.lines"
test "$(wc -l < "$COURSE_OUT/files.lines")" -eq 5
printf 'line_count=5 but file_count=4\n'

# STEP: 사본 변경과 원본 구분
cp "$COURSE_OUT/tree/file with spaces.txt" "$COURSE_OUT/review-copy.txt"
printf 'analyst annotation\n' >> "$COURSE_OUT/review-copy.txt"
status=0
cmp -s "$COURSE_OUT/tree/file with spaces.txt" "$COURSE_OUT/review-copy.txt" || status=$?
test "$status" -eq 1
test "$(cat "$COURSE_OUT/tree/file with spaces.txt")" = 'plain evidence'
printf 'copy_changed=yes source_text_preserved=yes\n'
