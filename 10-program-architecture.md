# 10. 프로그램 구조화

## 기본 학습과 보안 실습 연결

10-1·10-2에서 모듈·함수·Bash와 Python의 역할 분담을 학습한 뒤 [10-3. Journal 분석](10-program-architecture/10-3-journal-analysis.md)과 [10-4. Audit 이벤트](10-program-architecture/10-4-audit-analysis.md)에 적용합니다. 수집·파싱·검증·판단을 나누고 복잡한 형식에 맞는 도구를 선택합니다.

## 개요

한 파일에 뒤섞인 스크립트를 입력, 검증, 처리, 출력과 오류 처리 책임으로 나누어 유지 가능한 프로그램으로 구성합니다.

## 학습 순서

1. [10-1. 모듈 구성과 함수의 입력·출력](10-program-architecture/10-1-modules-contracts.md)
2. [10-2. Bash와 Python의 역할 분담](10-program-architecture/10-2-bash-python-boundary.md)

source 시 실행되는 명령, 함수의 숨은 전역 의존성, 프로그램 사이에 데이터를 전달하는 형식을 확인합니다. [노트북 10](jupyter-book/labs/10-modules-contracts.ipynb)에서 라이브러리를 만들고 호출합니다. 제공 로그 보고서 프로젝트의 bin·lib 분리를 실제 사례로 읽습니다.

{% hint style="info" %}
## 🧭 학습 목표

- `main` 진입점과 작은 함수로 실행 흐름을 구조화한다.
- 함수의 stdout과 종료 상태를 구분한다.
- 공통 라이브러리와 실행 파일의 경계를 설계한다.
{% endhint %}

## 1. 권장 골격

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly program_name=${0##*/}

validate_input() { [[ -r $1 ]]; }
collect() { wc -l -- "$1"; }

main() {
    (($# == 1)) || return 2
    validate_input "$1" || return 1
    collect "$1"
}

main "$@"
```

## 2. 함수의 입력과 출력

함수마다 입력 인수, stdout 형식, stderr 오류와 종료 상태를 문서화합니다. 전역 변수보다 `local` 변수를 사용하고 함수가 예상 밖의 디렉터리 변경이나 종료를 일으키지 않도록 합니다.

## 3. 라이브러리와 실행 진입점

```bash
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    main "$@"
fi
```

이 조건을 사용하면 파일을 `source`하여 함수를 테스트하면서도 `main`의 자동 실행을 막을 수 있습니다.

## 4. 언어 전환 기준

복잡한 JSON 처리, 여러 작업 사이의 상태 공유, 장기 실행 서비스가 필요해지면 Python이나 Go로 핵심 로직을 옮길지 검토합니다.

## 🧪 종합 실습

기존 로그 분석 스크립트를 `parse_args`, `validate_input`, `analyze`, `render_report`, `main`으로 분리하고 각 함수의 입력 인수, 출력 형식, 종료 상태를 문서화합니다.

## ✅ 완료 기준

- 실행 흐름이 `main`에서 한눈에 보인다.
- 각 함수가 한 가지 책임을 가진다.
- 핵심 함수를 독립적으로 테스트할 수 있다.
