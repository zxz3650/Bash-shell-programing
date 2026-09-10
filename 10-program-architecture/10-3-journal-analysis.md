# 10-3. systemd Journal을 시간·부팅·서비스로 분석하기

## 질문과 목표

“서비스가 언제 시작됐으며 인증·프로세스 기록과 같은 부팅에 속하는가?” Journal의 구조화 필드를 이해하고 기간·unit·boot를 명시합니다. 06장의 서비스, 09장의 시간창 교차 검증을 함수 단위의 분석으로 발전시킵니다.

## 왜 텍스트 파일 검색과 다른가

Journal은 MESSAGE 외에 시간·부팅 ID·프로그램·PID·unit 등 메타데이터를 저장할 수 있습니다. 모든 필드가 모든 레코드에 존재하지는 않습니다. 표시용 문자열과 원래 구조화 필드를 구분하고, 파일명 하나의 grep 결과로 전체 Journal을 대표하지 않습니다.

## 승인된 Ubuntu VM 조회

```bash
TZ=Asia/Seoul journalctl -b --no-pager -n 30
TZ=Asia/Seoul journalctl -u ssh.service --since '2026-09-10 09:00:00' --until '2026-09-10 10:00:00' --no-pager -o short-iso
```

첫 명령은 현재 부팅의 마지막 30개 레코드입니다. 전체 보존 범위가 아닙니다. 둘째는 KST 기준 시간창과 unit을 지정합니다. ssh.service 이름은 환경마다 다릅니다. 실행 날짜가 달라 해당 기간의 로그가 없을 수 있으며 실패를 재현하려고 운영 서버에 인증을 시도하지 않습니다.

원본 Journal 사본은 디렉터리로 지정합니다.

```bash
TZ=Asia/Seoul journalctl --directory=evidence/journal --list-boots --no-pager
TZ=Asia/Seoul journalctl --directory=evidence/journal --since '2026-09-10 09:00:00' --until '2026-09-10 10:00:00' --no-pager -o json
```

evidence/journal은 실제 바이너리 Journal 사본이어야 합니다. 현재 분석 호스트의 -b를 무심코 적용해 다른 호스트 자료를 제외하지 않습니다. 부팅 목록에서 조사할 ID를 확인합니다. JSON 출력은 jq/Python처럼 구조를 이해하는 파서로 읽습니다.

## 출력 해석

제공 journal-review.psv는 원래 Journal이 아니라 다음 정보를 사람이 이해하기 좋게 구성한 합성 요약입니다.

```text
09:05:00+09:00 | BOOT-A | report-helper.service | Started report helper
09:06:00+09:00 | BOOT-A | report-helper.service | Report completed
```

Started 메시지는 서비스 시작 흐름의 근거입니다. 승인·정상성·전체 작업 성공을 자동 보증하지 않습니다. MESSAGE 안의 PID 문자열과 Journal 메타데이터의 _PID는 다른 출처일 수 있습니다. 앱이 쓴 “completed”만 보고 검증된 데이터 산출이라고 주장하지 않습니다.

## 기록이 없는 경우

권한·보존·휘발성 저장·시간창·unit 이름·부팅 ID·수집 범위를 순서대로 확인합니다. journald가 있어도 모든 프로세스의 실행 인수가 자동으로 기록되는 것은 아닙니다. 서비스 stdout/stderr와 Audit 실행 감시는 목적·수집 조건이 다릅니다.

### Bash Point — 함수의 입력을 명확히 하기

조회 함수를 만든다면 journal 경로·unit·시작·종료를 인수로 받고 원본·stderr·상태를 별도 보존합니다. 기본값 “오늘”을 숨기지 않습니다. 문자열을 연결해 eval로 실행하지 말고 인용된 개별 인수로 전달합니다. 10-1의 함수 입출력 원칙을 적용합니다.

## 공격 관점·방어 관점

서비스를 통한 반복 실행이라는 가설 → unit 변경·실행 흔적 → 같은 부팅의 Journal·프로세스·파일 메타데이터 비교 → 승인 변경과 계정 활동 확인 → 최소 권한·설정 무결성·원격 로그 보존 검토로 연결합니다. 같은 service 이름의 정상 배포도 대안으로 남깁니다.

## 실습·완료 기준

ch10.sh의 첫 STEP은 report-helper 관련 2행을 고릅니다. BOOT-A는 교육용 표식이며 실제 32자리 boot ID가 아닙니다. 시간창·부팅·unit·출처를 기록하고, 원래 Journal 파일을 검사하지 않은 범위를 명시합니다. 다음 [Audit 분석](10-4-audit-analysis.md)에서 실행 행위의 이벤트 단위를 확인합니다.

## 참고 자료

- [journalctl](https://man7.org/linux/man-pages/man1/journalctl.1.html)
- [Journal fields](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html)
