# 03. Bash 기초 문법

## 개요

변수, 매개변수 확장, quoting과 배열을 학습하고 조건문·반복문·함수 문서로 확장합니다.

{% hint style="info" %}
## 🧭 학습 목표

- 변수와 환경 변수의 범위를 구분한다.
- word splitting과 glob을 제어하는 quoting 규칙을 적용한다.
- 여러 인수를 문자열이 아닌 배열로 보존한다.
{% endhint %}

## 선행 지식

- 02장의 명령 실행, 종료 상태와 shebang

## 3.1 변수와 환경 변수

```bash
course='bash-security'
printf '%s\n' "$course"

export LOG_LEVEL='info'
env | grep '^LOG_LEVEL='
```

일반 변수는 현재 셸에서만 사용되고, `export`한 환경 변수는 자식 프로세스에 전달됩니다. 비밀번호나 토큰을 명령행 인수로 전달하면 프로세스 목록과 기록에 노출될 수 있습니다.

## 매개변수 확장

```bash
name=${1:-student}
: "${INPUT_FILE:?INPUT_FILE is required}"
base=${path##*/}
extension=${base##*.}
```

- `${var:-default}`: 값이 없으면 기본값 사용
- `${var:?message}`: 값이 없으면 오류와 함께 중단
- `${var#pattern}`, `${var##pattern}`: 앞부분 패턴 제거
- `${var%pattern}`, `${var%%pattern}`: 뒷부분 패턴 제거

## 인용이 중요한 이유

```bash
file='incident report.txt'
printf '%s\n' "$file"       # 한 개의 인수
printf '%s\n' $file         # 두 단어로 분리될 수 있음
```

기본 규칙은 **변수 확장을 큰따옴표로 감싸는 것**입니다. 의도적인 단어 분리와 glob 확장이 필요한 경우에만 예외를 둡니다.

```bash
literal='$HOME/*.log'
expanded="$HOME"
printf 'literal=%s\n' "$literal"
printf 'expanded=%s\n' "$expanded"
```

작은따옴표는 모든 문자를 그대로 보존하고, 큰따옴표 안에서는 변수와 명령 치환이 확장됩니다.

## 배열

여러 인수는 문자열 하나가 아니라 배열로 보관합니다.

```bash
patterns=('failed password' 'invalid user' 'sudo:')

for pattern in "${patterns[@]}"; do
    printf 'pattern=%s\n' "$pattern"
done
```

명령 옵션도 배열로 구성하면 quoting 문제를 줄일 수 있습니다.

```bash
grep_args=(-n -F --)
grep "${grep_args[@]}" 'failed password' auth.log
```

## 🧪 직접 해보기

1. 인수가 없으면 `usage` 메시지와 함께 실패하는 스크립트를 작성하세요.
2. 공백이 포함된 IOC 문자열 세 개를 배열로 순회하세요.
3. 작은따옴표와 큰따옴표에서 `$HOME` 출력이 어떻게 다른지 확인하세요.

## ✅ 완료 기준

- 공백과 특수문자가 있는 값을 손실 없이 전달할 수 있다.
- `${var:-default}`와 `${var:?message}`를 상황에 맞게 사용한다.
- [`03-1. 조건문, 반복문과 함수`](03-control-flow-functions.md)로 제어 흐름을 구성할 수 있다.
