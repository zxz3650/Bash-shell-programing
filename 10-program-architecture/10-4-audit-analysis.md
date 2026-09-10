# 10-4. auditd의 여러 레코드를 하나의 행위로 묶기

COURSE_DATA를 사용하는 예제는 [공통 실습 준비](../examples/security-labs/README.md)를 먼저 수행합니다. ausearch·aureport 예제는 저장소 루트와 별도 Linux 분석 환경을 기준으로 합니다.

## 보안 질문과 목표

“어떤 로그인 신원에서 어떤 유효 권한으로 무엇을 실행했는가?” audit.log의 한 줄을 행위 하나로 세지 않고 같은 이벤트 ID의 레코드를 연결합니다. uid/euid/auid와 인수·경로·작업 디렉터리의 차이를 이해합니다.

## 수집 전제

일반적인 경로는 `/var/log/audit/audit.log`입니다. auditd 설치만으로 모든 필요한 행위가 기록되는 것은 아닙니다. 규칙·필터·커널 지원·손실·보존·수집 범위를 확인합니다. 이 실습은 규칙을 설치하거나 전체 exec 감시를 켜지 않습니다. 제공 파일은 무해한 id 실행을 설명하도록 만든 합성 이벤트입니다.

## 주요 레코드와 필드

| 레코드/필드 | 의미 | 조사 질문 |
|---|---|---|
| SYSCALL | 호출·결과·주체 정보 | 성공 여부·arch·syscall 해석이 맞는가? |
| EXECVE | 실행 인수 | 어떤 인수가 전달됐는가? |
| CWD | 작업 디렉터리 | 상대 경로 문맥은 무엇인가? |
| PATH | 관련 경로·inode·소유권 | 같은 이벤트에 여러 경로가 있는가? |
| PROCTITLE | 인수 표현, 인코딩될 수 있음 | EXECVE와 어떻게 대응하는가? |
| pid/ppid | 프로세스·부모 | 같은 부팅·수집 시각에 연결되는가? |
| uid/euid | 실제/유효 사용자 ID | 실행 시 권한이 무엇인가? |
| auid | 로그인 신원 추적용 ID | 원래 세션 주체를 추적할 수 있는가? |
| exe | 실행 파일 경로 | 경로와 파일 무결성을 확인했는가? |

auid는 설정되지 않은 값으로 나올 수 있습니다. euid=0은 root 권한 문맥을 보여주지만 불법 권한 상승을 자동 입증하지 않습니다. 정상 sudo 실행도 같은 형태일 수 있습니다. syscall 번호는 아키텍처별로 해석해야 합니다.

## 제공 이벤트 읽기

```text
msg=audit(1788998580.000:900)
auid=1000 uid=0 euid=0 pid=450 ppid=410
exe="/usr/bin/id"
```

epoch 시각은 KST 2026-09-10 09:03:00입니다. 900은 이벤트 일련번호이며 시간·호스트 문맥을 함께 보존합니다. 같은 일련번호가 다른 호스트·기간에 있을 수 있습니다. 이 자료의 6행은 SYSCALL·EXECVE·CWD·PATH·PROCTITLE·EOE로 구성한 **한 이벤트**입니다.

## ausearch·aureport로 읽기

Linux Audit 사용자 도구가 설치된 분석 VM에서 다음을 실행합니다. 입력은 제공 사본입니다.

```bash
TZ=Asia/Seoul ausearch -if examples/security-labs/data/audit.log -a 900
TZ=Asia/Seoul ausearch -if examples/security-labs/data/audit.log -a 900 -i
TZ=Asia/Seoul aureport -if examples/security-labs/data/audit.log -x --summary
```

첫 조회는 원래 값을, -i는 사람이 읽기 쉬운 해석을 제공합니다. 이름 해석은 현재 분석 환경의 계정 데이터에 영향을 받을 수 있으므로 원본 숫자 ID를 함께 보존합니다. 요약은 전체 레코드 검토를 대신하지 않습니다. 버전에 따라 표시 순서·날짜 형식은 달라질 수 있습니다.

제공 합성 파일을 Ubuntu의 Audit 도구로 읽으면 요약의 핵심 결과는 다음과 같습니다.

```text
total  file
1      /usr/bin/id
```

-i의 auid 이름은 분석 호스트의 UID 1000 계정 이름이 될 수 있습니다. 이를 사건 호스트의 실제 사용자 이름이라고 바꾸어 기록하지 않습니다. 일반 사용자 실행에서 설정 파일 접근 경고가 있으면 stderr도 남기고, 명시한 -if 사본의 이벤트 ID·내용·종료 상태를 확인합니다. 경고를 없애려고 원본 시스템 권한을 변경하지 않습니다.

## Bash Point — 레코드 수와 이벤트 수

```bash
sed -n 's/.*msg=audit(\([^)]*\)).*/\1/p' "$COURSE_DATA/audit.log" |
  LC_ALL=C sort -u
```

제공 형식의 괄호 안 시간·일련번호를 추출하여 같은 값을 묶습니다. 운영용 Audit 파서가 아니며, 여러 호스트 자료를 섞었거나 잘린 행이 있으면 별도 검증이 필요합니다. 범용 정규식만으로 모든 Audit 인코딩을 복원하려 하지 않습니다.

## 흔적과 판단

권한 있는 실행이라는 관찰 → auid·euid·exe·인수·부모 → sudo/세션 기록·승인 작업과 비교 → 정상 관리 또는 추가 조사로 분류합니다. 이 합성 자료에는 승인 정보가 없으므로 “권한 상승 공격 성공”이라고 결론 내릴 수 없습니다. 원본 로그에 없던 승인을 추측해 채우지도 않습니다.

## 실패 사례와 실습

ch10.sh는 이벤트 ID 1개, 레코드 6개, auid=1000/euid=0을 검증합니다. 공격 건수를 6건으로 보고하면 실패입니다. 다음 반례를 답합니다: EOE가 빠졌다면? PATH가 여러 개라면? -i의 사용자 이름이 분석 호스트와 다르다면? Audit 규칙이 사건 후 켜졌다면?

## 완료 기준

필드 의미·행과 이벤트의 차이·설정 의존성·정상 sudo 반례를 설명합니다. 원래 기록과 해석본을 분리하고, 원래 Linux 도구 실행 여부를 명시합니다. 기본 노트북은 형식·연결 실습이며 실제 Audit 도구 검증은 별도 환경 검증으로 구분합니다.

## 참고 자료

- [ausearch](https://man7.org/linux/man-pages/man8/ausearch.8.html)
- [aureport](https://man7.org/linux/man-pages/man8/aureport.8.html)
- [Linux Audit project](https://github.com/linux-audit/audit-userspace)
