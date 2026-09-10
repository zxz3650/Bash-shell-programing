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

# STEP: GTFOBins 검토 카드의 형식과 허용값 확인
# Synthetic assessment summaries, not live sudo policy or a binary catalogue.
awk -F '|' '
 NR==1 {
   if ($0!="case_id|tool_role|reference_listed|context|business_need|approval|scope_fit|telemetry") bad=1
   next
 }
 NF!=8 || $1!~/^R[0-9][0-9]$/ || seen[$1]++ || $2=="" ||
 $3!~/^(yes|no)$/ || $4!~/^(unprivileged|sudo|suid|capabilities|service)$/ ||
 $5!~/^(documented|unknown)$/ || $6!~/^(approved|unknown)$/ ||
 $7!~/^(aligned|review|unknown)$/ || $8!~/^(present|not_collected)$/ {bad=1}
 END {if (NR<2 || bad) exit 2}
' "$COURSE_DATA/tool-review.psv"
printf 'review_schema=valid\n'

# STEP: 설정 검토와 실행 자료를 서로 다른 축으로 집계
awk -F '|' 'NR>1 {print $1 "|" $3 "|" $7 "|" $8}' \
 "$COURSE_DATA/tool-review.psv" > "$COURSE_OUT/tool-review-results.psv"
awk -F '|' 'NR>1 {scope[$7]++; telemetry[$8]++}
 END {
   printf "aligned=%d review=%d unknown=%d\n", scope["aligned"],scope["review"],scope["unknown"]
   printf "telemetry_present=%d telemetry_not_collected=%d\n",telemetry["present"],telemetry["not_collected"]
 }' "$COURSE_DATA/tool-review.psv" > "$COURSE_OUT/tool-review-counts.txt"
grep -Fx 'aligned=2 review=1 unknown=1' "$COURSE_OUT/tool-review-counts.txt"
grep -Fx 'telemetry_present=2 telemetry_not_collected=2' "$COURSE_OUT/tool-review-counts.txt"
grep -Fx 'R02|yes|unknown|not_collected' "$COURSE_OUT/tool-review-results.psv"
grep -Fx 'R03|no|review|not_collected' "$COURSE_OUT/tool-review-results.psv"
printf 'catalogue_membership_is_not_a_verdict=yes\n'
