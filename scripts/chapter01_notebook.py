"""Chapter 01 companion, built by build_jupyter_book.py using existing cell helpers."""


def build_chapter01(md, code, setup_cell, notebook, root):
    fixture = (root / "examples/first-observation/fixtures/case.txt").read_text(encoding="utf-8")
    observer = (root / "examples/first-observation/observe-context.sh").read_text(encoding="utf-8")
    return notebook("01. Linux 보안 조사와 Shell 실행 모델", [
        md("""## Goal

어느 환경에서 누구의 권한으로 관찰하는지 확인하고, 출력·오류·상태를 구분해 첫 조사 기록을 만듭니다. Bash/Python 선택 기준도 같은 업무 안에서 검토합니다.

- [01-1](../../01-bash-intro/01-1-first-observation.md): 호스트·사용자·셸 정보 해석
- [01-2](../../01-bash-intro/01-2-shell-execution.md): 인용·환경·종료 상태
- [01-3](../../01-bash-intro/01-3-artifacts-and-reasoning.md): 사실·가설·기록 한계
- [01-4](../../01-bash-intro/01-4-observation-lab.md): 실습·평가

전체 시스템 조사나 외부 접속은 하지 않습니다. 고정된 합성 자료와 자기 환경 관찰을 구분합니다."""),
        md("""## Setup

Python 커널에서 `%%bash` 셀을 실행합니다. Bash 3.2 이상과 date·hostname·uname·id·ps, Asia/Seoul 시간대 데이터가 필요합니다. Ubuntu VM이 기준입니다. macOS·Colab에서는 그 실행 환경을 관찰할 뿐 Linux 서버 전체 증거가 아닙니다.

새 임시 디렉터리만 만들며 관리자 권한을 요구하지 않습니다. 임시 폴더는 OS 샌드박스가 아니므로 실행 코드를 먼저 읽습니다. 셀마다 Bash가 새로 시작하므로 파일과 BASH_LAB_DIR로 실습 상태를 전달합니다. 시간대는 각 날짜 명령에서 명시합니다. 시스템 시계를 변경하지 않습니다.

이 노트북은 실행 중 자료나 코드를 다운로드하지 않습니다. 아래 fixture와 도구는 저장소 원본에서 빌드 시 포함됩니다. 공개 노트북에는 실행 출력을 저장하지 않습니다."""),
        setup_cell("01"),
        code("from pathlib import Path\nimport hashlib\nimport os\n\nfixture = Path(os.environ['BASH_LAB_DIR']) / 'case.txt'\nfixture.write_text(" + repr(fixture) + ", encoding='utf-8')\noriginal_digest = hashlib.sha256(fixture.read_bytes()).hexdigest()\nprint('교육용 원본 준비 완료: 실제 사건 자료가 아닙니다.')"),
        md("""## Steps

### 1. 보안 질문과 입력 자료

무엇을 확인할까요? 출처, 호스트, 시각, 사용자 ID, 설정된 셸과 관찰한 셸의 차이를 찾습니다. **기대값:** source_type은 synthetic, UID는 1000, Audit 수집 범위는 unknown입니다. UID나 그룹만으로 실제 권한 상승을 결론 내리지 않습니다."""),
        code(r'''%%bash
set -euo pipefail
cat "$BASH_LAB_DIR/case.txt"
grep -Fx 'source_type=synthetic' "$BASH_LAB_DIR/case.txt"
grep -Fx 'uid=1000' "$BASH_LAB_DIR/case.txt"
grep -Fx 'audit_coverage=unknown' "$BASH_LAB_DIR/case.txt"
'''),
        md("""### 2. 원본 시각과 KST는 같은 순간을 다르게 표시할 수 있습니다

고정 교육용 시각 `2026-09-10T00:00:00Z`는 KST의 `2026-09-10T09:00:00+09:00`입니다. 원본 문자열은 유지하고 별도 표시값을 만듭니다. Python은 시간 계산의 작은 보조 역할만 담당합니다. 원본 문자열의 시간대 접미사만 바꾸지 않습니다."""),
        code("""from datetime import datetime, timedelta, timezone

raw_time = '2026-09-10T00:00:00Z'
parsed_time = datetime.fromisoformat(raw_time.replace('Z', '+00:00'))
kst_time = parsed_time.astimezone(timezone(timedelta(hours=9))).isoformat()
assert kst_time == '2026-09-10T09:00:00+09:00'
assert raw_time == '2026-09-10T00:00:00Z'
print(f'원본={raw_time}')
print(f'KST={kst_time}')"""),
        md("""### 3. Bash Point — 공백이 있는 조사 표식

잘못된 인용은 삭제 명령이 아닌 printf로만 관찰합니다. **예상:** 인용 없는 전달은 두 행, 인용한 전달은 `<case 01>` 한 행입니다. 일반 명령의 단어 분리 때문에 달라집니다."""),
        code(r'''%%bash
set -euo pipefail
label='case 01'
# 의도적으로 잘못된 인용을 출력만으로 관찰합니다.
printf '<%s>\n' $label > "$BASH_LAB_DIR/unquoted.txt"
printf '<%s>\n' "$label" > "$BASH_LAB_DIR/quoted.txt"
cat "$BASH_LAB_DIR/unquoted.txt"
cat "$BASH_LAB_DIR/quoted.txt"
test "$(wc -l < "$BASH_LAB_DIR/unquoted.txt")" -eq 2
test "$(wc -l < "$BASH_LAB_DIR/quoted.txt")" -eq 1
test "$(cat "$BASH_LAB_DIR/quoted.txt")" = '<case 01>'
'''),
        md("""### 4. Bash Point — 환경 전달과 새 프로세스

export는 자식에게 값을 전달하며 비밀정보 보호 기능이 아닙니다. **예상:** 일반 변수는 자식에서 unset, LAB_CASE는 LAB-001입니다. 개인 환경 전체를 출력하지 않습니다."""),
        code(r'''%%bash
set -euo pipefail
lab_label='parent-only'
export LAB_CASE='LAB-001'
observed=$(bash -c 'printf "label=%s case=%s" "${lab_label-unset}" "$LAB_CASE"')
printf '%s\n' "$observed"
test "$observed" = 'label=unset case=LAB-001'
'''),
        md("""### 5. Bash Point — 출력·오류·상태

자료 한 행이 나와도 실패할 수 있습니다. **예상:** stdout은 data, stderr는 diagnostic, 종료 상태는 7입니다. 7은 이 실습이 정한 값입니다. 실패를 예상하는 명령은 명시적으로 포착합니다."""),
        code(r'''%%bash
set -euo pipefail
status=0
bash -c 'printf "data\n"; printf "diagnostic\n" >&2; exit 7' \
  > "$BASH_LAB_DIR/out.txt" 2> "$BASH_LAB_DIR/err.txt" || status=$?
test "$status" -eq 7
test "$(cat "$BASH_LAB_DIR/out.txt")" = data
test "$(cat "$BASH_LAB_DIR/err.txt")" = diagnostic
printf 'stdout=data stderr=diagnostic status=%s\n' "$status"
'''),
        md("""### 6. 자기 환경 관찰 도구 준비

다음 코드는 교안의 기준 구현입니다. 수집 명령, 명령 치환, 실패 처리, printf를 찾아 표시합니다. 아직 함수를 새로 설계하는 과제는 아닙니다. 도구는 파일을 쓰지 않고 자기 환경 기본 정보만 stdout에 출력합니다. 조회 실패 때 완성 보고서를 내보내지 않습니다."""),
        code('%%bash\nset -euo pipefail\ncat > "$BASH_LAB_DIR/observe-context.sh" <<\'COURSE_OBSERVER\'\n' + observer + 'COURSE_OBSERVER\nbash -n "$BASH_LAB_DIR/observe-context.sh"'),
        md("""### 7. 자기 환경 관찰과 저장

**예상:** source_type=live_self, KST 오프셋 +0900, collection_status=complete가 있습니다. 호스트·ID·커널·PID는 고정 정답이 아닙니다. 이 스크립트의 Bash 프로세스만 관찰하며 전체 목록이 아닙니다.

set -C로 기존 일반 파일 덮어쓰기를 거부합니다. 이 셀만 다시 실행하면 충돌할 수 있으므로 처음부터 새 임시 폴더로 재실행합니다. 원본 fixture는 출력 대상으로 쓰지 않습니다."""),
        code(r'''%%bash
set -euo pipefail
umask 077
(set -C; bash "$BASH_LAB_DIR/observe-context.sh" > "$BASH_LAB_DIR/context.txt")
grep -Fx 'source_type=live_self' "$BASH_LAB_DIR/context.txt"
grep -E '^observed_at_kst=.+\+0900$' "$BASH_LAB_DIR/context.txt"
grep -Fx 'collection_status=complete' "$BASH_LAB_DIR/context.txt"
# 공유 출력은 민감한 호스트명·ID 대신 구조 확인 결과로 제한합니다.
printf '자기 환경 관찰 완료. 원문 context.txt는 검토 후 공유하세요.\n'
'''),
        md("""### 8. 사용 오류와 기존 결과 보존

**예상:** 인수가 있으면 상태 2와 사용법이 나오고, 이미 저장된 context.txt에는 새 내용이 기록되지 않습니다. 파일 존재만으로 수집 성공을 판정하지 않습니다."""),
        code(r'''%%bash
set -euo pipefail
status=0
bash "$BASH_LAB_DIR/observe-context.sh" unexpected \
  > "$BASH_LAB_DIR/usage-out.txt" 2> "$BASH_LAB_DIR/usage-err.txt" || status=$?
test "$status" -eq 2
test ! -s "$BASH_LAB_DIR/usage-out.txt"
grep -q '^usage:' "$BASH_LAB_DIR/usage-err.txt"
status=0
(set -C; printf 'replacement\n' > "$BASH_LAB_DIR/context.txt") \
  2> "$BASH_LAB_DIR/conflict.txt" || status=$?
test "$status" -ne 0
grep -Fx 'collection_status=complete' "$BASH_LAB_DIR/context.txt"
printf '사용 오류와 덮어쓰기 거부 확인\n'
'''),
        md("""### 9. 기존 명령 조합과 Bash/Python 선택

아래는 실제 인증 로그가 아니라 단순한 교육용 애플리케이션 로그입니다. **예상:** ERROR는 3건, database timeout은 2건, invalid token은 1건입니다. 짧은 명령 연결에는 Bash가 적합하지만 복잡한 로그 파싱·시간 계산은 전용 도구로 분리할 수 있습니다."""),
        code(r'''%%bash
set -euo pipefail
cat > "$BASH_LAB_DIR/app.log" <<'COURSE_LOG'
2026-09-10T09:00:00+09:00 INFO api started
2026-09-10T09:01:00+09:00 ERROR database timeout
2026-09-10T09:02:00+09:00 WARN retry scheduled
2026-09-10T09:03:00+09:00 ERROR database timeout
2026-09-10T09:04:00+09:00 ERROR invalid token
COURSE_LOG
grep ' ERROR ' "$BASH_LAB_DIR/app.log" |
  cut -d' ' -f3- | LC_ALL=C sort | uniq -c | LC_ALL=C sort -nr |
  tee "$BASH_LAB_DIR/summary.txt"
test "$(grep -c ' ERROR ' "$BASH_LAB_DIR/app.log")" -eq 3
grep -Eq '^[[:space:]]*2 database timeout$' "$BASH_LAB_DIR/summary.txt"
grep -Eq '^[[:space:]]*1 invalid token$' "$BASH_LAB_DIR/summary.txt"
'''),
        md("""### 10. 선택 학습 — 판단 기준을 함수로 읽기

기존 도구 선택 연습입니다. 함수·조건문은 후속 장에서 더 배우며 여기서는 **첫 결과 Bash, 뒤의 두 결과 Python**을 확인하고 이유를 설명합니다. 이 단순 분기는 모든 도구 선택 문제의 정답표가 아닙니다."""),
        code(r'''%%bash
set -euo pipefail
choose_tool() {
  local external_commands=$1 structured_data=$2 long_lived=$3
  if [[ $external_commands == yes && $structured_data == no && $long_lived == no ]]; then
    printf 'Bash\n'
  else
    printf 'Python\n'
  fi
}
test "$(choose_tool yes no no)" = Bash
test "$(choose_tool yes yes no)" = Python
test "$(choose_tool no yes yes)" = Python
printf '명령 조합=Bash, 복잡한 자료·장기 실행=Python 검토\n'
'''),
        md("""## Checks

실행 검사는 아래에서 확인합니다. 분석 질문은 직접 답하고 교안의 해설과 비교합니다.

1. 어떤 정보가 고정 자료이고 어떤 정보가 자기 환경의 현재 관찰인가?
2. sudo 그룹 소속만으로 어떤 행위를 입증할 수 없는가?
3. audit_coverage=unknown은 행위가 없었다는 뜻인가?
4. 출력이 있는데도 실패할 수 있는가?
5. 같은 환경 확인 명령을 정상 관리자와 공격자가 사용할 때 무엇을 더 보아야 하는가?
6. source_type=live_self를 실제 사건 당시 증거로 쓰면 왜 안 되는가?
7. 원본 시각과 KST 표시값을 왜 구분하는가?"""),
        code("""from pathlib import Path
import hashlib
import os

lab = Path(os.environ['BASH_LAB_DIR'])
assert hashlib.sha256((lab / 'case.txt').read_bytes()).hexdigest() == original_digest
report = (lab / 'context.txt').read_text()
assert 'source_type=live_self\\n' in report
assert 'display_timezone=Asia/Seoul (UTC+09:00)\\n' in report
assert report.endswith('collection_status=complete\\n')
assert (lab / 'usage-out.txt').stat().st_size == 0
print('원본 보존·출처·시간대·상태 검사 통과')"""),
        md("""## Next Steps

결과 파일은 검토할 수 있도록 임시 실습 디렉터리에 남깁니다. 호스트명·ID 등 실제 환경 정보가 포함될 수 있으므로 공개 저장소에 업로드하지 않습니다. 다음 실행은 새 임시 디렉터리에서 시작합니다.

01-4의 평가표로 사실·해석·추가 확인을 제출하고, 02장의 환경·증거 취급과 기존 03장의 필요한 문법을 이어서 학습합니다. 이 노트북은 전체 DFIR 수집기나 침해 판정 도구가 아닙니다.

참고: [GNU Shell Operation](https://www.gnu.org/software/bash/manual/html_node/Shell-Operation.html), [GNU date](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html), [MITRE T1082](https://attack.mitre.org/techniques/T1082/)."""),
    ])
