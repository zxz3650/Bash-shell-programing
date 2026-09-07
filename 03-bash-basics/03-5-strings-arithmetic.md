# 03-5. 문자열 처리와 산술식

짧은 문자열 처리는 매개변수 확장으로 해결할 수 있다. 정수 계산은 산술 확장을 사용한다. 숫자처럼 보이는 문자열도 계산 전에 형식과 범위를 검증한다.

{% hint style="info" %}
### 🧭 학습 목표

- 길이·기본값·접두사·접미사 제거를 사용한다.
- 패턴과 정규식을 구분한다.
- 정수 나눗셈과 산술 명령의 상태를 예측한다.
- 숫자 형식과 범위를 검증한다.
{% endhint %}

## 학습 전 확인

`$((5 / 2))`는 2인가 2.5인가? `((0))`는 성공인가? [03-1](03-1-execution-model.md)의 종료 상태와 연결한다.

## 1. 파일명 문자열 분리

```bash
path='/lab/reports/access.2026.log'
base=${path##*/}
stem=${base%.*}
suffix=${base##*.}
printf 'base=%s\nstem=%s\nsuffix=%s\n' "$base" "$stem" "$suffix"
```

```text
base=access.2026.log
stem=access.2026
suffix=log
```

| 문법 | 동작 |
|---|---|
| `${value#pattern}` | 앞에서 최단 일치 제거 |
| `${value##pattern}` | 앞에서 최장 일치 제거 |
| `${value%pattern}` | 뒤에서 최단 일치 제거 |
| `${value%%pattern}` | 뒤에서 최장 일치 제거 |
| `${#value}` | 문자열 길이 |

이 패턴은 정규식이 아니다. 점이 없는 이름과 `.env` 같은 숨김 파일은 확장자 정책을 따로 정해야 한다.

## 2. 기본값과 대입

```bash
unset lab_mode
printf '%s\n' "${lab_mode:-demo}"
printf 'after=%s\n' "${lab_mode-unset}"
```

출력은 demo, after=unset이다. `:-`는 원래 변수에 대입하지 않는다. 확정하려면 `lab_mode=${lab_mode:-demo}`로 대입한다.

## 3. 산술 확장과 산술 명령

```bash
count=5
printf 'half=%s\n' "$((count / 2))"
if (( count >= 3 )); then
    printf 'threshold reached\n'
fi
```

정수 나눗셈 결과는 2다. `$((...))`는 계산 결과를 확장하고 `((...))`는 식의 값이 0이면 상태 1, 0이 아니면 상태 0을 만든다.

```bash
count=0
((count++))
status=$?
printf 'count=%s status=%s\n' "$count" "$status"
```

set -e가 없는 연습 셸에서 실행하면 count=1 status=1이다. 후위 증가는 이전 값 0을 평가한다. 단순 증가는 `count=$((count + 1))`로 쓰면 산술 명령의 상태와 혼동하지 않는다.

## 4. 숫자 검증과 진법

```bash
raw='08'
if [[ $raw =~ ^[0-9]{1,3}$ ]]; then
    value=$((10#$raw))
    if (( value <= 100 )); then
        printf 'accepted=%s\n' "$value"
    fi
fi
```

검증 뒤 `10#`를 붙이면 선행 0이 있는 값을 십진수로 해석한다. 자릿수 제한은 과도하게 큰 수를 거부한다. Bash 산술은 고정 크기 정수이며 실수·임의 정밀도 계산 도구가 아니다.

## 실패 사례

검증하지 않은 입력을 산술식으로 해석하거나, 정수 나눗셈을 실수로 기대하거나, `((count++))`를 set -e 환경에서 무조건 성공하는 명령으로 생각하면 오류가 생긴다.

## 🧪 직접 해보기

1. archive.tar.gz에서 마지막 확장자를 제거한다.
2. 8, 08, 101, abc, 빈 값을 0~100 검증기에 전달한다.
3. `((0))`, `((1))`의 상태를 저장한다.

### 해설

첫 결과는 archive.tar다. 숫자 검사에서는 8과 08만 통과한다. 101은 숫자 형식은 맞지만 허용 범위인 0~100을 벗어난다. 따라서 숫자로만 구성되어 있는지와 허용 범위 안에 있는지를 따로 검사해야 한다.

## ✅ 완료 기준

- [ ] 외부 명령 없이 간단한 문자열을 처리한다.
- [ ] 식의 값과 명령 종료 상태를 구분한다.
- [ ] 숫자의 형식과 범위를 순서대로 검증한다.

다음: [03-6. 조건문과 case](03-6-conditions.md)
