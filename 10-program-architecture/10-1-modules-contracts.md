# 10-1. main·라이브러리·함수 계약

스크립트가 커지면 인수 처리, 데이터 처리, 파일 게시가 뒤섞인다. 함수 이름만 나누는 것보다 각 함수가 받는 입력과 바꾸는 상태를 제한해야 독립 테스트가 가능해진다.

{% hint style="info" %}
### 🧭 학습 목표

- 입력·검증·처리·출력을 분리한다.
- source의 실행 범위를 설명한다.
- 라이브러리에 전역 부수 효과를 넣지 않는다.
- 실행 파일 위치를 기준으로 의존 파일을 찾는다.
{% endhint %}

## 0. 학습 전 확인

라이브러리를 source했을 때 cd·exit·trap이 실행되면 호출자에게 어떤 영향을 주는가?

## 1. 프로젝트 구조

```text
examples/log-report/
├── bin/log-report.sh       인수·검증·파일 게시·종료
├── lib/report.sh           stdin 집계 → stdout TSV
├── fixtures/events.log    고정 입력
├── fixtures/expected.tsv  고정 정답
└── README.md               계약·사용법·한계
```

실행 파일은 CLI를 담당하고 라이브러리는 데이터 변환을 담당한다. 라이브러리 함수는 입력 파일 위치를 모르므로 stdin으로 받은 데이터만 처리한다.

## 2. 라이브러리 로드

```bash
# 저장소 루트에서 실행
source examples/log-report/lib/report.sh
printf 'INFO api\nERROR db\n' | summarize_events
```

헤더와 INFO=1, WARN=0, ERROR=1이 출력된다. source는 새 프로세스에서 실행하는 것이 아니라 현재 셸에 함수를 정의한다. 라이브러리 최상위에는 파일 생성·trap 설정·set 옵션 변경 등을 두지 않는다.

## 3. 위치 기준

```bash
# 실행 파일 내부
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P) || exit 1
source "$script_dir/../lib/report.sh" || exit 1
```

현재 작업 디렉터리와 무관하게 설치된 라이브러리를 찾는다. 라이브러리 파일이 없으면 필수 의존성 실패로 종료한다. 임의 사용자 경로의 스크립트를 자동 source하지 않는다.

## 4. 계약을 나누기

| 구성 | 입력 | 출력 | 부수 효과 |
|---|---|---|---|
| 옵션 해석 | argv | 설정 변수 | 없음 |
| summarize_events | stdin 레코드 | 검증된 TSV | 없음 |
| 결과 게시 | 임시·최종 경로 | 성공·실패 | 새 결과 파일 |
| main | 전체 요청 | 종료 상태·로그 | 작업 조정 |

함수 사이에 큰 문자열로 파일 전체를 복사하지 않는다. 스트림과 파일을 사용하면 메모리 사용과 인수 크기 제한 문제를 줄일 수 있다.

## 5. 실행 진입점 가드

```bash
main() { printf 'running\n'; }
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    main "$@"
fi
```

직접 실행할 때만 main을 호출하는 패턴이다. 단, 가드 밖의 명령은 source 시에도 실행된다. 위 가드만 넣고 최상위의 파일 생성이 차단된다고 생각하지 않는다.

## 🧪 직접 해보기

1. 라이브러리를 source한 뒤 아무 함수를 호출하지 않고 출력·파일 변경이 없는지 확인한다.
2. 다른 디렉터리에서 절대 경로로 CLI를 실행한다.
3. summarize_events를 파일 대신 printf 파이프로 시험한다.

## ✅ 완료 기준

- [ ] 각 함수의 입력·stdout·stderr·상태 계약이 있다.
- [ ] source 시 숨은 부수 효과가 없다.
- [ ] 현재 작업 위치에 의존하지 않는다.

다음: [10-2. Python과의 역할 분담](10-2-bash-python-boundary.md)
