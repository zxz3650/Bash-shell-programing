# 07-1. 입력 검증과 데이터·코드 경계

입력 검증은 허용된 값을 확인하는 단계이고 인용은 인수 경계를 유지하는 단계다. 검증에 성공했다고 인용을 생략하면 안 된다. 명령을 문자열로 조립하여 다시 해석하지 않고 명령과 인수를 분리한다.

{% hint style="info" %}
### 🧭 학습 목표

- 형식 검사와 업무 범위 검사를 구분한다.
- allowlist와 인용을 함께 적용한다.
- eval·source의 코드 실행 성격을 설명한다.
- 정상·빈 값·경계 입력을 검증한다.
{% endhint %}

## 0. 학습 전 확인

파일명에 공백이 있다는 이유로 거부해야 하는가? 숫자 정규식을 통과하면 원하는 범위의 정수인가?

## 1. 명령과 데이터 분리

```bash
pattern='ERROR [disk]'
input_file='./app.log'
args=(-n -F -- "$pattern" "$input_file")
printf 'argument=<%s>\n' "${args[@]}"
```

검색 대상은 문자 그대로의 ERROR [disk]다. 실행하려면 준비한 파일에 `grep "${args[@]}"`를 사용한다. 대괄호를 정규식으로 해석하지 않도록 -F를 지정했다.

## 2. 제한된 모드

```bash
validate_mode() {
    case ${1:-} in
        summary|count) return 0 ;;
        *) printf 'mode must be summary or count\n' >&2; return 2 ;;
    esac
}
validate_mode summary
```

허용된 모드가 두 개이면 두 개만 정의한다. 임의 입력을 함수 이름이나 외부 명령 이름으로 실행하지 않는다.

## 3. 형식과 범위

```bash
validate_workers() {
    [[ ${1:-} =~ ^[1-9][0-9]?$ ]] || return 2
    (( 10#$1 <= 8 )) || return 2
}
for value in 0 1 8 9 abc; do
    if validate_workers "$value"; then
        printf '%s accepted\n' "$value"
    else
        printf '%s rejected\n' "$value"
    fi
done
```

1과 8만 통과한다. 정규식은 숫자 모양과 자릿수를, 산술 비교는 업무 범위를 검사한다.

## 4. 설정 파일은 데이터로 읽기

source는 현재 셸에서 파일의 코드를 실행한다. 사용자가 편집하는 데이터 설정에는 필요한 키와 값을 파싱하는 방법을 사용한다.

```bash
parse_setting() {
    local key=$1 value=$2
    case $key in
        LEVEL)
            case $value in info|debug) printf 'LEVEL=%s\n' "$value" ;; *) return 2 ;; esac
            ;;
        *) return 2 ;;
    esac
}
parse_setting LEVEL info
```

전체 env 문법을 재구현하려 하지 않는다. 지원하는 형식만 문서화하거나 JSON 같은 구조화 형식과 파서를 선택한다.

## 실패 사례

eval로 명령 문자열을 다시 해석하면 입력 데이터가 셸 구문으로 바뀔 수 있다. 해결책은 문자를 몇 개 제거하는 것이 아니라 처음부터 인수 배열을 유지하는 것이다. 경로 인용은 심볼릭 링크나 디렉터리 탈출 검증을 대신하지 않는다.

## 🧪 직접 해보기

1. 모드에 빈 값·help·summary·count를 전달한다.
2. workers에 1·8·9·01을 넣고 정책을 설명한다.
3. 공백과 별표가 포함된 검색어가 한 인수로 전달되는지 출력한다.

## ✅ 완료 기준

- [ ] 형식·범위·인수 경계를 따로 검증한다.
- [ ] 데이터 설정을 실행 코드로 읽지 않는다.
- [ ] 거부 입력의 진단과 종료 상태를 기록한다.

다음: [07-2. 변경 계획과 재실행](07-2-dry-run-idempotency.md)
