#!/usr/bin/env bash
set -euo pipefail
: "${COURSE_DATA:?}" "${COURSE_OUT:?}"

# STEP: 필드와 프로세스 수 확인
head -n 1 "$COURSE_DATA/processes.psv"
awk -F '|' 'NR>1 {print $1, $2, $3, $5}' "$COURSE_DATA/processes.psv" > "$COURSE_OUT/process-preview.txt"
test "$(wc -l < "$COURSE_OUT/process-preview.txt")" -eq 4
printf 'process_rows=4\n'

# STEP: PID로 연결하되 시각 한계를 유지
awk -F '|' 'NR==FNR {if (FNR>1) exe[$1]=$5; next}
 FNR>1 {print $1 "|" $3 "|" $4 "|" (($4 in exe) ? exe[$4] : "unknown")}' \
 "$COURSE_DATA/processes.psv" "$COURSE_DATA/sockets.psv" > "$COURSE_OUT/linked.psv"
grep -Fx 'ESTAB|203.0.113.7:443|520|/opt/collector/bin/report' "$COURSE_OUT/linked.psv"

# STEP: 부모와 서비스 문맥 확인
awk -F '|' 'NR>1 && $1==520 {print "parent=" $2 " user=" $3 " unit=" $6}' \
 "$COURSE_DATA/processes.psv" > "$COURSE_OUT/context.txt"
grep -Fx 'parent=1 user=collector unit=report-helper.service' "$COURSE_OUT/context.txt"
printf 'verdict=needs_service_and_destination_review\n'
