# 09-2. 테스트 설계·ShellCheck·Bats

좋은 테스트는 구현 줄을 따라 쓰는 것이 아니라 입력과 외부에서 관찰 가능한 결과를 검증한다. Bash 도구는 stdout, stderr, 종료 상태, 파일 변경을 함께 확인해야 한다.

{% hint style="info" %}
### 🧭 학습 목표

- 구문·정적 분석·서식·동작 검사를 구분한다.
- 정상·경계·실패 테스트를 설계한다.
- Bats의 run과 상태·출력을 사용한다.
- 임시 폴더에서 독립적으로 검증한다.
{% endhint %}

## 0. 테스트 표부터 작성

| 사례 | 기대 결과 | 확인 방법 |
|---|---|---|
| 정상 로그 | 정확한 수준별 행 수 | 기대 TSV와 비교 |
| 빈 로그 | 각 수준 0 | 빈 문자열과 구분 |
| 입력 없음 | 사용 오류 2 | 상태·stderr |
| 잘못된 레코드 | 오류, 결과 미생성 | 상태·파일 없음 |
| 기존 결과 | 덮어쓰기 거부 | 기존 내용 비교 |
| dry-run | 생성 없음 | 전후 파일 목록 |
| 공백 경로 | 정상 처리 | 같은 정답 |

## 1. 검사 계층

```bash
bash -n examples/log-report/bin/log-report.sh
shellcheck examples/log-report/bin/log-report.sh examples/log-report/lib/report.sh
shfmt -d examples/log-report/bin examples/log-report/lib
bash tests/test-course.sh
```

저장소 루트에서 실행한다. ShellCheck와 shfmt는 별도 설치가 필요하다. 첫 검사는 구문, 둘째는 알려진 위험 패턴, 셋째는 서식, 마지막은 실제 동작이다. 어느 하나가 다른 검사를 대신하지 않는다.

## 2. Bats 기본형

```bash
#!/usr/bin/env bats
@test "help exits successfully" {
    run bash examples/log-report/bin/log-report.sh --help
    [ "$status" -eq 0 ]
    [[ "$output" == usage:* ]]
}
```

run은 대상 명령을 실행하여 상태와 출력을 저장한다. 단순 기본 사용에서는 stdout과 stderr가 합쳐질 수 있으므로 스트림 분리가 필요한 검증은 파일 리다이렉션이나 지원하는 Bats 옵션을 사용한다. Bats 파일은 일반 bash -n 대상으로 보지 않고 bats로 실행한다.

## 3. 재현성과 독립성

각 테스트는 새 임시 디렉터리를 사용한다. 사용자 로그나 시스템 파일을 입력으로 쓰지 않는다. 테스트 성공 여부가 현재 작업 위치·기존 파일·시스템 시각에 의존하면 원인을 재현하기 어렵다.

권한 테스트는 root에서 의미가 달라질 수 있다. 읽기 권한을 제거한 사례를 시험한다면 실제 실행 사용자와 플랫폼을 기록하고 결과를 해석한다.

## 4. 실패 메시지

“test failed”만 출력하면 원인을 알기 어렵다. 기대한 상태와 관찰한 상태, 테스트 이름, 관련 stderr를 제한된 길이로 보여 준다. 테스트가 없는 경로를 지원한다고 문서에 쓰지 않는다.

## 5. 변경과 회귀

입력 형식을 바꾸면 정상 예제뿐 아니라 기존 형식이 거부되는지 검사한다. 오류를 수정했으면 해당 입력을 회귀 테스트에 남긴다. 코드 줄 수보다 요구한 동작과 오류 처리를 빠짐없이 검증하는지가 중요하다.

## 🧪 직접 해보기

1. tests/test-course.sh의 테스트 사례를 읽고 실행한다.
2. ERROR 집계를 일부러 틀리게 바꾸어 테스트가 실패하는지 확인한 뒤 복구한다.
3. CRITICAL 수준을 추가하는 변경에 필요한 테스트를 설계한다.

### 해설

테스트가 잘못된 구현에서도 통과하면 검증 대상이 약하다. 정답 행 수, 최종 결과 파일의 생성 여부, 기존 파일 보존은 서로 독립적으로 확인한다.

## ✅ 완료 기준

- [ ] 네 가지 검사 역할을 설명한다.
- [ ] 실패 입력에서도 원본과 기존 결과를 보존한다.
- [ ] 같은 테스트를 연속 두 번 실행해 통과한다.

근거: [Bats 공식 테스트 안내](https://bats-core.readthedocs.io/en/stable/writing-tests.html), [ShellCheck](https://www.shellcheck.net/).

다음: [10. 프로그램 구조화](../10-program-architecture.md)
