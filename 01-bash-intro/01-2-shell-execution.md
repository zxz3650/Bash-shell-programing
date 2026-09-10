# 01-2. 명령이 실행되는 과정

## 개요와 학습 목표

조사 결과 파일 이름을 `case 01.txt`로 정했는데 두 개의 인수로 처리되거나, 실패한 수집을 성공으로 기록할 수 있습니다. 이런 오류는 보안 도구를 더 설치한다고 해결되지 않습니다. **Bash가 입력을 해석하는 과정**을 이해해야 합니다.

이 절에서는 인용·명령 치환·환경 전달·표준 스트림·종료 상태를 짧은 관찰 실습으로 익힙니다. 상세 문법은 기존 [03장](../03-bash-basics.md)을 참고 자료로 사용합니다.

## 1. Terminal, Shell, Script의 역할

| 구성 | 역할 | 이 실습에서의 예 |
|---|---|---|
| Terminal | 키 입력과 화면 출력 연결 | Ubuntu 터미널 창 |
| Shell | 명령 해석과 실행 조정 | Bash 프로세스 |
| Shell Script | 명령을 저장한 텍스트 | `observe-context.sh` |
| 외부 명령 | 자신의 옵션과 인수를 처리 | `uname`, `id`, `ps` |

대화형 셸은 입력을 받으며 사용하고, 비대화형 셸은 파일이나 문자열의 명령을 실행합니다. `%%bash`는 Python 커널이 실행하는 비대화형 Bash 셀입니다. 대화형 alias와 설정이 자동으로 동일하게 적용된다고 가정하지 않습니다.

`#!/usr/bin/env bash`는 직접 실행할 때 사용할 인터프리터를 명시합니다. `bash script.sh`로 실행하면 앞에서 지정한 Bash가 파일을 읽습니다. `.sh` 확장자만으로 Bash가 선택되지 않습니다. `/bin/sh`를 사용하는 스크립트에는 Bash 전용 문법을 무조건 넣을 수 없습니다.

## 2. 입력에서 종료 상태까지

```text
입력 읽기 → 토큰·구문 해석 → 확장 → 리다이렉션 준비
                                      ↓
                           명령 실행 → 종료 상태
```

이 도식은 일반 명령을 설명하는 요약입니다. 인용 여부와 구문에 따라 세부 규칙이 달라집니다. Bash는 전체 스크립트를 먼저 실행 인수로 바꾸는 것이 아니라 명령을 읽고 처리하며 진행합니다.

다음 예제의 해석을 순서대로 설명해 봅니다.

```bash
label='case 01'
printf '<%s>\n' "$label"
```

1. `label='case 01'`은 변수 대입입니다. 대입의 `=` 주변에는 공백을 넣지 않습니다.
2. `printf`가 명령 이름이며, `'<%s>\n'`은 형식 인수입니다.
3. `"$label"`은 값으로 확장되면서 한 인수의 경계를 유지합니다.
4. 결과는 stdout에 `<case 01>` 한 행으로 나옵니다.
5. 성공 여부는 화면 문자열이 아니라 종료 상태로도 확인합니다.

## 3. 잘못된 인용을 안전하게 관찰

> **Bash Point — Quoting과 Word Splitting**

아래 첫 명령은 잘못된 인용을 관찰하기 위한 예입니다. 삭제·이동 대신 출력 명령만 사용합니다.

```bash
label='case 01'
printf '<%s>\n' $label
printf '<%s>\n' "$label"
```

```text
<case>
<01>
<case 01>
```

일반 명령에서 인용되지 않은 확장 결과는 단어 분리와 파일명 확장을 거칠 수 있습니다. `*`가 들어 있으면 현재 디렉터리 내용에 따라 인수 목록도 달라질 수 있습니다. 공백이 있는 파일명이 잘못된 것이 아니라 인수 전달이 잘못된 것입니다.

`"$file"`로 인용하는 것과 `--`로 옵션 해석을 끝내는 것은 서로 다른 문제를 해결합니다. 큰따옴표만 추가했다고 모든 경로 검증과 안전성이 해결되지는 않습니다. `--` 지원 여부도 명령마다 확인합니다.

## 4. 명령 탐색과 PATH

```bash
type printf
type cd
command -v bash
command -v uname
```

예시:

```text
printf is a shell builtin
cd is a shell builtin
/usr/bin/bash
/usr/bin/uname
```

경로는 환경마다 달라집니다. `printf`, `cd`는 Bash 내부 기능일 수 있고, `uname`은 외부 실행 파일입니다. 함수·builtin·PATH 탐색과 alias 치환은 같은 단계가 아닙니다. `command -v`는 선택되는 명령을 확인하는 데 도움을 주지만, 파일의 진위를 검증하는 도구는 아닙니다.

보안 분석에서는 “어떤 명령을 썼는가”뿐 아니라 “어떤 프로그램이 선택되었는가”도 중요합니다. 이 장에서는 PATH 변경이나 다른 실행 파일로 치환하는 실습을 하지 않습니다.

## 5. 자식에게 전달되는 환경

> **Bash Point — Variable와 Environment Variable**

```bash
lab_label='parent-only'
export LAB_CASE='LAB-001'
bash -c 'printf "label=%s case=%s\n" "${lab_label-unset}" "$LAB_CASE"'
```

예상 출력은 `label=unset case=LAB-001`입니다. `export`한 값은 새 자식에게 전달됩니다. 자식에서 값을 바꾸어도 부모의 값이 자동 변경되지는 않습니다. `export`는 비밀정보 보호 기능이 아닙니다.

전체 `env` 출력 대신 필요한 변수만 확인합니다. 토큰과 사용자 설정이 포함될 수 있는 전체 환경을 공개 보고서에 붙이지 않습니다. 위의 LAB_CASE는 비밀정보가 아닌 교육용 표식입니다.

## 6. 출력이 있으면 성공인가?

> **Bash Point — Exit Status**

```bash
bash -c 'printf "partial observation\n"; exit 7'
status=$?
printf 'observed_status=%s\n' "$status"
```

이 관찰 블록은 `set -e`가 꺼진 별도 Bash에서 실행합니다. 출력은 있지만 상태는 7입니다. 7은 이 실습이 정한 실패 상태이며 모든 명령에 같은 의미가 있는 번호는 아닙니다.

```text
partial observation
observed_status=7
```

`$?`는 직전 명령의 상태입니다. 중간에 `printf`를 실행한 뒤 확인하면 원래 실패를 놓칩니다. 스크립트에서 예상 실패를 처리할 때는 다음 패턴을 사용합니다.

```bash
if bash -c 'exit 7'; then
    printf 'completed\n'
else
    status=$?
    printf 'collection failed: %s\n' "$status" >&2
fi
```

`if`는 명령 상태 0을 성공으로 판단합니다. 오류 상태를 기록하는 최소 분기로 사용하며 모든 조건문 문법을 지금 암기할 필요는 없습니다.

## 7. stdout과 stderr를 분리

새 실습 디렉터리를 만들며, 모든 파일은 그 안에만 기록합니다. 아래 블록은 한 번에 실행합니다.

```bash
lab_dir=$(mktemp -d) || exit 1
umask 077
status=0
bash -c 'printf "data\n"; printf "read failed\n" >&2; exit 7' \
    > "$lab_dir/output.txt" 2> "$lab_dir/error.txt" || status=$?
printf 'status=%s lab=%s\n' "$status" "$lab_dir"
cat "$lab_dir/output.txt"
cat "$lab_dir/error.txt"
```

`output.txt`에는 data, `error.txt`에는 read failed가 들어갑니다. 자료와 진단을 분리해야 후속 도구가 오류 메시지를 정상 레코드로 집계하지 않습니다. `>`는 기존 파일을 비울 수 있으므로 원본 증거를 출력 대상으로 지정하지 않습니다. 새 파일 저장과 기존 파일 거부는 [01-4](01-4-observation-lab.md)에서 연습합니다.

## 실패 사례 / 주의사항

- `set -e`를 붙였다고 모든 오류가 처리되는 것은 아닙니다. 조건부 호출 등 문맥별 한계는 [09-1](../09-testing-debugging/09-1-errors-tracing.md)에 있습니다.
- 변수에 들어 있는 데이터를 `eval`로 다시 해석하지 않습니다. 조사 자료는 코드가 아닙니다.
- `<file`·`>file`은 Bash가 처리하고, `grep`의 검색 옵션은 grep이 처리합니다.
- `%%bash`를 터미널에 입력하지 않습니다. Python 커널의 셀 매직입니다.

## 실습·분석 질문

1. `case 01`이 한 인수인 결과와 두 인수인 결과를 비교합니다.
2. 정상 데이터 한 행·오류 한 행·상태 7을 각각 구분합니다.
3. `printf`를 중간에 넣으면 `$?`가 달라지는 이유를 설명합니다.
4. 전체 환경을 보고서에 덤프하지 않아야 하는 이유를 적습니다.

## 완료 기준과 정리

- [ ] 입력 문자열에서 최종 인수의 경계를 설명합니다.
- [ ] 설정값과 실제 명령 실행을 구분합니다.
- [ ] 데이터·진단·상태를 서로 다른 정보로 기록합니다.
- [ ] 실패를 발견한 뒤 성공으로 덮지 않습니다.

## 참고 자료

- [GNU Shell Operation](https://www.gnu.org/software/bash/manual/html_node/Shell-Operation.html)
- [GNU Shell Expansions](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html)
- [ShellCheck SC2086](https://www.shellcheck.net/wiki/SC2086)

다음: [01-3. 행위·흔적·판단의 구분](01-3-artifacts-and-reasoning.md)
