# 03-1. 조건문, 반복문과 함수

{% hint style="info" %}
## 🧭 학습 목표

- `[[ ]]`, `(( ))`, `case`로 조건을 표현한다.
- 파일과 표준 입력을 안전하게 반복 처리한다.
- 출력 데이터와 종료 상태를 구분하는 함수를 작성한다.
{% endhint %}

## 조건문

```bash
if [[ -r "$file" ]]; then
    printf 'readable: %s\n' "$file"
elif [[ -e "$file" ]]; then
    printf 'exists but is not readable: %s\n' "$file" >&2
else
    printf 'not found: %s\n' "$file" >&2
fi
```

문자열과 파일 조건에는 `[[ ... ]]`, 산술 비교에는 `(( ... ))`가 읽기 쉽습니다.

```bash
if [[ $role == 'analyst' && -n $ticket ]]; then
    printf 'authorized workflow\n'
fi

if (( count > 100 )); then
    printf 'high volume\n'
fi
```

## case

```bash
case ${1:-} in
    collect) printf 'collect mode\n' ;;
    analyze) printf 'analyze mode\n' ;;
    *)
        printf 'usage: %s {collect|analyze}\n' "$0" >&2
        exit 2
        ;;
esac
```

## 반복문

```bash
for file in "$@"; do
    [[ -r $file ]] || continue
    printf '%s\t%s bytes\n' "$file" "$(stat -c %s -- "$file")"
done
```

```bash
while IFS= read -r line; do
    [[ $line == \#* || -z $line ]] && continue
    printf 'IOC=%s\n' "$line"
done <iocs.txt
```

`read -r`은 백슬래시를 그대로 보존하고, `IFS=`는 앞뒤 공백 제거를 막습니다.

## 함수

```bash
log_error() {
    printf 'ERROR: %s\n' "$*" >&2
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || {
        log_error "required command not found: $1"
        return 1
    }
}

main() {
    require_command jq || return 1
    printf 'ready\n'
}

main "$@"
```

함수는 출력값과 종료 상태를 구분해야 합니다. 자료는 stdout으로 출력하고 성공·실패는 `return` 상태로 전달합니다.

## 🧪 직접 해보기

1. `collect`, `analyze`, `help` 하위 명령을 처리하는 `case`를 작성하세요.
2. 빈 줄과 주석을 제외하고 IOC 파일을 읽으세요.
3. 필요한 명령 세 개의 설치 여부를 확인하는 함수를 작성하세요.

## ✅ 완료 기준

- 빈 줄, 주석과 공백이 포함된 입력을 안전하게 순회한다.
- `main "$@"` 구조로 실행 흐름을 구성한다.
