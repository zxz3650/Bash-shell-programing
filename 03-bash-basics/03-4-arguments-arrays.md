# 03-4. 위치 인자와 배열

스크립트는 명령줄 인수로 입력을 받는다. 다른 명령에 전달할 때 값과 각 인수의 경계를 함께 보존해야 한다. 위치 인자와 배열을 올바르게 사용하면 공백이 포함된 값도 하나의 인수로 전달할 수 있다.

{% hint style="info" %}
### 🧭 학습 목표

- `$0`, `$1`, `$#`, `"$@"`를 구분한다.
- shift와 인수 개수 검증을 적용한다.
- 배열 원소·길이·순회를 사용한다.
- 명령 인수를 배열로 구성한다.
{% endhint %}

## 학습 전 확인

`two words.log`가 두 파일로 처리된다면 어떤 인용이 빠졌는가? [03-3](03-3-quoting-expansion.md)에서 배운 인수 경계를 떠올린다.

## 1. 위치 인자 관찰

다음을 `show-args.sh`로 저장한다.

```bash
#!/usr/bin/env bash
printf 'program=%s count=%s\n' "$0" "$#"
index=1
for arg in "$@"; do
    printf '%s=<%s>\n' "$index" "$arg"
    index=$((index + 1))
done
```

```bash
bash show-args.sh alpha 'two words' ''
```

```text
program=show-args.sh count=3
1=<alpha>
2=<two words>
3=<>
```

`"$@"`는 인수별 경계를 유지한다. `"$*"`는 IFS의 첫 문자로 연결한 한 단어가 된다. 인수 전달에는 전자를 사용한다.

## 2. shift

```bash
set -- report './input file.log'
if (( $# == 2 )); then
    mode=$1
    shift
    printf 'mode=%s file=%s remaining=%s\n' "$mode" "$1" "$#"
fi
```

set --는 연습용 위치 인자를 설정한다. shift는 첫 인수를 제거하고 뒤 인수를 당긴다. 입력 개수를 확인한 다음 실행한다.

## 3. 인덱스 배열

```bash
files=('one.log' 'two words.log' '-draft.log')
printf 'first=%s count=%s\n' "${files[0]}" "${#files[@]}"
files+=('last.log')
for file in "${files[@]}"; do
    printf '<%s>\n' "$file"
done
```

인덱스는 0부터 시작한다. `"${files[@]}"`는 원소별 경계를, `"${files[*]}"`는 연결한 한 문자열을 만든다. `${files}`를 전체 배열로 생각하면 안 된다.

## 4. 명령 인수를 배열로 보존

```bash
args=('%s\n' 'alpha beta' '*.log')
printf "${args[@]}"
```

검색 명령도 `args=(-n -F -- "$pattern" "$input_file")`로 구성하고 `grep "${args[@]}"`로 실행한다. 문자열 한 개에 옵션과 따옴표를 넣어 재분리하지 않는다.

`--` 지원은 명령마다 다르다. 경로가 하이픈으로 시작하면 `./-draft.log`처럼 경로로 전달하는 방법도 있다.

## 5. 버전과 배열 종류

기본 인덱스 배열은 Bash 3.2를 지원한다. 연관 배열은 Bash 4 이상 전용이다.

```bash
# Bash 4 이상 전용
declare -A counts=([INFO]=2 [ERROR]=1)
printf '%s\n' "${counts[ERROR]}"
```

큰 집계에는 awk, 복잡한 중첩 자료에는 Python을 선택할 수 있다. Bash 배열을 Python 딕셔너리와 동일하게 다루지 않는다.

## 실패 사례와 실습

1. show-args에 인수 없음·빈 인수 하나·공백 인수를 전달한다.
2. `"$@"`를 `"$*"`로 바꾼 결과를 비교한다.
3. 배열 끝에 원소를 추가하고 길이를 확인한다.

### 해설

인수 없음은 개수 0, 빈 인수 하나는 개수 1이다. 값의 길이와 인수 개수는 별개다. `"$*"` 순회는 전체가 하나의 값으로 합쳐진다.

## ✅ 완료 기준

- [ ] 개수를 확인한 뒤 위치 인자를 사용한다.
- [ ] 배열을 합쳤다가 다시 분리하지 않는다.
- [ ] Bash 버전별 배열 지원을 구분한다.

실습: [노트북 02](../jupyter-book/labs/02-arguments-variables-arrays.ipynb)

다음: [03-5. 문자열과 산술식](03-5-strings-arithmetic.md)
