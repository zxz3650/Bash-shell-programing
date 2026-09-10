# 05-4. SSH 인증 실패 로그를 단계별로 분석하기

터미널 예제는 [공통 실습 준비](../examples/security-labs/README.md)를 먼저 수행합니다. 노트북은 Setup부터 실행합니다.

## 보안 질문과 목표

“어느 주소에서 어떤 계정으로 실패가 반복됐고, 이후 성공과 관련이 있는가?” grep·awk·sort·uniq를 외우기 위해 로그를 붙이는 것이 아니라, 이 질문에 답하기 위해 파이프라인을 만듭니다. 선수지식은 03장의 인용·상태, 04장의 원본·결과 분리입니다.

## 원본 위치와 형식

Ubuntu/Debian에서는 `/var/log/auth.log`, RHEL/Rocky/AlmaLinux에서는 `/var/log/secure`를 볼 수 있습니다. rsyslog·보존 설정에 따라 파일이 없고 Journal만 있을 수도 있습니다. 이름만으로 존재와 범위를 가정하지 않습니다. 실습은 제공 auth.log 사본만 읽습니다.

입력 예:

```text
2026-09-10T09:01:00+09:00 lab-web-01 sshd[101]: Failed password for invalid user guest from 192.0.2.10 port 50100 ssh2
```

시각·호스트·프로그램/PID·메시지를 나눕니다. invalid user는 이 메시지에서 계정이 유효하지 않았다는 단서이며, analyst 실패 메시지는 같은 구조라도 필드 수가 다릅니다. 모든 주소를 `$11`처럼 고정 위치로 추출하면 형식 변형에서 틀릴 수 있습니다.

## 1단계 — 필요한 행

```bash
grep -F 'Failed password' "$COURSE_DATA/auth.log"
```

제공 원본 5행 중 실패 3행이 남습니다. grep은 출처·시간·계정 정보를 유지합니다. 먼저 head·tail로 시작과 끝을 보고 wc -l로 범위를 확인합니다. 마지막 개행이 없는 경우 wc -l은 논리적 레코드 수와 다를 수 있습니다.

## 2단계 — 주소

```bash
grep -F 'Failed password' "$COURSE_DATA/auth.log" |
  awk '{for (i=1; i<NF; i++) if ($i=="from") {print $(i+1); break}}'
```

```text
192.0.2.10
192.0.2.10
198.51.100.8
```

from 표식을 기준으로 찾는 이 코드는 **제공 OpenSSH 형태의 행**에 맞춘 학습용입니다. 다른 프로그램의 메시지, 인용·구조화 필드, malformed 행에는 별도 파서·거부 정책이 필요합니다. 주소만 남기면 계정·시각이 사라지므로 원문 행을 반드시 함께 보관합니다.

## 3단계 — 정렬과 집계

```bash
grep -F 'Failed password' "$COURSE_DATA/auth.log" |
  awk '{for (i=1; i<NF; i++) if ($i=="from") {print $(i+1); break}}' |
  LC_ALL=C sort | uniq -c | LC_ALL=C sort -nr
```

```text
      2 192.0.2.10
      1 198.51.100.8
```

sort는 같은 값을 인접하게 만들고 uniq -c는 **연속된 동일 행**의 개수를 셉니다. sort -nr은 숫자 빈도 내림차순입니다. 단순 uniq만 쓰면 떨어져 있는 같은 주소를 놓칩니다. 상위 N개만 보면 저빈도 분산 시도를 놓칠 수 있으므로 전체 결과도 보존합니다.

### Bash Point — Pipe와 종료 상태

파이프는 stdout을 다음 stdin으로 전달하고 stderr는 기본적으로 별도입니다. 마지막 sort만 성공해도 기본 파이프 상태가 0일 수 있습니다. pipefail과 단계별 결과 저장으로 실패를 확인합니다. grep의 “일치 없음” 상태 1은 정상적인 분석 결과일 수도 있으므로 오류 2와 구분합니다. `2>/dev/null`로 접근 실패를 숨기지 않습니다.

## 성공·계정·시간대를 연결하기

제공 자료에는 09:02에 `.10`에서 analyst의 publickey 성공 1건, 09:03에 sudo 기록 1건이 있습니다. **비밀번호 실패 뒤 공개키 성공**은 동일 비밀번호 공격의 성공을 뜻하지 않습니다. NAT·공유 단말·정상 관리·인증 방식 차이·PID/세션 관계를 확인합니다.

계정별·시간대별 집계는 원문에서 다시 수행합니다. 필드 위치를 바꾸기 전에 메시지 변형별 정상·실패 테스트를 준비합니다. cut은 단순 구분 형식, sed는 명시적 형식 변환, tr은 제어문자·구분자 처리에 사용하며 원본을 덮어쓰지 않습니다.

## Attack → Artifact → Detection

반복 인증 시도라는 행위 가설 → sshd/PAM 메시지 → auth.log/secure·Journal·로그인 기록 → 주소·계정·시간창·인증 방식 비교 → 계정 소유자와 변경 이력 확인 → 필요하면 접근 제한·MFA·키 관리·로그 보존 개선으로 이어집니다. 이 절은 실제 인증 공격을 발생시키지 않습니다.

## 실패 사례와 반례

| 오해 | 반례 | 보완 |
|---|---|---|
| 실패가 많으면 침해 성공 | 설정 오류·사용자 실수 | 성공·세션·후속 행위 확인 |
| 같은 IP면 같은 사람 | NAT·프록시·공유 단말 | 계정·기기·세션 문맥 |
| 기록 없으면 시도 없음 | 회전·수집 누락·다른 인증 방식 | 수집 범위 명시 |
| 형식을 모르면 NF-3 사용 | 메시지 꼬리 필드 변화 | 샘플 검증·거부 행 집계 |

## 실습·질문·완료 기준

ch05.sh는 중간 결과를 failed.txt → addresses.txt → counts.txt로 남깁니다. 기대값은 실패 3행, 주소별 2/1건, 공개키 성공 1건, sudo 1건입니다. 각 단계에서 잃는 정보, 정상 관리 가설, 추가 수집할 자료를 설명합니다. 성공 1건을 공격 성공 1건으로 표시하지 않으면 완료입니다. 09장에서 로그인 아티팩트와 교차 검증합니다.

## 참고 자료

- [GNU grep](https://www.gnu.org/software/grep/manual/grep.html)
- [GNU awk](https://www.gnu.org/software/gawk/manual/gawk.html)
- [OpenSSH sshd](https://man.openbsd.org/sshd)
