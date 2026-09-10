# 03. Bash 기초 문법

## 기본 학습과 보안 실습 연결

처음 배우는 학생은 01·02장을 마친 뒤 아래 03-1부터 03-9까지의 기본 문법을 순서대로 학습합니다. 변수·인용·인수·조건·반복·함수를 직접 실행한 다음 [03-10. IOC 검색 실습](03-bash-basics/03-10-ioc-search.md)에 적용합니다. 문법을 이미 아는 학생은 적용 실습의 질문부터 시작해 필요한 절을 복습할 수 있습니다. [Bash 문법 찾아보기](bash-syntax-index.md)에서도 각 상세 절로 바로 이동할 수 있습니다.

## 개요

명령 실행부터 변수·인용·배열·조건·반복·함수까지 단계별로 학습합니다. 아래 상세 절이 본 학습 경로이며, 이 페이지의 짧은 예제는 복습용입니다. Python의 객체·반환값·어휘적 스코프를 Bash의 문자열·종료 상태·동적 스코프와 구분합니다.

## 학습 전 확인

1. 출력이 없는 명령도 성공할 수 있는가?
2. 공백을 포함한 값을 한 인수로 전달하려면 무엇이 필요한가?
3. 함수의 return과 stdout은 같은 것인가?
4. 파이프 안에서 바꾼 변수는 부모 셸에 남는가?

## 학습 순서

1. [03-1. 명령 실행과 종료 상태](03-bash-basics/03-1-execution-model.md)
2. [03-2. 변수와 환경 변수](03-bash-basics/03-2-variables-environment.md)
3. [03-3. 인용과 확장 순서](03-bash-basics/03-3-quoting-expansion.md)
4. [03-4. 위치 인자와 배열](03-bash-basics/03-4-arguments-arrays.md)
5. [03-5. 문자열과 산술식](03-bash-basics/03-5-strings-arithmetic.md)
6. [03-6. 조건문과 case](03-bash-basics/03-6-conditions.md)
7. [03-7. 반복문과 입력 스트리밍](03-bash-basics/03-7-loops.md)
8. [03-8. 함수와 스코프](03-bash-basics/03-8-functions.md)
9. [03-9. 문법 종합 실습](03-bash-basics/03-9-syntax-project.md)

노트북 02·03으로 문법을 실행하고 마지막 절에서 이벤트 분류기를 완성합니다. [실습 연결표](course-guide.md)를 참고합니다.

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
path='./reports/sample.log'
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
- [03-9. 문법 종합 실습](03-bash-basics/03-9-syntax-project.md)의 정상·실패 입력을 검증할 수 있다.
