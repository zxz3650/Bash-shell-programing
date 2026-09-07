# 03-9. 문법 종합 실습: 이벤트 분류기

변수·배열·인용·조건·반복·함수를 연결하여 입력한 이벤트 수준을 분류한다. 파일과 시스템 정보 없이 메모리 안의 입력부터 검증한다. 이후 같은 계약을 로그 분석기로 확장한다.

{% hint style="info" %}
### 🧭 학습 목표

- 요구사항을 함수 계약으로 바꾼다.
- 여러 인수의 경계를 보존한다.
- 한 입력 오류와 전체 실행 상태를 구분한다.
- 정상·빈 값·미지원 값에 대한 검증표를 작성한다.
{% endhint %}

## 0. 요구사항

입력은 INFO, WARN, ERROR 여러 개다. stdout에 원본 수준과 조치를 TSV로 출력한다. INFO는 normal, WARN은 watch, ERROR는 review다. 잘못된 값은 stderr로 알리고 나머지는 계속 처리한다. 하나라도 잘못된 값이 있으면 최종 상태 1, 인수가 없으면 2다.

## 1. 학생 구현 순서

1. classify 함수가 수준 하나를 받고 조치 한 행을 출력하게 작성한다.
2. main에서 인수가 없으면 usage를 출력한다.
3. `for level in "$@"`로 입력을 순회한다.
4. classify 실패를 if로 분기하고 전체 실패 여부를 누적한다.
5. 종료 상태와 두 스트림을 따로 검증한다.

## 2. 기준 구현

다음을 `classify-events.sh`로 저장한다.

```bash
#!/usr/bin/env bash
classify() {
    case ${1:-} in
        INFO) printf 'normal\n' ;;
        WARN) printf 'watch\n' ;;
        ERROR) printf 'review\n' ;;
        *) return 2 ;;
    esac
}

main() {
    (( $# > 0 )) || {
        printf 'usage: classify-events.sh LEVEL...\n' >&2
        return 2
    }
    local level action failed=0
    for level in "$@"; do
        if action=$(classify "$level"); then
            printf '%s\t%s\n' "$level" "$action"
        else
            printf 'invalid level: <%s>\n' "$level" >&2
            failed=1
        fi
    done
    return "$failed"
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    main "$@"
fi
```

## 3. 실행과 예상 결과

```bash
bash classify-events.sh INFO ERROR WARN
printf 'status=%s\n' "$?"
```

```text
INFO    normal
ERROR   review
WARN    watch
status=0
```

열 사이는 실제 탭이다. 문서의 정렬된 화면만 보고 공백 개수를 계약으로 삼지 않는다.

## 4. 실패 입력

```bash
bash classify-events.sh INFO '' DEBUG ERROR
status=$?
printf 'status=%s\n' "$status"
```

stdout에는 INFO와 ERROR 두 행이 남고 stderr에는 빈 값과 DEBUG에 대한 진단이 나온다. 상태는 1이다. 오류가 있는 결과도 일부 데이터를 포함할 수 있으므로 호출자는 상태와 데이터를 함께 확인한다.

## 5. 자기 점검표

| 입력 | 정상 행 수 | 진단 수 | 상태 |
|---|---:|---:|---:|
| 인수 없음 | 0 | 1 | 2 |
| INFO | 1 | 0 | 0 |
| INFO ERROR WARN | 3 | 0 | 0 |
| 빈 값 | 0 | 1 | 1 |
| INFO DEBUG ERROR | 2 | 1 | 1 |

## 확장 과제와 해설

DEBUG를 허용하려면 함수의 case, 요구사항 표, 테스트를 함께 바꾼다. 모든 소문자를 자동 변환할지 엄격하게 거부할지도 먼저 정한다. 코드만 변경하고 계약을 남겨 두면 학생마다 성공 기준이 달라진다.

## ✅ 완료 기준

- [ ] 위 다섯 사례의 상태와 행 수가 일치한다.
- [ ] 빈 인수도 한 입력으로 처리한다.
- [ ] source로 함수를 불러올 때 main이 자동 실행되지 않는다.
- [ ] 구현 선택을 입력·출력·상태 계약으로 설명한다.

다음: [04. 파일 입출력과 권한](../04-file-io.md)
