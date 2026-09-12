# 12. Bash 활용 종합 프로젝트

**[12장 학습용 노트북 ZIP 받기](https://github.com/zxz3650/Bash-shell-programing/raw/refs/heads/master/downloads/chapter-12.zip)** · [처음 실행하는 방법](PRACTICE.md) · [포함 노트북과 자료 버전](downloads/README.md)

압축을 푼 뒤 `START-HERE.md`의 순서대로 기본 실습부터 실행하고 보안 적용 실습으로 이어갑니다.

## 기본 프로젝트와 보안 종합 실습 연결

12-1 로그 보고서와 12-2 로컬 스냅샷 프로젝트에서 문법·안전 설계·테스트를 통합합니다. 이어서 [12-3. Linux DFIR Capstone](12-capstone/12-3-dfir-capstone.md)에서 장별 보안 자료를 연결하고, 기능별 오프라인 수집 함수·manifest·해시·KST·부분 실패·사실/가설 보고서를 제출합니다. 기본 프로젝트와 보안 종합 실습의 요구사항을 각각 확인합니다.

## 개요

앞 장의 문법, 파일, 텍스트, 시스템 조사, 안전 설계와 테스트를 결합해 읽기 전용 triage 도구를 완성합니다.

## 프로젝트 학습 순서

1. [12-1. 프로젝트 A: 검증 가능한 로그 보고서](12-capstone/12-1-log-report-project.md) — 고정 입력·정답·기준 구현·테스트를 제공합니다.
2. [12-2. 프로젝트 B: 로컬 스냅샷과 최종 평가](12-capstone/12-2-snapshot-assessment.md) — 노트북 08의 기본 수집기를 확장하고 평가 루브릭으로 검증합니다.

아래 짧은 실습은 개념 복습이며 GNU/Linux 명령을 포함합니다. 전체 제출은 상세 프로젝트의 입력 형식·오류 처리 방침·완료 기준을 따릅니다. 정상 결과뿐 아니라 잘못된 입력, 기존 결과 충돌, dry-run, 부분 실패를 설명해야 합니다.

{% hint style="info" %}
## 🧭 프로젝트 목표

- 인증 로그, 파일 무결성과 프로세스 상태를 수집한다.
- 실행 범위와 권한을 제한하고 결과 해시를 생성한다.
- ShellCheck와 Bats로 결과를 재현 가능하게 검증한다.
{% endhint %}

모든 실습은 임시 디렉터리, 제공된 샘플 로그 또는 승인된 VM에서만 수행합니다.

## 실습 1: 인증 로그 요약

샘플 파일을 만듭니다.

```bash
cat >auth-sample.log <<'LOG'
Aug 24 10:01:00 lab sshd[101]: Failed password for invalid user guest from 192.0.2.10 port 50100 ssh2
Aug 24 10:01:10 lab sshd[102]: Failed password for analyst from 192.0.2.10 port 50101 ssh2
Aug 24 10:02:00 lab sshd[103]: Accepted publickey for analyst from 198.51.100.5 port 50102 ssh2
LOG
```

목표:

1. 실패한 로그인 행만 출력합니다.
2. 출발지 IP를 추출해 빈도순으로 정렬합니다.
3. 결과가 없을 때와 입력 파일이 없을 때를 구분합니다.

예시 파이프라인:

```bash
grep -F 'Failed password' auth-sample.log |
    awk '{for (i=1; i<=NF; i++) if ($i=="from") print $(i+1)}' |
    sort |
    uniq -c |
    sort -nr
```

## 실습 2: 파일 무결성 기준선

```bash
find ./sample-tree -type f -print0 |
    sort -z |
    xargs -0 sha256sum >baseline.sha256
```

파일 하나를 변경한 뒤 다음 명령으로 차이를 확인합니다.

```bash
sha256sum --check baseline.sha256
```

블루팀 관점에서는 변경 탐지와 증거 보존을, 레드팀 관점에서는 어떤 행위가 파일 메타데이터와 해시 흔적을 남기는지 관찰합니다.

## 실습 3: 프로세스 스냅샷

다음 필드를 TSV 보고서로 저장합니다.

```bash
umask 077
ps -eo pid=,ppid=,user=,lstart=,comm=,args= --sort=ppid >process-snapshot.txt
```

확인 항목:

- 부모가 예상과 다른 프로세스
- 임시 디렉터리에서 실행된 프로그램
- 장시간 지속되는 대화형 셸
- 명령행에 노출된 자격증명

## 실습 4: 공격자 입력을 이용한 방어 테스트

파일 검색 스크립트에 다음 입력을 전달하되 입력을 실행하지 않습니다.

```text
normal.log
file with spaces.log
-n
$(touch should-not-exist)
; echo injected
```

검증 기준:

- 입력 문자열 때문에 추가 명령이 실행되지 않는다.
- 하이픈으로 시작하는 값이 옵션으로 해석되지 않는다.
- 공백을 포함한 파일명을 한 개의 인수로 처리한다.
- 실패 시 0이 아닌 종료 상태와 이해 가능한 오류를 반환한다.

## 미니 프로젝트

`triage.sh`를 작성해 다음 정보를 읽기 전용으로 수집합니다.

- 호스트명과 수집 시각
- OS와 커널 버전
- 로그인 사용자
- 프로세스 목록
- 열린 로컬 수신 포트
- 최근 인증 오류의 요약

필수 요구사항:

1. `--output DIR`과 `--dry-run`을 지원합니다.
2. 결과 디렉터리 권한을 제한합니다.
3. 필요한 명령이 없으면 해당 항목만 건너뛰고 경고합니다.
4. 수집한 파일의 SHA-256 목록을 생성합니다.
5. ShellCheck와 Bats 테스트를 통과합니다.

## ✅ 완료 기준

- `README.md`에 목적, 사용법, 제한사항과 예시 결과가 있다.
- `--output`, `--dry-run`, `--help`를 지원한다.
- 임시 자원과 시그널을 안전하게 처리한다.
- 정상 입력과 실패 입력의 Bats 테스트가 있다.
