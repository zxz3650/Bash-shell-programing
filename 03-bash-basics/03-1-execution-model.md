# 03-1. 명령 실행과 종료 상태

셸 프로그래밍의 기본 단위는 명령이다. Bash는 입력을 읽고 확장한 뒤 명령과 인수를 구분하여 실행한다. 명령에는 인수 목록, 표준 스트림, 종료 상태라는 계약이 있다.

{% hint style="info" %}
### 🧭 학습 목표

- 명령 이름, 옵션, 피연산자를 구분한다.
- builtin과 외부 실행 파일을 구분한다.
- stdout, stderr, 종료 상태를 각각 관찰한다.
- 순차 실행과 조건부 실행을 예측한다.
{% endhint %}

## 선행 지식과 준비

[02장](../02-bash-setup.md)의 Bash 터미널이 필요하다. 아래 예제는 파일을 변경하지 않는다. 코드는 블록 안에서 위에서 아래로 실행한다.

## 0. 학습 전 확인

1. 화면에 아무것도 나오지 않으면 실패인가?
2. 명령의 옵션은 Bash가 모두 해석하는가?
3. 실패 후 다른 명령을 실행하면 `$?`는 무엇인가?

## 1. 명령과 인수

```bash
printf '%s\n' 'blue team' 'red team'
```

명령은 `printf`이며 나머지 세 값은 각각 하나의 인수다. 첫 인수는 출력 형식, 이후 인수는 데이터다. 따옴표는 경계를 보존하고 실제 인수에는 포함되지 않는다.

```text
blue team
red team
```

`grep -nF -- 'ERROR' ./app.log`에서 옵션의 의미는 grep이 해석한다. Bash는 인수의 경계를 만든다. 리다이렉션 `>`나 파이프 `|`는 셸이 처리한다.

## 2. 명령의 정체

```bash
type cd
type printf
type -a bash
command -v grep
```

`cd`는 현재 셸의 작업 디렉터리를 바꿔야 하므로 builtin이다. 외부 프로그램이 자기 디렉터리를 바꾸어도 부모 셸에는 영향을 주지 않는다. `printf`는 builtin과 외부 실행 파일이 함께 존재할 수 있다.

alias는 입력을 읽을 때 치환되며 기본적으로 비대화형 Bash에서는 확장되지 않는다. 이후 함수·builtin·PATH의 실행 파일 등을 찾아 실행한다. 자동화에서 개인 alias 설정에 의존하지 않는다.

## 3. 출력과 성공 여부

```bash
true
printf 'true status=%s\n' "$?"
false
status=$?
printf 'false status=%s\n' "$status"
```

예상 출력은 `true status=0`, `false status=1`이다. 두 명령 자체는 아무것도 출력하지 않는다. 실패를 관찰하는 예제는 `set -e`가 없는 별도 Bash에서 실행한다.

| 경로 | 전달하는 것 | 소비자 |
|---|---|---|
| stdout, FD 1 | 정상 데이터 | 다음 명령 또는 결과 파일 |
| stderr, FD 2 | 진단·진행 메시지 | 운영자 또는 로그 |
| 종료 상태 | 성공·실패 정수 | if, 호출 프로그램 |

0은 성공이다. 1 이상은 명령별 의미를 확인해야 한다. grep의 1은 검색 결과 없음, 2는 오류다. 모든 비영 값을 같은 장애로 취급하면 빈 결과를 잘못 판단한다.

## 4. 조건부 실행

```bash
false; printf 'semicolon continues\n'
false && printf 'not printed\n'
false || printf 'fallback\n'
if true; then
    printf 'success branch\n'
fi
```

`;`는 성공 여부와 무관하게 다음 명령을 실행한다. `&&`는 앞 명령이 성공할 때, `||`는 실패할 때 다음 명령을 실행한다. 복잡한 분기는 `if`로 작성한다.

`A && B || C`는 삼항 연산자가 아니다. A가 성공해도 B가 실패하면 C가 실행된다.

## 5. 실패 사례

```bash
false
printf 'another command\n'
printf 'observed=%s\n' "$?"
```

관찰한 상태는 false가 아니라 직전 printf의 결과인 0이다. 실패 직후 상태를 저장해야 한다. 화면의 성공 문구만 검사하면 실패 상태로 종료한 프로그램을 놓칠 수 있다.

## 🧪 직접 해보기

1. stdout에 report, stderr에 warning을 출력하고 3으로 종료하는 자식 Bash를 만든다.
2. 그 상태를 저장하여 `status=3`을 출력한다.
3. `false && true || printf 'recovered\n'`의 흐름을 설명한다.

### 힌트와 해설

`bash -c '명령들; exit 3'`를 사용한다. 현재 터미널에 exit를 직접 입력하면 세션이 끝난다. 자료가 출력되어도 명령은 실패할 수 있다.

## ✅ 완료 기준

- [ ] 인수 세 개와 공백을 포함한 인수 하나를 구분한다.
- [ ] 출력 내용과 종료 상태를 각각 기록한다.
- [ ] 조건부 실행을 if문으로 바꿔 설명한다.

다음: [03-2. 변수와 환경 변수](03-2-variables-environment.md)
