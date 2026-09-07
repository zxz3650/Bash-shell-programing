# 12-1. 프로젝트 A: 검증 가능한 로그 보고서 도구

지금까지의 문법·파일·텍스트·오류 처리를 하나의 명령줄 도구로 연결한다. 제공된 합성 로그를 검증하고 수준별 개수를 TSV 보고서로 생성한다. 입력 형식을 검사하고 오류를 처리하여, 검증을 통과한 결과만 보고서로 저장하는 과정을 연습한다.

{% hint style="info" %}
### 🧭 프로젝트 목표

- --input·--output·--dry-run·--help를 지원한다.
- 잘못된 입력에서 결과를 최종 파일로 저장하지 않는다.
- 기존 파일과 원본을 보존한다.
- 동작 테스트로 정상·실패 경로를 입증한다.
{% endhint %}

## 0. 입력 형식

각 행은 LEVEL SERVICE 두 필드다. LEVEL은 INFO, WARN, ERROR이며 SERVICE는 영문자·숫자·밑줄·점·하이픈이다. 빈 행은 오류, 빈 파일은 유효한 입력이다. 마지막 개행이 없어도 레코드를 처리한다.

```text
INFO api
ERROR db
WARN api
ERROR db
ERROR api
```

집계 정답은 INFO 1, WARN 1, ERROR 3이다. 실제 예제 파일은 [fixtures/events.log](https://github.com/zxz3650/Bash-shell-programing/blob/master/examples/log-report/fixtures/events.log)에 있다.

## 1. 설계부터 제출하기

| 구성 | 요구사항 |
|---|---|
| CLI | 필수 옵션 누락·중복·미지원 옵션 거부 |
| 입력 | 읽을 수 있는 일반 파일 |
| 파서 | 잘못된 행 번호 진단 |
| 집계 | INFO/WARN/ERROR 순서, 없는 수준은 0 |
| 저장 | 기존 결과 거부, 완성된 결과만 저장 |
| 상태 | 성공 0, 실행 오류 1, 사용 오류 2 |

stdout은 일반 실행에서 비워 두고 진단을 stderr에 기록한다. dry-run은 입력도 검증한 뒤 stdout에 계획만 출력한다.

## 2. 단계별 구현 과제

1. 인수 파싱과 도움말만 구현하고 잘못된 요청을 검증한다.
2. stdin에서 읽어 TSV를 출력하는 summarize_events 함수를 만든다.
3. 고정 샘플과 빈 입력을 시험한다.
4. 결과를 같은 디렉터리의 임시 파일에 생성한다.
5. 사전 검사 이후 같은 이름의 파일이 생겨도 기존 결과를 덮어쓰지 않는 저장 방식을 선택한다.
6. trap으로 임시 파일을 정리한다.
7. dry-run의 변경 없음을 검증한다.

## 3. 기준 구현 실행

저장소 루트에서 실행한다.

```bash
lab_dir=$(mktemp -d)
bash examples/log-report/bin/log-report.sh \
    --input examples/log-report/fixtures/events.log \
    --output "$lab_dir/report.tsv" --dry-run
test ! -e "$lab_dir/report.tsv"
bash examples/log-report/bin/log-report.sh \
    --input examples/log-report/fixtures/events.log \
    --output "$lab_dir/report.tsv"
diff -u examples/log-report/fixtures/expected.tsv "$lab_dir/report.tsv"
```

diff가 비어 있고 상태 0이면 정답과 일치한다. 다시 같은 결과 경로로 실행하면 실패하고 기존 보고서는 유지된다.

## 4. 기존 파일을 덮어쓰지 않고 결과 저장하기

기준 구현은 같은 디렉터리의 임시 파일을 만든 뒤 하드 링크를 만들어 완성된 결과를 최종 경로에서 읽을 수 있게 한다. 최종 경로가 이미 있으면 링크 생성이 실패하여 덮어쓰지 않는다. 이 방식을 지원하지 않는 파일시스템에서는 실패하도록 설계했다. Linux/macOS의 일반 로컬 파일시스템에서 실습한다.

임의의 공유 디렉터리가 적대적으로 교체되는 경우까지 다루는 범용 저장 API는 아니다. 작업 디렉터리 소유권과 수업 범위를 명시한다.

## 5. 검증 실행

```bash
bash tests/test-course.sh
```

도움말, 누락 옵션, 정상 집계, 기존 결과, 없는 입력, 잘못된 행, 빈 파일, 공백 경로, 마지막 개행 없음, 깨진 링크, dry-run, 임시 정리를 확인한다. 기준 구현은 [프로젝트 README](https://github.com/zxz3650/Bash-shell-programing/blob/master/examples/log-report/README.md)와 비교한다.

## 확장 과제

서비스별 집계, JSON 출력, 허용할 로그 수준 설정 중 하나를 추가한다. 먼저 입력·출력 형식과 종료 상태를 정하고, 이를 확인하는 테스트를 작성한다. 현재 예제는 수업용 로그 형식을 처리하므로 실제 로그에 적용하려면 해당 형식과 오류 처리 방법을 따로 정의해야 한다.

## ✅ 제출 기준

- [ ] README에 입출력 형식·사용법·지원 환경·한계가 있다.
- [ ] 고정 정답과 결과가 일치한다.
- [ ] 실패·재실행에서 원본과 기존 결과가 유지된다.
- [ ] dry-run에서 파일 생성이 없다.
- [ ] 테스트 결과와 변경 이유를 함께 제출한다.

다음: [12-2. 시스템 스냅샷과 최종 평가](12-2-snapshot-assessment.md)
