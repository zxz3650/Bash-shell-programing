#!/usr/bin/env python3
"""Generate the student-facing Bash tutorial notebooks deterministically."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "jupyter-book" / "labs"


def md(source: str) -> dict:
    normalized = source.strip() + "\n"
    cell_id = "m-" + hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:10]
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": normalized}


def code(source: str) -> dict:
    normalized = source.strip() + "\n"
    cell_id = "c-" + hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:10]
    return {
        "cell_type": "code",
        "id": cell_id,
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": normalized,
    }


def setup_cell(slug: str) -> dict:
    return code(
        f'''from pathlib import Path
import os
import shutil
import tempfile

lab_dir = Path(tempfile.mkdtemp(prefix="bash-book-{slug}-"))
os.environ["BASH_LAB_DIR"] = str(lab_dir)
print(f"격리된 실습 디렉터리: {{lab_dir}}")'''
    )


def cleanup_cell() -> dict:
    return code(
        '''import shutil
from pathlib import Path
import os

lab_dir = Path(os.environ["BASH_LAB_DIR"])
shutil.rmtree(lab_dir, ignore_errors=True)
print(f"정리 완료: {lab_dir}")'''
    )


def notebook(title: str, cells: list[dict]) -> dict:
    return {
        "cells": [md(f"# {title}")] + cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


NOTEBOOKS: dict[str, dict] = {
    "00-orientation-and-safety.ipynb": notebook(
        "00. 환경 확인과 안전 규칙",
        [
            md(
                """## Goal

- 현재 셸과 Bash 버전을 확인한다.
- 실습 파일을 격리된 임시 디렉터리에서만 만든다.
- 명령의 출력과 종료 상태를 함께 관찰한다."""
            ),
            md(
                """## Setup

아래 Python 셀은 매 실습마다 새로운 임시 디렉터리를 만들고 `BASH_LAB_DIR` 환경 변수에 저장합니다. 이후 Bash 셀은 이 경로 안에서만 파일을 생성합니다."""
            ),
            setup_cell("00"),
            md("## Steps\n\n### 1. 실행 환경 확인"),
            code(
                '''%%bash
set -euo pipefail
printf 'Bash path: %s\\n' "$(command -v bash)"
bash --version | head -n 1
printf 'Lab directory: %s\\n' "$BASH_LAB_DIR"
test -d "$BASH_LAB_DIR"'''
            ),
            md("### 2. 출력과 오류 분리"),
            code(
                '''%%bash
set -u
printf '정상 출력\\n'
printf '오류 출력 예시\\n' >&2
bash -c 'exit 7' || status=$?
printf '관찰한 종료 상태=%s\\n' "${status:-0}"'''
            ),
            md("### 3. 실습 파일 생성"),
            code(
                '''%%bash
set -euo pipefail
printf 'student=ready\\n' > "$BASH_LAB_DIR/state.txt"
ls -l "$BASH_LAB_DIR/state.txt"
cat "$BASH_LAB_DIR/state.txt"'''
            ),
            md(
                """## Checks

- Bash 실행 경로와 버전이 출력되었는가?
- 실패한 명령의 종료 상태가 `7`로 표시되었는가?
- 생성한 파일이 `BASH_LAB_DIR` 안에 있는가?"""
            ),
            md("## Next Steps\n\n다음 실습에서는 같은 문제를 Bash와 Python 중 어느 언어로 해결할지 판단합니다."),
            cleanup_cell(),
        ],
    ),
    "01-when-to-use-bash.ipynb": notebook(
        "01. Bash를 선택하는 기준",
        [
            md(
                """## Goal

- 외부 명령 조합, 단순 텍스트, 종료 상태가 중심인 작업을 식별한다.
- 복잡한 데이터 구조와 예외 처리가 필요한 작업은 Python으로 넘긴다.
- 짧은 로그 파이프라인을 직접 구성한다."""
            ),
            md("## Setup"),
            setup_cell("01"),
            code(
                '''%%bash
set -euo pipefail
cat > "$BASH_LAB_DIR/app.log" <<'EOF'
2026-09-04T09:00:00Z INFO api started
2026-09-04T09:01:00Z ERROR database timeout
2026-09-04T09:02:00Z WARN retry scheduled
2026-09-04T09:03:00Z ERROR database timeout
2026-09-04T09:04:00Z ERROR invalid token
EOF
wc -l "$BASH_LAB_DIR/app.log"'''
            ),
            md("## Steps\n\n### 1. 기존 명령을 파이프로 조합"),
            code(
                '''%%bash
set -euo pipefail
grep ' ERROR ' "$BASH_LAB_DIR/app.log" \
  | cut -d' ' -f3- \
  | sort \
  | uniq -c \
  | sort -nr'''
            ),
            md(
                """### 2. 선택 기준 적용

위 작업은 행 단위 텍스트를 `grep`, `cut`, `sort`, `uniq`로 처리합니다. 별도 데이터 모델이 없고 각 단계의 입력·출력이 눈에 보이므로 Bash가 적합합니다.

반대로 다음 요구가 추가되면 Python 전환을 검토합니다.

- 중첩 JSON의 스키마 검증
- 오류 유형별 복잡한 재시도 정책
- 데이터베이스와 API를 함께 사용하는 장기 실행 서비스
- 여러 모듈로 나뉘는 대규모 테스트 코드"""
            ),
            md("### 3. 판단표를 명령으로 표현"),
            code(
                '''%%bash
set -euo pipefail
choose_tool() {
  local external_commands=$1 structured_data=$2 long_lived=$3
  if [[ $external_commands == yes && $structured_data == no && $long_lived == no ]]; then
    printf 'Bash\\n'
  else
    printf 'Python or another general-purpose language\\n'
  fi
}

choose_tool yes no no
choose_tool yes yes no
choose_tool no yes yes'''
            ),
            md(
                """## Checks

아래 질문 중 앞의 세 항목에 대부분 `예`, 뒤의 두 항목에 `아니오`라면 Bash를 우선 검토합니다.

1. 외부 명령 실행이 작업의 중심인가?
2. 데이터가 파일 경로나 행 단위 텍스트인가?
3. 짧은 실행 후 종료하는 자동화인가?
4. 복잡한 객체·스키마·비즈니스 로직이 필요한가?
5. 장시간 실행되는 서비스인가?"""
            ),
            md("## Next Steps\n\nBash가 적합한 작은 작업을 인자, 변수, 배열로 일반화합니다."),
            cleanup_cell(),
        ],
    ),
    "02-arguments-variables-arrays.ipynb": notebook(
        "02. 인자, 변수, 배열과 안전한 인용",
        [
            md("## Goal\n\n위치 인자와 배열을 사용하고, 공백이 포함된 값을 손상 없이 전달합니다."),
            md("## Setup"),
            setup_cell("02"),
            md("## Steps\n\n### 1. 위치 인자 검증"),
            code(
                '''%%bash
set -euo pipefail
bash -s -- "report file.txt" "high priority" <<'BASH'
set -euo pipefail
if [[ $# -ne 2 ]]; then
  printf 'Usage: %s <file> <label>\\n' "$0" >&2
  exit 64
fi
printf 'file=<%s> label=<%s>\\n' "$1" "$2"
BASH'''
            ),
            md("### 2. 배열 원소 경계 보존"),
            code(
                '''%%bash
set -euo pipefail
items=("alpha.log" "two words.log" "final.log")
printf '원소 수=%s\\n' "${#items[@]}"
for item in "${items[@]}"; do
  printf '[%s]\\n' "$item"
done'''
            ),
            md("### 3. 실패 사례와 수정"),
            code(
                '''%%bash
set -euo pipefail
value='two words'
printf '올바른 전달: '
printf '<%s>\\n' "$value"
printf '항상 변수 확장을 큰따옴표로 감싸는 습관을 유지합니다.\\n' ''
'''
            ),
            md(
                """## Checks

- 출력에서 `report file.txt`가 두 단어로 분리되지 않았는가?
- 배열 원소 수가 `3`인가?
- `"$value"`, `"$@"`, `"${items[@]}"`가 각각 어떤 경계를 보존하는지 설명할 수 있는가?"""
            ),
            md("## Next Steps\n\n검증한 입력을 조건문, 반복문, 함수로 처리합니다."),
            cleanup_cell(),
        ],
    ),
    "03-conditions-loops-functions.ipynb": notebook(
        "03. 조건문, 반복문과 함수",
        [
            md("## Goal\n\n조건에 따라 파일을 분류하고 반복 작업을 함수로 캡슐화합니다."),
            md("## Setup"),
            setup_cell("03"),
            code(
                '''%%bash
set -euo pipefail
printf 'ok\\n' > "$BASH_LAB_DIR/a.log"
: > "$BASH_LAB_DIR/empty.log"
printf '# notes\\n' > "$BASH_LAB_DIR/readme.md"'''
            ),
            md("## Steps\n\n### 1. 파일 상태를 함수로 분류"),
            code(
                '''%%bash
set -euo pipefail
classify_file() {
  local path=$1
  if [[ ! -e $path ]]; then
    printf '%s: missing\\n' "$path"
  elif [[ ! -s $path ]]; then
    printf '%s: empty\\n' "$path"
  elif [[ $path == *.log ]]; then
    printf '%s: non-empty log\\n' "$path"
  else
    printf '%s: other file\\n' "$path"
  fi
}

for path in "$BASH_LAB_DIR"/* "$BASH_LAB_DIR/missing.txt"; do
  classify_file "$path"
done'''
            ),
            md("### 2. 함수의 출력과 종료 상태 구분"),
            code(
                '''%%bash
set -euo pipefail
require_readable() {
  local path=$1
  [[ -r $path ]] || { printf 'not readable: %s\\n' "$path" >&2; return 1; }
  printf '%s\\n' "$path"
}

if readable=$(require_readable "$BASH_LAB_DIR/a.log"); then
  printf '검증 성공: %s\\n' "$readable"
fi'''
            ),
            md(
                """## Checks

- 빈 파일, 로그 파일, 기타 파일, 없는 파일이 서로 다르게 분류되는가?
- `local`이 함수 밖의 변수 오염을 줄이는 이유를 설명할 수 있는가?
- 데이터는 표준 출력, 오류는 표준 오류, 성공 여부는 종료 상태로 전달했는가?"""
            ),
            md("## Next Steps\n\n분류한 파일을 권한·리다이렉션·파이프라인과 함께 처리합니다."),
            cleanup_cell(),
        ],
    ),
    "04-files-permissions-pipelines.ipynb": notebook(
        "04. 파일, 권한과 파이프라인",
        [
            md("## Goal\n\n파일을 안전하게 만들고 권한을 제한하며 파이프라인 실패를 감지합니다."),
            md("## Setup"),
            setup_cell("04"),
            md("## Steps\n\n### 1. 제한된 권한으로 파일 생성"),
            code(
                '''%%bash
set -euo pipefail
umask 077
printf 'case_id=LAB-001\\n' > "$BASH_LAB_DIR/evidence.txt"
ls -l "$BASH_LAB_DIR/evidence.txt"
test ! -x "$BASH_LAB_DIR/evidence.txt"'''
            ),
            md("### 2. 표준 출력과 표준 오류 저장"),
            code(
                '''%%bash
set -euo pipefail
{
  printf 'collection started\\n'
  printf 'sample warning\\n' >&2
} >"$BASH_LAB_DIR/stdout.log" 2>"$BASH_LAB_DIR/stderr.log"
printf '%s\\n' '--- stdout ---'
cat "$BASH_LAB_DIR/stdout.log"
printf '%s\\n' '--- stderr ---'
cat "$BASH_LAB_DIR/stderr.log"'''
            ),
            md("### 3. `pipefail`로 중간 실패 감지"),
            code(
                '''%%bash
set -uo pipefail
if bash -c 'printf data; exit 9' | wc -c > /dev/null; then
  printf '예상하지 못한 성공\\n'
else
  printf '파이프라인 실패를 감지했습니다. status=%s\\n' "$?"
fi'''
            ),
            md(
                """## Checks

- 민감한 실습 파일이 다른 사용자에게 쓰기 가능하지 않은가?
- 정상 출력과 오류 출력이 서로 다른 파일에 저장되었는가?
- 파이프의 첫 명령이 실패했을 때 전체 파이프라인도 실패했는가?"""
            ),
            md("## Next Steps\n\n행 단위 로그를 필터링하고 요약 보고서를 만듭니다."),
            cleanup_cell(),
        ],
    ),
    "05-text-processing.ipynb": notebook(
        "05. 로그 텍스트 처리",
        [
            md("## Goal\n\n작은 로그를 필터링·집계하고 결과를 검증합니다."),
            md("## Setup"),
            setup_cell("05"),
            code(
                '''%%bash
set -euo pipefail
cat > "$BASH_LAB_DIR/auth.log" <<'EOF'
2026-09-04T10:00:00Z alice SUCCESS 10.0.0.10
2026-09-04T10:01:00Z bob FAILED 10.0.0.20
2026-09-04T10:02:00Z alice FAILED 10.0.0.20
2026-09-04T10:03:00Z carol FAILED 10.0.0.30
2026-09-04T10:04:00Z bob FAILED 10.0.0.20
EOF'''
            ),
            md("## Steps\n\n### 1. 실패 이벤트만 선택"),
            code(
                '''%%bash
set -euo pipefail
grep ' FAILED ' "$BASH_LAB_DIR/auth.log" > "$BASH_LAB_DIR/failed.log"
cat "$BASH_LAB_DIR/failed.log"'''
            ),
            md("### 2. 출발지 IP별 집계"),
            code(
                '''%%bash
set -euo pipefail
awk '$3 == "FAILED" { count[$4]++ } END { for (ip in count) print count[ip], ip }' \
  "$BASH_LAB_DIR/auth.log" \
  | sort -nr \
  | tee "$BASH_LAB_DIR/ip-summary.txt"'''
            ),
            md("### 3. 결과에 대한 자동 점검"),
            code(
                '''%%bash
set -euo pipefail
failed_count=$(wc -l < "$BASH_LAB_DIR/failed.log" | tr -d ' ')
top_count=$(awk 'NR == 1 { print $1 }' "$BASH_LAB_DIR/ip-summary.txt")
[[ $failed_count -eq 4 ]]
[[ $top_count -eq 3 ]]
printf 'checks passed: failed=%s top_count=%s\\n' "$failed_count" "$top_count"'''
            ),
            md(
                """## Checks

- 실패 이벤트가 정확히 4개인가?
- `10.0.0.20`이 3회로 가장 많은가?
- 공백 구분 로그가 아닌 CSV·JSON이라면 전용 파서나 Python을 선택해야 하는 이유를 설명할 수 있는가?"""
            ),
            md("## Next Steps\n\n운영체제의 상태를 읽기 전용으로 수집하고 안전 옵션을 적용합니다."),
            cleanup_cell(),
        ],
    ),
    "06-system-inspection-secure-scripting.ipynb": notebook(
        "06. 시스템 조사와 안전한 스크립팅",
        [
            md("## Goal\n\n로컬 시스템 정보를 읽기 전용으로 수집하고 실패에 안전한 스크립트 골격을 사용합니다."),
            md("## Setup"),
            setup_cell("06"),
            md("## Steps\n\n### 1. 읽기 전용 상태 스냅샷"),
            code(
                '''%%bash
set -euo pipefail
report="$BASH_LAB_DIR/system-snapshot.txt"
{
  printf '== timestamp ==\\n'
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf '\\n== kernel ==\\n'
  uname -a
  printf '\\n== filesystem ==\\n'
  df -h .
  printf '\\n== current process ==\\n'
  ps -p "$$" -o pid,ppid,comm,args
} | tee "$report"
test -s "$report"'''
            ),
            md("### 2. 입력 경로를 신뢰하기 전에 검증"),
            code(
                '''%%bash
set -euo pipefail
safe_read() {
  local requested=$1
  case $requested in
    "$BASH_LAB_DIR"/*) ;;
    *) printf '범위 밖 경로 거부: %s\\n' "$requested" >&2; return 64 ;;
  esac
  [[ -f $requested && -r $requested ]] || return 66
  cat -- "$requested"
}

safe_read "$BASH_LAB_DIR/system-snapshot.txt" | sed -n '1,4p'
if safe_read /etc/hosts >/dev/null 2>&1; then
  printf '예상하지 못한 허용\\n'
else
  printf '범위 밖 경로를 정상적으로 거부했습니다.\\n'
fi'''
            ),
            md("### 3. 종료 처리 등록"),
            code(
                '''%%bash
set -euo pipefail
demo="$BASH_LAB_DIR/trap-demo.sh"
cat > "$demo" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
tmp=$(mktemp -d)
cleanup() { rm -rf -- "$tmp"; }
trap cleanup EXIT
printf 'temporary=%s\\n' "$tmp"
printf 'done\\n' > "$tmp/result.txt"
BASH
bash "$demo"'''
            ),
            md(
                """## Checks

- 스냅샷에 시각, 커널, 파일시스템, 프로세스 정보가 포함되는가?
- 허용된 임시 디렉터리 밖의 경로를 거부하는가?
- `trap ... EXIT`가 정상 종료와 오류 종료 모두에서 정리를 보장하는 이유를 설명할 수 있는가?"""
            ),
            md("## Next Steps\n\n스크립트를 반복 실행 가능한 도구로 만들고 자동 점검을 추가합니다."),
            cleanup_cell(),
        ],
    ),
    "07-automation-testing.ipynb": notebook(
        "07. 자동화와 종료 상태 기반 테스트",
        [
            md("## Goal\n\n작은 CLI 스크립트를 만들고 성공·실패 경로를 자동으로 검증합니다."),
            md("## Setup"),
            setup_cell("07"),
            md("## Steps\n\n### 1. 검증 가능한 CLI 작성"),
            code(
                '''%%bash
set -euo pipefail
cat > "$BASH_LAB_DIR/count-lines.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  printf 'Usage: %s <readable-file>\\n' "$0" >&2
  exit 64
fi
input=$1
if [[ ! -f $input || ! -r $input ]]; then
  printf 'not a readable file: %s\\n' "$input" >&2
  exit 66
fi
wc -l < "$input" | tr -d ' '
BASH
chmod 700 "$BASH_LAB_DIR/count-lines.sh"
printf 'one\\ntwo\\nthree\\n' > "$BASH_LAB_DIR/input.txt"'''
            ),
            md("### 2. 성공 경로 테스트"),
            code(
                '''%%bash
set -euo pipefail
actual=$("$BASH_LAB_DIR/count-lines.sh" "$BASH_LAB_DIR/input.txt")
[[ $actual == 3 ]]
printf 'success test passed: %s lines\\n' "$actual"'''
            ),
            md("### 3. 실패 경로 테스트"),
            code(
                '''%%bash
set -euo pipefail
if "$BASH_LAB_DIR/count-lines.sh" "$BASH_LAB_DIR/missing.txt" \
    >"$BASH_LAB_DIR/out.txt" 2>"$BASH_LAB_DIR/err.txt"; then
  printf 'missing-file test failed\\n' >&2
  exit 1
else
  status=$?
fi
[[ $status -eq 66 ]]
grep -q 'not a readable file' "$BASH_LAB_DIR/err.txt"
printf 'failure test passed: status=%s\\n' "$status"'''
            ),
            md("### 4. 선택적 정적 분석"),
            code(
                '''%%bash
set -euo pipefail
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck "$BASH_LAB_DIR/count-lines.sh"
  printf 'ShellCheck passed\\n'
else
  printf 'ShellCheck가 없어 실행을 건너뜁니다. Ubuntu: sudo apt install shellcheck\\n'
fi'''
            ),
            md(
                """## Checks

- 정상 입력에서 `3`을 출력하고 종료 상태 `0`을 반환하는가?
- 없는 파일에서 종료 상태 `66`과 오류 메시지를 반환하는가?
- 테스트가 출력 문자열뿐 아니라 종료 상태도 검증하는가?"""
            ),
            md("## Next Steps\n\n지금까지의 패턴을 결합해 로컬 triage 수집기를 만듭니다."),
            cleanup_cell(),
        ],
    ),
    "08-capstone-triage-collector.ipynb": notebook(
        "08. 종합 프로젝트: 로컬 Triage 수집기",
        [
            md(
                """## Goal

허가된 로컬 시스템에서 읽기 전용 정보를 수집하고, 실행 로그와 체크섬을 남기는 작은 triage 도구를 완성합니다. 이 실습은 외부 호스트에 접속하거나 스캔하지 않습니다."""
            ),
            md("## Setup"),
            setup_cell("08"),
            md("## Steps\n\n### 1. 수집기 작성"),
            code(
                '''%%bash
set -euo pipefail
cat > "$BASH_LAB_DIR/collect.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
umask 077

if [[ $# -ne 1 ]]; then
  printf 'Usage: %s <output-directory>\\n' "$0" >&2
  exit 64
fi

output=$1
mkdir -p -- "$output"
log="$output/collection.log"
report="$output/system-report.txt"

log_message() { printf '%s %s\\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*" | tee -a "$log"; }

log_message 'collection started'
{
  printf '== host ==\\n'
  hostname
  printf '\\n== kernel ==\\n'
  uname -a
  printf '\\n== disk ==\\n'
  df -h .
  printf '\\n== processes ==\\n'
  ps -eo pid,ppid,user,comm | sed -n '1,21p'
} > "$report"

if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "$report" > "$output/SHA256SUMS"
else
  sha256sum "$report" > "$output/SHA256SUMS"
fi
log_message 'collection completed'
BASH
chmod 700 "$BASH_LAB_DIR/collect.sh"'''
            ),
            md("### 2. 수집 실행"),
            code(
                '''%%bash
set -euo pipefail
output="$BASH_LAB_DIR/output"
"$BASH_LAB_DIR/collect.sh" "$output"
find "$output" -maxdepth 1 -type f -print | sort
printf '%s\\n' '--- report preview ---'
sed -n '1,18p' "$output/system-report.txt"'''
            ),
            md("### 3. 결과 무결성 검증"),
            code(
                '''%%bash
set -euo pipefail
cd "$BASH_LAB_DIR/output"
if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 -c SHA256SUMS
else
  sha256sum -c SHA256SUMS
fi
grep -q 'collection started' collection.log
grep -q 'collection completed' collection.log
test -s system-report.txt
printf 'all capstone checks passed\\n' ''
'''
            ),
            md(
                """## Checks

- 출력 디렉터리에 보고서, 실행 로그, 체크섬이 생성되는가?
- 보고서가 비어 있지 않고 체크섬 검증이 성공하는가?
- 인자가 없을 때 사용법을 출력하고 실패하는가?
- 파일 권한과 허가된 실행 범위를 설명할 수 있는가?"""
            ),
            md(
                """## Next Steps

1. 수집 항목별 함수를 분리합니다.
2. `--output`, `--help` 옵션을 추가합니다.
3. Linux 환경에서 ShellCheck와 Bats 테스트를 추가합니다.
4. 결과 보존 기간과 민감정보 취급 절차를 문서화합니다."""
            ),
            cleanup_cell(),
        ],
    ),
}


def main() -> None:
    LABS.mkdir(parents=True, exist_ok=True)
    for filename, data in NOTEBOOKS.items():
        destination = LABS / filename
        destination.write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        print(destination.relative_to(ROOT))


if __name__ == "__main__":
    main()
