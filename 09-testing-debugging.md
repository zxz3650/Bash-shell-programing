# 09. 로그인 아티팩트와 분석 검증

## 보안 질문에서 시작하기

“인증·세션 기록이 일치하고 계산에 중복이나 누락이 없는가?” [로그인 아티팩트 실습](09-testing-debugging/09-3-login-artifacts.md)을 진행한 뒤 아래 ShellCheck·동작 테스트를 적용합니다. 실행 코드뿐 아니라 분석 전제에도 반례를 준비합니다.

## 개요

구문 검사, 정적 분석, 서식 검사와 동작 테스트를 결합해 스크립트 변경을 검증합니다.

## 학습 순서와 실습

1. [09-1. 종료 상태·errexit·추적](09-testing-debugging/09-1-errors-tracing.md)
2. [09-2. 테스트 설계·품질 검사](09-testing-debugging/09-2-tests-quality.md)

set -e가 모든 오류를 막는지, bash -n 성공이 올바른 결과를 의미하는지, 테스트가 원본 보존도 확인하는지 질문합니다. [노트북 09](jupyter-book/labs/09-error-contracts.ipynb)와 `bash tests/test-course.sh`로 실행 결과를 검증합니다.

{% hint style="info" %}
## 🧭 학습 목표

- `bash -n`, ShellCheck, shfmt와 Bats의 역할을 구분한다.
- 정상·실패·악의적 입력을 테스트한다.
- 실패 결과에서 원인을 재현하고 수정한다.
{% endhint %}

## 구문 검사

```bash
bash -n script.sh
```

스크립트를 실행하지 않고 Bash 구문 오류를 검사합니다. 실행 중 발생하는 논리 오류는 찾지 못합니다.

## ShellCheck

```bash
shellcheck script.sh
```

ShellCheck는 인용 누락, 잘못된 배열 처리, 의도하지 않은 glob과 word splitting 등 잠재 결함을 탐지합니다. 경고를 제외해야 한다면 이유와 최소 범위를 기록합니다.

```bash
# shellcheck disable=SC1091  # 배포 시 생성되는 환경 파일
source "$config_file"
```

## shfmt

```bash
shfmt -d .          # 차이 확인
shfmt -w -i 4 .     # 들여쓰기 4칸으로 수정
```

shfmt는 스타일을 통일하지만 코드의 안전성이나 정확성을 보장하지 않습니다.

## Bats

테스트 대상:

```bash
#!/usr/bin/env bash

greet() {
    (($# == 1)) || return 2
    printf 'hello, %s\n' "$1"
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    greet "$@"
fi
```

`test/greet.bats`:

```bash
#!/usr/bin/env bats

@test "이름을 출력한다" {
    run ./greet.sh 'blue team'
    [ "$status" -eq 0 ]
    [ "$output" = 'hello, blue team' ]
}

@test "인수가 없으면 사용 오류를 반환한다" {
    run ./greet.sh
    [ "$status" -eq 2 ]
}
```

```bash
bats test/
```

## 권장 검사 순서

```bash
for script in scripts/*.sh; do
    [[ -e $script ]] || continue
    bash -n "$script" || break
done
shfmt -d scripts test
shellcheck scripts/*.sh test/*.bats
bats test/
```

각 도구의 역할은 다음과 같습니다.

| 도구 | 질문 |
|---|---|
| `bash -n` | Bash 문법이 올바른가? |
| shfmt | 코드 형식이 일관적인가? |
| ShellCheck | 알려진 위험 패턴이 있는가? |
| Bats | 실제 결과와 종료 상태가 요구사항에 맞는가? |

## 🧪 직접 해보기

1. 기존 스크립트 하나에 네 가지 검사를 모두 적용하세요.
2. 공백, 빈 값, 하이픈, 읽기 불가 파일을 테스트 케이스로 추가하세요.
3. 실패한 테스트가 문제를 명확히 설명하는지 확인하세요.

## ✅ 완료 기준

- 네 가지 검사를 일관된 순서로 실행한다.
- 종료 상태, stdout과 stderr를 테스트로 검증한다.
