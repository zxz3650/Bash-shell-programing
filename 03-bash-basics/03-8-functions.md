# 03-8. 함수와 스코프

Bash 함수는 명령 묶음에 이름을 붙인다. Python 함수의 객체 반환과 달리 Bash 함수는 stdout으로 데이터를 내보내고 return으로 종료 상태를 전달한다. 이 둘을 섞으면 재사용하기 어렵다.

{% hint style="info" %}
### 🧭 학습 목표

- 정의와 호출을 구분한다.
- 위치 인자·local·stdout·return의 역할을 설명한다.
- Bash의 동적 스코프가 만드는 의존성을 찾는다.
- 함수가 받는 인수, 출력하는 내용, 반환하는 종료 상태, 변경하는 파일이나 변수를 문서화한다.
{% endhint %}

## 학습 전 확인

`return 5`는 숫자 5라는 데이터를 반환하는가? 함수의 printf 결과는 어디에 도착하는가?

## 1. 정의와 호출

```bash
greet() {
    local name=${1:-student}
    printf 'hello, %s\n' "$name"
}
printf 'before\n'
greet 'blue team'
printf 'after\n'
```

정의 시 본문은 실행되지 않는다. 호출 시 함수의 위치 인자는 전달한 인수로 설정된다. 함수 호출에는 Python처럼 괄호 안에 인수를 넣지 않는다.

## 2. 출력 데이터와 종료 상태 구분하기

```bash
classify() {
    (( $# == 1 )) || return 2
    case $1 in
        ERROR) printf 'review\n' ;;
        INFO) printf 'normal\n' ;;
        *) printf 'unknown level\n' >&2; return 2 ;;
    esac
}
if result=$(classify ERROR); then
    printf 'result=%s\n' "$result"
fi
```

result=review다. 함수 데이터는 명령 치환으로 캡처한다. return 2는 실패 상태이며 출력 문자열이 아니다. 종료 상태는 0~255로 표현되므로 큰 숫자 계산 결과를 return에 담지 않는다.

## 3. local과 동적 스코프

```bash
show_label() { printf '%s\n' "$label"; }
outer() {
    local label='inside outer'
    show_label
}
label='global'
outer
printf '%s\n' "$label"
```

출력은 inside outer, global이다. 호출한 함수의 local 변수가 내부에서 호출한 함수에도 보일 수 있다. Python의 어휘적 스코프와 차이가 있다. 재사용 함수는 숨은 label 대신 인수로 값을 받게 설계한다.

## 4. 대입 상태를 보존

```bash
capture() {
    local result
    result=$(printf 'ready') || return 1
    printf '%s\n' "$result"
}
capture
```

`local result=$(command)`는 local 명령의 성공 상태가 command 실패를 가릴 수 있다. 선언과 값을 얻는 명령을 분리한다.

## 5. 함수의 입력과 출력

함수를 사용하려는 사람이 알아야 할 내용을 표로 정리한다. 파일이나 전역 변수를 변경하는 동작은 부수 효과라고 하며, 입력·출력과 함께 명시한다.

| 항목 | classify의 동작 |
|---|---|
| 입력 | INFO 또는 ERROR 한 개 |
| stdout | normal 또는 review 한 행 |
| stderr | 잘못된 입력 설명 |
| 상태 | 성공 0, 사용 오류 2 |
| 부수 효과 | 파일 변경 없음 |

호출자가 조건문으로 함수를 실행하면 errexit 동작도 달라질 수 있다. 함수 내부에서 중요한 실패를 명시적으로 처리한다. [09-1](../09-testing-debugging/09-1-errors-tracing.md)에서 확인한다.

## 🧪 직접 해보기

1. classify에 인수 없음·INFO·ERROR·DEBUG를 전달한다.
2. stdout, stderr, 상태를 각각 기록한다.
3. show_label을 인수 기반 함수로 고쳐 전역 label을 제거한다.

### 해설

DEBUG는 빈 성공 결과가 아니라 사용 오류로 다룬다. 정상 데이터를 stderr에 섞거나 진행 로그를 stdout에 넣으면 캡처한 result가 오염된다.

## ✅ 완료 기준

- [ ] 함수의 입력 인수, 정상 출력, 오류 메시지, 종료 상태와 파일·변수 변경 여부를 설명한다.
- [ ] local 선언과 실패 가능한 대입을 분리한다.
- [ ] 숨은 전역 의존성을 인수로 바꾼다.

다음: [03-9. 문법 종합 실습](03-9-syntax-project.md)
