# 05-3. JSON과 데이터 형식의 계약

JSON은 행의 모양보다 자료 구조가 중요하다. 공백·키 순서·중첩 깊이가 달라도 같은 데이터일 수 있다. 정규식이나 문자열 자르기로 필드를 찾기보다 JSON 파서를 사용한다.

{% hint style="info" %}
### 🧭 학습 목표

- JSON의 객체·배열·null을 구분한다.
- jq로 검증·선택·변환을 단계별 수행한다.
- 문자열을 --arg로 전달한다.
- Bash·jq·Python의 역할을 선택한다.
{% endhint %}

## 준비

jq가 필요하다. [02장](../02-bash-setup.md)에서 설치하고 `jq --version`을 확인한다.

```bash
lab_dir=$(mktemp -d)
printf '%s\n' '{"events":[{"level":"INFO","count":2},{"level":"ERROR","count":3}]}' > "$lab_dir/events.json"
```

## 1. 구조 확인

```bash
jq 'type' "$lab_dir/events.json"
jq '.events | length' "$lab_dir/events.json"
jq '.events[] | .level' "$lab_dir/events.json"
```

첫 출력은 object라는 JSON 문자열, 둘째는 2, 마지막은 INFO·ERROR JSON 문자열이다. `-r`은 문자열을 따옴표 없이 출력한다. 셸에서 읽기 쉽게 바꾸는 것과 JSON으로 보존하는 목적을 구분한다.

## 2. 입력 검증

```bash
jq -e '
    (.events | type == "array") and
    all(.events[];
        type == "object" and
        (.level | type == "string") and
        (.count | type == "number"))
' "$lab_dir/events.json"
```

정상 입력은 true와 상태 0이다. -e는 마지막 출력이 false 또는 null이면 비영 상태를 만든다. 문법 오류나 타입 오류도 실패하지만 원인은 다르므로 stderr를 확인한다. 빈 배열을 허용하는지도 업무 계약에 적는다.

## 3. 값과 jq 코드를 분리

```bash
wanted=ERROR
jq -r --arg level "$wanted" '
    .events[] | select(.level == $level) | [.level, .count] | @tsv
' "$lab_dir/events.json"
```

결과는 ERROR와 3의 TSV 한 행이다. `$level`은 jq 변수이며 Bash가 확장하지 않는다. 사용자 값을 코드 문자열에 끼워 넣지 않고 --arg로 전달한다.

## 4. JSON 생성

```bash
label='two words'
jq -n --arg label "$label" --argjson count 3 '{label:$label,count:$count}'
```

--arg는 문자열, --argjson은 유효한 JSON 값을 받는다. 임의 문자열을 printf로 JSON 따옴표 안에 끼워 넣으면 이스케이프 문자가 깨질 수 있다.

## 5. 형식 선택

| 형식 | 적합한 데이터 | 주의점 |
|---|---|---|
| 행 텍스트 | 단순 로그 | 필드와 줄바꿈 계약 |
| TSV | 단순 표 | 탭·개행 이스케이프 규칙 |
| JSON | 중첩 구조 | 파서와 자료형 검증 |
| JSON Lines | 레코드 스트림 | 행 단위 오류 정책 |

복잡한 스키마, 여러 API, 날짜 계산, 레코드별 복구가 많으면 Python으로 핵심 처리를 옮긴다. Bash는 실행 순서와 종료 상태를 관리한다.

## 🧪 직접 해보기

1. count를 숫자 3에서 문자열 "3"으로 바꾸어 검증 결과를 비교한다.
2. events가 없는 객체와 빈 배열의 정책을 정한다.
3. 따옴표가 포함된 label을 --arg로 생성한 뒤 다시 파싱한다.

## ✅ 완료 기준

- [ ] 문법적으로 유효한 JSON과 업무적으로 유효한 JSON을 구분한다.
- [ ] 값과 jq 코드를 분리한다.
- [ ] 자료형이 변하면 테스트가 실패한다.

근거: [jq 공식 매뉴얼](https://jqlang.org/manual/).

다음: [06. 프로세스와 시스템 조사](../06-system-inspection.md)
