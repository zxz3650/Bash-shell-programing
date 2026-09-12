# 07-4. GTFOBins로 정상 도구의 권한 경계 검토하기

## 개요와 학습 목표

“운영팀이 사용하는 정상 프로그램인데 왜 권한 검토가 필요한가?” 프로그램의 이름보다 **실행하는 사람·유효 권한·허용된 기능·입력과 파일 범위**가 중요하기 때문입니다. 이 절은 07-3에서 배운 계정·SUID·sudo·Capabilities를 공개 레퍼런스의 해석과 연결합니다.

- GTFOBins의 등재와 제품 취약점 판정을 구분합니다.
- 기능과 실행 권한 문맥을 서로 다른 축으로 읽습니다.
- 설정상 위험, 실제 실행, 업무 승인 여부를 별도로 기록합니다.
- Red Team의 위험 가설을 Blue Team의 조사 질문·수집 요건·완화안으로 바꿉니다.
- 합성 검토표를 Bash로 집계하되 자동 취약점 판정을 만들지 않습니다.

## GTFOBins란 무엇인가

[GTFOBins 공식 프로젝트](https://gtfobins.org/)는 잘못 구성된 환경에서 정상 Unix 계열 실행 파일의 기능이 어떻게 보안 제약을 벗어나는 데 이용될 수 있는지 정리한 자료입니다. **등재된 프로그램 자체가 취약하다는 목록이나 CVE 목록은 아닙니다.** 2026-09-10 확인 기준 기존 gtfobins.github.io 주소는 gtfobins.org로 연결됩니다.

진단자는 레퍼런스를 통해 검토할 기능을 이해하고, 관리자는 실제 업무에 위임한 권한이 그 기능에 비해 넓지 않은지 확인합니다. 실행 파일 이름을 대조해 “발견=취약”으로 출력하는 방식은 이 두 작업을 대신하지 못합니다. 미등재 프로그램도 안전하다고 보증되지 않습니다.

## 기능과 실행 권한 문맥을 나누어 읽기

공식 사이트의 Functions는 무엇을 할 수 있는지를, Contexts는 어떤 권한 문맥에 관한 설명인지를 구분합니다. 아래는 수업에서 다룰 범주입니다. 모든 기능이 모든 문맥에서 성립하는 것은 아닙니다.

| 기능 범주 | 교육에서 확인할 질문 |
|---|---|
| File read / File write | 업무상 필요한 파일 범위와 실제 접근 가능한 범위가 일치하는가? |
| Shell / Command | 단일 작업 위임과 일반적인 명령 실행 권한을 구분했는가? |
| Upload / Download | 승인된 자료 이동·목적지·접근 정책이 있는가? |
| Library load | 로드하는 코드의 출처와 변경 권한을 관리하는가? |

| 권한 문맥 | 해석할 때 확인할 것 |
|---|---|
| Unprivileged | 현재 사용자의 권한. 기능 사용이 곧 권한 상승은 아님 |
| Sudo | 허용 주체·실행 사용자·작업 범위가 무엇인지 |
| SUID | 소유자·특수 비트와 실제 실행 시 적용 조건 |
| Capabilities | 부여된 개별 권한과 실제 필요한 기능의 대응 |

페이지의 예제가 있다는 사실과 자신의 시스템에서 조건이 성립한다는 사실을 혼동하지 않습니다. 수업에서는 악용 명령을 복사하거나 시스템에 특수 권한을 추가하지 않고, 설정 사본과 업무 요구사항을 검토합니다.

## 정상 사용 사례 — grep으로 수집 사본 읽기

grep은 이 교재에서 인증 로그를 검색하는 도구입니다. 같은 파일 읽기 기능도 권한과 대상이 달라지면 검토해야 할 경계가 달라집니다. 정상적인 사용부터 범위를 기록합니다.

```bash
grep -nF 'Accepted publickey' "$COURSE_DATA/auth.log"
```

제공 합성 파일의 출력은 다음과 같습니다.

```text
4:2026-09-10T09:02:00+09:00 lab-web-01 sshd[104]: Accepted publickey for analyst from 192.0.2.10 port 50103 ssh2
```

이 명령은 분석가가 이미 읽을 수 있는 사본에서 한 행을 찾습니다. 추가 권한을 얻거나 다른 사용자의 자료에 접근하지 않습니다. 행 번호 4는 이 사본의 위치이며 원래 전체 로그의 행 번호는 아닙니다. grep을 사용했다는 이유로 이 작업을 악성 행위로 분류할 수 없습니다.

> **Bash Point — 인용과 패턴의 역할**
> `"$COURSE_DATA/auth.log"`는 공백이 있는 경로를 한 인수로 유지합니다. 작은따옴표는 검색어를 셸 확장 없이 전달하고 `-F`는 정규식이 아닌 고정 문자열로 검색합니다. 이 안전한 인수 전달과 파일 접근 권한은 별개의 문제입니다.

## 설정 검토에서 적어야 할 네 가지

| 기록 | 포함할 내용 | 성급한 결론 |
|---|---|---|
| 프로그램 신원 | 전체 경로·패키지·버전·확인 시각 | 같은 이름이면 동일 구현 |
| 권한 출처 | 사용자·그룹·sudo 정책·특수 비트·Capability | root 소유 파일이면 root로 실행 |
| 작업 범위 | 허용 업무·읽기/쓰기 범위·변경 승인 | 업무 이름이 정해졌으니 기능도 제한됨 |
| 실행 근거 | 이벤트·기간·수집 범위·기록 설정 | 정책에 존재하므로 이미 악용됨 |

[sudoers 매뉴얼](https://man7.org/linux/man-pages/man5/sudoers.5.html)은 위임 정책·환경 관리·이벤트 및 I/O 기록을 구분합니다. 명령 허용 정책은 검토 대상이고, sudo 로그는 사용 흔적이며, I/O 기록의 존재는 별도 설정 사항입니다. 하나를 확인했다고 셋을 모두 확보했다고 쓰지 않습니다.

[execve](https://man7.org/linux/man-pages/man2/execve.2.html)에서 설명하는 SUID 적용 조건과 [Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)의 권한 모델도 함께 봅니다. SUID 비트, 일반 rwx 비트, ACL, 마운트 정책은 서로 다른 정보입니다. Capability는 root와 동의어가 아니며 필요한 권한 하나만 부여했는지도 별도로 검토합니다.

## Red Team ↔ Blue Team 사례 분석

### 사례: 업무용 도구 위임의 범위가 문서화되지 않았다

**Red Team 질문:** “파일 보고서 작성이라는 업무에 필요한 권한과 도구가 수행할 수 있는 기능 사이에 차이가 있는가?” 목적은 경계의 과도한 위임 가능성을 식별하는 것입니다. 프로그램 등재만으로 성립 조건이나 영향 범위를 확정하지 않습니다.

| 연결 단계 | 확인·기록할 내용 |
|---|---|
| Technique / Goal | 정상 도구 기능이 의도한 작업 범위를 넘을 가능성이라는 가설 |
| Command / Technique | 제공 권한·업무 요약표를 awk로 읽고, 실제 진단에서는 승인된 설정 사본 검토 |
| Security Meaning | 위임한 업무와 허용 기능이 다르면 최소 권한 검토 필요 |
| System Change / Artifact | 정책 변경 흔적과 도구 실행 흔적은 별개. 파일 읽기는 내용 변경을 남기지 않을 수도 있음 |
| Log / 수집 전제 | sudo 이벤트·승인 이력, 사전 규칙이 있는 Audit/EDR 실행·파일 접근 기록. auth.log가 모든 파일 읽기를 기록하지 않음 |
| Blue Team Investigation | 실행 주체·대상 사용자·인수·파일 범위·시각을 승인 업무와 비교 |
| Detection | 승인 범위와 실행 기록의 차이를 조사 후보로 분류. 도구 이름만으로 경보하지 않음 |
| Mitigation | 업무별 최소 위임, 경로·데이터 접근 통제, 변경 관리, 필요한 감사와 보존을 설계 |

**정상 반례:** 승인된 관리자가 허용된 보고서를 읽었습니다. 이 경우 높은 권한의 실행 기록이 있어도 업무 범위 일치 여부를 먼저 확인해야 합니다.

**자료 부족 사례:** 허용 정책만 있고 실행 기록이 수집되지 않았습니다. “위임 범위 확인 필요, 사용 여부 미확인”까지 보고할 수 있으며 “침해 없음”이나 “권한 상승 성공”은 모두 근거를 넘습니다.

관련 분류는 [Sudo and Sudo Caching — T1548.003](https://attack.mitre.org/techniques/T1548/003/)과 [Setuid and Setgid — T1548.001](https://attack.mitre.org/techniques/T1548/001/)입니다. 정상 정책 검토에 공격 발생 판정을 붙이는 ID가 아닙니다. 실제 행위 문맥과 근거가 맞을 때만 분석 보고서에 연결합니다.

### 탐지 설계 연습

탐지 요구사항을 “GTFOBins 이름 발견 시 경보”가 아니라 “업무 승인 범위와 권한 있는 실행의 불일치 검토”로 작성합니다. 입력에는 호스트·사건 시각·주체·대상 권한·실행 경로·정책 버전·승인 범위가 필요합니다. 사전에 기록되지 않은 필드는 unknown으로 남기고 경보의 확신도를 높이는 근거로 쓰지 않습니다.

평가 데이터는 최소 세 종류를 준비합니다: 승인 업무와 일치, 승인 범위와 차이, 로그 미수집. 각각 정상 검토·추가 검토·판단 보류로 구분되는지 확인합니다. 정책 변경 뒤에는 정상 업무도 재검증하며, 탐지를 통과했다고 최소 권한 설정이 보장되는 것은 아닙니다.

## 실습 — 목록 등재, 설정 상태, 실행 기록을 분리하기

07장 노트북 또는 ch07.sh의 마지막 두 STEP을 실행합니다. `tool-review.psv`는 강사가 작성한 **가상 검토 카드 네 개**입니다. 실제 GTFOBins 목록을 내려받거나 실제 시스템을 스캔한 결과가 아닙니다. 도구 역할 이름도 수업용입니다. `reference_listed`는 오해를 비교하기 위한 가정이고 `scope_fit`는 이미 제공된 검토 요약입니다. 스크립트가 sudo 정책을 파싱해 판정하는 것이 아닙니다.

| 카드 | 레퍼런스 등재 가정 | 설정 검토 요약 | 실행 자료 | 적절한 결론 |
|---|---|---|---|---|
| R01 text-filter | yes | aligned | present | 설정 검토 범위 내 일치, 실행의 정당성은 별도 |
| R02 report-helper | yes | unknown | not_collected | 설정·실행 자료 추가 요청 |
| R03 custom-helper | no | review | not_collected | 미등재여도 설정 검토 필요 |
| R04 network-helper | yes | aligned | present | 필요한 권한과 범위의 일치 사례 |

다음 명령은 이미 입력된 설정 검토 상태를 집계합니다.

```bash
awk -F '|' 'NR>1 {print $7}' "$COURSE_DATA/tool-review.psv" |
  LC_ALL=C sort | uniq -c
```

```text
      2 aligned
      1 review
      1 unknown
```

aligned 두 개는 시스템 전체 안전 판정이 아닙니다. review 한 개는 침해 성공 한 건이 아닙니다. unknown 한 개를 정상으로 합산하면 검토 미완료가 숨겨집니다. 실행 자료 present 두 개 역시 공격 두 건이 아니라 카드에 자료가 제공됐다는 뜻입니다.

**Bash Point — 검증 후 집계:** `-F '|'`는 필드 구분자이고 `NR>1`은 헤더를 제외합니다. 셸은 파일 경로를 전달하고 awk는 필드를 읽습니다. ch07.sh는 먼저 헤더·필드 수·ID 중복·허용값을 검사합니다. 잘못된 상태값을 결과에서 조용히 버리지 않고 중단합니다.

## 기능이 악용되면 어떤 영향이 생기는가

공격자는 정상 프로그램의 기능을 자신에게 허용되지 않은 권한이나 데이터 범위에 적용하려고 합니다. 아래는 **영향과 성립 조건을 설명하는 모델**이며 실행 레시피가 아닙니다. 정상 기능의 실행만으로 아래 공격이 성립하지는 않습니다.

| 기능 | 경계가 잘못 설정됐을 때 가능한 영향 | 추가로 확인해야 하는 조건 | 방어자가 연결할 자료 |
|---|---|---|---|
| 파일 읽기 | 비인가 정보 열람, 민감 자료 노출 | 실제 실행 권한이 대상 파일에 접근할 수 있는가, 그 접근이 업무상 승인됐는가 | 접근 제어·위임 정책·파일 접근 기록·승인 범위 |
| 파일 쓰기 | 무결성 훼손, 설정 변조 | 실제 쓰기 권한과 변경 대상의 보안 역할은 무엇인가 | 변경 전후 해시·메타데이터·승인·후속 동작 |
| 하위 명령 실행 | 단일 작업 위임이 범용 실행 권한으로 확대 | 하위 프로그램 실행 기능, 상속되는 권한, 실행 제약이 어떻게 결합하는가 | 부모/자식 프로세스·실행 권한·인수·승인 |
| 코드·라이브러리 로드 | 신뢰하지 않은 코드가 신뢰된 프로세스 안에서 실행 | 로드 경로와 코드의 변경 주체를 통제하는가 | 배포·파일 변경·프로세스 로드 기록 |
| 자료 송수신 | 비인가 외부 전송이나 승인되지 않은 파일 반입 | 데이터 접근과 통신 경로가 모두 허용되는가 | 목적지·프로세스·전송 기록·자료 반출 승인 |

**Sudo, SUID, Capabilities는 공격 이름이 아니라 권한이 부여되는 서로 다른 문맥**입니다. Sudo는 정책에 따른 실행 위임, SUID는 실행 파일 소유자와 관련된 유효 ID 전환, Capabilities는 세분화된 권한 모델입니다. 실제 적용은 실행 파일 종류, 프로세스 상태, 마운트 옵션 등 조건에 영향을 받습니다. root 소유라는 사실만으로 SUID가 설정됐거나 root로 실행된다고 판단하지 않습니다. 특수 비트나 Capability가 존재한다는 사실만으로 임의 명령 실행이 가능하다고 결론 내리지도 않습니다.

## 확장 실습 환경

**[07장 노트북 ZIP 받기](https://github.com/zxz3650/Bash-shell-programing/raw/refs/heads/master/downloads/chapter-07.zip)**에서 `security-07-permissions.ipynb`를 열고 Setup부터 실행합니다. 기존 계정·카드 실습 뒤에 아래 실험이 이어집니다. [설치와 실행 안내](../PRACTICE.md)를 먼저 확인합니다.

이 확장 실습의 기준은 **Ubuntu의 일반 사용자, Python 3 커널, Bash와 GNU 기본 도구**입니다. root로 동작하는 Colab 환경 대신 일반 사용자로 실행하는 Ubuntu VM/WSL을 사용합니다. 관리 권한을 부여하거나 시스템 정책을 수정할 필요가 없습니다. 명령이 준비되지 않았다면 강사가 환경을 준비한 후 재실행합니다. `getcap` 관찰만 선택 사항입니다.

교안만 보고 터미널에서 실습할 때는 아래 한 줄로 새 임시 폴더를 만든 후, 1~6단계를 **같은 터미널**에서 진행합니다. 노트북에서는 Python Setup이 동일한 환경 변수를 준비하므로 이 줄을 별도 Bash 셀에 복사하지 않습니다.

```bash
export GTFO_LAB="$(mktemp -d)"
```

실험은 자신이 생성한 일반 파일만 사용합니다. sudo 정책·SUID·Capability를 추가하지 않고 다른 계정의 데이터나 시스템 비밀 파일에 접근하지 않습니다. 권한 거부는 우회 대상이 아니라 확인할 결과입니다. 실제 공격 성공을 재현하는 실습과 구분합니다.

<!-- gtfo-notebook:start -->
## GTFOBins 확장 실험 — 권한과 데이터 경계 관찰

목표는 “프로그램이 파일을 읽을 수 있다”와 “그 프로그램이 권한을 상승시켰다”를 분리하는 것입니다. 자신이 소유한 더미 자료로 정상 기능·접근 거부·원본 보존을 관찰하고, 마지막에는 가상 실행 기록을 승인 범위와 비교합니다.

### 1. 환경과 파일의 출처 확인

```bash
set -euo pipefail
: "${GTFO_LAB:?실습 Setup부터 실행하세요}"
if [ "$(uname -s)" != Linux ] || [ "$(id -u)" -eq 0 ]; then
    printf 'Ubuntu 일반 사용자 환경에서 실행하세요.\n' >&2
    exit 2
fi
for tool in grep stat sha256sum base64 cmp find awk; do
    command -v "$tool" >/dev/null
done
umask 077
printf 'TRAINING_ONLY\n' > "$GTFO_LAB/report.txt"
printf 'uid=%s\n' "$(id -u)"
TZ=Asia/Seoul date '+observed_at=%Y-%m-%dT%H:%M:%S%:z'
stat -c 'mode=%a owner_uid=%u file=%n' "$GTFO_LAB/report.txt"
```

출력 예시는 `uid=1000`, `observed_at=...+09:00`, `mode=600 owner_uid=1000 file=/tmp/.../report.txt`입니다. UID·시각·임시 경로는 환경마다 다릅니다. `600`은 소유자 읽기/쓰기만 허용하는 모드입니다. `umask 077`은 이 셀에서 **새로 만드는 파일**의 기본 권한을 제한하며 기존 파일을 소급 변경하지 않습니다.

**Bash Point — 프로세스와 환경:** `command -v`는 필요한 명령의 존재를 확인합니다. `$()`는 표준 출력을 문자열로 받아 인수에 넣습니다. 각 `%%bash` 셀은 별도 프로세스이므로 `umask`와 셸 옵션은 필요한 셀마다 다시 설정합니다.

### 2. 동일한 grep, 다른 파일 접근 결과

먼저 자신이 소유한 자료를 정상적으로 읽습니다. 이어 이 더미 파일의 접근 비트를 잠시 제거하고 같은 작업이 거부되는지 확인합니다. 파일 내용은 바꾸지 않습니다.

```bash
set -euo pipefail
: "${GTFO_LAB:?}"
file="$GTFO_LAB/report.txt"
before=$(sha256sum "$file" | cut -d ' ' -f1)
grep -nF 'TRAINING_ONLY' "$file"
trap 'chmod 600 "$file"' EXIT
chmod 000 "$file"
if grep -nF 'TRAINING_ONLY' "$file" > "$GTFO_LAB/read.out" 2> "$GTFO_LAB/read.err"; then
    printf '예상과 달리 읽기 성공: 환경의 추가 권한을 확인하세요.\n' >&2
    exit 1
else
    status=$?
fi
printf 'denied_status=%s\n' "$status"
test "$status" -eq 2
test ! -s "$GTFO_LAB/read.out"
chmod 600 "$file"
trap - EXIT
after=$(sha256sum "$file" | cut -d ' ' -f1)
test "$before" = "$after"
printf 'restored_mode=%s content_unchanged=yes\n' "$(stat -c %a "$file")"
```

예상 출력:

```text
1:TRAINING_ONLY
denied_status=2
restored_mode=600 content_unchanged=yes
```

**해석:** grep은 같은 기능을 실행했지만 접근 권한이 없으면 읽지 못했습니다. 따라서 GTFOBins에 파일 읽기 기능이 설명되어 있다는 이유만으로 접근 제어가 자동 우회되는 것은 아닙니다. 이 파일은 학생 자신의 파일이므로 학생이 권한을 원복한 것 역시 권한 상승이 아닙니다. `chmod`는 메타데이터를 바꾸므로 이 실험은 실제 증거 원본에 수행하지 않습니다. 해시가 같아도 메타데이터까지 보존됐다는 뜻은 아닙니다.

**실패 사례:** `grep ... || true`로 모든 오류를 숨기면 검색어 부재(1)와 읽기 오류(2)를 구분하지 못합니다. 위 코드는 `else`에 들어가자마자 `$?`를 저장하고 기대한 실패인지 검사합니다. 특수 권한이 있는 환경에서 성공한다면 권한을 더 부여해 맞추지 말고 일반 사용자 환경으로 돌아갑니다. EXIT trap도 SIGKILL이나 호스트 종료까지 보장하지 않습니다.

### 3. 파일 쓰기 기능과 무결성 관찰

```bash
set -euo pipefail
: "${GTFO_LAB:?}"
umask 077
cp "$GTFO_LAB/report.txt" "$GTFO_LAB/work-copy.txt"
printf 'REVIEW_NOTE\n' >> "$GTFO_LAB/work-copy.txt"
if cmp -s "$GTFO_LAB/report.txt" "$GTFO_LAB/work-copy.txt"; then
    printf '사본 변경이 관찰되지 않았습니다.\n' >&2
    exit 1
else
    status=$?
fi
test "$status" -eq 1
printf 'original_lines=%s copy_lines=%s\n' \
    "$(wc -l < "$GTFO_LAB/report.txt" | tr -d ' ')" \
    "$(wc -l < "$GTFO_LAB/work-copy.txt" | tr -d ' ')"
sha256sum "$GTFO_LAB/report.txt" "$GTFO_LAB/work-copy.txt"
```

`original_lines=1 copy_lines=2`이며 두 해시는 다릅니다. 이것은 학생이 자신의 **작업 사본에 메모를 추가한 정상 변경**입니다. 파일 쓰기 능력과 설정 변조 공격을 같다고 보지 않습니다. 실제 조사에서는 변경 대상의 역할, 변경 주체의 권한, 승인 기록, 후속 실행을 연결해야 합니다. 해시 차이는 바이트 차이의 근거이지 공격자 신원의 근거가 아닙니다.

**Bash Point — 리다이렉션:** `>>`는 셸이 출력 파일을 열어 내용을 덧붙입니다. 단순 파일 출력을 “명령 자체가 모든 쓰기를 수행했다”고 해석하면 프로세스·파일 접근 기록을 잘못 연결할 수 있습니다.

### 4. 인코딩은 기밀성 보호가 아니다

```bash
set -euo pipefail
: "${GTFO_LAB:?}"
umask 077
base64 "$GTFO_LAB/report.txt" > "$GTFO_LAB/report.b64"
base64 --decode "$GTFO_LAB/report.b64" > "$GTFO_LAB/decoded.txt"
cmp -s "$GTFO_LAB/report.txt" "$GTFO_LAB/decoded.txt"
printf 'roundtrip_equal=yes\n'
stat -c 'encoded_mode=%a' "$GTFO_LAB/report.b64"
```

예상 결과는 `roundtrip_equal=yes`, `encoded_mode=600`입니다. 더미 자료를 변환했다가 복원했을 뿐이고 권한 변경이나 외부 전송은 없습니다. base64는 암호화가 아니므로 문자열이 바로 읽히지 않는다는 이유로 비밀 자료를 공개해도 되는 것은 아닙니다. 생성한 인코딩 파일과 복원 파일에도 원본과 같은 취급 기준이 필요합니다. 도구 실행이나 인코딩 문자열 하나만으로 정보 유출 발생을 확정하지 않습니다.

### 5. 제한된 범위의 권한 메타데이터 확인

```bash
set -euo pipefail
: "${GTFO_LAB:?}"
find "$GTFO_LAB" -maxdepth 1 -type f -perm -4000 -print > "$GTFO_LAB/suid-list.txt"
test ! -s "$GTFO_LAB/suid-list.txt"
printf 'lab_suid_files=0\n'
stat -c 'mode=%a owner_uid=%u' "$GTFO_LAB/report.txt"
if command -v getcap >/dev/null; then
    getcap "$GTFO_LAB/report.txt"
    printf 'getcap_checked=yes\n'
else
    printf 'getcap_checked=no (선택 도구 미설치)\n'
fi
```

`lab_suid_files=0`은 **이 임시 폴더의 일반 파일**에서 SUID 비트를 발견하지 않았다는 뜻입니다. 호스트 전체 안전 판정이 아닙니다. getcap의 빈 출력은 성공적으로 확인한 이 파일에 표시할 파일 Capability가 없다는 뜻이며, 호출 실패나 권한 부족과 구분합니다. 이 실습에서 특수 권한은 부여하지 않습니다. 07-3의 SUID/Capability 설명과 실제 파일 메타데이터의 역할을 연결하는 관찰입니다.

### 6. 실행 기록과 승인 범위를 비교하기

다음 자료는 **교육용으로 작성한 정규화 이벤트 세 개**입니다. 방금 실행한 명령의 OS 감사 로그가 아니며 실제 sudo/audit 로그 형식도 아닙니다. 가상의 승인 업무는 “analyst가 자신의 권한으로 report 범주의 자료를 읽는 것”입니다.

```bash
set -euo pipefail
: "${GTFO_LAB:?}"
umask 077
printf '%s\n' \
  'id|time|actor|effective_role|action|resource' \
  'E01|2026-09-12T09:00:00+09:00|analyst|analyst|read|report' \
  'E02|2026-09-12T09:01:00+09:00|analyst|administrator|read|outside_scope' \
  'E03|2026-09-12T09:02:00+09:00|analyst|unknown|read|report' \
  > "$GTFO_LAB/events.psv"
awk -F '|' 'NR>1 {
  if ($4=="unknown") verdict="unknown";
  else if ($3=="analyst" && $4=="analyst" && $5=="read" && $6=="report") verdict="aligned";
  else verdict="review";
  print $1, verdict
}' "$GTFO_LAB/events.psv" | tee "$GTFO_LAB/verdicts.txt"
test "$(grep -c ' aligned$' "$GTFO_LAB/verdicts.txt")" -eq 1
test "$(grep -c ' review$' "$GTFO_LAB/verdicts.txt")" -eq 1
test "$(grep -c ' unknown$' "$GTFO_LAB/verdicts.txt")" -eq 1
```

```text
E01 aligned
E02 review
E03 unknown
```

E02는 가상의 실행 권한·자료 범위가 승인 예시와 달라 **추가 검토할 항목**입니다. 실제 공격 재현 결과나 확정 침해가 아닙니다. 임시 관리자 작업 승인 여부라는 정상 반례를 확인해야 합니다. E03은 권한 자료가 없으므로 E01과 합쳐 정상으로 집계하지 않습니다. 이 짧은 awk는 형식이 고정된 세 행의 설명용 분류기이며, 신뢰하지 않은 실제 로그용 검증기나 sudoers 파서가 아닙니다.

**Artifact와 탐지의 한계:** 2단계의 `read.err`, 6단계의 `verdicts.txt`는 실습 프로그램이 만든 파일입니다. auth.log/secure가 모든 파일 읽기를 기록하는 것은 아닙니다. 실제 추적에는 사전에 설정된 감사 규칙·EDR 수집, 명령 실행 문맥, 파일 대상, 승인 자료가 필요하며 수집하지 않은 필드는 추측하지 않습니다.

### 확장 실습 완료 기준

- `denied_status=2`, 권한 원복 600, 원본 내용 보존을 설명한다.
- 파일 소유자·유효 권한·rwx·SUID·Capability를 같은 개념으로 쓰지 않는다.
- 사본의 변경과 원본의 변경, 파일 해시와 메타데이터 보존을 구분한다.
- base64 왕복 일치가 암호화나 비인가 접근 성공을 뜻하지 않는 이유를 설명한다.
- E01/E02/E03을 일치/추가 검토/미확인으로 나누고 정상 반례를 제시한다.
- 각 기능별로 **공격자가 얻으려는 효과 / 필요한 권한 조건 / 실제 관찰 / 미수집 자료 / 완화안**을 한 행씩 작성한다.

이 실험의 PASS는 정상 기능과 접근 제어를 이해했다는 뜻입니다. sudo·SUID 악용이나 실제 권한 상승을 실행·검증했다는 뜻이 아닙니다. 다음 검토에서는 업무별 권한을 최소화하고 자료 범위·정책 변경·감사 설정을 함께 확인합니다.
<!-- gtfo-notebook:end -->

## 실패 사례와 수정

잘못된 판단: “R01은 listed=yes이므로 vulnerable, R03은 no이므로 safe.”

왜 실패할까요? 입력의 reference_listed는 공개 레퍼런스 관련성이고 시스템의 권한 조건·실행·업무 승인을 표현하지 않습니다. 한 필드를 다른 의미로 바꾸는 분석 오류입니다. Bash 구문이 올바르고 종료 상태가 0이어도 이 결론은 틀립니다.

수정: R01의 설정 검토와 실제 사용 승인을 구분하고, R03의 검토 사유를 계속 조사합니다. 자동화는 네 카드의 원문 식별자를 보존한 상태로 상태별 목록을 만들고 미확인 항목을 명시합니다. 일반 사용자 입력을 정책 문장으로 실행하거나 레퍼런스 명령을 자동 실행하는 기능은 필요하지 않습니다.

## 분석 질문과 완료 기준

1. GTFOBins 등재와 CVE 발견은 왜 다른가?
2. 기능이 같아도 Unprivileged와 Sudo 문맥에서 검토할 경계가 어떻게 다른가?
3. R02에 먼저 요청할 설정 자료와 실행 자료를 각각 하나씩 적었는가?
4. R03을 미등재 이유로 제외하면 무엇을 놓치는가?
5. 모든 일반 명령 실행이 auth.log에 기록된다고 가정하면 왜 안 되는가?
6. 설정 일치·실행 관찰·업무 승인·침해 판정을 별도 문장으로 작성했는가?

제출물은 네 카드별 **사실 / Red Team 위험 질문 / 필요한 조건 / Blue Team 자료 / 정상 반례 / 탐지 요건 / 완화 제안**입니다. 정답은 공격 성공 재현이 아니라 근거에 맞는 위험 설명과 검증 가능한 개선안입니다. ch07.sh의 값 검증 및 원본 보존 검사를 통과하고, R02를 판단 보류·R03을 검토 필요로 설명하면 이 절의 기본 실습을 완료합니다.

## 정리와 다음 학습

GTFOBins는 위험을 이해하는 참고 자료이고 실제 설정 검토를 대체하지 않습니다. 08장에서는 같은 질문을 자동 시작 구성의 변경 권한에, 10장에서는 권한 있는 실행 기록에, 12장에서는 근거와 누락이 분리된 보고서에 적용합니다.

## 참고 자료

- [GTFOBins 공식 프로젝트](https://gtfobins.org/) — 정의와 기능·문맥 분류
- [sudoers](https://man7.org/linux/man-pages/man5/sudoers.5.html) — 위임 정책·환경·로깅
- [execve](https://man7.org/linux/man-pages/man2/execve.2.html) — 실행 시 권한 적용 조건
- [Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) — Linux 세분화 권한
- [GNU grep 종료 상태](https://www.gnu.org/software/grep/manual/html_node/Exit-Status.html) — 일치·불일치·오류 구분
- [GNU Coreutils](https://www.gnu.org/software/coreutils/manual/coreutils.html) — chmod·stat·base64·sha256sum
- [MITRE ATT&CK T1548.003](https://attack.mitre.org/techniques/T1548/003/), [T1548.001](https://attack.mitre.org/techniques/T1548/001/) — 관련 행위 분류
