# 03-3. 인용과 확장 순서

Bash 문자열 오류의 흔한 원인은 인수 경계가 바뀌는 것이다. 변수에 공백이나 `*`가 있으면 인용 여부에 따라 여러 인수가 되거나 파일명으로 확장될 수 있다.

{% hint style="info" %}
### 🧭 학습 목표

- 작은따옴표·큰따옴표·인용 없는 확장을 비교한다.
- 단어 분리와 파일명 확장을 구분한다.
- 명령 치환의 개행 제거를 설명한다.
- 출력 형식과 데이터를 분리한다.
{% endhint %}

## 선행 지식

[03-2](03-2-variables-environment.md)의 변수 대입을 사용한다. 실습은 [노트북 02](../jupyter-book/labs/02-arguments-variables-arrays.ipynb)다.

## 0. 학습 전 확인

`label='two words'`일 때 인용 없이 출력하면 몇 줄이 되는가?

## 1. 세 가지 인용 방식

```bash
label='two words'
printf '<%s>\n' "$label"
printf '<%s>\n' '$label'
printf '<%s>\n' $label
```

```text
<two words>
<$label>
<two>
<words>
```

마지막 인용 누락은 관찰용이다. 실제 전달에는 `"$label"`을 사용한다. 작은따옴표는 그대로 보존하고 큰따옴표는 변수·명령·산술 치환을 허용하면서 경계를 보존한다.

## 2. 확장 과정

일반 명령의 단어는 다음 순서를 거친다.

```text
중괄호 확장
→ 틸드·변수·산술·명령 치환
→ 인용되지 않은 확장 결과의 단어 분리
→ 파일명 확장(glob)
→ 구문 따옴표 제거
→ 최종 인수 목록
```

대입문이나 `[[ ... ]]`는 일반 명령 인수와 규칙이 다르다. 모든 문맥에 같은 규칙을 적용하지 않는다. 인용하지 않은 변수 값이 `*.log`라면 현재 디렉터리 내용에 따라 인수 수가 달라질 수 있다.

## 3. glob과 정규식

| 표현 | 사용 위치 | 의미 |
|---|---|---|
| `*.log` | 셸 파일명 확장 | .log로 끝나는 경로 |
| `^ERROR` | grep 정규식 | 행 시작 ERROR |
| `[[ $name == *.log ]]` | Bash 패턴 비교 | 값과 패턴의 일치 |

grep에 파일 목록을 전달하는 것과 파일 안에서 행을 검색하는 것을 구분한다.

## 4. 명령 치환

```bash
result=$(printf 'alpha\n\n')
printf '<%s>\n' "$result"
printf 'length=%s\n' "${#result}"
```

결과는 `<alpha>`, `length=5`다. `$(...)`는 stdout을 캡처하며 끝의 개행을 제거한다. 내부 개행은 남는다. 바이너리나 NUL 구분 목록은 변수에 저장하지 않고 파일 또는 파이프로 전달한다.

```bash
label='two words'
result=$(printf '%s' "$label")
printf '%s\n' "$result"
```

명령 치환 내부에서도 변수 인용은 별도로 필요하다.

## 5. 안전한 printf

```bash
message='progress=50% \n remains data'
printf '%s\n' "$message"
```

형식 문자열을 코드에 고정한다. `printf "$message"`는 퍼센트나 백슬래시를 형식으로 해석하여 의도와 다르게 출력할 수 있다.

## 실패 사례

변수 안에 따옴표 문자를 넣는다고 인수 경계가 생기지 않는다. `text='"two words"'`를 인용해 출력하면 따옴표도 데이터로 남는다. 여러 인수는 배열로 저장한다. eval로 다시 해석하여 해결하지 않는다.

## 🧪 직접 해보기

1. alpha beta, 빈 문자열, `*.log`를 각각 한 인수로 출력한다.
2. 작은따옴표의 `$label`이 그대로 나오는 이유를 설명한다.
3. 끝 개행이 있는 값을 명령 치환으로 저장하고 길이를 비교한다.

### 해설

빈 문자열도 인용하면 한 인수다. 인용하지 않은 빈 확장은 인수가 사라질 수 있다. 개행 보존이 필요하면 파일을 사용한다.

## ✅ 완료 기준

- [ ] 실행 전에 최종 인수 수를 예측한다.
- [ ] glob과 정규식의 해석 주체를 구분한다.
- [ ] 형식과 데이터를 분리한다.

근거: [GNU 확장 순서](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html), [SC2086](https://www.shellcheck.net/wiki/SC2086).

다음: [03-4. 위치 인자와 배열](03-4-arguments-arrays.md)
