# 03-6. 조건문과 case

Bash의 if는 Python처럼 조건식 객체를 받는 대신 명령의 종료 상태를 판단한다. test, `[[ ... ]]`, `(( ... ))`도 상태를 만드는 명령 또는 구문이다.

{% hint style="info" %}
### 🧭 학습 목표

- if·elif·else의 실행 경로를 예측한다.
- 문자열·파일·산술 조건을 구분한다.
- 패턴 비교와 문자 그대로 비교를 선택한다.
- case로 입력 모드를 제한한다.
{% endhint %}

## 0. 학습 전 확인

문자열 10과 2의 비교가 숫자 비교와 같은가? 빈 문자열의 길이를 검사하는 연산자는 무엇인가?

## 1. if가 판단하는 것

```bash
if command -v bash >/dev/null 2>&1; then
    printf 'Bash is available\n'
else
    printf 'Bash not found\n' >&2
fi
```

조건 위치에는 명령이 들어간다. 성공 0일 때 then, 실패일 때 else를 실행한다. 세미콜론은 then을 같은 줄에 두기 위한 구분자다.

## 2. 문자열·파일·숫자

| 목적 | 예 | 의미 |
|---|---|---|
| 빈 값 | `[[ -z $value ]]` | 길이 0 |
| 값 있음 | `[[ -n $value ]]` | 길이 비영 |
| 문자열 일치 | `[[ $value == "$expected" ]]` | 문자 그대로 비교 |
| 일반 파일 | `[[ -f $path ]]` | 일반 파일을 가리킴 |
| 읽기 가능 | `[[ -r $path ]]` | 현재 사용자 기준 |
| 정수 비교 | `(( count >= 3 ))` | 산술 비교 |

파일 검사는 심볼릭 링크를 따라갈 수 있다. `-L`은 링크 자체인지 검사한다. 파일 존재만 확인했다고 이후 읽기가 반드시 성공하는 것은 아니다.

```bash
count=3
if (( count >= 5 )); then
    printf 'HIGH\n'
elif (( count >= 3 )); then
    printf 'MEDIUM\n'
else
    printf 'LOW\n'
fi
```

결과는 MEDIUM이다. 높은 임계값부터 검사하지 않으면 높은 값도 낮은 단계에서 먼저 잡힐 수 있다.

## 3. 패턴과 인용

```bash
name='report.log'
pattern='*.log'
[[ $name == $pattern ]] && printf 'pattern match\n'
[[ $name == "$pattern" ]] || printf 'not literal *.log\n'
```

첫 비교는 패턴, 둘째는 문자 그대로 비교다. 여기서 인용 여부는 일반 명령의 단어 분리 문제와 다른 규칙이다.

## 4. case로 모드 선택

```bash
mode='summary'
case $mode in
    summary|count) printf 'accepted mode=%s\n' "$mode" ;;
    help) printf 'modes: summary count help\n' ;;
    *) printf 'unknown mode\n' >&2 ;;
esac
```

case 패턴도 정규식이 아니다. `;;`는 해당 분기를 끝낸다. 알려진 모드만 허용하면 실행 경로와 테스트 대상이 분명해진다.

## 5. test와 이식성

POSIX sh 스크립트에서는 `[ "$value" = "$expected" ]`를 사용한다. `[`는 명령 이름이며 마지막 `]`와 각 인수 사이에 공백이 필요하다. Bash 전용 교안은 `[[ ... ]]`를 사용하되 sh와의 차이를 표시한다.

## 실패 사례와 실습

1. count가 0, 2, 3, 4, 5일 때 분기를 표로 만든다.
2. summary, help, 빈 값, 알 수 없는 모드의 출력을 정한다.
3. 숫자 비교를 문자열 비교로 바꾸었을 때 10과 2의 차이를 관찰한다.

### 해설

임계값 경계 3과 5를 반드시 포함한다. 정상 입력 몇 개만 실행하면 비교 연산자의 경계 오류를 놓친다.

## ✅ 완료 기준

- [ ] if가 종료 상태를 판단함을 설명한다.
- [ ] 숫자와 문자열 비교를 구분한다.
- [ ] 임계값 직전·같음·직후를 시험한다.

다음: [03-7. 반복문](03-7-loops.md)
