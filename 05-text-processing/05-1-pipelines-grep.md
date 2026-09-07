# 05-1. 파이프라인과 grep의 결과 해석

파이프는 앞 명령의 stdout을 뒤 명령의 stdin에 연결한다. 각 단계는 동시에 실행될 수 있고, stderr는 기본적으로 파이프에 들어가지 않는다. 데이터 흐름과 상태 흐름을 따로 이해해야 한다.

{% hint style="info" %}
### 🧭 학습 목표

- 파이프 단계별 입출력을 설명한다.
- grep 고정 문자열과 정규식을 선택한다.
- 검색 없음과 읽기 오류를 구분한다.
- pipefail·PIPESTATUS의 의미를 설명한다.
{% endhint %}

## 0. 샘플 준비

```bash
lab_dir=$(mktemp -d)
printf '%s\n' 'INFO start' 'ERROR disk' 'WARN retry' 'ERROR disk' > "$lab_dir/app.log"
```

## 1. 검색 목적에 맞는 옵션

```bash
grep -nF -- 'ERROR' "$lab_dir/app.log"
grep -nE -- '^(WARN|ERROR) ' "$lab_dir/app.log"
```

첫 결과는 2행과 4행, 둘째는 2·3·4행이다. -F는 문자 그대로, -E는 확장 정규식을 해석한다. 사용자 제공 검색 문자열을 정규식으로 해석할 필요가 없다면 -F를 선택한다.

| 옵션 | 의미 |
|---|---|
| -n | 원본 행 번호 |
| -F | 고정 문자열 |
| -E | 확장 정규식 |
| -v | 일치하지 않는 행 |
| -c | 일치하는 행 수 |
| -q | 내용 없이 일치 여부만 검사 |

-c는 문자열 출현 횟수가 아니라 일치 행 수다. 한 행에 ERROR가 두 번 있어도 한 행으로 센다.

## 2. 0·1·2 구분

```bash
if grep -F -- 'MISSING' "$lab_dir/app.log"; then
    printf 'matched\n' >&2
else
    status=$?
    case $status in
        1) printf 'no matching lines\n' >&2 ;;
        *) printf 'grep failed: %s\n' "$status" >&2 ;;
    esac
fi
```

예상 결과는 no matching lines다. 없는 파일을 전달하면 grep의 오류와 실패 상태를 관찰한다. `|| true`로 모두 덮으면 이 차이가 사라진다.

## 3. 파이프라인 상태

```bash
bash -c 'false | true; printf "default=%s\n" "$?"'
bash -o pipefail -c 'false | true; printf "pipefail=%s\n" "$?"'
```

기본 상태는 마지막 명령의 0이다. pipefail에서는 가장 오른쪽의 실패 상태를 반환하여 1이다. 각 단계의 상태는 바로 저장한다.

```bash
false | true
states=("${PIPESTATUS[@]}")
printf 'first=%s last=%s\n' "${states[0]}" "${states[1]}"
```

다른 명령을 실행하면 PIPESTATUS도 갱신된다. 이 관찰 예제는 set -e가 꺼진 Bash에서 실행한다.

## 4. 조기 종료와 SIGPIPE

head나 grep -q가 충분한 입력을 읽고 종료하면 생산자는 SIGPIPE를 받을 수 있다. pipefail에서 이를 무조건 장애라고 판단하지 않는다. 전체 입력 처리 여부와 “일치 하나만 확인” 중 목적을 먼저 정한다.

## 🧪 직접 해보기

1. ERROR·MISSING·없는 파일의 상태를 표로 만든다.
2. -c와 실제 문자열 등장 횟수를 비교한다.
3. false를 파이프의 첫째·마지막 위치에 놓고 상태를 비교한다.

## ✅ 완료 기준

- [ ] 검색 없음과 파일 오류를 구분한다.
- [ ] 단계별 데이터를 따로 확인한다.
- [ ] pipefail이 실패를 해결하지 않고 드러내는 옵션임을 설명한다.

다음: [05-2. awk·sed·집계](05-2-awk-sed-aggregation.md)
